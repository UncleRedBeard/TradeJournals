#!/usr/bin/env python3
"""Extract IDs, URL-bearing attributes, and robots metadata from HTML documents."""

from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from typing import Any


class _DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.references: list[dict[str, str]] = []
        self.robots: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._collect(tag, attrs)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._collect(tag, attrs)

    def _collect(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name.lower(): "" if value is None else value for name, value in attrs}
        anchor_ids: list[str] = []
        if "id" in values:
            anchor_ids.append(values["id"])
        if tag.lower() == "a" and "name" in values and values["name"] not in anchor_ids:
            anchor_ids.append(values["name"])
        self.ids.extend(anchor_ids)
        for attribute in ("href", "src", "srcset"):
            if attribute in values:
                self.references.append({"tag": tag.lower(), "attribute": attribute, "value": values[attribute]})
        if tag.lower() == "meta" and values.get("name", "").lower() == "robots":
            self.robots.append(values.get("content", ""))


def parse_html(document: str) -> dict[str, list[Any]]:
    parser = _DocumentParser()
    parser.feed(document)
    parser.close()
    return {"ids": parser.ids, "references": parser.references, "robots": parser.robots}


def _error(message: str) -> int:
    print(json.dumps({"error": message}), file=sys.stderr)
    return 1


def main() -> int:
    try:
        requests = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return _error("stdin must contain a JSON array")
    if not isinstance(requests, list):
        return _error("request must be a JSON array")
    parsed: list[dict[str, Any]] = []
    for item in requests:
        if not isinstance(item, dict) or set(item) != {"path", "html"}:
            return _error("each request must contain only path and html")
        if not isinstance(item["path"], str) or not item["path"] or not isinstance(item["html"], str):
            return _error("path and html must be nonempty string and string")
        parsed.append({"path": item["path"], **parse_html(item["html"])})
    print(json.dumps(parsed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
