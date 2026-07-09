#!/usr/bin/env python3
"""Import Google Photos album evidence from a durable manifest or local export.

Google Photos shared album pages are not treated as a stable public API in this
project. This script records a source album and, when provided, turns a small
JSON manifest or local export folder into a Markdown journal entry.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SECTION_DIRS = {
    "residence": Path("01_the_residence_1894/trade_journals"),
    "forge": Path("02_the_forge_and_shop/trade_journals"),
    "machines": Path("03_the_machines/trade_journals"),
    "materials": Path("04_materials_and_alchemy/trade_journals"),
    "lens": Path("05_the_lens/trade_journals"),
}

IMAGE_EXTENSIONS = {
    ".avif",
    ".gif",
    ".heic",
    ".jpeg",
    ".jpg",
    ".png",
    ".tif",
    ".tiff",
    ".webp",
}


@dataclass
class PhotoEvidence:
    """Normalized photo evidence used by the Markdown generator."""

    title: str
    source: str
    date_taken: str = ""
    description: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a Google Photos-backed TradeJournals entry."
    )
    parser.add_argument("--share-url", help="Google Photos shared album URL.")
    parser.add_argument("--title", help="Album title to use in Markdown.")
    parser.add_argument(
        "--section",
        choices=sorted(SECTION_DIRS),
        required=True,
        help="TradeJournals section to write into.",
    )
    parser.add_argument(
        "--format",
        default="Google Photos visual archive",
        help="Short format/classification note for the album.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="JSON manifest with album metadata and photo evidence.",
    )
    parser.add_argument(
        "--local-dir",
        type=Path,
        help="Local photo export directory to list as evidence.",
    )
    parser.add_argument("--output", type=Path, help="Explicit output path.")
    parser.add_argument("--note", help="Archive note paragraph.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "google_photos_album"


def album_key_from_url(url: str | None) -> str:
    if not url:
        return "unknown"
    token = url.rstrip("/").split("/")[-1]
    return re.sub(r"[^A-Za-z0-9_-]", "", token)[:18] or "unknown"


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def first_present(mapping: dict[str, Any], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = mapping.get(key)
        if value is not None:
            return str(value)
    return ""


def normalize_photo(item: dict[str, Any]) -> PhotoEvidence:
    title = first_present(item, ("title", "name", "filename", "file_name"))
    source = first_present(item, ("url", "source_url", "share_url", "path"))
    date_taken = first_present(
        item,
        ("date_taken", "taken_at", "creation_time", "timestamp"),
    )
    description = first_present(item, ("description", "note", "caption"))

    if not title:
        title = Path(source).name if source else "untitled Google Photos item"

    return PhotoEvidence(
        title=title,
        source=source,
        date_taken=date_taken,
        description=description,
    )


def photos_from_manifest(path: Path) -> tuple[dict[str, Any], list[PhotoEvidence]]:
    payload = read_json(path)
    if isinstance(payload, list):
        return {}, [normalize_photo(item) for item in payload]

    if not isinstance(payload, dict):
        raise ValueError("Manifest must be a JSON object or a list of photos.")

    album = payload.get("album", {})
    photos = payload.get("photos", payload.get("items", []))
    if not isinstance(album, dict) or not isinstance(photos, list):
        raise ValueError("Manifest needs an object album and list photos/items.")

    return album, [normalize_photo(item) for item in photos]


def sidecar_data(path: Path) -> dict[str, Any]:
    """Read simple Google Takeout-style JSON sidecars when they exist."""
    candidates = [
        path.with_suffix(path.suffix + ".json"),
        path.with_suffix(".json"),
    ]
    for candidate in candidates:
        if candidate.exists():
            payload = read_json(candidate)
            if isinstance(payload, dict):
                return payload
    return {}


def photos_from_local_dir(path: Path) -> list[PhotoEvidence]:
    if not path.exists() or not path.is_dir():
        raise ValueError(f"Local export directory does not exist: {path}")

    photos: list[PhotoEvidence] = []
    for item in sorted(path.iterdir()):
        if item.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        sidecar = sidecar_data(item)
        title = first_present(sidecar, ("title", "name")) or item.name
        description = first_present(sidecar, ("description", "caption"))
        date_taken = ""

        photo_taken = sidecar.get("photoTakenTime")
        if isinstance(photo_taken, dict):
            date_taken = first_present(photo_taken, ("formatted", "timestamp"))

        photos.append(
            PhotoEvidence(
                title=title,
                source=str(item),
                date_taken=date_taken,
                description=description,
            )
        )

    return photos


def link_or_code(label: str, source: str) -> str:
    if source.startswith(("http://", "https://")):
        return f"[{label}]({source})"
    if source:
        return f"`{source}`"
    return label


def markdown_for_album(
    *,
    title: str,
    share_url: str | None,
    section: str,
    format_note: str,
    note: str | None,
    photos: list[PhotoEvidence],
    source_mode: str,
) -> str:
    url_line = (
        f"- Shared album URL: [{title}]({share_url})"
        if share_url
        else "- Shared album URL: pending"
    )
    photo_count = len(photos)
    status = "image manifest imported" if photo_count else "source recorded"

    lines = [
        f"# Google Photos: {title}",
        "",
        "## Purpose",
        "",
        (
            f"Catalog the Google Photos album `{title}` as part of the "
            "TradeJournals visual evidence archive."
        ),
        "",
        "## Album Identity",
        "",
        "- Platform: Google Photos",
        f"- Album name: `{title}`",
        url_line,
        f"- Format: {format_note}",
        f"- TradeJournals section: `{section}`",
        f"- Import status: {status}",
        f"- Source mode: {source_mode}",
        f"- Photo evidence count: {photo_count}",
        "",
        "## Archive Notes",
        "",
    ]

    if note:
        lines.extend([note, ""])

    lines.extend(
        [
            (
                "Google Photos shared album pages are not treated as a stable "
                "public metadata API for this project. Durable image-level "
                "evidence should come from a project manifest, a local export, "
                "or a future authenticated importer."
            ),
            "",
            "## Photo Evidence",
            "",
        ]
    )

    if not photos:
        lines.extend(
            [
                "- Image-level evidence pending a manifest or local export.",
                "- Album title, date range, and section placement should be "
                "confirmed during the first visual review.",
            ]
        )
    else:
        for photo in photos:
            label = photo.title
            if photo.date_taken:
                label = f"{photo.date_taken} - {label}"

            item = f"- {link_or_code(label, photo.source)}"
            if photo.description:
                item += f" - {photo.description}"
            lines.append(item)

    return "\n".join(lines).rstrip() + "\n"


def resolve_output_path(
    *,
    output: Path | None,
    section: str,
    title: str,
    share_url: str | None,
) -> Path:
    if output:
        return output

    album_key = album_key_from_url(share_url)
    slug = slugify(title)
    if slug.startswith("google_photos_shared_album"):
        filename = f"{slug}.md"
    else:
        filename = f"google_photos_{slug}.md"

    if album_key != "unknown" and slug == "google_photos_shared_album":
        filename = f"google_photos_shared_album_{album_key.lower()}.md"

    return SECTION_DIRS[section] / filename


def main() -> None:
    args = parse_args()
    album: dict[str, Any] = {}
    photos: list[PhotoEvidence] = []
    source_modes: list[str] = []

    if args.manifest:
        album, photos = photos_from_manifest(args.manifest)
        source_modes.append(f"manifest: {args.manifest}")

    if args.local_dir:
        photos.extend(photos_from_local_dir(args.local_dir))
        source_modes.append(f"local export: {args.local_dir}")

    title = (
        args.title
        or first_present(album, ("title", "album_title", "name"))
        or f"Google Photos Shared Album {album_key_from_url(args.share_url)}"
    )
    share_url = args.share_url or first_present(album, ("share_url", "url"))
    source_mode = ", ".join(source_modes) if source_modes else "share URL only"

    markdown = markdown_for_album(
        title=title,
        share_url=share_url,
        section=args.section,
        format_note=args.format,
        note=args.note,
        photos=photos,
        source_mode=source_mode,
    )

    output = resolve_output_path(
        output=args.output,
        section=args.section,
        title=title,
        share_url=share_url,
    )

    if args.dry_run:
        print(markdown, end="")
        return

    if output.exists() and not args.force:
        raise FileExistsError(f"Refusing to overwrite existing file: {output}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
