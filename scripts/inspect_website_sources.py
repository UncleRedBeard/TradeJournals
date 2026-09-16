#!/usr/bin/env python3
"""Inspect explicitly selected local sources for website content preparation.

No source files are changed and no network requests are made. The CLI reads a
JSON request array from stdin and writes the complete facts array to stdout.
Input/source failures write one JSON diagnostic to stderr and return status 1;
argument usage errors use argparse's normal status 2.
"""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit

if __package__:
    from .build_site_evidence import EvidenceBuildError, parse_inventory_counts
else:
    from build_site_evidence import EvidenceBuildError, parse_inventory_counts


class SourceInspectionError(ValueError):
    """A selected source cannot produce trustworthy preparation facts."""

    def __init__(self, code: str, record_id: str, field: str, message: str):
        super().__init__(message)
        self.code = code
        self.recordId = record_id
        self.field = field
        self.message = message

    def as_dict(self) -> dict[str, str]:
        return {
            "code": self.code,
            "recordId": self.recordId,
            "field": self.field,
            "message": self.message,
        }


def _validate_request(value: Any, index: int) -> dict[str, str]:
    record_id = f"requests[{index}]"
    if not isinstance(value, dict):
        raise SourceInspectionError(
            "INVALID_REQUEST", record_id, "request", "Request must be an object."
        )
    if isinstance(value.get("key"), str) and value["key"].strip():
        record_id = value["key"]
    unknown = set(value) - {"key", "kind", "path", "anchor"}
    if unknown:
        raise SourceInspectionError(
            "INVALID_REQUEST", record_id, str(next(iter(unknown))),
            "Request contains an unsupported field."
        )
    for field in ("key", "kind", "path"):
        if not isinstance(value.get(field), str) or not value[field].strip():
            raise SourceInspectionError(
                "INVALID_REQUEST", record_id, field,
                "Request field must be a nonempty string."
            )
    if value["kind"] not in {"journal", "inventory", "reference", "media"}:
        raise SourceInspectionError(
            "INVALID_REQUEST", record_id, "kind", "Unsupported source kind."
        )
    if value["kind"] == "inventory":
        anchor = value.get("anchor")
        if not isinstance(anchor, str) or not re.fullmatch(r"album-[A-Za-z0-9][A-Za-z0-9_-]*", anchor):
            raise SourceInspectionError(
                "INVALID_REQUEST", record_id, "anchor",
                "Inventory requests require an exact album-<id> anchor."
            )
    elif "anchor" in value:
        raise SourceInspectionError(
            "INVALID_REQUEST", record_id, "anchor",
            "Only inventory requests may include an anchor."
        )
    return value


def _read_source(root: Path, request: dict[str, str]) -> bytes:
    source = request["path"]
    key = request["key"]
    relative = PurePosixPath(source)
    if relative.is_absolute() or ".." in relative.parts or "\\" in source or "\x00" in source:
        raise SourceInspectionError(
            "INVALID_PATH", key, "path",
            "Source path must be repository-relative without traversal."
        )
    try:
        resolved = (root / source).resolve()
        if not resolved.is_relative_to(root):
            raise SourceInspectionError(
                "INVALID_PATH", key, "path", "Source resolves outside the repository."
            )
        if not resolved.exists():
            raise SourceInspectionError(
                "MISSING_SOURCE", key, "path", "Selected source does not exist."
            )
        if not resolved.is_file():
            raise SourceInspectionError(
                "INVALID_PATH", key, "path", "Selected source must be a file."
            )
        return resolved.read_bytes()
    except (OSError, RuntimeError) as exc:
        raise SourceInspectionError(
            "SOURCE_READ_ERROR", key, "path", "Selected source could not be read."
        ) from exc


def _is_https_url(value: str) -> bool:
    if any(character.isspace() or ord(character) < 32 or ord(character) == 127 for character in value) or "\\" in value:
        return False
    try:
        url = urlsplit(value)
        if (
            url.scheme != "https" or not url.hostname or not url.netloc
            or url.username is not None or url.password is not None
            or (url.port is not None and not 0 < url.port < 65536)
        ):
            return False
        if ":" in url.hostname:
            ipaddress.IPv6Address(url.hostname)
            return True
        host = url.hostname.encode("idna").decode("ascii").rstrip(".")
        return len(host) <= 253 and all(
            re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?", label)
            for label in host.split(".")
        )
    except ValueError:
        return False


def _inspect_inventory(data: bytes, request: dict[str, str]) -> dict[str, Any]:
    key, anchor = request["key"], request["anchor"]
    try:
        markdown = data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    except UnicodeDecodeError as exc:
        raise SourceInspectionError(
            "INVALID_INVENTORY", key, "path", "Inventory must contain UTF-8 text."
        ) from exc

    anchors = list(re.finditer(r'<a id="(album-[^"]+)"></a>', markdown))
    selected = [index for index, match in enumerate(anchors) if match.group(1) == anchor]
    if len(selected) != 1:
        code = "MISSING_ANCHOR" if not selected else "DUPLICATE_ANCHOR"
        raise SourceInspectionError(
            code, key, "anchor", "Selected inventory anchor must occur exactly once."
        )
    index = selected[0]
    end = anchors[index + 1].start() if index + 1 < len(anchors) else len(markdown)
    block = markdown[anchors[index].start():end]

    if len(re.findall(r"^- Photos:[^\n]*$", block, re.MULTILINE)) != 1:
        raise SourceInspectionError(
            "INVALID_INVENTORY", key, "count", "Selected block requires one photo count."
        )
    try:
        count = parse_inventory_counts(block, inventory_name=request["path"])[anchor[6:]]
    except (EvidenceBuildError, KeyError) as exc:
        raise SourceInspectionError(
            "INVALID_INVENTORY", key, "count", "Selected block has no valid photo count."
        ) from exc

    links = re.findall(
        r"^- (?:Album URL|Shared album URL): \[([^\n]+)\]\(([^\n]*)\)[ \t]*$",
        block, re.MULTILINE,
    )
    link_lines = re.findall(r"^- (?:Album URL|Shared album URL):[^\n]*$", block, re.MULTILINE)
    if len(link_lines) != 1 or len(links) != 1 or not links[0][0].strip() or not _is_https_url(links[0][1]):
        raise SourceInspectionError(
            "INVALID_INVENTORY", key, "sourceUrl",
            "Selected block requires one labeled HTTPS album link without credentials."
        )
    label, source_url = links[0]
    return {
        "key": key,
        "sha256": hashlib.sha256(block.encode("utf-8")).hexdigest(),
        "count": count,
        "label": label.strip(),
        "sourceUrl": source_url,
    }


def inspect_sources(repo_root: Path, requests: list[dict]) -> list[dict]:
    """Return scoped fingerprints and album facts, or raise SourceInspectionError.

    Journal, reference and media fingerprints cover original file bytes.
    Inventory fingerprints cover the named album block with LF line endings.
    Only explicitly requested files are read; results preserve request order.
    """
    if not isinstance(requests, list):
        raise SourceInspectionError(
            "INVALID_REQUEST", "requests", "requests", "Requests must be a JSON array."
        )
    try:
        root = Path(repo_root).resolve(strict=True)
        if not root.is_dir():
            raise ValueError("Not a directory")
    except (OSError, RuntimeError, ValueError) as exc:
        raise SourceInspectionError(
            "INVALID_PATH", "repoRoot", "repoRoot", "Repository root must be an existing directory."
        ) from exc

    checked = [_validate_request(request, index) for index, request in enumerate(requests)]
    seen: set[str] = set()
    facts: list[dict] = []
    for request in checked:
        key = request["key"]
        if key in seen:
            raise SourceInspectionError(
                "DUPLICATE_KEY", key, "key", "Source request keys must be unique."
            )
        seen.add(key)
        data = _read_source(root, request)
        if request["kind"] == "inventory":
            facts.append(_inspect_inventory(data, request))
        else:
            facts.append({"key": key, "sha256": hashlib.sha256(data).hexdigest()})
    return facts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True, type=Path)
    args = parser.parse_args()
    try:
        try:
            requests = json.load(sys.stdin)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise SourceInspectionError(
                "INVALID_JSON", "requests", "stdin", "Stdin must contain a JSON request array."
            ) from exc
        facts = inspect_sources(args.repo_root, requests)
    except SourceInspectionError as exc:
        print(json.dumps(exc.as_dict()), file=sys.stderr)
        return 1
    print(json.dumps(facts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
