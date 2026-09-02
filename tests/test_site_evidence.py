"""Network-free tests for the static website evidence builder."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_site_builder():
    """Load the site builder without requiring scripts to be a package."""

    spec = importlib.util.spec_from_file_location(
        "tradejournals_site_evidence_builder",
        REPO_ROOT / "scripts" / "build_site_evidence.py",
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load build_site_evidence.py")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


site_evidence = load_site_builder()


class SiteEvidenceBuilderTests(unittest.TestCase):
    def create_fixture(self, root: Path) -> dict[str, Path]:
        site_directory = root / "site_example"
        journal_directory = root / "journals"
        asset_directory = site_directory / "assets"
        site_directory.mkdir()
        journal_directory.mkdir()
        asset_directory.mkdir()
        (journal_directory / "flickr.md").write_text("# Flickr journal\n", encoding="utf-8")
        (journal_directory / "google.md").write_text("# Google journal\n", encoding="utf-8")
        (asset_directory / "sample.jpg").write_bytes(b"synthetic-image")

        flickr_inventory = root / "FLICKR_PUBLIC_ALBUMS.md"
        flickr_inventory.write_text(
            "# Flickr\n\n"
            "- Public albums visible via API: 1\n\n"
            '<a id="album-111"></a>\n\n'
            "### Flickr Sample\n\n"
            "- Photos: 98\n",
            encoding="utf-8",
        )
        google_inventory = root / "GOOGLE_PHOTOS_ALBUMS.md"
        google_inventory.write_text(
            "# Google\n\n"
            '<a id="album-google-sample"></a>\n\n'
            "### Google Sample\n\n"
            "- Photos: 296 at the latest review\n",
            encoding="utf-8",
        )
        html_path = site_directory / "index.html"
        html_path.write_text(
            '<article id="flickr-target">'
            '<span data-album-count="flickr:111">98</span>'
            "</article>"
            '<article id="google-target">'
            '<span data-album-count="google_photos:google-sample">296</span>'
            "</article>",
            encoding="utf-8",
        )
        source_path = site_directory / "evidence-source.json"
        source_path.write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "archive": {"connectedPractices": 5},
                    "journals": [
                        {
                            "title": "Flickr Journal",
                            "area": "01 / Sample",
                            "source": "journals/flickr.md",
                            "target": "flickr-target",
                            "summary": "A sample Flickr journal.",
                            "tags": ["flickr"],
                            "evidence": {
                                "stage": "Recorded",
                                "recorded": "2026",
                                "sourceLabel": "Flickr",
                            },
                            "albums": [
                                {
                                    "platform": "flickr",
                                    "id": "111",
                                    "label": "Flickr Sample",
                                    "shown": 1,
                                }
                            ],
                            "images": [
                                {
                                    "src": "assets/sample.jpg",
                                    "alt": "Sample evidence",
                                }
                            ],
                        },
                        {
                            "title": "Google Journal",
                            "area": "01 / Sample",
                            "source": "journals/google.md",
                            "target": "google-target",
                            "summary": "A sample Google journal.",
                            "tags": ["google"],
                            "evidence": {
                                "stage": "Review pending",
                                "recorded": "2026",
                                "sourceLabel": "Google Photos",
                            },
                            "albums": [
                                {
                                    "platform": "google_photos",
                                    "id": "google-sample",
                                    "label": "Google Sample",
                                    "shown": 0,
                                }
                            ],
                            "images": [],
                        },
                    ],
                }
            ),
            encoding="utf-8",
        )
        return {
            "source": source_path,
            "flickr": flickr_inventory,
            "google": google_inventory,
            "html": html_path,
        }

    def build_fixture_manifest(self, root: Path, paths: dict[str, Path]):
        return site_evidence.build_manifest(
            repo_root=root,
            source_path=paths["source"],
            flickr_inventory_path=paths["flickr"],
            google_inventory_path=paths["google"],
            html_path=paths["html"],
        )

    def test_build_resolves_flickr_and_google_counts(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            paths = self.create_fixture(root)

            manifest = self.build_fixture_manifest(root, paths)

        self.assertEqual(manifest["archive"]["publicFlickrAlbums"], 1)
        self.assertEqual(manifest["archive"]["connectedPractices"], 5)
        self.assertEqual(manifest["journals"][0]["albums"][0]["count"], 98)
        self.assertEqual(manifest["journals"][1]["albums"][0]["count"], 296)
        self.assertEqual(manifest["journals"][0]["url"], "#flickr-target")

    def test_build_rejects_album_missing_from_inventory(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            paths = self.create_fixture(root)
            source = json.loads(paths["source"].read_text(encoding="utf-8"))
            source["journals"][0]["albums"][0]["id"] = "missing"
            paths["source"].write_text(json.dumps(source), encoding="utf-8")

            with self.assertRaisesRegex(
                site_evidence.EvidenceBuildError,
                "absent from its inventory",
            ):
                self.build_fixture_manifest(root, paths)

    def test_build_rejects_stale_html_fallback_count(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            paths = self.create_fixture(root)
            html = paths["html"].read_text(encoding="utf-8").replace(
                ">98</span>",
                ">97</span>",
            )
            paths["html"].write_text(html, encoding="utf-8")

            with self.assertRaisesRegex(
                site_evidence.EvidenceBuildError,
                "fallback count",
            ):
                self.build_fixture_manifest(root, paths)

    def test_build_rejects_invalid_album_presentation_count(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            paths = self.create_fixture(root)
            source = json.loads(paths["source"].read_text(encoding="utf-8"))
            source["journals"][0]["albums"][0]["shown"] = -1
            paths["source"].write_text(json.dumps(source), encoding="utf-8")

            with self.assertRaisesRegex(
                site_evidence.EvidenceBuildError,
                "non-negative integer",
            ):
                self.build_fixture_manifest(root, paths)

    def test_check_mode_detects_stale_generated_manifest(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "evidence-manifest.js"
            output_path.write_text("stale\n", encoding="utf-8")

            with self.assertRaisesRegex(
                site_evidence.EvidenceBuildError,
                "is stale",
            ):
                site_evidence.write_or_check_manifest(
                    output_path=output_path,
                    rendered="current\n",
                    check=True,
                )


if __name__ == "__main__":
    unittest.main()
