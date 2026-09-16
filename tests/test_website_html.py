"""Focused HTML extraction and stdin/stdout contract checks."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from scripts.check_website_html import parse_html


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_website_html.py"


class WebsiteHtmlTests(unittest.TestCase):
    def test_collects_decoded_targets_and_references(self):
        result = parse_html(
            '<section id="care&amp;repair"><a name="old-office" '
            'href="/work/?a=1&amp;b=2#care&#38;repair">Office</a>'
            '<img src="/media/floor.jpg" '
            'srcset="/media/floor.jpg 1x, /media/floor-large.jpg 2x"></section>'
        )
        self.assertEqual(result["ids"], ["care&repair", "old-office"])
        self.assertEqual(result["references"], [
            {"tag": "a", "attribute": "href", "value": "/work/?a=1&b=2#care&repair"},
            {"tag": "img", "attribute": "src", "value": "/media/floor.jpg"},
            {"tag": "img", "attribute": "srcset",
             "value": "/media/floor.jpg 1x, /media/floor-large.jpg 2x"},
        ])
        self.assertEqual(result["robots"], [])

    def test_handles_uppercase_self_closing_source_and_link_tags(self):
        result = parse_html(
            '<LINK HREF="/styles/site.css"/><picture>'
            '<SOURCE SRCSET="/media/small.jpg 400w, /media/large.jpg 800w"/>'
            '<img src="/media/large.jpg" /></picture>'
            '<META NAME="ROBOTS" CONTENT="noindex, nofollow"/>'
        )
        self.assertEqual(result["references"], [
            {"tag": "link", "attribute": "href", "value": "/styles/site.css"},
            {"tag": "source", "attribute": "srcset",
             "value": "/media/small.jpg 400w, /media/large.jpg 800w"},
            {"tag": "img", "attribute": "src", "value": "/media/large.jpg"},
        ])
        self.assertEqual(result["robots"], ["noindex, nofollow"])

    def test_ignores_fake_tags_in_comments_script_and_style_text(self):
        result = parse_html(
            '<!-- <a id="comment" href="/missing/"> -->'
            '<script src="/search.js">const x = \'<a href="/fake/" id="fake">\';</script>'
            '<style>p::before { content: \'<img src="/fake.jpg">\'; }</style>'
        )
        self.assertEqual(result["ids"], [])
        self.assertEqual(result["references"], [
            {"tag": "script", "attribute": "src", "value": "/search.js"},
        ])

    def test_preserves_duplicate_targets_between_elements(self):
        result = parse_html('<div id="office"></div><a name="office"></a>')
        self.assertEqual(result["ids"], ["office", "office"])

    def test_one_legacy_anchor_with_matching_id_and_name_is_one_target(self):
        result = parse_html('<a id="office" name="office"></a><a id="new" name="old"></a>')
        self.assertEqual(result["ids"], ["office", "new", "old"])

    def test_ignores_non_anchor_names_but_retains_empty_url_attributes(self):
        result = parse_html('<input name="title"><a href=""><img src><div id=""></div>')
        self.assertEqual(result["ids"], [""])
        self.assertEqual(result["references"], [
            {"tag": "a", "attribute": "href", "value": ""},
            {"tag": "img", "attribute": "src", "value": ""},
        ])

    def test_decodes_entities_only_once(self):
        result = parse_html('<a href="/a?x=&amp;amp;" id="a&amp;amp;"></a>')
        self.assertEqual(result["ids"], ["a&amp;"])
        self.assertEqual(result["references"][0]["value"], "/a?x=&amp;")

    def run_cli(self, payload):
        return subprocess.run(
            [sys.executable, str(SCRIPT)], input=payload, text=True,
            capture_output=True, check=False,
        )

    def test_cli_accepts_multiple_documents_without_reading_their_paths(self):
        result = self.run_cli(json.dumps([
            {"path": "nonexistent/index.html", "html": '<main id="office"></main>'},
            {"path": "/also/not/a/file.html", "html": ""},
        ]))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(json.loads(result.stdout), [
            {"path": "nonexistent/index.html", "ids": ["office"], "references": [], "robots": []},
            {"path": "/also/not/a/file.html", "ids": [], "references": [], "robots": []},
        ])

    def test_cli_empty_batch_is_valid(self):
        result = self.run_cli("[]")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), [])

    def test_cli_rejects_malformed_requests_without_partial_output(self):
        invalid_payloads = [
            "not JSON", "{}", "null", "[1]",
            '[{"path":"index.html"}]',
            '[{"path":"index.html","html":null}]',
            '[{"path":false,"html":""}]',
            '[{"path":"","html":""}]',
            '[{"path":"index.html","html":"","unexpected":true}]',
            '[{"path":"index.html","html":""},{"path":"later.html"}]',
        ]
        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                result = self.run_cli(payload)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertIn("error", json.loads(result.stderr))


if __name__ == "__main__":
    unittest.main()
