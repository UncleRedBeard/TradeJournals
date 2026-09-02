#!/usr/bin/env python3
"""Import a public Flickr album into a TradeJournals Markdown entry.

This is intentionally a small, dependency-free prototype. By default it uses
public Flickr endpoints only:

1. oEmbed JSON for album-level display metadata.
2. the public album page to discover the owner's NSID.
3. the public photoset feed for photo titles, links, and date_taken values.

Pass `--use-api` to use Flickr's REST API for public album discovery and full
photo pagination. API mode reads `FLICKR_API_KEY` from the environment. The API
secret is intentionally not used for public-read workflows.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "TradeJournals Flickr importer"
FETCH_TIMEOUT_SECONDS = 30
FLICKR_API_ENDPOINT = "https://www.flickr.com/services/rest/"
API_PAGE_SIZE = 500
LOCAL_ENV_PATH = REPO_ROOT / ".env"
DEFAULT_INVENTORY_PATH = REPO_ROOT / "FLICKR_PUBLIC_ALBUMS.md"
DEFAULT_EXCLUDED_ALBUM_IDS = {
    # User-approved TradeJournals exclusions from the public Flickr inventory.
    "72157682532227305",
    "72157679575662395",
    "72157677807747011",
    "72157644736396663",
    "72157644693416375",
    "72157629724747813",
    "72157624945269229",
}
REDACTED_CREDENTIAL = "REDACTED"
INVENTORY_DETAIL_FIELDS = (
    "Album URL",
    "Album ID",
    "Visibility",
    "Photos",
    "TradeJournals status",
    "Section",
    "Existing journal",
)
INVENTORY_REQUIRED_DETAIL_FIELDS = {
    "Album URL",
    "Album ID",
    "Visibility",
    "Photos",
    "TradeJournals status",
}
INVENTORY_NUMERIC_SUMMARY_PREFIXES = (
    "- Public albums visible via API:",
    "- Existing TradeJournals coverage:",
    "- Albums excluded from TradeJournals import:",
    "- Albums still needing review/mapping:",
)
METADATA_PREVIEW_EXTRAS = ",".join(
    (
        "date_upload",
        "date_taken",
        "tags",
        "o_dims",
        "url_o",
    )
)
EXIF_ALLOWLIST = {
    ("TIFF", "271"): "Camera make",
    ("TIFF", "272"): "Camera model",
    ("EXIF", "33434"): "Exposure time",
    ("EXIF", "33437"): "Aperture",
    ("EXIF", "34855"): "ISO",
    ("EXIF", "36867"): "EXIF original date/time",
    ("EXIF", "37386"): "Focal length",
    ("EXIF", "42036"): "Lens model",
}

# Keep section names short on the command line, but write into the existing
# TradeJournals folder structure.
SECTION_DIRS = {
    "residence": REPO_ROOT / "01_the_residence_1894" / "trade_journals",
    "forge": REPO_ROOT / "02_the_forge_and_shop" / "trade_journals",
    "machines": REPO_ROOT / "03_the_machines" / "trade_journals",
    "materials": REPO_ROOT / "04_materials_and_alchemy" / "trade_journals",
    "lens": REPO_ROOT / "05_the_lens" / "trade_journals",
}


@dataclass(frozen=True)
class Photo:
    """Small normalized record for one Flickr photo item."""

    title: str
    link: str
    date_taken: str
    photo_id: str


@dataclass(frozen=True)
class Album:
    """Normalized album data used by the Markdown renderer.

    The model carries both feed-backed and API-backed values. Some field names
    still reflect the original feed-only prototype so existing render and merge
    paths stay stable while API mode evolves.
    """

    title: str
    url: str
    short_url: str
    owner: str
    owner_nsid: str
    thumbnail_alt: str
    feed_title: str
    feed_modified: str
    photo_count: int
    # Legacy field name retained for compatibility with existing render paths.
    # In API mode this is the full listed photo count, not only a starter set.
    starter_photo_count: int
    photo_listing_source: str
    photos: list[Photo]


@dataclass(frozen=True)
class PublicAlbum:
    """Summary record for one album discovered from HTML or API scans."""

    title: str
    url: str
    album_id: str
    visibility: str = "public"
    photo_count: int | None = None
    view_count: int | None = None


@dataclass(frozen=True)
class AlbumDiscovery:
    """Result of scanning public Flickr albums through one discovery source."""

    albums: list[PublicAlbum]
    advertised_total: int | None = None
    source: str = "initial page HTML"


@dataclass(frozen=True)
class JournalReference:
    """One Flickr album reference found in an existing journal file."""

    album_id: str
    journal_path: Path


@dataclass(frozen=True)
class ReconcileChange:
    """One line-level update made or proposed during reconciliation."""

    journal_path: Path
    line_number: int
    before: str
    after: str


@dataclass(frozen=True)
class InventoryRow:
    """One public album row in the TradeJournals inventory report."""

    index: int
    album: PublicAlbum
    status: str
    section: str
    existing_journal: Path | None


class CuratedContentError(RuntimeError):
    """Raised when regeneration could destroy reviewable Markdown metadata."""

    def __init__(
        self,
        path: Path,
        preview: str,
        reason: str | None = None,
    ) -> None:
        message = f"Refusing to overwrite curated Markdown: {path}"

        if reason:
            message += f" ({reason})"

        super().__init__(message)
        self.path = path
        self.preview = preview


class FlickrAPIError(RuntimeError):
    """Structured public Flickr API failure with a safe rendered message."""

    def __init__(self, method: str, code: object, message: str) -> None:
        super().__init__(f"Flickr API {method} failed ({code}): {message}")
        self.method = method
        self.code = str(code)


class InitialAlbumMetadataError(RuntimeError):
    """Failure before an album preview can obtain its public header."""


@dataclass(frozen=True)
class MetadataValue:
    """One public metadata value plus its observed availability state."""

    status: str
    value: str = ""


@dataclass(frozen=True)
class ExifValue:
    """One allowlisted digital-file EXIF value."""

    label: str
    value: str


@dataclass(frozen=True)
class PhotoMetadataPreview:
    """Review-only public metadata for one photo in album order."""

    photo_id: str
    title: str
    photo_page_url: str
    static_image_url: MetadataValue
    dimensions: MetadataValue
    date_taken: MetadataValue
    date_posted: MetadataValue
    description: MetadataValue
    tags: MetadataValue
    metadata_expansion: str
    exif_status: str
    exif: tuple[ExifValue, ...]
    error: str = ""


@dataclass(frozen=True)
class AlbumMetadataPreview:
    """A bounded, read-only snapshot of public Flickr album metadata."""

    album_id: str
    album_url: str
    title: str
    description: MetadataValue
    retrieved_at_utc: str
    requested_scope: str
    reported_photo_count: int | None
    data_sources: tuple[str, ...]
    photos: tuple[PhotoMetadataPreview, ...]
    complete: bool = True
    errors: tuple[str, ...] = ()


def redact_flickr_credentials(value: object, *, url: str = "") -> str:
    """Remove Flickr API keys from text before it crosses an output boundary."""

    text = str(value)
    secrets = parse_qs(urlparse(url).query).get("api_key", []) if url else []

    for secret in secrets:
        if secret:
            text = text.replace(secret, REDACTED_CREDENTIAL)

    return re.sub(
        r"(?i)(api_key=)[^&\s>'\"]+",
        rf"\g<1>{REDACTED_CREDENTIAL}",
        text,
    )


def fetch_text(url: str) -> str:
    """Fetch text from a public URL with a clear user agent.

    `urllib` is part of Python's standard library, which keeps this prototype
    easy to run in the repo without installing dependencies.
    """

    request = Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urlopen(request, timeout=FETCH_TIMEOUT_SECONDS) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            body = response.read()
    except (HTTPError, URLError, TimeoutError) as exc:
        safe_url = redact_flickr_credentials(url, url=url)
        safe_error = redact_flickr_credentials(exc, url=url)
        raise RuntimeError(f"failed to fetch {safe_url}: {safe_error}") from None

    return body.decode(charset, errors="replace")


def fetch_json(url: str) -> dict[str, Any]:
    """Fetch and parse a JSON response."""

    text = fetch_text(url)

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        safe_url = redact_flickr_credentials(url, url=url)
        safe_error = redact_flickr_credentials(exc, url=url)
        raise RuntimeError(
            f"failed to parse JSON from {safe_url}: {safe_error}"
        ) from None


def load_local_env_value(name: str) -> str:
    """Read one value from the repo-local `.env` file.

    This intentionally supports only simple `NAME=value` lines. The importer
    does not need a full shell parser, and keeping this small avoids surprising
    behavior for anyone reviewing how local secrets are handled.
    """

    if not LOCAL_ENV_PATH.exists():
        return ""

    for line in LOCAL_ENV_PATH.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        key, separator, value = stripped.partition("=")

        if separator and key.strip() == name:
            return value.strip().strip('"').strip("'")

    return ""


def require_flickr_api_key() -> str:
    """Return the Flickr API key from the environment.

    Keeping the key outside the repo prevents accidental commits of credentials.
    Public API calls only need the key; authenticated/private calls would need a
    separate OAuth flow and are outside this importer for now.
    """

    api_key = (
        os.environ.get("FLICKR_API_KEY", "").strip()
        or load_local_env_value("FLICKR_API_KEY")
    )

    if not api_key:
        raise RuntimeError(
            "FLICKR_API_KEY is required when using --use-api; export it or "
            "add it to the gitignored .env file"
        )

    return api_key


def build_flickr_api_url(
    method: str,
    params: dict[str, Any],
    *,
    api_key: str | None = None,
) -> str:
    """Build a Flickr REST API URL for a public JSON response."""

    query_params = {
        "method": method,
        "api_key": api_key or require_flickr_api_key(),
        "format": "json",
        "nojsoncallback": "1",
    }
    query_params.update(params)
    return f"{FLICKR_API_ENDPOINT}?{urlencode(query_params)}"


def fetch_flickr_api(
    method: str,
    params: dict[str, Any],
    *,
    api_key: str | None = None,
) -> dict[str, Any]:
    """Fetch one Flickr API response and raise clear errors on API failures."""

    api_url = build_flickr_api_url(method, params, api_key=api_key)
    response = fetch_json(api_url)

    if response.get("stat") == "fail":
        code = response.get("code", "unknown")
        message = redact_flickr_credentials(
            response.get("message", "unknown Flickr API error"),
            url=api_url,
        )
        raise FlickrAPIError(method, code, message)

    return response


def flickr_content(value: Any) -> str:
    """Return Flickr's `_content` field, falling back to plain strings."""

    if isinstance(value, dict):
        return str(value.get("_content", "")).strip()

    if value is None:
        return ""

    return str(value).strip()


def require_environment_flickr_api_key() -> str:
    """Return only an exported Flickr key for metadata-preview mode."""

    api_key = os.environ.get("FLICKR_API_KEY", "").strip()

    if not api_key:
        raise RuntimeError(
            "--metadata-preview requires an exported FLICKR_API_KEY environment "
            "variable"
        )

    return api_key


def sanitize_metadata_text(value: Any) -> str:
    """Normalize public Flickr prose for safe, compact terminal review."""

    text = html.unescape(flickr_content(value))
    text = re.sub(r"<[^>]*>", " ", text)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def metadata_value(mapping: dict[str, Any], key: str) -> MetadataValue:
    """Read a string field while preserving missing-versus-empty state."""

    if key not in mapping:
        return MetadataValue("not-exposed-by-endpoint")

    value = sanitize_metadata_text(mapping.get(key))
    if not value:
        return MetadataValue("fetched-empty")

    return MetadataValue("fetched", value)


def metadata_tags(photo: dict[str, Any]) -> MetadataValue:
    """Normalize public Flickr tags from bulk or getInfo responses."""

    if "tags" not in photo:
        return MetadataValue("not-exposed-by-endpoint")

    tags_value = photo.get("tags")
    if isinstance(tags_value, dict):
        tag_items = tags_value.get("tag", [])
        tags = [
            sanitize_metadata_text(tag.get("raw") or tag.get("_content"))
            for tag in tag_items
            if isinstance(tag, dict)
        ]
    else:
        tags = [sanitize_metadata_text(tag) for tag in str(tags_value or "").split()]

    tags = [tag for tag in tags if tag]
    if not tags:
        return MetadataValue("fetched-empty")

    return MetadataValue("fetched", ", ".join(tags))


def metadata_photo_page_url(
    photo: dict[str, Any],
    owner_alias: str,
    photo_id: str,
) -> str:
    """Prefer Flickr's canonical photo page URL from getInfo."""

    for item in photo.get("urls", {}).get("url", []):
        if item.get("type") == "photopage":
            value = flickr_content(item)
            if value:
                return value

    return f"https://www.flickr.com/photos/{owner_alias}/{photo_id}/"


def allowlisted_exif(response: dict[str, Any]) -> tuple[ExifValue, ...]:
    """Return only the explicitly approved digital-file EXIF fields."""

    values: list[ExifValue] = []

    for item in response.get("photo", {}).get("exif", []):
        key = (str(item.get("tagspace", "")).upper(), str(item.get("tag", "")))
        label = EXIF_ALLOWLIST.get(key)
        if not label:
            continue

        value = sanitize_metadata_text(item.get("clean") or item.get("raw"))
        if value:
            values.append(ExifValue(label=label, value=value))

    return tuple(values)


def extract_album_id(url: str) -> str:
    """Return the Flickr album/photoset ID from a public album URL."""

    match = re.search(r"/(?:albums|sets)/(\d+)", url)

    if not match:
        raise ValueError("Flickr URL must include /albums/<id>/ or /sets/<id>")

    return match.group(1)


def normalize_album_url(url: str, album_id: str) -> str:
    """Normalize Flickr album URLs before using them in requests."""

    parsed = urlparse(url)
    path = parsed.path

    # Flickr accepts both /sets/<id> and /albums/<id>. The journal convention
    # uses /albums/<id>, so normalize to that spelling.
    if f"/sets/{album_id}" in path:
        path = path.replace(f"/sets/{album_id}", f"/albums/{album_id}")

    normalized = parsed._replace(
        query="",
        fragment="",
        path=path.rstrip("/") + "/",
    )
    return normalized.geturl()


def normalize_albums_url(url: str) -> str:
    """Normalize a Flickr `/albums` directory URL."""

    parsed = urlparse(url)
    normalized = parsed._replace(
        query="",
        fragment="",
        path=parsed.path.rstrip("/") + "/",
    )
    return normalized.geturl()


def extract_photos_path_alias(url: str) -> str:
    """Return the Flickr user path segment from a `/photos/<user>` URL."""

    parsed = urlparse(url)
    match = re.search(r"/photos/([^/]+)", parsed.path)

    if not match:
        raise ValueError("Flickr URL must include /photos/<user>")

    return match.group(1)


def build_flickr_user_url(alias: str) -> str:
    """Build a canonical public Flickr profile URL for API lookup."""

    return f"https://www.flickr.com/photos/{alias}/"


def absolute_flickr_url(base_url: str, path_or_url: str) -> str:
    """Convert a Flickr-relative path to an absolute URL."""

    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        return path_or_url

    parsed = urlparse(base_url)
    return f"{parsed.scheme}://{parsed.netloc}{path_or_url}"


def build_oembed_url(album_url: str) -> str:
    """Build Flickr's public oEmbed endpoint URL."""

    query = urlencode({"url": album_url, "format": "json"})
    return f"https://www.flickr.com/services/oembed/?{query}"


def build_photoset_feed_url(owner_nsid: str, album_id: str) -> str:
    """Build Flickr's public photoset feed endpoint URL."""

    query = urlencode(
        {
            "nsid": owner_nsid,
            "set": album_id,
            "lang": "en-us",
            "format": "json",
            "nojsoncallback": "1",
        }
    )
    return f"https://www.flickr.com/services/feeds/photoset.gne?{query}"


def lookup_user_nsid_from_albums_url(albums_url: str) -> str:
    """Resolve a public Flickr `/albums` URL to a stable user NSID."""

    alias = extract_photos_path_alias(albums_url)
    response = fetch_flickr_api(
        "flickr.urls.lookupUser",
        {"url": build_flickr_user_url(alias)},
    )
    user = response.get("user", {})
    nsid = user.get("id")

    if not nsid:
        raise RuntimeError("Flickr API lookupUser did not return a user id")

    return str(nsid)


def build_album_url(owner: str, album_id: str) -> str:
    """Build the journal's preferred album URL shape.

    `owner` can be either a friendly Flickr alias or an NSID. API discovery
    returns an NSID, while direct user-provided URLs often use aliases.
    """

    return f"https://www.flickr.com/photos/{owner}/albums/{album_id}/"


def extract_owner_nsid(album_html: str, album_id: str) -> str:
    """Find the Flickr owner NSID embedded in the album page.

    The public photoset feed needs the owner's NSID, but the friendly album URL
    only includes the path alias (`boocher`). Flickr exposes the NSID in the
    album page's feed link and model data, so we check both places.
    """

    patterns = (
        rf"nsid&#x3D;([^&]+)&amp;set&#x3D;{album_id}",
        r'"ownerNsid":"([^"]+)"',
    )

    for pattern in patterns:
        match = re.search(pattern, album_html)
        if match:
            return html.unescape(match.group(1))

    raise RuntimeError("could not find Flickr owner NSID in album page")


def extract_photo_id(link: str) -> str:
    """Pull the numeric Flickr photo ID out of a photo URL."""

    match = re.search(r"/photos/[^/]+/(\d+)/", link)
    return match.group(1) if match else "unknown"


def decode_html_attribute(value: str) -> str:
    """Decode HTML entities used in Flickr attributes."""

    return html.unescape(value).strip()


def extract_thumbnail_alt(embed_html: str) -> str:
    """Extract the thumbnail alt text from Flickr's oEmbed HTML snippet."""

    match = re.search(r"\salt=['\"]([^'\"]*)['\"]", embed_html)
    return html.unescape(match.group(1)) if match else ""


def extract_album_photo_count(album_html: str, album_id: str) -> int | None:
    """Find the full public photo count in a Flickr album page.

    Flickr's public photoset feed often returns only the first page of items.
    The album page model carries the actual public count, so prefer that for
    journal identity metadata.
    """

    album_model_pattern = re.compile(
        r'"_flickrModelRegistry":"set-models".*?'
        r'"id":"' + re.escape(album_id) + r'"',
        re.DOTALL,
    )
    album_model_match = album_model_pattern.search(album_html)

    if not album_model_match:
        return None

    album_model = album_model_match.group(0)
    count_patterns = (
        r'"publicPhotosCount":(?P<count>\d+)',
        r'"photoCount":(?P<count>\d+)',
        r'"totalItems":(?P<count>\d+)',
    )

    for pattern in count_patterns:
        count_match = re.search(pattern, album_model)
        if count_match:
            return int(count_match.group("count"))

    return None


def label_date(date_taken: str) -> str:
    """Convert Flickr date_taken values to `YYYY-MM-DD HH:MM` labels."""

    if not date_taken:
        return "date unknown"

    cleaned = date_taken.replace("Z", "+0000")
    formats = (
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
    )

    for date_format in formats:
        try:
            parsed = datetime.strptime(cleaned, date_format)
        except ValueError:
            continue
        return parsed.strftime("%Y-%m-%d %H:%M")

    # If Flickr ever returns a new format, keep a useful shortened label rather
    # than failing the whole import.
    return date_taken[:16]


def slugify(value: str) -> str:
    """Make a safe filename slug from a title."""

    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "untitled"


def format_suffix(format_label: str) -> str:
    """Add a small filename suffix for common film formats."""

    lowered = format_label.lower()

    if "35" in lowered:
        return "_35mm"
    if "120" in lowered:
        return "_120"

    return ""


def markdown_escape_inline(value: str) -> str:
    """Avoid breaking inline code spans in generated Markdown."""

    return value.replace("`", "'")


def feed_item_to_photo(item: dict[str, Any]) -> Photo:
    """Normalize one Flickr feed item into a Photo object."""

    link = item.get("link", "")

    return Photo(
        title=item.get("title", ""),
        link=link,
        date_taken=item.get("date_taken", ""),
        photo_id=extract_photo_id(link),
    )


def api_photo_to_photo(photo: dict[str, Any], owner: str, album_id: str) -> Photo:
    """Normalize one Flickr API photo record into a Photo object."""

    photo_id = str(photo.get("id", "unknown"))
    link = f"https://www.flickr.com/photos/{owner}/{photo_id}/in/set-{album_id}/"

    return Photo(
        title=flickr_content(photo.get("title")),
        link=link,
        date_taken=str(photo.get("datetaken", "")),
        photo_id=photo_id,
    )


def deduplicate_photos(photos: list[Photo]) -> list[Photo]:
    """Keep the first occurrence of each known Flickr photo ID."""

    unique: list[Photo] = []
    seen_ids: set[str] = set()

    for photo in photos:
        if photo.photo_id != "unknown":
            if photo.photo_id in seen_ids:
                continue
            seen_ids.add(photo.photo_id)

        unique.append(photo)

    return unique


def fetch_api_photos(owner: str, album_id: str) -> tuple[list[Photo], int]:
    """Fetch every public photo in an album through Flickr API pagination."""

    photos: list[Photo] = []
    page = 1
    total = 0

    while True:
        response = fetch_flickr_api(
            "flickr.photosets.getPhotos",
            {
                "photoset_id": album_id,
                "extras": "date_taken",
                "per_page": API_PAGE_SIZE,
                "page": page,
            },
        )
        photoset = response.get("photoset", {})
        page_photos = photoset.get("photo", [])

        for photo in page_photos:
            photos.append(api_photo_to_photo(photo, owner, album_id))

        # Flickr returns these as strings in some responses. Convert once so
        # loop control is obvious for the next person reading the script.
        current_page = int(photoset.get("page", page))
        pages = int(photoset.get("pages", current_page))
        total = int(photoset.get("total", len(photos)))

        if current_page >= pages:
            break

        page = current_page + 1

    return deduplicate_photos(photos), total


def fetch_metadata_preview_photos(
    owner: str,
    album_id: str,
    *,
    api_key: str,
) -> tuple[list[dict[str, Any]], int, list[str]]:
    """Fetch the complete public album list with one bounded call per page."""

    photos: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    errors: list[str] = []
    page = 1
    total = 0
    expected_total: int | None = None

    while True:
        try:
            response = fetch_flickr_api(
                "flickr.photosets.getPhotos",
                {
                    "photoset_id": album_id,
                    "user_id": owner,
                    "extras": METADATA_PREVIEW_EXTRAS,
                    "per_page": API_PAGE_SIZE,
                    "page": page,
                },
                api_key=api_key,
            )
        except RuntimeError as exc:
            safe_error = redact_flickr_credentials(exc)
            errors.append(f"flickr.photosets.getPhotos page {page}: {safe_error}")
            break
        photoset = response.get("photoset", {})

        try:
            current_page = int(photoset.get("page", page))
            pages = int(photoset.get("pages", current_page))
            page_total = int(photoset.get("total", len(photos)))
        except (TypeError, ValueError):
            errors.append(
                f"flickr.photosets.getPhotos page {page}: invalid pagination "
                "counters"
            )
            break

        if current_page != page:
            errors.append(
                f"requested listing page {page}, but Flickr returned page "
                f"{current_page}"
            )
            break

        if current_page < 1 or pages < current_page:
            errors.append(
                f"flickr.photosets.getPhotos page {page}: inconsistent "
                "pagination counters"
            )
            break

        if expected_total is None:
            expected_total = page_total
        elif page_total != expected_total:
            errors.append(
                f"Flickr listing total changed from {expected_total} to "
                f"{page_total} on page {page}"
            )
            break

        total = page_total

        for photo in photoset.get("photo", []):
            photo_id = str(photo.get("id", ""))
            if not photo_id or photo_id in seen_ids:
                continue
            seen_ids.add(photo_id)
            photos.append(photo)

        if current_page >= pages:
            break

        page = current_page + 1

    return photos, total, errors


def select_metadata_photo_ids(
    photos: list[dict[str, Any]],
    photo_ids: list[str] | None,
    limit: int | None,
) -> tuple[set[str], str]:
    """Resolve an explicit bounded per-photo metadata scope."""

    available_ids = [str(photo.get("id", "")) for photo in photos]

    if photo_ids and limit is not None:
        raise RuntimeError(
            "--metadata-photo-id and --metadata-limit are separate scope controls"
        )

    if limit is not None:
        if limit <= 0:
            raise RuntimeError("--metadata-limit must be greater than zero")
        selected = available_ids[:limit]
        return set(selected), f"first {len(selected)} photo(s) in album order"

    if photo_ids:
        requested = list(dict.fromkeys(str(photo_id) for photo_id in photo_ids))
        missing = [photo_id for photo_id in requested if photo_id not in available_ids]
        if missing:
            raise RuntimeError(
                "requested photo ID(s) not present in public album: "
                + ", ".join(missing)
            )
        return set(requested), f"{len(requested)} explicit photo ID(s)"

    return set(), "bulk album metadata only"


def validate_metadata_scope_args(
    photo_ids: list[str] | None,
    limit: int | None,
) -> None:
    """Reject invalid preview scope before reading credentials or the network."""

    if photo_ids and limit is not None:
        raise RuntimeError(
            "--metadata-photo-id and --metadata-limit are separate scope controls"
        )

    if limit is not None and limit <= 0:
        raise RuntimeError("--metadata-limit must be greater than zero")


def describe_metadata_scope(
    photo_ids: list[str] | None,
    limit: int | None,
) -> str:
    """Describe a requested scope without requiring a successful album fetch."""

    if limit is not None:
        return f"first up to {limit} photo(s) in album order"

    if photo_ids:
        requested = list(dict.fromkeys(str(photo_id) for photo_id in photo_ids))
        return f"{len(requested)} explicit photo ID(s)"

    return "bulk album metadata only"


def bulk_photo_metadata(
    photo: dict[str, Any],
    owner_alias: str,
) -> PhotoMetadataPreview:
    """Normalize one bulk album record before optional detail expansion."""

    photo_id = str(photo.get("id", "unknown"))
    width = metadata_value(photo, "o_width")
    height = metadata_value(photo, "o_height")

    if width.status == "fetched" and height.status == "fetched":
        dimensions = MetadataValue("fetched", f"{width.value} x {height.value}")
    elif width.status == "fetched-empty" or height.status == "fetched-empty":
        dimensions = MetadataValue("fetched-empty")
    else:
        dimensions = MetadataValue("not-exposed-by-endpoint")

    return PhotoMetadataPreview(
        photo_id=photo_id,
        title=sanitize_metadata_text(photo.get("title")),
        photo_page_url=metadata_photo_page_url(photo, owner_alias, photo_id),
        static_image_url=metadata_value(photo, "url_o"),
        dimensions=dimensions,
        date_taken=metadata_value(photo, "datetaken"),
        date_posted=metadata_value(photo, "dateupload"),
        description=MetadataValue("not-requested"),
        tags=metadata_tags(photo),
        metadata_expansion="not-requested",
        exif_status="not-requested",
        exif=(),
    )


def expand_photo_metadata(
    photo: PhotoMetadataPreview,
    owner_alias: str,
    *,
    api_key: str,
    methods_called: list[str],
) -> PhotoMetadataPreview:
    """Fetch getInfo and allowlisted getExif for one explicitly scoped photo."""

    if "flickr.photos.getInfo" not in methods_called:
        methods_called.append("flickr.photos.getInfo")
    info_response = fetch_flickr_api(
        "flickr.photos.getInfo",
        {"photo_id": photo.photo_id},
        api_key=api_key,
    )
    info = info_response.get("photo", {})
    dates = info.get("dates", {})
    description = metadata_value(info, "description")
    tags = metadata_tags(info)
    date_taken = metadata_value(dates, "taken")
    date_posted = metadata_value(dates, "posted")

    error = ""
    try:
        if "flickr.photos.getExif" not in methods_called:
            methods_called.append("flickr.photos.getExif")
        exif_response = fetch_flickr_api(
            "flickr.photos.getExif",
            {"photo_id": photo.photo_id},
            api_key=api_key,
        )
    except FlickrAPIError as exc:
        if exc.code == "2":
            exif_status = "permission-denied"
        else:
            exif_status = "unavailable"
            error = redact_flickr_credentials(exc)
        exif = ()
    except RuntimeError as exc:
        exif_status = "unavailable"
        exif = ()
        error = redact_flickr_credentials(exc)
    else:
        exif = allowlisted_exif(exif_response)
        exif_status = "fetched" if exif else "fetched-empty"

    return PhotoMetadataPreview(
        photo_id=photo.photo_id,
        title=sanitize_metadata_text(info.get("title")) or photo.title,
        photo_page_url=metadata_photo_page_url(info, owner_alias, photo.photo_id),
        static_image_url=photo.static_image_url,
        dimensions=photo.dimensions,
        date_taken=date_taken,
        date_posted=date_posted,
        description=description,
        tags=tags,
        metadata_expansion="fetched",
        exif_status=exif_status,
        exif=exif,
        error=error,
    )


def fetch_album_metadata_preview(
    album_url: str,
    *,
    photo_ids: list[str] | None,
    limit: int | None,
    api_key: str,
) -> AlbumMetadataPreview:
    """Fetch a deterministic, bounded public metadata snapshot."""

    album_id = extract_album_id(album_url)
    normalized_url = normalize_album_url(album_url, album_id)
    owner_alias = extract_photos_path_alias(normalized_url)
    try:
        album_response = fetch_flickr_api(
            "flickr.photosets.getInfo",
            {"photoset_id": album_id},
            api_key=api_key,
        )
        photoset = album_response.get("photoset")
        if not isinstance(photoset, dict) or not photoset:
            raise RuntimeError(
                "flickr.photosets.getInfo did not return an album record"
            )
        owner = str(photoset.get("owner", "")) or owner_alias
        reported_photo_count = int(photoset.get("photos", 0))
    except RuntimeError as exc:
        raise InitialAlbumMetadataError(str(exc)) from exc
    except (TypeError, ValueError) as exc:
        raise InitialAlbumMetadataError(
            "flickr.photosets.getInfo returned an invalid public photo count"
        ) from exc
    bulk_photos, reported_total, errors = fetch_metadata_preview_photos(
        owner,
        album_id,
        api_key=api_key,
    )
    if not errors and len(bulk_photos) != reported_total:
        errors.append(
            f"listed {len(bulk_photos)} unique photo(s), but Flickr reported "
            f"{reported_total}"
        )
    if not errors and reported_photo_count != reported_total:
        errors.append(
            f"album info reported {reported_photo_count} photo(s), but the "
            f"listing reported {reported_total}"
        )
    if errors:
        available_ids = [str(photo.get("id", "")) for photo in bulk_photos]
        requested_scope = describe_metadata_scope(photo_ids, limit)
        if limit is not None:
            selected_ids = set(available_ids[:limit])
        elif photo_ids:
            requested_ids = list(dict.fromkeys(str(item) for item in photo_ids))
            selected_ids = set(requested_ids).intersection(available_ids)
            missing_ids = [item for item in requested_ids if item not in selected_ids]
            if missing_ids:
                errors.append(
                    "listing incomplete; could not verify requested photo ID(s): "
                    + ", ".join(missing_ids)
                )
        else:
            selected_ids = set()
    else:
        selected_ids, requested_scope = select_metadata_photo_ids(
            bulk_photos,
            photo_ids,
            limit,
        )
    photos: list[PhotoMetadataPreview] = []
    methods_called = [
        "flickr.photosets.getInfo",
        "flickr.photosets.getPhotos",
    ]
    for raw_photo in bulk_photos:
        photo = bulk_photo_metadata(raw_photo, owner_alias)
        if photo.photo_id in selected_ids:
            try:
                photo = expand_photo_metadata(
                    photo,
                    owner_alias,
                    api_key=api_key,
                    methods_called=methods_called,
                )
            except RuntimeError as exc:
                safe_error = redact_flickr_credentials(exc)
                photo = PhotoMetadataPreview(
                    photo_id=photo.photo_id,
                    title=photo.title,
                    photo_page_url=photo.photo_page_url,
                    static_image_url=photo.static_image_url,
                    dimensions=photo.dimensions,
                    date_taken=photo.date_taken,
                    date_posted=photo.date_posted,
                    description=MetadataValue("unavailable"),
                    tags=photo.tags,
                    metadata_expansion="unavailable",
                    exif_status="not-requested",
                    exif=(),
                    error=safe_error,
                )
            if photo.error:
                errors.append(f"Photo {photo.photo_id}: {photo.error}")
        photos.append(photo)

    return AlbumMetadataPreview(
        album_id=album_id,
        album_url=normalized_url,
        title=sanitize_metadata_text(photoset.get("title")) or "Untitled",
        description=metadata_value(photoset, "description"),
        retrieved_at_utc=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        requested_scope=requested_scope,
        reported_photo_count=reported_photo_count,
        data_sources=tuple(methods_called),
        photos=tuple(photos),
        complete=not errors,
        errors=tuple(errors),
    )


def render_metadata_value(field: MetadataValue) -> str:
    """Render one metadata field without hiding its availability state."""

    if field.status == "fetched":
        return f"`{markdown_escape_inline(field.value)}`"

    return field.status


def render_album_metadata_preview(preview: AlbumMetadataPreview) -> str:
    """Render a review-only metadata snapshot for stdout."""

    status = "complete" if preview.complete else "incomplete"
    reviewed_photos = [
        photo for photo in preview.photos if photo.metadata_expansion == "fetched"
    ]
    reviewed_descriptions = [
        photo.description.value
        for photo in reviewed_photos
        if photo.description.status == "fetched"
    ]
    repeated_description = ""
    if (
        len(reviewed_photos) > 1
        and len(reviewed_descriptions) == len(reviewed_photos)
        and len(set(reviewed_descriptions)) == 1
    ):
        repeated_description = reviewed_descriptions[0]

    all_reviewed_tags_empty = bool(reviewed_photos) and all(
        photo.tags.status == "fetched-empty" for photo in reviewed_photos
    )
    common_exif_status = ""
    if reviewed_photos:
        exif_statuses = {photo.exif_status for photo in reviewed_photos}
        if len(exif_statuses) == 1:
            candidate = next(iter(exif_statuses))
            if candidate in {"fetched-empty", "permission-denied"}:
                common_exif_status = candidate

    common_static_image_status = ""
    if preview.photos:
        static_statuses = {photo.static_image_url.status for photo in preview.photos}
        if len(static_statuses) == 1:
            candidate = next(iter(static_statuses))
            if candidate != "fetched":
                common_static_image_status = candidate

    common_dimensions_status = ""
    if preview.photos:
        dimension_statuses = {photo.dimensions.status for photo in preview.photos}
        if len(dimension_statuses) == 1:
            candidate = next(iter(dimension_statuses))
            if candidate != "fetched":
                common_dimensions_status = candidate
    data_sources = ", ".join(f"`{method}`" for method in preview.data_sources)
    lines = [
        "# Flickr metadata preview",
        "",
        f"- Status: {status}",
        f"- Album: [{preview.title}]({preview.album_url})",
        f"- Album ID: `{preview.album_id}`",
        f"- Retrieved at (UTC): `{preview.retrieved_at_utc}`",
        f"- Requested scope: {preview.requested_scope}",
        "- Public photo count: "
        + (
            str(preview.reported_photo_count)
            if preview.reported_photo_count is not None
            else "unavailable"
        ),
        f"- Data sources: {data_sources}",
        f"- Album description: {render_metadata_value(preview.description)}",
    ]

    if preview.errors:
        lines.extend(["", "## Retrieval errors", ""])
        for error in preview.errors:
            lines.append(f"- {markdown_escape_inline(error)}")

    if (
        repeated_description
        or all_reviewed_tags_empty
        or common_exif_status
        or common_static_image_status
        or common_dimensions_status
    ):
        lines.extend(["", "## Album-level findings", ""])

        if repeated_description:
            value = markdown_escape_inline(repeated_description)
            lines.append(
                f"- Repeated public description ({len(reviewed_photos)} reviewed "
                f"photos): `{value}`"
            )

        if all_reviewed_tags_empty:
            lines.append(
                f"- Public tags: fetched-empty for all {len(reviewed_photos)} "
                "reviewed photos"
            )

        if common_exif_status:
            lines.append(
                f"- Digital-file EXIF: {common_exif_status} for all "
                f"{len(reviewed_photos)} reviewed photos"
            )

        if common_static_image_status:
            lines.append(
                f"- Static image URL: {common_static_image_status} for all "
                f"{len(preview.photos)} photos"
            )

        if common_dimensions_status:
            lines.append(
                f"- Dimensions: {common_dimensions_status} for all "
                f"{len(preview.photos)} photos"
            )

    lines.extend(["", "## Photos"])

    for photo in preview.photos:
        lines.extend(
            [
                "",
                f"### Photo `{photo.photo_id}`",
                "",
                f"- Flickr photo page: [{photo.title or photo.photo_id}]"
                f"({photo.photo_page_url})",
                f"- Metadata expansion: {photo.metadata_expansion}",
                f"- Flickr date taken: {render_metadata_value(photo.date_taken)}",
                f"- Flickr date posted: {render_metadata_value(photo.date_posted)}",
            ]
        )

        if not common_static_image_status:
            lines.append(
                f"- Static image URL: {render_metadata_value(photo.static_image_url)}"
            )

        if not common_dimensions_status:
            lines.append(f"- Dimensions: {render_metadata_value(photo.dimensions)}")

        if not common_exif_status:
            lines.append(f"- Digital-file EXIF status: {photo.exif_status}")

        if photo.error:
            lines.append(f"- Error: {markdown_escape_inline(photo.error)}")

        if photo.description.value != repeated_description:
            lines.append(
                f"- Public description: {render_metadata_value(photo.description)}"
            )

        if not all_reviewed_tags_empty or photo.metadata_expansion != "fetched":
            lines.append(f"- Public tags: {render_metadata_value(photo.tags)}")

        if photo.exif:
            lines.append("- Digital-file EXIF:")
            for item in photo.exif:
                value = markdown_escape_inline(item.value)
                lines.append(f"  - {item.label}: `{value}`")

    lines.extend(["", "## Candidate journal additions (not written)", ""])

    if not preview.complete:
        lines.append("- No candidate journal additions: preview incomplete.")
    elif repeated_description:
        value = markdown_escape_inline(repeated_description)
        lines.append(
            f"- Public Flickr description, repeated across "
            f"{len(reviewed_photos)} reviewed photos: `{value}`"
        )

    if preview.complete and all_reviewed_tags_empty:
        lines.append(
            f"- Public Flickr tags: none returned for all "
            f"{len(reviewed_photos)} reviewed photos at retrieval time"
        )

    if preview.complete and not repeated_description and not all_reviewed_tags_empty:
        lines.append("- No album-level additions supported by this preview.")

    return "\n".join(lines).rstrip() + "\n"


def fetch_album_api(album_url: str, title_override: str | None) -> Album:
    """Fetch album metadata and all public photos through the Flickr API."""

    album_id = extract_album_id(album_url)
    response = fetch_flickr_api(
        "flickr.photosets.getInfo",
        {"photoset_id": album_id},
    )
    photoset = response.get("photoset", {})
    owner = str(photoset.get("owner", ""))

    if not owner:
        owner = extract_photos_path_alias(album_url)

    normalized_url = normalize_album_url(build_album_url(owner, album_id), album_id)
    title = title_override or flickr_content(photoset.get("title")) or "Untitled"
    photos, api_photo_count = fetch_api_photos(owner, album_id)
    photo_count = int(photoset.get("photos", api_photo_count))

    return Album(
        title=title,
        url=normalized_url,
        short_url="",
        owner=str(photoset.get("username", "")),
        owner_nsid=owner,
        thumbnail_alt="",
        feed_title="",
        feed_modified="",
        photo_count=photo_count,
        starter_photo_count=len(photos),
        photo_listing_source="Flickr API photo list",
        photos=photos,
    )


def fetch_album(album_url: str, title_override: str | None) -> Album:
    """Fetch and normalize album data through the public feed fallback."""

    album_id = extract_album_id(album_url)
    normalized_url = normalize_album_url(album_url, album_id)

    # oEmbed gives us the album title, short URL, author, and thumbnail alt text.
    oembed = fetch_json(build_oembed_url(normalized_url))

    # The page HTML gives us the owner NSID required by the feed endpoint.
    album_html = fetch_text(normalized_url)
    owner_nsid = extract_owner_nsid(album_html, album_id)

    # The feed provides photo title, link, and date_taken for starter photos.
    feed = fetch_json(build_photoset_feed_url(owner_nsid, album_id))
    photos = deduplicate_photos(
        [feed_item_to_photo(item) for item in feed.get("items", [])]
    )
    photo_count = extract_album_photo_count(album_html, album_id) or len(photos)

    title = title_override or oembed.get("title") or feed.get("title", "Untitled")

    return Album(
        title=title,
        url=normalized_url,
        short_url=oembed.get("web_page_short_url", ""),
        owner=oembed.get("author_name", ""),
        owner_nsid=owner_nsid,
        thumbnail_alt=extract_thumbnail_alt(oembed.get("html", "")),
        feed_title=feed.get("title", ""),
        feed_modified=feed.get("modified", ""),
        photo_count=photo_count,
        starter_photo_count=len(photos),
        photo_listing_source="public photoset feed",
        photos=photos,
    )


def extract_album_cards(albums_html: str, albums_url: str) -> list[PublicAlbum]:
    """Extract public album cards from the initial Flickr `/albums` HTML.

    This intentionally starts from server-rendered album links instead of the
    large client model blob. The links are simpler and represent what the page
    exposes publicly without requiring the logged-in browser.
    """

    albums_by_id: dict[str, PublicAlbum] = {}
    pattern = re.compile(
        r'href="(?P<path>/photos/[^"]+/(?:albums|sets)/(?P<id>\d+))"'
        r'\s+title="(?P<title>[^"]*)"',
    )

    for match in pattern.finditer(albums_html):
        album_id = match.group("id")

        # Keep the first card for each album. Flickr repeats some links in
        # scripts and interaction views, and duplicate imports would be noisy.
        if album_id in albums_by_id:
            continue

        raw_url = absolute_flickr_url(albums_url, match.group("path"))
        album_url = normalize_album_url(raw_url, album_id)
        title = decode_html_attribute(match.group("title"))
        albums_by_id[album_id] = PublicAlbum(
            title=title,
            url=album_url,
            album_id=album_id,
            visibility="public",
        )

    return list(albums_by_id.values())


def extract_album_counts(albums_html: str) -> dict[str, tuple[int | None, int | None]]:
    """Extract photo and view counts from Flickr's embedded set models."""

    counts_by_id: dict[str, tuple[int | None, int | None]] = {}
    pattern = re.compile(
        r'"_flickrModelRegistry":"set-models".*?'
        r'"photoCount":(?P<photo_count>\d+).*?'
        r'"viewCount":(?P<view_count>\d+).*?'
        r'"id":"(?P<id>\d+)"',
        re.DOTALL,
    )

    for match in pattern.finditer(albums_html):
        album_id = match.group("id")
        photo_count = int(match.group("photo_count"))
        view_count = int(match.group("view_count"))
        counts_by_id[album_id] = (photo_count, view_count)

    return counts_by_id


def extract_advertised_album_total(
    albums_html: str,
    visible_count: int,
) -> int | None:
    """Find Flickr's advertised total album count when available."""

    totals = []

    for match in re.finditer(r'"totalItems":(?P<total>\d+)', albums_html):
        total = int(match.group("total"))

        if total > visible_count:
            totals.append(total)

    if not totals:
        return None

    # Flickr also exposes broader totals, such as photostream photo count.
    # The album collection total is the smallest value larger than the album
    # cards exposed in the initial HTML.
    return min(totals)


def discover_public_albums(
    albums_url: str,
    *,
    include_excluded: bool = False,
) -> AlbumDiscovery:
    """Discover albums from Flickr's initial public `/albums` HTML."""

    normalized_url = normalize_albums_url(albums_url)
    albums_html = fetch_text(normalized_url)
    albums = extract_album_cards(albums_html, normalized_url)
    counts_by_id = extract_album_counts(albums_html)
    advertised_total = extract_advertised_album_total(
        albums_html,
        visible_count=len(albums),
    )

    enriched = []
    for album in albums:
        photo_count, view_count = counts_by_id.get(album.album_id, (None, None))
        enriched.append(
            PublicAlbum(
                title=album.title,
                url=album.url,
                album_id=album.album_id,
                visibility=album.visibility,
                photo_count=photo_count,
                view_count=view_count,
            )
        )

    discovery = AlbumDiscovery(
        albums=enriched,
        advertised_total=advertised_total,
        source="initial page HTML",
    )
    return discovery if include_excluded else discovery_without_exclusions(discovery)[0]


def api_photoset_to_public_album(
    photoset: dict[str, Any],
    owner_nsid: str,
) -> PublicAlbum:
    """Normalize one public Flickr API photoset into an album summary."""

    album_id = str(photoset.get("id", ""))
    title = flickr_content(photoset.get("title")) or "Untitled"
    photo_count = photoset.get("photos")

    return PublicAlbum(
        title=title,
        url=build_album_url(owner_nsid, album_id),
        album_id=album_id,
        visibility="public",
        photo_count=int(photo_count) if photo_count is not None else None,
        view_count=None,
    )


def discover_api_albums(
    albums_url: str,
    *,
    include_excluded: bool = False,
) -> AlbumDiscovery:
    """Discover all API-visible public albums through Flickr pagination."""

    owner_nsid = lookup_user_nsid_from_albums_url(albums_url)
    albums: list[PublicAlbum] = []
    page = 1
    total = 0

    while True:
        response = fetch_flickr_api(
            "flickr.photosets.getList",
            {
                "user_id": owner_nsid,
                "per_page": API_PAGE_SIZE,
                "page": page,
            },
        )
        photosets = response.get("photosets", {})

        for photoset in photosets.get("photoset", []):
            albums.append(api_photoset_to_public_album(photoset, owner_nsid))

        current_page = int(photosets.get("page", page))
        pages = int(photosets.get("pages", current_page))
        total = int(photosets.get("total", len(albums)))

        if current_page >= pages:
            break

        page = current_page + 1

    discovery = AlbumDiscovery(
        albums=albums,
        advertised_total=total,
        source="Flickr API",
    )
    return discovery if include_excluded else discovery_without_exclusions(discovery)[0]


def find_existing_journal(album: PublicAlbum) -> Path | None:
    """Return an existing journal file that appears to reference an album."""

    title_slug = slugify(album.title)
    candidate_slugs = (
        f"flickr_{title_slug}",
        title_slug,
    )

    for section_dir in SECTION_DIRS.values():
        for journal_path in sorted(section_dir.glob("*.md")):
            if journal_path.stem.startswith(candidate_slugs):
                return journal_path

            try:
                content = journal_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            if album.album_id in content:
                return journal_path

    return None


def iter_journal_paths() -> list[Path]:
    """Return Markdown journal files that can contain Flickr album references."""

    journal_paths: list[Path] = []

    for section_dir in SECTION_DIRS.values():
        for journal_path in sorted(section_dir.glob("*.md")):
            if journal_path.name == "README.md":
                continue

            journal_paths.append(journal_path)

    return journal_paths


def extract_album_ids_from_markdown(markdown: str) -> list[str]:
    """Find Flickr album IDs referenced by a journal file.

    Journals may link albums directly with `/albums/<id>/` or link individual
    photos with Flickr's `/in/set-<id>/` suffix. Both point back to the album
    identity we need for public API reconciliation.
    """

    album_ids: list[str] = []
    patterns = (
        r"flickr\.com/photos/[^)\s]+/(?:albums|sets)/(?P<id>\d+)",
        r"/in/set-(?P<id>\d+)",
    )

    for pattern in patterns:
        for match in re.finditer(pattern, markdown):
            album_id = match.group("id")

            if album_id not in album_ids:
                album_ids.append(album_id)

    return album_ids


def find_known_journal_references() -> list[JournalReference]:
    """Find every Flickr album currently referenced by TradeJournals."""

    references: list[JournalReference] = []

    for journal_path in iter_journal_paths():
        markdown = journal_path.read_text(encoding="utf-8")

        for album_id in extract_album_ids_from_markdown(markdown):
            references.append(
                JournalReference(
                    album_id=album_id,
                    journal_path=journal_path,
                )
            )

    return references


def album_id_from_line(line: str) -> str | None:
    """Return a Flickr album ID when a Markdown line references one."""

    patterns = (
        r"flickr\.com/photos/[^)\s]+/(?:albums|sets)/(?P<id>\d+)",
        r"/in/set-(?P<id>\d+)",
    )

    for pattern in patterns:
        match = re.search(pattern, line)

        if match:
            return match.group("id")

    return None


def reconcile_photo_count_line(album: PublicAlbum, original: str) -> str:
    """Replace only a mismatched numeric photo count in a metadata bullet."""

    if album.photo_count is None:
        return original

    stripped = original.strip()

    if stripped.startswith("- Album status:"):
        count_match = re.search(r"\b(?P<count>\d+)(?=\s+photos?\b)", original)
    elif stripped.startswith("- Public photo count:"):
        count_match = re.search(
            r"^\s*- Public photo count:\s*(?P<count>\d+)\b",
            original,
        )
    else:
        return original

    if not count_match or int(count_match.group("count")) == album.photo_count:
        return original

    start, end = count_match.span("count")
    return original[:start] + str(album.photo_count) + original[end:]


def reconcile_journal_markdown(
    markdown: str,
    public_albums_by_id: dict[str, PublicAlbum],
    journal_path: Path,
) -> tuple[str, list[ReconcileChange]]:
    """Update Flickr count/status bullets in one journal Markdown document."""

    lines = markdown.splitlines()
    changes: list[ReconcileChange] = []
    current_album_id: str | None = None

    for index, line in enumerate(lines):
        if re.match(r"^#{1,6}\s", line):
            current_album_id = None

        referenced_album_id = album_id_from_line(line)

        if referenced_album_id:
            current_album_id = referenced_album_id

        if not current_album_id:
            continue

        album = public_albums_by_id.get(current_album_id)

        if not album:
            continue

        replacement = reconcile_photo_count_line(album, line)

        if line == replacement:
            continue

        changes.append(
            ReconcileChange(
                journal_path=journal_path,
                line_number=index + 1,
                before=line,
                after=replacement,
            )
        )
        lines[index] = replacement

    return "\n".join(lines).rstrip() + "\n", changes


def markdown_table_cell(value: str) -> str:
    """Escape text for use in a Markdown table cell."""

    return value.replace("|", "\\|").replace("\n", " ").strip()


def album_detail_anchor(album: PublicAlbum) -> str:
    """Return the stable in-page anchor for one album detail block."""

    return f"album-{album.album_id}"


def linked_section_cell(row: InventoryRow) -> str:
    """Render a Section table cell with links for confirmed sections only."""

    confirmed_sections = set(SECTION_DIRS)

    if row.section not in confirmed_sections:
        return markdown_table_cell(row.section)

    return f"[{row.section}](#{album_detail_anchor(row.album)})"


def load_inventory_exclusions(inventory_path: Path) -> set[str]:
    """Return album IDs intentionally excluded from TradeJournals.

    The inventory is generated output, so exclusions live in code for now. That
    keeps a bad generated report from preserving an accidental status forever.
    When the user makes more exclusion decisions, add those album IDs to the
    explicit set above or move this to a reviewed config file.
    """

    return set(DEFAULT_EXCLUDED_ALBUM_IDS)


def discovery_without_exclusions(
    discovery: AlbumDiscovery,
) -> tuple[AlbumDiscovery, int]:
    """Remove user-approved exclusions from scan, import, and reconcile flows."""

    albums = [
        album
        for album in discovery.albums
        if album.album_id not in DEFAULT_EXCLUDED_ALBUM_IDS
    ]
    excluded_count = len(discovery.albums) - len(albums)
    return (
        AlbumDiscovery(
            albums=albums,
            advertised_total=discovery.advertised_total,
            source=discovery.source,
        ),
        excluded_count,
    )


def section_from_journal_path(journal_path: Path | None) -> str:
    """Return the TradeJournals section name for a known journal path."""

    if not journal_path:
        return ""

    for section, section_dir in SECTION_DIRS.items():
        try:
            journal_path.relative_to(section_dir)
        except ValueError:
            continue

        return section

    return ""


def guess_section(album_title: str) -> str:
    """Suggest a likely section for an album that has no journal yet."""

    title = album_title.lower()

    if title.startswith("home reno"):
        return "residence?"

    machine_terms = (
        "bike",
        "cycle",
        "vespa",
        "ride",
        "klr",
        "honda",
        "cornhole board",
    )

    if any(term in title for term in machine_terms):
        return "machines?"

    lens_terms = (
        "diana",
        "sxsw",
        "paris",
        "marseille",
        "cassis",
        "ciotat",
        "toulon",
        "turbie",
        "roqueburne",
        "lomography",
        "pinhole",
    )

    if any(term in title for term in lens_terms):
        return "lens?"

    return "review"


def inventory_status(
    album: PublicAlbum,
    existing_journal: Path | None,
    excluded_album_ids: set[str],
) -> str:
    """Classify one album for the inventory gap report."""

    if album.album_id in excluded_album_ids:
        return "excluded"

    if existing_journal:
        return "imported"

    return "gap"


def build_inventory_rows(
    albums: list[PublicAlbum],
    excluded_album_ids: set[str],
) -> list[InventoryRow]:
    """Combine public album data with local journal/import status."""

    rows: list[InventoryRow] = []

    for index, album in enumerate(albums, start=1):
        existing_journal = find_existing_journal(album)
        status = inventory_status(album, existing_journal, excluded_album_ids)
        section = section_from_journal_path(existing_journal)

        if not section and status != "excluded":
            section = guess_section(album.title)

        rows.append(
            InventoryRow(
                index=index,
                album=album,
                status=status,
                section=section,
                existing_journal=existing_journal,
            )
        )

    return rows


def summarize_inventory(rows: list[InventoryRow]) -> dict[str, int]:
    """Count inventory rows by TradeJournals status."""

    summary = {
        "imported": 0,
        "excluded": 0,
        "gap": 0,
    }

    for row in rows:
        summary[row.status] = summary.get(row.status, 0) + 1

    return summary


def render_inventory_report(
    discovery: AlbumDiscovery,
    inventory_path: Path,
) -> str:
    """Render a full public Flickr album inventory and gap report."""

    excluded_album_ids = load_inventory_exclusions(inventory_path)
    rows = build_inventory_rows(discovery.albums, excluded_album_ids)
    summary = summarize_inventory(rows)
    checked_date = datetime.now().strftime("%Y-%m-%d")

    lines = [
        "# Flickr Public Album Inventory",
        "",
        f"Last checked: {checked_date}",
        "",
        "Source: Flickr API public-read scan of",
        "<https://www.flickr.com/photos/boocher/albums>.",
        "",
        "This list only includes albums visible through the public Flickr API.",
        "Private albums are intentionally excluded from this workflow.",
        "",
        "## Summary",
        "",
        f"- Public albums visible via API: {len(discovery.albums)}",
        f"- Existing TradeJournals coverage: {summary.get('imported', 0)}",
        f"- Albums excluded from TradeJournals import: {summary.get('excluded', 0)}",
        f"- Albums still needing review/mapping: {summary.get('gap', 0)}",
        "- API mode: public-read only",
        "- OAuth/private album access: intentionally not used",
        "",
        "## Gap Report",
        "",
        "|#|Album|Photos|Status|Section|Existing Journal|",
        "|---:|---|---:|---|---|---|",
    ]

    for row in rows:
        album = row.album
        existing = display_path(row.existing_journal) if row.existing_journal else ""
        title = markdown_table_cell(album.title)
        section = linked_section_cell(row)
        status = markdown_table_cell(row.status)
        journal = markdown_table_cell(existing)
        lines.append(
            f"|{row.index}|[{title}]({album.url})|"
            f"{format_optional_int(album.photo_count)}|{status}|"
            f"{section}|{journal}|"
        )

    lines.extend(
        [
            "",
            "## Album Details",
            "",
        ]
    )

    for row in rows:
        album = row.album
        lines.extend(
            [
                f'<a id="{album_detail_anchor(album)}"></a>',
                "",
                f"### {row.index}. {album.title}",
                "",
                f"- Album URL: [{album.title}]({album.url})",
                f"- Album ID: `{album.album_id}`",
                f"- Visibility: {album.visibility}",
                f"- Photos: {format_optional_int(album.photo_count)}",
                f"- TradeJournals status: {row.status}",
            ]
        )

        if row.section:
            lines.append(f"- Section: {row.section}")

        if row.existing_journal:
            lines.append(
                f"- Existing journal: `{display_path(row.existing_journal)}`"
            )

        lines.append("")

    generated = "\n".join(lines).rstrip() + "\n"

    if not inventory_path.exists():
        return generated

    existing = inventory_path.read_text(encoding="utf-8")
    return preserve_inventory_annotations(existing, generated, inventory_path)


def inventory_block_ranges(
    markdown: str,
    inventory_path: Path,
    preview: str,
) -> list[tuple[str, int, int]]:
    """Return unique album-detail block ranges keyed by stable Flickr ID."""

    matches = list(
        re.finditer(r'^<a id="album-(?P<id>\d+)"></a>\n', markdown, re.MULTILINE)
    )

    if not matches:
        raise CuratedContentError(
            inventory_path,
            preview,
            "no inventory album anchors could be mapped safely",
        )

    seen_ids: set[str] = set()
    ranges: list[tuple[str, int, int]] = []

    for index, match in enumerate(matches):
        album_id = match.group("id")

        if album_id in seen_ids:
            raise CuratedContentError(
                inventory_path,
                preview,
                f"duplicate album anchor {album_id}",
            )

        seen_ids.add(album_id)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        ranges.append((album_id, match.start(), end))

    return ranges


def inventory_field_name(line: str) -> str | None:
    """Return the importer-owned inventory field represented by one line."""

    for field_name in INVENTORY_DETAIL_FIELDS:
        if line.startswith(f"- {field_name}:"):
            return field_name

    return None


def inventory_preamble_shape(preamble: str) -> list[str]:
    """Normalize generated preamble values while retaining its structure."""

    normalized: list[str] = []
    table_rows_seen = False

    for line in preamble.splitlines():
        if line.startswith("Last checked:"):
            normalized.append("Last checked: <generated>")
            continue

        summary_prefix = next(
            (
                prefix
                for prefix in INVENTORY_NUMERIC_SUMMARY_PREFIXES
                if line.startswith(prefix)
            ),
            None,
        )

        if summary_prefix:
            normalized.append(f"{summary_prefix} <generated>")
            continue

        if line.startswith("|") and line not in {
            "|#|Album|Photos|Status|Section|Existing Journal|",
            "|---:|---|---:|---|---|---|",
        }:
            cells = re.split(r"(?<!\\)\|", line)

            if len(cells) != 8 or not cells[1].isdigit():
                normalized.append(line)
                continue

            if not table_rows_seen:
                normalized.append("|<generated album rows>|")
                table_rows_seen = True
            continue

        normalized.append(line)

    return normalized


def inventory_annotations_for_block(
    block: str,
    album_id: str,
    inventory_path: Path,
    preview: str,
) -> list[tuple[str, str]]:
    """Extract curated lines and their preceding generated-field slot."""

    annotations: list[tuple[str, str]] = []
    fields_seen: set[str] = set()
    heading_seen = False
    current_slot = "heading"

    for line in block.splitlines()[1:]:
        if not line:
            continue

        if line.startswith("### "):
            if heading_seen:
                raise CuratedContentError(
                    inventory_path,
                    preview,
                    f"multiple headings in album block {album_id}",
                )
            heading_seen = True
            current_slot = "heading"
            continue

        field_name = inventory_field_name(line)

        if field_name:
            if field_name in fields_seen:
                raise CuratedContentError(
                    inventory_path,
                    preview,
                    f"duplicate {field_name} field in album block {album_id}",
                )
            fields_seen.add(field_name)
            current_slot = field_name

            if field_name == "Album ID" and f"`{album_id}`" not in line:
                raise CuratedContentError(
                    inventory_path,
                    preview,
                    f"album ID field does not match anchor {album_id}",
                )
            continue

        annotations.append((current_slot, line))

    missing_fields = INVENTORY_REQUIRED_DETAIL_FIELDS - fields_seen

    if not heading_seen or missing_fields:
        missing = ", ".join(sorted(missing_fields)) or "detail heading"
        raise CuratedContentError(
            inventory_path,
            preview,
            f"incomplete album block {album_id}: missing {missing}",
        )

    return annotations


def insert_inventory_annotations(
    block: str,
    annotations: list[tuple[str, str]],
    album_id: str,
    inventory_path: Path,
    preview: str,
) -> str:
    """Insert curated annotation lines after their mapped generated fields."""

    annotations_by_slot: dict[str, list[str]] = {}

    for slot, line in annotations:
        annotations_by_slot.setdefault(slot, []).append(line)

    output_lines: list[str] = []
    used_slots: set[str] = set()

    for raw_line in block.splitlines(keepends=True):
        output_lines.append(raw_line)
        line = raw_line.rstrip("\r\n")
        slot: str | None = None

        if line.startswith("### "):
            slot = "heading"
        else:
            slot = inventory_field_name(line)

        if slot not in annotations_by_slot:
            continue

        output_lines.extend(f"{annotation}\n" for annotation in annotations_by_slot[slot])
        used_slots.add(slot)

    missing_slots = set(annotations_by_slot) - used_slots

    if missing_slots:
        slots = ", ".join(sorted(missing_slots))
        raise CuratedContentError(
            inventory_path,
            preview,
            f"annotation slot missing from album block {album_id}: {slots}",
        )

    return "".join(output_lines)


def preserve_inventory_annotations(
    existing: str,
    generated: str,
    inventory_path: Path,
) -> str:
    """Merge reviewed album annotations into a newly generated inventory."""

    existing_ranges = inventory_block_ranges(existing, inventory_path, generated)
    generated_ranges = inventory_block_ranges(generated, inventory_path, generated)
    existing_preamble = existing[: existing_ranges[0][1]]
    generated_preamble = generated[: generated_ranges[0][1]]

    if inventory_preamble_shape(existing_preamble) != inventory_preamble_shape(
        generated_preamble
    ):
        raise CuratedContentError(
            inventory_path,
            generated,
            "content outside album detail blocks cannot be mapped safely",
        )

    annotations_by_album: dict[str, list[tuple[str, str]]] = {}

    for album_id, start, end in existing_ranges:
        annotations_by_album[album_id] = inventory_annotations_for_block(
            existing[start:end],
            album_id,
            inventory_path,
            generated,
        )

    generated_ids = {album_id for album_id, _, _ in generated_ranges}
    missing_album_ids = set(annotations_by_album) - generated_ids

    if missing_album_ids:
        album_ids = ", ".join(sorted(missing_album_ids))
        raise CuratedContentError(
            inventory_path,
            generated,
            f"existing album blocks missing from generated inventory: {album_ids}",
        )

    merged = generated

    for album_id, start, end in reversed(generated_ranges):
        annotations = annotations_by_album.get(album_id, [])

        if not annotations:
            continue

        block = insert_inventory_annotations(
            merged[start:end],
            annotations,
            album_id,
            inventory_path,
            generated,
        )
        merged = merged[:start] + block + merged[end:]

    return merged


def format_optional_int(value: int | None) -> str:
    """Format optional count fields for report output."""

    return str(value) if value is not None else "?"


def render_discovery_report(discovery: AlbumDiscovery, limit: int | None) -> str:
    """Render a scan-only report for a Flickr albums directory."""

    discovery, excluded_count = discovery_without_exclusions(discovery)
    albums = discovery.albums
    selected_albums = albums[:limit] if limit else albums
    lines = [
        f"Found {len(albums)} public album(s) via {discovery.source}.",
    ]

    if excluded_count:
        label = "exclusion" if excluded_count == 1 else "exclusions"
        lines.append(
            f"Omitted {excluded_count} approved {label} from discovery results."
        )

    if (
        discovery.source == "initial page HTML"
        and discovery.advertised_total
        and discovery.advertised_total > len(albums)
    ):
        lines.append(
            f"Flickr advertises {discovery.advertised_total} total album(s); "
            "the remaining albums appear to require Flickr's lazy-load/API path."
        )
    elif discovery.advertised_total and discovery.advertised_total != len(albums):
        lines.append(
            f"Flickr reports {discovery.advertised_total} total album(s)."
        )

    if limit and len(albums) > limit:
        lines.append(f"Showing first {limit} album(s).")

    lines.extend(
        [
            "",
            "| # | Title | Album ID | Visibility | Photos | Views | Existing Journal |",
            "|---:|---|---|---|---:|---:|---|",
        ]
    )

    for index, album in enumerate(selected_albums, start=1):
        existing = find_existing_journal(album)
        existing_label = display_path(existing) if existing else ""
        lines.append(
            "| "
            f"{index} | "
            f"[{album.title}]({album.url}) | "
            f"`{album.album_id}` | "
            f"{album.visibility} | "
            f"{format_optional_int(album.photo_count)} | "
            f"{format_optional_int(album.view_count)} | "
            f"{existing_label} |"
        )

    return "\n".join(lines)


def build_identity_lines(album: Album, format_label: str) -> list[str]:
    """Build the bullet list for the Album Identity section."""

    safe_title = markdown_escape_inline(album.title)
    identity_lines = [
        "- Platform: Flickr",
        f"- Album name: `{safe_title}`",
        f"- Public album URL: [{album.title}]({album.url})",
    ]

    if album.short_url:
        identity_lines.append(f"- Short URL: [flic.kr]({album.short_url})")

    identity_lines.append(f"- Format: {format_label}, per project note")

    optional_fields = (
        ("Owner", album.owner),
        ("Owner NSID", album.owner_nsid),
        ("Flickr oEmbed thumbnail alt text", album.thumbnail_alt),
        ("Public feed title", album.feed_title),
        ("Public feed modified", album.feed_modified),
    )

    for label, value in optional_fields:
        if value:
            safe_value = markdown_escape_inline(value)
            identity_lines.append(f"- {label}: `{safe_value}`")

    identity_lines.append(f"- Public photo count: {album.photo_count}")
    identity_lines.append(
        f"- Photo IDs listed from {album.photo_listing_source}: "
        f"{album.starter_photo_count}"
    )
    return identity_lines


def default_archive_note() -> str:
    """Return the default Archive Notes paragraph."""

    return (
        "This Flickr album belongs in the visual archive. Keep this Flickr "
        "source separate from any related Lomography catalog entry so platform "
        "metadata, URLs, and image IDs remain clean."
    )


def render_photo_lines(photos: list[Photo]) -> list[str]:
    """Render photo ID bullets for either public feed or API sources."""

    if not photos:
        return ["- No photo items were visible from the selected Flickr source."]

    lines = []

    for photo in photos:
        title = markdown_escape_inline(photo.title)
        label = label_date(photo.date_taken)
        lines.append(
            f"- [{label}, photo {photo.photo_id}]({photo.link}) - "
            f"Flickr title `{title}`."
        )

    return lines


def photo_ids_heading(album: Album) -> str:
    """Choose a photo-ID section heading that matches the data source."""

    if album.photo_listing_source == "Flickr API photo list":
        return "Photo IDs"

    return "Starter Photo IDs"


def render_markdown(album: Album, format_label: str, note: str | None) -> str:
    """Render a complete TradeJournals Markdown entry."""

    safe_title = markdown_escape_inline(album.title)
    note_paragraph = note.strip() if note else default_archive_note()

    lines = [
        f"# Flickr: {album.title}",
        "",
        "## Purpose",
        "",
        (
            f"Catalog the Flickr album `{safe_title}` as part of the "
            "TradeJournals visual evidence archive. This entry records the "
            "public Flickr source, the user-supplied format classification, "
            "and the image-level metadata visible through Flickr."
        ),
        "",
        "## Album Identity",
        "",
        *build_identity_lines(album, format_label),
        "",
        "## Archive Notes",
        "",
        note_paragraph,
        "",
        (
            "The photo titles are preserved as Flickr labels. The "
            "human-readable photo labels below use Flickr's `date_taken` "
            "metadata and drop seconds. API-backed imports can list the full "
            "public album; feed-backed imports may expose only the starter "
            "photo set."
        ),
        "",
        f"## {photo_ids_heading(album)}",
        "",
        *render_photo_lines(album.photos),
    ]

    return "\n".join(lines).rstrip() + "\n"


def render_existing_album_lines(album: Album, format_label: str) -> list[str]:
    """Render Flickr album metadata for an existing journal section."""

    safe_title = markdown_escape_inline(album.title)
    lines = [
        f"- Album name: `{safe_title}`.",
        f"- Album URL: [{album.title}]({album.url}).",
    ]

    if album.short_url:
        lines.append(f"- Short URL: [flic.kr]({album.short_url}).")

    lines.append(f"- Format: {format_label}, per project note.")

    optional_fields = (
        ("Owner", album.owner),
        ("Owner NSID", album.owner_nsid),
        ("Flickr oEmbed thumbnail alt text", album.thumbnail_alt),
        ("Public feed title", album.feed_title),
        ("Public feed modified", album.feed_modified),
    )

    for label, value in optional_fields:
        if value:
            safe_value = markdown_escape_inline(value)
            lines.append(f"- {label}: `{safe_value}`.")

    lines.append(f"- Public photo count: {album.photo_count}.")
    lines.append(
        f"- Photo IDs listed from {album.photo_listing_source}: "
        f"{album.starter_photo_count}."
    )
    return lines


def replace_section_body(
    markdown: str,
    heading: str,
    body_lines: list[str],
) -> tuple[str, bool]:
    """Replace a Markdown section body while preserving neighboring headings."""

    heading_pattern = re.escape(heading)
    pattern = re.compile(
        rf"(^### {heading_pattern}\n\n)(.*?)(?=\n### |\n## |\Z)",
        re.DOTALL | re.MULTILINE,
    )

    def replacement(match: re.Match[str]) -> str:
        """Preserve the original heading and replace only its body."""

        return match.group(1) + "\n".join(body_lines) + "\n"

    updated, count = pattern.subn(replacement, markdown, count=1)
    return updated, count > 0


def section_body(markdown: str, heading: str) -> str | None:
    """Return one level-three section body without changing the document."""

    pattern = re.compile(
        rf"^### {re.escape(heading)}\n\n(?P<body>.*?)(?=\n### |\n## |\Z)",
        re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(markdown)
    return match.group("body") if match else None


def append_visual_evidence_block(
    markdown: str,
    album: Album,
    format_label: str,
) -> str:
    """Append a Flickr block when a journal has no placeholder sections."""

    block_lines = [
        "",
        "### Flickr Album",
        "",
        *render_existing_album_lines(album, format_label),
        "",
        f"### {photo_ids_heading(album)}",
        "",
        *render_photo_lines(album.photos),
    ]
    block = "\n".join(block_lines).rstrip() + "\n"

    if "## Visual Evidence\n" in markdown:
        visual_marker = "## Visual Evidence\n"
        start = markdown.index(visual_marker) + len(visual_marker)
        return markdown[:start] + block + markdown[start:]

    return markdown.rstrip() + "\n\n## Visual Evidence\n" + block


def merge_album_into_journal(
    journal_path: Path,
    album: Album,
    format_label: str,
) -> bool:
    """Merge Flickr album metadata into an existing journal.

    The importer looks for the placeholder sections used by hand-authored
    journals. Existing placeholders may still use the legacy `Starter Photo
    IDs` heading; API imports can still fill that section with the full public
    photo list. If placeholders are missing, the importer appends a compact
    Flickr block under `Visual Evidence` with a source-appropriate heading.
    """

    album_id = extract_album_id(album.url)
    markdown = journal_path.read_text(encoding="utf-8")

    if album.url in markdown or album_id in markdown:
        return False

    targeted_bodies = [
        body
        for heading in ("Flickr Album", "Starter Photo IDs")
        if (body := section_body(markdown, heading)) is not None
    ]
    updated = markdown.replace(
        "- Album URL: pending.",
        f"- Album URL: [{album.title}]({album.url}).",
    )
    updated, album_section_changed = replace_section_body(
        updated,
        "Flickr Album",
        render_existing_album_lines(album, format_label),
    )
    updated, photo_section_changed = replace_section_body(
        updated,
        "Starter Photo IDs",
        render_photo_lines(album.photos),
    )

    if not album_section_changed and not photo_section_changed:
        updated = append_visual_evidence_block(updated, album, format_label)

    preview = updated.rstrip() + "\n"
    if targeted_bodies and any(
        "pending" not in body.casefold() for body in targeted_bodies
    ):
        raise CuratedContentError(journal_path, preview)

    journal_path.write_text(preview, encoding="utf-8")
    return True


def build_readme_entry(
    filename: str,
    title: str,
    format_label: str,
) -> str:
    """Build the one-line README entry for an imported Flickr journal."""

    return (
        f"- [Flickr: {title}]({filename}) - catalog record for a "
        f"{format_label} Flickr album with photo-level metadata."
    )


def update_readme(
    readme_path: Path,
    filename: str,
    title: str,
    format_label: str,
) -> bool:
    """Insert a new journal link into the section README.

    Returns True when the README changed and False when the file was already
    referenced.
    """

    entry = build_readme_entry(filename, title, format_label)
    existing = readme_path.read_text(encoding="utf-8")

    if filename in existing:
        return False

    marker = "## Journals\n\n"

    if marker in existing:
        updated = existing.replace(marker, marker + entry + "\n", 1)
    else:
        updated = existing.rstrip() + "\n\n" + entry + "\n"

    readme_path.write_text(updated, encoding="utf-8")
    return True


def display_path(path: Path) -> str:
    """Show repo-relative paths when possible, absolute paths otherwise."""

    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Import a public Flickr album into a Markdown journal."
    )
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--url", help="Public Flickr album URL.")
    source_group.add_argument(
        "--albums-url",
        help="Public Flickr /albums directory URL to scan.",
    )
    parser.add_argument("--title", help="Album title override.")
    parser.add_argument(
        "--format",
        dest="format_label",
        help="Project classification, such as '35mm film' or '120 film'.",
    )
    parser.add_argument(
        "--section",
        choices=sorted(SECTION_DIRS),
        default="lens",
        help="TradeJournals section to write into.",
    )
    parser.add_argument("--slug", help="Filename slug override.")
    parser.add_argument(
        "--output",
        type=Path,
        help="Explicit output Markdown path.",
    )
    parser.add_argument(
        "--update-readme",
        action="store_true",
        help="Add a link to the target section trade_journals README.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help=(
            "Request regeneration of an existing output; changed Markdown is "
            "previewed and rejected instead of overwritten."
        ),
    )
    parser.add_argument(
        "--merge-existing",
        action="store_true",
        help="Merge album metadata into a matching journal when one exists.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated Markdown instead of writing files.",
    )
    parser.add_argument(
        "--import-discovered",
        action="store_true",
        help="Import albums discovered from --albums-url instead of reporting only.",
    )
    parser.add_argument(
        "--reconcile-known",
        action="store_true",
        help=(
            "Update existing journal Flickr metadata from a public albums scan. "
            "Use with --albums-url and --use-api."
        ),
    )
    parser.add_argument(
        "--write-inventory",
        action="store_true",
        help=(
            "Write a public album inventory/gap report from --albums-url. "
            "Use with --use-api."
        ),
    )
    parser.add_argument(
        "--inventory-output",
        type=Path,
        default=DEFAULT_INVENTORY_PATH,
        help="Inventory Markdown path for --write-inventory.",
    )
    parser.add_argument(
        "--use-api",
        action="store_true",
        help=(
            "Use the Flickr API for discovery and full public photo pagination. "
            "Requires FLICKR_API_KEY."
        ),
    )
    parser.add_argument(
        "--metadata-preview",
        action="store_true",
        help=(
            "Print a read-only public metadata review. Use with --url and "
            "--use-api; this mode never writes files."
        ),
    )
    metadata_scope = parser.add_mutually_exclusive_group()
    metadata_scope.add_argument(
        "--metadata-photo-id",
        action="append",
        dest="metadata_photo_ids",
        help="Expand one explicit Flickr photo ID; repeat for additional IDs.",
    )
    metadata_scope.add_argument(
        "--metadata-limit",
        type=int,
        help="Expand the first N photos in Flickr album order.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit the number of discovered albums to report or import.",
    )
    parser.add_argument("--note", help="Archive note paragraph override.")
    return parser.parse_args()


def choose_output_path(args: argparse.Namespace, album: Album) -> Path:
    """Choose where the generated Markdown file should be written."""

    if args.output:
        return args.output

    slug = args.slug or slugify(album.title) + format_suffix(args.format_label)
    return SECTION_DIRS[args.section] / f"flickr_{slug}.md"


def write_album_markdown(
    output_path: Path,
    markdown: str,
    force: bool,
) -> bool:
    """Write Markdown to disk, protecting existing files by default."""

    if output_path.exists():
        existing = output_path.read_text(encoding="utf-8")

        if existing == markdown:
            return False

        if not force:
            raise RuntimeError(
                f"{output_path} already exists; pass --force to preview changes"
            )

        raise CuratedContentError(output_path, markdown)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    return True


def fetch_album_for_args(
    args: argparse.Namespace,
    album_url: str,
    title: str | None,
) -> Album:
    """Fetch an album with the selected public-feed or API strategy."""

    if args.use_api:
        return fetch_album_api(album_url, title)

    return fetch_album(album_url, title)


def main() -> int:
    """Run the command-line importer."""

    args = parse_args()

    try:
        metadata_preview = getattr(args, "metadata_preview", False)
        metadata_photo_ids = getattr(args, "metadata_photo_ids", None)
        metadata_limit = getattr(args, "metadata_limit", None)

        if not metadata_preview and metadata_photo_ids:
            raise RuntimeError("--metadata-photo-id requires --metadata-preview")

        if not metadata_preview and metadata_limit is not None:
            raise RuntimeError("--metadata-limit requires --metadata-preview")

        if metadata_preview:
            return handle_metadata_preview(args)

        if args.albums_url:
            return handle_albums_directory(args)

        if not args.format_label:
            raise RuntimeError("--format is required when importing one album")

        album = fetch_album_for_args(args, args.url, args.title)
        discovered_album = PublicAlbum(
            title=album.title,
            url=album.url,
            album_id=extract_album_id(album.url),
            visibility="public",
        )
        existing_journal = find_existing_journal(discovered_album)

        if args.merge_existing and existing_journal:
            if args.dry_run:
                print(f"Would merge into {display_path(existing_journal)}")
                return 0

            changed = merge_album_into_journal(
                existing_journal,
                album,
                args.format_label,
            )

            if changed:
                print(f"Merged into {display_path(existing_journal)}")
            else:
                print(f"Already merged {display_path(existing_journal)}")

            return 0

        output_path = choose_output_path(args, album)
        markdown = render_markdown(album, args.format_label, args.note)

        if args.dry_run:
            print(markdown, end="")
            return 0

        wrote_output = write_album_markdown(output_path, markdown, args.force)
        action = "Wrote" if wrote_output else "Unchanged"
        print(f"{action} {display_path(output_path)}")

        if args.update_readme:
            readme_path = output_path.parent / "README.md"
            changed = update_readme(
                readme_path,
                output_path.name,
                album.title,
                args.format_label,
            )

            if changed:
                print(f"Updated {display_path(readme_path)}")
            else:
                print(f"README already references {output_path.name}")

        return 0
    except CuratedContentError as exc:
        print(f"error: {exc}", file=sys.stderr)
        print("\n--- Proposed Markdown preview ---\n")
        print(exc.preview, end="")
        return 1
    except Exception as exc:
        print(
            f"error: {redact_flickr_credentials(exc)}",
            file=sys.stderr,
        )
        return 1


def handle_metadata_preview(args: argparse.Namespace) -> int:
    """Print one bounded public metadata snapshot without writing files."""

    if not args.url:
        raise RuntimeError("--metadata-preview requires --url")

    if not args.use_api:
        raise RuntimeError("--metadata-preview requires --use-api")

    if args.dry_run:
        raise RuntimeError(
            "--metadata-preview is already read-only and cannot use --dry-run"
        )

    photo_ids = getattr(args, "metadata_photo_ids", None)
    limit = getattr(args, "metadata_limit", None)
    validate_metadata_scope_args(photo_ids, limit)
    api_key = require_environment_flickr_api_key()
    try:
        preview = fetch_album_metadata_preview(
            args.url,
            photo_ids=photo_ids,
            limit=limit,
            api_key=api_key,
        )
    except InitialAlbumMetadataError as exc:
        album_id = extract_album_id(args.url)
        preview = AlbumMetadataPreview(
            album_id=album_id,
            album_url=normalize_album_url(args.url, album_id),
            title="Unavailable",
            description=MetadataValue("unavailable"),
            retrieved_at_utc=datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            requested_scope=describe_metadata_scope(photo_ids, limit),
            reported_photo_count=None,
            data_sources=("flickr.photosets.getInfo",),
            photos=(),
            complete=False,
            errors=(redact_flickr_credentials(exc),),
        )
    print(render_album_metadata_preview(preview), end="")
    return 0 if preview.complete else 1


def handle_albums_directory(args: argparse.Namespace) -> int:
    """Scan or batch-import public Flickr albums with the selected strategy."""

    if args.title:
        raise RuntimeError("--title can only be used with --url")

    if args.output:
        raise RuntimeError("--output can only be used with --url")

    if args.slug:
        raise RuntimeError("--slug can only be used with --url")

    if args.reconcile_known and args.import_discovered:
        raise RuntimeError(
            "--reconcile-known and --import-discovered are separate workflows"
        )

    if args.write_inventory and args.import_discovered:
        raise RuntimeError(
            "--write-inventory and --import-discovered are separate workflows"
        )

    if args.write_inventory and args.reconcile_known:
        raise RuntimeError(
            "--write-inventory and --reconcile-known are separate workflows"
        )

    if args.reconcile_known and not args.use_api:
        raise RuntimeError(
            "--reconcile-known requires --use-api so counts come from Flickr API"
        )

    if args.write_inventory and not args.use_api:
        raise RuntimeError(
            "--write-inventory requires --use-api for complete public inventory"
        )

    if args.use_api:
        discovery = discover_api_albums(
            args.albums_url,
            include_excluded=True,
        )
    else:
        discovery = discover_public_albums(
            args.albums_url,
            include_excluded=True,
        )
    if args.reconcile_known:
        eligible_discovery, _ = discovery_without_exclusions(discovery)
        return handle_reconcile_known(args, eligible_discovery)

    if args.write_inventory:
        return handle_write_inventory(args, discovery)

    if not args.import_discovered:
        print(render_discovery_report(discovery, args.limit))
        return 0

    if not args.format_label:
        raise RuntimeError("--format is required with --import-discovered")

    eligible_discovery, excluded_count = discovery_without_exclusions(discovery)
    albums = eligible_discovery.albums
    selected_albums = albums[: args.limit] if args.limit else albums
    imported_count = 0
    dry_merge_count = 0
    dry_write_count = 0
    merged_count = 0
    skipped_count = 0

    for discovered_album in selected_albums:
        existing_journal = find_existing_journal(discovered_album)

        if existing_journal and args.merge_existing:
            album = fetch_album_for_args(
                args,
                discovered_album.url,
                discovered_album.title,
            )

            if args.dry_run:
                dry_merge_count += 1
                print(f"Would merge into {display_path(existing_journal)}")
                continue

            changed = merge_album_into_journal(
                existing_journal,
                album,
                args.format_label,
            )

            if changed:
                merged_count += 1
                print(f"Merged into {display_path(existing_journal)}")
            else:
                skipped_count += 1
                print(f"Already merged {display_path(existing_journal)}")

            continue

        if existing_journal and not args.force:
            skipped_count += 1
            print(f"Skipped existing {display_path(existing_journal)}")
            continue

        album = fetch_album_for_args(
            args,
            discovered_album.url,
            discovered_album.title,
        )
        output_path = choose_output_path(args, album)

        if output_path.exists() and not args.force:
            skipped_count += 1
            print(f"Skipped existing {display_path(output_path)}")
            continue

        markdown = render_markdown(album, args.format_label, args.note)

        if args.dry_run:
            dry_write_count += 1
            print(f"Would write {display_path(output_path)}")
            continue

        wrote_output = write_album_markdown(output_path, markdown, args.force)

        if wrote_output:
            imported_count += 1

        action = "Wrote" if wrote_output else "Unchanged"
        print(f"{action} {display_path(output_path)}")

        if args.update_readme:
            readme_path = output_path.parent / "README.md"
            changed = update_readme(
                readme_path,
                output_path.name,
                album.title,
                args.format_label,
            )
            if changed:
                print(f"Updated {display_path(readme_path)}")

    if args.dry_run:
        print(
            f"Finished discovered dry run: {dry_write_count} would be "
            f"written, {dry_merge_count} would be merged, "
            f"{skipped_count} skipped, {excluded_count} approved "
            "exclusion(s) omitted."
        )
    else:
        print(
            f"Finished discovered import: {imported_count} written, "
            f"{merged_count} merged, {skipped_count} skipped, "
            f"{excluded_count} approved exclusion(s) omitted."
        )
    return 0


def unique_references_by_album(
    references: list[JournalReference],
) -> dict[str, list[Path]]:
    """Group known journal references by Flickr album ID."""

    grouped: dict[str, list[Path]] = {}

    for reference in references:
        grouped.setdefault(reference.album_id, [])

        if reference.journal_path not in grouped[reference.album_id]:
            grouped[reference.album_id].append(reference.journal_path)

    return grouped


def render_reconcile_change(change: ReconcileChange) -> str:
    """Render one proposed or applied line update for console output."""

    return (
        f"- {display_path(change.journal_path)}:{change.line_number}\n"
        f"  - old: {change.before}\n"
        f"  - new: {change.after}"
    )


def handle_write_inventory(
    args: argparse.Namespace,
    discovery: AlbumDiscovery,
) -> int:
    """Write or preview the public Flickr album inventory report."""

    output_path = args.inventory_output
    report = render_inventory_report(discovery, output_path)

    if args.dry_run:
        print(report, end="")
        return 0

    if output_path.exists():
        existing = output_path.read_text(encoding="utf-8")

        if existing == report:
            print(f"Inventory unchanged {display_path(output_path)}")
            return 0

        output_path.write_text(report, encoding="utf-8")
        print(f"Updated {display_path(output_path)}")
        return 0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Wrote {display_path(output_path)}")
    return 0


def handle_reconcile_known(
    args: argparse.Namespace,
    discovery: AlbumDiscovery,
) -> int:
    """Reconcile known journal album metadata against public API discovery."""

    public_albums_by_id = {
        album.album_id: album
        for album in discovery.albums
    }
    references_by_album = unique_references_by_album(
        find_known_journal_references()
    )
    all_changes: list[ReconcileChange] = []
    changed_files = 0

    for journal_path in sorted(
        {path for paths in references_by_album.values() for path in paths}
    ):
        markdown = journal_path.read_text(encoding="utf-8")
        updated, changes = reconcile_journal_markdown(
            markdown,
            public_albums_by_id,
            journal_path,
        )

        if not changes:
            continue

        all_changes.extend(changes)
        changed_files += 1

        if not args.dry_run:
            journal_path.write_text(updated, encoding="utf-8")

    missing_album_ids = sorted(
        album_id
        for album_id in references_by_album
        if album_id not in public_albums_by_id
    )

    action = "Would reconcile" if args.dry_run else "Reconciled"
    print(
        f"{action} {len(all_changes)} line(s) in {changed_files} journal file(s) "
        f"using {len(discovery.albums)} public API-visible album(s)."
    )

    if all_changes:
        print("")

        for change in all_changes:
            print(render_reconcile_change(change))

    if missing_album_ids:
        print("")
        print(
            "Known journal album(s) not visible in the public API scan; "
            "left unchanged:"
        )

        for album_id in missing_album_ids:
            paths = ", ".join(
                display_path(path)
                for path in references_by_album[album_id]
            )
            print(f"- `{album_id}`: {paths}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
