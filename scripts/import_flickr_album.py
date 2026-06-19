#!/usr/bin/env python3
"""Import a public Flickr album into a TradeJournals Markdown entry.

This is intentionally a small, dependency-free prototype. It uses public
Flickr endpoints only:

1. oEmbed JSON for album-level display metadata.
2. the public album page to discover the owner's NSID.
3. the public photoset feed for photo titles, links, and date_taken values.

The script does not use a Flickr API key and does not access private albums.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "TradeJournals Flickr importer"
FETCH_TIMEOUT_SECONDS = 30

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
    """Small normalized record for one Flickr feed item."""

    title: str
    link: str
    date_taken: str
    photo_id: str


@dataclass(frozen=True)
class Album:
    """Normalized album data used by the Markdown renderer."""

    title: str
    url: str
    short_url: str
    owner: str
    owner_nsid: str
    thumbnail_alt: str
    feed_title: str
    feed_modified: str
    photo_count: int
    photos: list[Photo]


@dataclass(frozen=True)
class PublicAlbum:
    """Summary record for one album discovered from a Flickr /albums page."""

    title: str
    url: str
    album_id: str
    photo_count: int | None = None
    view_count: int | None = None


@dataclass(frozen=True)
class AlbumDiscovery:
    """Result of scanning a public Flickr `/albums` directory."""

    albums: list[PublicAlbum]
    advertised_total: int | None = None


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
        raise RuntimeError(f"failed to fetch {url}: {exc}") from exc

    return body.decode(charset, errors="replace")


def fetch_json(url: str) -> dict[str, Any]:
    """Fetch and parse a JSON response."""

    text = fetch_text(url)

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"failed to parse JSON from {url}: {exc}") from exc


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


def fetch_album(album_url: str, title_override: str | None) -> Album:
    """Fetch and normalize all album data needed for Markdown output."""

    album_id = extract_album_id(album_url)
    normalized_url = normalize_album_url(album_url, album_id)

    # oEmbed gives us the album title, short URL, author, and thumbnail alt text.
    oembed = fetch_json(build_oembed_url(normalized_url))

    # The page HTML gives us the owner NSID required by the feed endpoint.
    album_html = fetch_text(normalized_url)
    owner_nsid = extract_owner_nsid(album_html, album_id)

    # The feed provides photo title, link, date_taken, and public item count.
    feed = fetch_json(build_photoset_feed_url(owner_nsid, album_id))
    photos = [feed_item_to_photo(item) for item in feed.get("items", [])]

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
        photo_count=len(photos),
        photos=photos,
    )


def extract_album_cards(albums_html: str, albums_url: str) -> list[PublicAlbum]:
    """Extract visible public album cards from a Flickr `/albums` page.

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


def discover_public_albums(albums_url: str) -> AlbumDiscovery:
    """Discover public albums visible from a Flickr `/albums` directory."""

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
                photo_count=photo_count,
                view_count=view_count,
            )
        )

    return AlbumDiscovery(albums=enriched, advertised_total=advertised_total)


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


def format_optional_int(value: int | None) -> str:
    """Format optional count fields for report output."""

    return str(value) if value is not None else "?"


def render_discovery_report(discovery: AlbumDiscovery, limit: int | None) -> str:
    """Render a scan-only report for a Flickr albums directory."""

    albums = discovery.albums
    selected_albums = albums[:limit] if limit else albums
    lines = [
        f"Found {len(albums)} public album card(s) in the initial page HTML.",
    ]

    if discovery.advertised_total and discovery.advertised_total > len(albums):
        lines.append(
            f"Flickr advertises {discovery.advertised_total} total album(s); "
            "the remaining albums appear to require Flickr's lazy-load/API path."
        )

    if limit and len(albums) > limit:
        lines.append(f"Showing first {limit} album(s).")

    lines.extend(
        [
            "",
            "| # | Title | Album ID | Photos | Views | Existing Journal |",
            "|---:|---|---|---:|---:|---|",
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
    return identity_lines


def default_archive_note() -> str:
    """Return the default Archive Notes paragraph."""

    return (
        "This Flickr album belongs in the visual archive. Keep this Flickr "
        "source separate from any related Lomography catalog entry so platform "
        "metadata, URLs, and image IDs remain clean."
    )


def render_photo_lines(photos: list[Photo]) -> list[str]:
    """Render the Starter Photo IDs bullet list."""

    if not photos:
        return ["- No public photo items were visible in the Flickr feed."]

    lines = []

    for photo in photos:
        title = markdown_escape_inline(photo.title)
        label = label_date(photo.date_taken)
        lines.append(
            f"- [{label}, photo {photo.photo_id}]({photo.link}) - "
            f"Flickr title `{title}`."
        )

    return lines


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
            "metadata and drop seconds."
        ),
        "",
        "## Starter Photo IDs",
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
        "### Starter Photo IDs",
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

    The importer looks for the placeholder sections used by the hand-authored
    machine journals. If those sections are missing, it appends a compact
    Flickr block under `Visual Evidence` so the album still lands in context.
    """

    album_id = extract_album_id(album.url)
    markdown = journal_path.read_text(encoding="utf-8")

    if album.url in markdown or album_id in markdown:
        return False

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

    journal_path.write_text(updated.rstrip() + "\n", encoding="utf-8")
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
        help="Overwrite the output file if it already exists.",
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
) -> None:
    """Write Markdown to disk, protecting existing files by default."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not force:
        raise RuntimeError(
            f"{output_path} already exists; pass --force to overwrite"
        )

    output_path.write_text(markdown, encoding="utf-8")


def main() -> int:
    """Run the command-line importer."""

    args = parse_args()

    try:
        if args.albums_url:
            return handle_albums_directory(args)

        if not args.format_label:
            raise RuntimeError("--format is required when importing one album")

        album = fetch_album(args.url, args.title)
        discovered_album = PublicAlbum(
            title=album.title,
            url=album.url,
            album_id=extract_album_id(album.url),
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

        write_album_markdown(output_path, markdown, args.force)
        print(f"Wrote {display_path(output_path)}")

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
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


def handle_albums_directory(args: argparse.Namespace) -> int:
    """Scan or batch-import a public Flickr `/albums` directory."""

    if args.title:
        raise RuntimeError("--title can only be used with --url")

    if args.output:
        raise RuntimeError("--output can only be used with --url")

    if args.slug:
        raise RuntimeError("--slug can only be used with --url")

    discovery = discover_public_albums(args.albums_url)
    albums = discovery.albums

    if not args.import_discovered:
        print(render_discovery_report(discovery, args.limit))
        return 0

    if not args.format_label:
        raise RuntimeError("--format is required with --import-discovered")

    selected_albums = albums[: args.limit] if args.limit else albums
    imported_count = 0
    dry_merge_count = 0
    dry_write_count = 0
    merged_count = 0
    skipped_count = 0

    for discovered_album in selected_albums:
        existing_journal = find_existing_journal(discovered_album)

        if existing_journal and args.merge_existing:
            album = fetch_album(discovered_album.url, discovered_album.title)

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

        album = fetch_album(discovered_album.url, discovered_album.title)
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

        write_album_markdown(output_path, markdown, args.force)
        imported_count += 1
        print(f"Wrote {display_path(output_path)}")

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
            f"{skipped_count} skipped."
        )
    else:
        print(
            f"Finished discovered import: {imported_count} written, "
            f"{merged_count} merged, {skipped_count} skipped."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
