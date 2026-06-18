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
    parser.add_argument("--url", required=True, help="Public Flickr album URL.")
    parser.add_argument("--title", help="Album title override.")
    parser.add_argument(
        "--format",
        required=True,
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
        "--dry-run",
        action="store_true",
        help="Print generated Markdown instead of writing files.",
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
        album = fetch_album(args.url, args.title)
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


if __name__ == "__main__":
    raise SystemExit(main())
