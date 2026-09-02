#!/usr/bin/env python3
"""Build the static website evidence manifest from tracked archive sources.

The builder is deliberately offline. Curated search language and presentation
metadata live in ``site_example/evidence-source.json``; album counts come from
the repository's Flickr and Google Photos inventories. The generated JavaScript
keeps the static site usable without a framework or runtime API.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_PATH = REPO_ROOT / "site_example" / "evidence-source.json"
DEFAULT_OUTPUT_PATH = REPO_ROOT / "site_example" / "evidence-manifest.js"
FLICKR_INVENTORY_PATH = REPO_ROOT / "FLICKR_PUBLIC_ALBUMS.md"
GOOGLE_INVENTORY_PATH = REPO_ROOT / "GOOGLE_PHOTOS_ALBUMS.md"
SITE_HTML_PATH = REPO_ROOT / "site_example" / "index.html"
MANIFEST_PREFIX = "window.tradeJournalEvidence = Object.freeze("
MANIFEST_SUFFIX = ");\n"


class EvidenceBuildError(ValueError):
    """Raised when tracked evidence cannot safely produce a site manifest."""


def parse_inventory_counts(markdown: str, *, inventory_name: str) -> dict[str, int]:
    """Return album counts keyed by inventory anchor ID."""

    anchors = list(re.finditer(r'<a id="album-([^\"]+)"></a>', markdown))
    counts: dict[str, int] = {}

    for index, match in enumerate(anchors):
        album_id = match.group(1)
        section_end = anchors[index + 1].start() if index + 1 < len(anchors) else len(markdown)
        section = markdown[match.end() : section_end]
        count_match = re.search(r"^- Photos:\s*(\d+)\b", section, flags=re.MULTILINE)
        if count_match is None:
            continue
        if album_id in counts:
            raise EvidenceBuildError(
                f"Duplicate album anchor {album_id!r} in {inventory_name}"
            )
        counts[album_id] = int(count_match.group(1))

    if not counts:
        raise EvidenceBuildError(f"No album counts found in {inventory_name}")
    return counts


def parse_public_flickr_album_total(markdown: str) -> int:
    """Read the inventory's public-album summary value."""

    match = re.search(
        r"^- Public albums visible via API:\s*(\d+)\s*$",
        markdown,
        flags=re.MULTILINE,
    )
    if match is None:
        raise EvidenceBuildError("Flickr public-album summary is missing")
    return int(match.group(1))


def require_mapping(value: Any, *, label: str) -> Mapping[str, Any]:
    """Validate a JSON object boundary with a useful error."""

    if not isinstance(value, Mapping):
        raise EvidenceBuildError(f"{label} must be a JSON object")
    return value


def require_nonempty_string(value: Any, *, label: str) -> str:
    """Validate a required non-empty string."""

    if not isinstance(value, str) or not value.strip():
        raise EvidenceBuildError(f"{label} must be a non-empty string")
    return value


def build_manifest(
    *,
    repo_root: Path,
    source_path: Path,
    flickr_inventory_path: Path,
    google_inventory_path: Path,
    html_path: Path,
) -> dict[str, Any]:
    """Build and validate the browser-facing evidence manifest."""

    source = require_mapping(
        json.loads(source_path.read_text(encoding="utf-8")),
        label="Evidence source",
    )
    schema_version = source.get("schemaVersion")
    if not isinstance(schema_version, int) or schema_version < 1:
        raise EvidenceBuildError("schemaVersion must be a positive integer")
    flickr_markdown = flickr_inventory_path.read_text(encoding="utf-8")
    google_markdown = google_inventory_path.read_text(encoding="utf-8")
    html = html_path.read_text(encoding="utf-8")
    inventory_counts = {
        "flickr": parse_inventory_counts(
            flickr_markdown,
            inventory_name=flickr_inventory_path.name,
        ),
        "google_photos": parse_inventory_counts(
            google_markdown,
            inventory_name=google_inventory_path.name,
        ),
    }

    archive_source = require_mapping(source.get("archive"), label="archive")
    connected_practices = archive_source.get("connectedPractices")
    if not isinstance(connected_practices, int) or connected_practices < 1:
        raise EvidenceBuildError("archive.connectedPractices must be a positive integer")

    journals_source = source.get("journals")
    if not isinstance(journals_source, list) or not journals_source:
        raise EvidenceBuildError("journals must be a non-empty JSON array")

    seen_targets: set[str] = set()
    seen_album_keys: set[str] = set()
    journals: list[dict[str, Any]] = []

    for position, raw_entry in enumerate(journals_source, start=1):
        entry = dict(require_mapping(raw_entry, label=f"journals[{position}]"))
        title = require_nonempty_string(entry.get("title"), label=f"journals[{position}].title")
        target = require_nonempty_string(
            entry.get("target"),
            label=f"journals[{position}].target",
        )
        if target in seen_targets:
            raise EvidenceBuildError(f"Duplicate target {target!r}")
        if f'id="{target}"' not in html:
            raise EvidenceBuildError(f"Target #{target} for {title!r} is missing from index.html")
        seen_targets.add(target)

        journal_path = require_nonempty_string(
            entry.get("source"),
            label=f"journals[{position}].source",
        )
        resolved_journal = (repo_root / journal_path).resolve()
        if (
            not resolved_journal.is_relative_to(repo_root.resolve())
            or not resolved_journal.is_file()
        ):
            raise EvidenceBuildError(f"Journal source does not exist: {journal_path}")

        require_nonempty_string(entry.get("area"), label=f"area for {title!r}")
        require_nonempty_string(entry.get("summary"), label=f"summary for {title!r}")
        tags = entry.get("tags")
        if (
            not isinstance(tags, list)
            or not tags
            or any(not isinstance(tag, str) or not tag.strip() for tag in tags)
        ):
            raise EvidenceBuildError(f"tags for {title!r} must contain non-empty strings")

        evidence = require_mapping(entry.get("evidence"), label=f"evidence for {title!r}")
        for field_name in ("stage", "recorded", "sourceLabel"):
            require_nonempty_string(
                evidence.get(field_name),
                label=f"evidence.{field_name} for {title!r}",
            )
        if "boundary" in evidence:
            require_nonempty_string(
                evidence.get("boundary"),
                label=f"evidence.boundary for {title!r}",
            )

        images = entry.get("images", [])
        if not isinstance(images, list):
            raise EvidenceBuildError(f"images for {title!r} must be an array")
        for image_position, raw_image in enumerate(images, start=1):
            image = require_mapping(
                raw_image,
                label=f"images[{image_position}] for {title!r}",
            )
            image_path = require_nonempty_string(
                image.get("src"),
                label=f"image src for {title!r}",
            )
            require_nonempty_string(
                image.get("alt"),
                label=f"image alt for {title!r}",
            )
            resolved_image = (html_path.parent / image_path).resolve()
            if not resolved_image.is_file():
                raise EvidenceBuildError(f"Image source does not exist: {image_path}")

        albums = entry.get("albums", [])
        if not isinstance(albums, list):
            raise EvidenceBuildError(f"albums for {title!r} must be an array")
        resolved_albums: list[dict[str, Any]] = []
        for raw_album in albums:
            album = dict(require_mapping(raw_album, label=f"album for {title!r}"))
            platform = require_nonempty_string(
                album.get("platform"),
                label=f"album platform for {title!r}",
            )
            album_id = require_nonempty_string(
                album.get("id"),
                label=f"album id for {title!r}",
            )
            require_nonempty_string(
                album.get("label"),
                label=f"album label for {title!r}",
            )
            shown = album.get("shown")
            if not isinstance(shown, int) or shown < 0:
                raise EvidenceBuildError(
                    f"album shown count for {title!r} must be a non-negative integer"
                )
            platform_counts = inventory_counts.get(platform)
            if platform_counts is None:
                raise EvidenceBuildError(f"Unsupported album platform: {platform}")
            if album_id not in platform_counts:
                raise EvidenceBuildError(
                    f"Album {platform}:{album_id} for {title!r} is absent from its inventory"
                )

            album_key = f"{platform}:{album_id}"
            if album_key in seen_album_keys:
                raise EvidenceBuildError(f"Album is assigned more than once: {album_key}")
            seen_album_keys.add(album_key)
            album["key"] = album_key
            album["count"] = platform_counts[album_id]
            resolved_albums.append(album)

            fallback_pattern = re.compile(
                rf'<span\s+data-album-count="{re.escape(album_key)}">'
                rf'{platform_counts[album_id]}</span>'
            )
            if fallback_pattern.search(html) is None:
                raise EvidenceBuildError(
                    f"HTML fallback count for {album_key} must be {platform_counts[album_id]}"
                )

        entry["url"] = f"#{target}"
        entry["albums"] = resolved_albums
        journals.append(entry)

    return {
        "schemaVersion": schema_version,
        "archive": {
            "publicFlickrAlbums": parse_public_flickr_album_total(flickr_markdown),
            "connectedPractices": connected_practices,
        },
        "journals": journals,
    }


def render_manifest(manifest: Mapping[str, Any]) -> str:
    """Render deterministic JavaScript for a classic static page."""

    payload = json.dumps(manifest, indent=2, ensure_ascii=False)
    return f"{MANIFEST_PREFIX}{payload}{MANIFEST_SUFFIX}"


def write_or_check_manifest(*, output_path: Path, rendered: str, check: bool) -> None:
    """Write atomically, or fail when the checked-in output is stale."""

    if check:
        current = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
        if current != rendered:
            raise EvidenceBuildError(
                f"{output_path} is stale; run scripts/build_site_evidence.py"
            )
        return

    temporary_path = output_path.with_suffix(f"{output_path.suffix}.tmp")
    temporary_path.write_text(rendered, encoding="utf-8")
    temporary_path.replace(output_path)


def build_parser() -> argparse.ArgumentParser:
    """Return the command-line parser."""

    parser = argparse.ArgumentParser(
        description="Build the static TradeJournals website evidence manifest.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail without writing when the checked-in manifest is stale.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Build the default repository manifest."""

    args = build_parser().parse_args(argv)
    try:
        manifest = build_manifest(
            repo_root=REPO_ROOT,
            source_path=DEFAULT_SOURCE_PATH,
            flickr_inventory_path=FLICKR_INVENTORY_PATH,
            google_inventory_path=GOOGLE_INVENTORY_PATH,
            html_path=SITE_HTML_PATH,
        )
        write_or_check_manifest(
            output_path=DEFAULT_OUTPUT_PATH,
            rendered=render_manifest(manifest),
            check=args.check,
        )
    except (EvidenceBuildError, OSError, json.JSONDecodeError) as exc:
        print(f"Site evidence build failed: {exc}", file=sys.stderr)
        return 1

    action = "is current" if args.check else "updated"
    print(f"Site evidence manifest {action}: {DEFAULT_OUTPUT_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
