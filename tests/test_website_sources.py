"""Offline source-selection and CLI tests for the Astro content preparation."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.inspect_website_sources import SourceInspectionError, inspect_sources


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inspect_website_sources.py"
FIRST_BLOCK = (
    '<a id="album-111"></a>\n\n'
    '### 1. Sample floor\n\n'
    '- Album URL: [Sample floor](https://example.org/albums/111/)\n'
    '- Photos: 12\n\n'
)
SECOND_BLOCK = (
    '<a id="album-222"></a>\n\n'
    '### 2. Other work\n\n'
    '- Album URL: [Other work](https://example.org/albums/222/)\n'
    '- Photos: 9\n'
)


class WebsiteSourceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repo"
        self.root.mkdir()
        self.inventory = self.root / "inventory.md"
        self.inventory.write_text("# Inventory\n\n" + FIRST_BLOCK + SECOND_BLOCK, encoding="utf-8")
        self.request = {
            "key": "inventory:floor",
            "kind": "inventory",
            "path": "inventory.md",
            "anchor": "album-111",
        }

    def inspect_inventory(self):
        return inspect_sources(self.root, [self.request])[0]

    def assert_source_error(self, request, code, field):
        with self.assertRaises(SourceInspectionError) as caught:
            inspect_sources(self.root, [request])
        self.assertEqual(caught.exception.code, code)
        self.assertEqual(caught.exception.field, field)
        return caught.exception

    def test_selected_inventory_produces_facts_and_exact_block_digest(self):
        self.assertEqual(self.inspect_inventory(), {
            "key": "inventory:floor",
            "sha256": hashlib.sha256(FIRST_BLOCK.encode("utf-8")).hexdigest(),
            "count": 12,
            "label": "Sample floor",
            "sourceUrl": "https://example.org/albums/111/",
        })

    def test_unselected_inventory_changes_leave_selected_fingerprint_unchanged(self):
        before = self.inspect_inventory()
        self.inventory.write_text("# Changed heading\n" + FIRST_BLOCK + SECOND_BLOCK.replace("Photos: 9", "Photos: 90"), encoding="utf-8")
        self.assertEqual(self.inspect_inventory(), before)

    def test_selected_inventory_change_changes_digest_and_count(self):
        before = self.inspect_inventory()
        self.inventory.write_text(FIRST_BLOCK.replace("Photos: 12", "Photos: 13") + SECOND_BLOCK, encoding="utf-8")
        after = self.inspect_inventory()
        self.assertNotEqual(after["sha256"], before["sha256"])
        self.assertEqual(after["count"], 13)

    def test_inventory_fingerprints_normalize_line_endings(self):
        before = self.inspect_inventory()
        for ending in ("\r\n", "\r"):
            with self.subTest(ending=repr(ending)):
                self.inventory.write_bytes((FIRST_BLOCK + SECOND_BLOCK).replace("\n", ending).encode("utf-8"))
                self.assertEqual(self.inspect_inventory(), before)

    def test_last_album_block_ends_at_end_of_file(self):
        self.request["anchor"] = "album-222"
        fact = self.inspect_inventory()
        self.assertEqual(fact["count"], 9)
        self.assertEqual(fact["sha256"], hashlib.sha256(SECOND_BLOCK.encode()).hexdigest())

    def test_shared_album_url_and_qualified_count_are_supported(self):
        self.inventory.write_text(FIRST_BLOCK.replace("- Album URL:", "- Shared album URL:").replace("Photos: 12", "Photos: 12 at the latest review"), encoding="utf-8")
        self.assertEqual(self.inspect_inventory()["count"], 12)
        self.assertEqual(self.inspect_inventory()["sourceUrl"], "https://example.org/albums/111/")

    def test_missing_anchor_fails_without_using_a_near_match(self):
        self.assert_source_error({**self.request, "anchor": "album-11"}, "MISSING_ANCHOR", "anchor")

    def test_duplicate_anchor_fails_even_when_duplicate_has_no_count(self):
        self.inventory.write_text(FIRST_BLOCK + SECOND_BLOCK + '<a id="album-111"></a>\nNo count.\n', encoding="utf-8")
        self.assert_source_error(self.request, "DUPLICATE_ANCHOR", "anchor")

    def test_missing_count_or_album_link_fails(self):
        for fragment, field in (("- Photos: 12\n", "count"), ("- Album URL: [Sample floor](https://example.org/albums/111/)\n", "sourceUrl")):
            with self.subTest(field=field):
                self.inventory.write_text(FIRST_BLOCK.replace(fragment, "") + SECOND_BLOCK, encoding="utf-8")
                self.assert_source_error(self.request, "INVALID_INVENTORY", field)

    def test_duplicate_selected_count_or_album_link_fails(self):
        for fragment, field in (("- Photos: 12\n", "count"), ("- Album URL: [Sample floor](https://example.org/albums/111/)\n", "sourceUrl")):
            with self.subTest(field=field):
                self.inventory.write_text(FIRST_BLOCK + fragment + SECOND_BLOCK, encoding="utf-8")
                self.assert_source_error(self.request, "INVALID_INVENTORY", field)

    def test_album_url_requires_valid_https_without_credentials(self):
        urls = (
            "http://example.org/", "https:///missing-host",
            "https://user:secret@example.org/", "javascript:alert(1)",
            "//example.org/", "https://example.org:invalid/",
            "https://exa mple.org/", "https://example.org\\other/",
            "https://exa%mple.org/", "https://-example.org/",
            "https://example..org/", "https://example.org/\x7f",
        )
        for url in urls:
            with self.subTest(url=url):
                self.inventory.write_text(FIRST_BLOCK.replace("https://example.org/albums/111/", url), encoding="utf-8")
                self.assert_source_error(self.request, "INVALID_INVENTORY", "sourceUrl")

    def test_malformed_duplicate_album_link_is_not_silently_ignored(self):
        self.inventory.write_text(FIRST_BLOCK + "- Album URL: broken\n", encoding="utf-8")
        self.assert_source_error(self.request, "INVALID_INVENTORY", "sourceUrl")

    def test_file_kinds_hash_original_bytes_without_text_conversion(self):
        data = b"original\r\nbytes\x00\xff"
        (self.root / "source.bin").write_bytes(data)
        requests = [{"key": kind, "kind": kind, "path": "source.bin"} for kind in ("journal", "reference", "media")]
        self.assertEqual(inspect_sources(self.root, requests), [{"key": request["key"], "sha256": hashlib.sha256(data).hexdigest()} for request in requests])

    def test_only_selected_files_are_read(self):
        (self.root / "unselected.md").write_bytes(b"invalid utf8 \xff")
        (self.root / "selected.md").write_text("Selected", encoding="utf-8")
        self.assertEqual(inspect_sources(self.root, [{"key": "selected", "kind": "journal", "path": "selected.md"}])[0]["key"], "selected")

    def test_missing_source_has_request_key_and_field(self):
        error = self.assert_source_error({"key": "journal:missing", "kind": "journal", "path": "missing.md"}, "MISSING_SOURCE", "path")
        self.assertEqual(error.recordId, "journal:missing")

    def test_directory_is_not_a_source_file(self):
        self.assert_source_error({**self.request, "path": "."}, "INVALID_PATH", "path")

    def test_absolute_traversal_and_backslash_paths_are_rejected(self):
        paths = (str(self.inventory), "../repo/inventory.md", "sub/../inventory.md", "..\\inventory.md", "C:\\inventory.md", "bad\x00path")
        for path in paths:
            with self.subTest(path=path):
                self.assert_source_error({**self.request, "path": path}, "INVALID_PATH", "path")

    def test_symlink_escape_is_rejected(self):
        outside = self.root.parent / "outside.md"
        outside.write_text("Outside", encoding="utf-8")
        (self.root / "escaped.md").symlink_to(outside)
        self.assert_source_error({**self.request, "path": "escaped.md"}, "INVALID_PATH", "path")

    def test_internal_file_symlink_remains_supported(self):
        (self.root / "selected.md").symlink_to(self.inventory)
        self.assertEqual(inspect_sources(self.root, [{**self.request, "path": "selected.md"}]), [self.inspect_inventory()])

    def test_invalid_request_shapes_are_rejected(self):
        cases = (
            (None, "request"),
            ({**self.request, "extra": True}, "extra"),
            ({**self.request, "key": ""}, "key"),
            ({**self.request, "kind": "remote"}, "kind"),
            ({**self.request, "kind": []}, "kind"),
            ({**self.request, "path": None}, "path"),
            ({**self.request, "anchor": "111"}, "anchor"),
            ({key: value for key, value in self.request.items() if key != "anchor"}, "anchor"),
            ({"key": "journal", "kind": "journal", "path": "inventory.md", "anchor": "album-111"}, "anchor"),
        )
        for request, field in cases:
            with self.subTest(request=request):
                self.assert_source_error(request, "INVALID_REQUEST", field)

    def test_duplicate_keys_are_rejected(self):
        with self.assertRaises(SourceInspectionError) as caught:
            inspect_sources(self.root, [self.request, self.request])
        self.assertEqual(caught.exception.code, "DUPLICATE_KEY")

    def test_top_level_requests_must_be_a_list(self):
        with self.assertRaises(SourceInspectionError) as caught:
            inspect_sources(self.root, {"requests": []})
        self.assertEqual(caught.exception.code, "INVALID_REQUEST")

    def test_empty_request_list_is_valid(self):
        self.assertEqual(inspect_sources(self.root, []), [])

    def test_invalid_inventory_encoding_is_actionable(self):
        self.inventory.write_bytes(b"invalid \xff")
        self.assert_source_error(self.request, "INVALID_INVENTORY", "path")

    def run_cli(self, stdin):
        return subprocess.run([sys.executable, str(SCRIPT), "--repo-root", str(self.root)], input=stdin, text=True, capture_output=True, check=False)

    def test_cli_success_is_only_json_facts(self):
        result = self.run_cli(json.dumps([self.request]))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(json.loads(result.stdout), [self.inspect_inventory()])

    def test_cli_failure_is_structured_stderr_without_partial_stdout(self):
        result = self.run_cli(json.dumps([self.request, {"key": "missing", "kind": "journal", "path": "missing.md"}]))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        error = json.loads(result.stderr)
        self.assertEqual(set(error), {"code", "recordId", "field", "message"})
        self.assertEqual((error["code"], error["recordId"], error["field"]), ("MISSING_SOURCE", "missing", "path"))

    def test_cli_malformed_json_is_structured_input_error(self):
        result = self.run_cli("invalid JSON")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertEqual(json.loads(result.stderr)["code"], "INVALID_JSON")


if __name__ == "__main__":
    unittest.main()
