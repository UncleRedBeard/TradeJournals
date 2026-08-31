"""Network-free regression tests for the Flickr and Google Photos importers."""

from __future__ import annotations

import importlib.util
import io
import sys
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock
from urllib.error import URLError
from urllib.parse import parse_qs, urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_script(module_name: str, filename: str):
    """Load a repository script without requiring scripts to be a package."""

    spec = importlib.util.spec_from_file_location(
        module_name,
        REPO_ROOT / "scripts" / filename,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {filename}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


flickr = load_script("tradejournals_flickr_importer", "import_flickr_album.py")
google = load_script(
    "tradejournals_google_photos_importer",
    "import_google_photos_album.py",
)


class FlickrCredentialSafetyTests(unittest.TestCase):
    def test_transport_failure_redacts_api_key_from_exception_and_cause(self):
        api_key = "synthetic-key-never-log"
        url = f"{flickr.FLICKR_API_ENDPOINT}?method=test&api_key={api_key}"

        with mock.patch.object(
            flickr,
            "urlopen",
            side_effect=URLError(f"transport rejected {url}"),
        ):
            with self.assertRaises(RuntimeError) as raised:
                flickr.fetch_text(url)

        rendered_exception = repr(raised.exception)
        if raised.exception.__cause__ is not None:
            rendered_exception += repr(raised.exception.__cause__)

        self.assertNotIn(api_key, rendered_exception)
        self.assertIn("api_key=REDACTED", str(raised.exception))

    def test_public_api_url_uses_key_without_authentication_parameters(self):
        with mock.patch.object(
            flickr,
            "require_flickr_api_key",
            return_value="synthetic-public-key",
        ):
            url = flickr.build_flickr_api_url(
                "flickr.photosets.getList",
                {"user_id": "12345@N00"},
            )

        query = parse_qs(urlparse(url).query)
        self.assertEqual(query["api_key"], ["synthetic-public-key"])
        self.assertNotIn("auth_token", query)
        self.assertNotIn("api_sig", query)
        self.assertNotIn("oauth_token", query)
        self.assertNotIn("api_secret", query)

    def test_api_failure_message_cannot_echo_key(self):
        api_key = "synthetic-key-never-log"

        with (
            mock.patch.object(
                flickr,
                "require_flickr_api_key",
                return_value=api_key,
            ),
            mock.patch.object(
                flickr,
                "fetch_json",
                return_value={
                    "stat": "fail",
                    "code": 99,
                    "message": f"upstream echoed {api_key}",
                },
            ),
            self.assertRaises(RuntimeError) as raised,
        ):
            flickr.fetch_flickr_api("flickr.test.echo", {})

        self.assertNotIn(api_key, repr(raised.exception))
        self.assertIn("REDACTED", str(raised.exception))

    def test_main_redacts_credential_bearing_exception_from_console(self):
        api_key = "synthetic-key-never-log"
        args = DryRunAndCuratedMetadataTests.flickr_args(
            Path("unused.md"),
            dry_run=True,
            force=False,
        )
        stderr = io.StringIO()

        with (
            mock.patch.object(flickr, "parse_args", return_value=args),
            mock.patch.object(
                flickr,
                "fetch_album_for_args",
                side_effect=RuntimeError(
                    f"transport failed at {flickr.FLICKR_API_ENDPOINT}"
                    f"?api_key={api_key}"
                ),
            ),
            redirect_stderr(stderr),
        ):
            result = flickr.main()

        self.assertEqual(result, 1)
        self.assertNotIn(api_key, stderr.getvalue())
        self.assertIn("api_key=REDACTED", stderr.getvalue())


class FlickrDuplicateAndExclusionTests(unittest.TestCase):
    def test_api_pagination_keeps_first_photo_for_duplicate_id(self):
        responses = [
            {
                "photoset": {
                    "page": "1",
                    "pages": "2",
                    "total": "3",
                    "photo": [
                        {
                            "id": "100",
                            "title": {"_content": "first title"},
                            "datetaken": "2026-01-01 10:00:00",
                        },
                        {
                            "id": "200",
                            "title": {"_content": "second"},
                            "datetaken": "2026-01-01 11:00:00",
                        },
                    ],
                }
            },
            {
                "photoset": {
                    "page": "2",
                    "pages": "2",
                    "total": "3",
                    "photo": [
                        {
                            "id": "100",
                            "title": {"_content": "duplicate title"},
                            "datetaken": "2026-01-02 10:00:00",
                        }
                    ],
                }
            },
        ]

        with mock.patch.object(
            flickr,
            "fetch_flickr_api",
            side_effect=responses,
        ):
            photos, total = flickr.fetch_api_photos(
                "12345@N00",
                "72177700000000000",
            )

        self.assertEqual([photo.photo_id for photo in photos], ["100", "200"])
        self.assertEqual(photos[0].title, "first title")
        self.assertEqual(total, 3)

    def test_api_discovery_omits_exclusions_by_default(self):
        excluded_id = next(iter(flickr.DEFAULT_EXCLUDED_ALBUM_IDS))
        response = {
            "photosets": {
                "page": "1",
                "pages": "1",
                "total": "2",
                "photoset": [
                    {
                        "id": excluded_id,
                        "title": {"_content": "Excluded personal album"},
                        "photos": "1",
                    },
                    {
                        "id": "999",
                        "title": {"_content": "Eligible archive"},
                        "photos": "2",
                    },
                ],
            }
        }

        with (
            mock.patch.object(
                flickr,
                "lookup_user_nsid_from_albums_url",
                return_value="12345@N00",
            ),
            mock.patch.object(flickr, "fetch_flickr_api", return_value=response),
        ):
            discovery = flickr.discover_api_albums(
                "https://www.flickr.com/photos/example/albums/"
            )

        self.assertEqual(
            [album.album_id for album in discovery.albums],
            ["999"],
        )

    def test_discovery_report_omits_user_approved_exclusions(self):
        excluded_id = next(iter(flickr.DEFAULT_EXCLUDED_ALBUM_IDS))
        discovery = flickr.AlbumDiscovery(
            albums=[
                flickr.PublicAlbum(
                    title="Excluded personal album",
                    url=f"https://www.flickr.com/photos/example/albums/{excluded_id}/",
                    album_id=excluded_id,
                ),
                flickr.PublicAlbum(
                    title="Eligible archive",
                    url="https://www.flickr.com/photos/example/albums/999/",
                    album_id="999",
                ),
            ],
            source="synthetic public scan",
        )

        with mock.patch.object(flickr, "find_existing_journal", return_value=None):
            report = flickr.render_discovery_report(discovery, limit=None)

        self.assertNotIn("Excluded personal album", report)
        self.assertIn("Eligible archive", report)
        self.assertIn("1 approved exclusion", report)

    def test_batch_limit_is_applied_after_exclusions(self):
        excluded_id = next(iter(flickr.DEFAULT_EXCLUDED_ALBUM_IDS))
        excluded = flickr.PublicAlbum(
            title="Excluded personal album",
            url=f"https://www.flickr.com/photos/example/albums/{excluded_id}/",
            album_id=excluded_id,
        )
        eligible = flickr.PublicAlbum(
            title="Eligible archive",
            url="https://www.flickr.com/photos/example/albums/999/",
            album_id="999",
        )
        discovery = flickr.AlbumDiscovery(
            albums=[excluded, eligible],
            source="synthetic public scan",
        )
        fetched_album = flickr.Album(
            title="Eligible archive",
            url=eligible.url,
            short_url="",
            owner="Example",
            owner_nsid="12345@N00",
            thumbnail_alt="",
            feed_title="",
            feed_modified="",
            photo_count=0,
            starter_photo_count=0,
            photo_listing_source="public photoset feed",
            photos=[],
        )
        args = Namespace(
            title=None,
            output=None,
            slug=None,
            reconcile_known=False,
            import_discovered=True,
            write_inventory=False,
            use_api=False,
            albums_url="https://www.flickr.com/photos/example/albums/",
            format_label="archive",
            limit=1,
            merge_existing=False,
            force=False,
            dry_run=True,
            note=None,
            section="lens",
            update_readme=False,
            inventory_output=Path("unused.md"),
        )

        with (
            mock.patch.object(flickr, "discover_public_albums", return_value=discovery),
            mock.patch.object(flickr, "find_existing_journal", return_value=None),
            mock.patch.object(
                flickr,
                "fetch_album_for_args",
                return_value=fetched_album,
            ) as fetch_album,
            redirect_stdout(io.StringIO()),
        ):
            result = flickr.handle_albums_directory(args)

        self.assertEqual(result, 0)
        fetch_album.assert_called_once_with(args, eligible.url, eligible.title)


class GooglePhotosDuplicateTests(unittest.TestCase):
    def test_combined_sources_keep_first_record_and_all_provenance(self):
        manifest_photo = google.PhotoEvidence(
            title="Manifest title",
            source="https://photos.example/item-1",
            date_taken="2026-01-01 10:00",
            description="Curated manifest description",
            record_id="item-1",
            provenance=("manifest",),
        )
        local_duplicate = google.PhotoEvidence(
            title="Local filename.jpg",
            source="Local filename.jpg",
            record_id="item-1",
            provenance=("local export",),
        )

        combined = google.deduplicate_photo_evidence(
            [manifest_photo, local_duplicate]
        )

        self.assertEqual(len(combined), 1)
        self.assertEqual(combined[0].title, "Manifest title")
        self.assertEqual(combined[0].source, "https://photos.example/item-1")
        self.assertEqual(combined[0].provenance, ("manifest", "local export"))

        markdown = google.markdown_for_album(
            title="Synthetic album",
            share_url=None,
            section="lens",
            format_note="archive",
            note=None,
            photos=combined,
            source_mode="manifest, local export",
        )
        self.assertIn("Provenance: manifest, local export.", markdown)

    def test_manifest_and_local_export_use_explicit_record_id_for_deduplication(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            manifest = root / "manifest.json"
            manifest.write_text(
                """
                {
                  "album": {"title": "Synthetic album"},
                  "photos": [
                    {
                      "id": "item-1",
                      "title": "Manifest title",
                      "url": "https://photos.example/item-1"
                    }
                  ]
                }
                """,
                encoding="utf-8",
            )
            image = root / "Local filename.jpg"
            image.write_bytes(b"synthetic image bytes")
            image.with_suffix(".jpg.json").write_text(
                '{"id": "item-1", "title": "Local title"}',
                encoding="utf-8",
            )

            _, manifest_photos = google.photos_from_manifest(manifest)
            local_photos = google.photos_from_local_dir(root)
            combined = google.deduplicate_photo_evidence(
                [*manifest_photos, *local_photos]
            )

        self.assertEqual(len(combined), 1)
        self.assertEqual(combined[0].title, "Manifest title")
        self.assertEqual(combined[0].record_id, "item-1")
        self.assertEqual(combined[0].provenance, ("manifest", "local export"))


class DryRunAndCuratedMetadataTests(unittest.TestCase):
    @staticmethod
    def flickr_args(output: Path, *, dry_run: bool, force: bool) -> Namespace:
        return Namespace(
            url="https://www.flickr.com/photos/example/albums/999/",
            albums_url=None,
            title=None,
            format_label="archive",
            section="lens",
            slug=None,
            output=output,
            update_readme=True,
            force=force,
            merge_existing=False,
            dry_run=dry_run,
            import_discovered=False,
            reconcile_known=False,
            write_inventory=False,
            inventory_output=output.parent / "inventory.md",
            use_api=False,
            limit=None,
            note=None,
        )

    @staticmethod
    def synthetic_flickr_album() -> object:
        return flickr.Album(
            title="Synthetic archive",
            url="https://www.flickr.com/photos/example/albums/999/",
            short_url="",
            owner="Example",
            owner_nsid="12345@N00",
            thumbnail_alt="",
            feed_title="",
            feed_modified="",
            photo_count=0,
            starter_photo_count=0,
            photo_listing_source="public photoset feed",
            photos=[],
        )

    def test_flickr_dry_run_does_not_change_output_or_neighboring_files(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            output = root / "nested" / "journal.md"
            sentinel = root / "sentinel.txt"
            sentinel.write_text("unchanged", encoding="utf-8")
            before = {
                path.relative_to(root): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file()
            }
            args = self.flickr_args(output, dry_run=True, force=False)

            with (
                mock.patch.object(flickr, "parse_args", return_value=args),
                mock.patch.object(
                    flickr,
                    "fetch_album_for_args",
                    return_value=self.synthetic_flickr_album(),
                ),
                mock.patch.object(flickr, "find_existing_journal", return_value=None),
                redirect_stdout(io.StringIO()),
            ):
                result = flickr.main()

            after = {
                path.relative_to(root): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file()
            }

        self.assertEqual(result, 0)
        self.assertEqual(after, before)
        self.assertFalse(output.parent.exists())

    def test_google_dry_run_does_not_change_output_or_neighboring_files(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            output = root / "nested" / "journal.md"
            sentinel = root / "sentinel.txt"
            sentinel.write_text("unchanged", encoding="utf-8")
            manifest = root / "manifest.json"
            manifest.write_text(
                '{"photos": [{"id": "one", "title": "One"}]}',
                encoding="utf-8",
            )
            local_export = root / "local-export"
            local_export.mkdir()
            (local_export / "photo.jpg").write_bytes(b"synthetic image bytes")
            before = {
                path.relative_to(root): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file()
            }
            args = Namespace(
                share_url="https://photos.example/share/synthetic",
                title="Synthetic album",
                section="lens",
                format="archive",
                manifest=manifest,
                local_dir=local_export,
                output=output,
                note=None,
                dry_run=True,
                force=False,
            )

            with (
                mock.patch.object(google, "parse_args", return_value=args),
                redirect_stdout(io.StringIO()),
            ):
                result = google.main()

            after = {
                path.relative_to(root): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file()
            }

        self.assertEqual(result, 0)
        self.assertEqual(after, before)
        self.assertFalse(output.parent.exists())

    def test_flickr_force_refuses_curated_output_and_prints_preview(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "curated.md"
            curated = "# Hand-curated journal\n\nMaterial judgment stays here.\n"
            output.write_text(curated, encoding="utf-8")
            args = self.flickr_args(output, dry_run=False, force=True)
            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                mock.patch.object(flickr, "parse_args", return_value=args),
                mock.patch.object(
                    flickr,
                    "fetch_album_for_args",
                    return_value=self.synthetic_flickr_album(),
                ),
                mock.patch.object(flickr, "find_existing_journal", return_value=None),
                redirect_stdout(stdout),
                redirect_stderr(stderr),
            ):
                result = flickr.main()

            preserved = output.read_text(encoding="utf-8")

        self.assertEqual(result, 1)
        self.assertEqual(preserved, curated)
        self.assertIn("Refusing to overwrite curated Markdown", stderr.getvalue())
        self.assertIn("# Flickr: Synthetic archive", stdout.getvalue())

    def test_google_force_refuses_curated_output_and_prints_preview(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "curated.md"
            curated = "# Hand-curated journal\n\nMaterial judgment stays here.\n"
            output.write_text(curated, encoding="utf-8")
            args = Namespace(
                share_url="https://photos.example/share/synthetic",
                title="Synthetic album",
                section="lens",
                format="archive",
                manifest=None,
                local_dir=None,
                output=output,
                note=None,
                dry_run=False,
                force=True,
            )
            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                mock.patch.object(google, "parse_args", return_value=args),
                redirect_stdout(stdout),
                redirect_stderr(stderr),
            ):
                result = google.main()

            preserved = output.read_text(encoding="utf-8")

        self.assertEqual(result, 1)
        self.assertEqual(preserved, curated)
        self.assertIn("Refusing to overwrite curated Markdown", stderr.getvalue())
        self.assertIn("# Google Photos: Synthetic album", stdout.getvalue())

    def test_inventory_regeneration_refuses_changed_existing_content(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "inventory.md"
            curated = "# Curated inventory\n\nKeep the reviewed classifications.\n"
            output.write_text(curated, encoding="utf-8")
            discovery = flickr.AlbumDiscovery(
                albums=[],
                advertised_total=0,
                source="synthetic public scan",
            )
            args = Namespace(dry_run=False, inventory_output=output)

            with self.assertRaises(flickr.CuratedContentError) as raised:
                flickr.handle_write_inventory(args, discovery)

            preserved = output.read_text(encoding="utf-8")

        self.assertEqual(preserved, curated)
        self.assertIn("# Flickr Public Album Inventory", raised.exception.preview)

    def test_inventory_render_preserves_annotation_during_generated_refresh(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "inventory.md"
            old_discovery = flickr.AlbumDiscovery(
                albums=[
                    flickr.PublicAlbum(
                        title="Synthetic archive",
                        url="https://www.flickr.com/photos/example/albums/999/",
                        album_id="999",
                        photo_count=1,
                    )
                ],
                advertised_total=1,
                source="synthetic public scan",
            )
            new_discovery = flickr.AlbumDiscovery(
                albums=[
                    flickr.PublicAlbum(
                        title="Synthetic archive",
                        url="https://www.flickr.com/photos/example/albums/999/",
                        album_id="999",
                        photo_count=2,
                    )
                ],
                advertised_total=1,
                source="synthetic public scan",
            )

            with (
                mock.patch.object(flickr, "find_existing_journal", return_value=None),
                mock.patch.object(flickr, "datetime") as mocked_datetime,
            ):
                mocked_datetime.now.return_value.strftime.return_value = "2026-08-04"
                original = flickr.render_inventory_report(old_discovery, output)
                curated = original.replace(
                    "- Photos: 1\n",
                    "- Photos: 1\n- Curator review: retain this judgment.\n",
                    1,
                )
                output.write_text(curated, encoding="utf-8")
                mocked_datetime.now.return_value.strftime.return_value = "2026-08-30"

                refreshed = flickr.render_inventory_report(new_discovery, output)

        self.assertIn("Last checked: 2026-08-30", refreshed)
        self.assertIn(
            "- Photos: 2\n- Curator review: retain this judgment.\n"
            "- TradeJournals status: gap",
            refreshed,
        )

    def test_inventory_write_refreshes_generated_fields_after_safe_merge(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "inventory.md"
            old_album = flickr.PublicAlbum(
                title="Synthetic archive",
                url="https://www.flickr.com/photos/example/albums/999/",
                album_id="999",
                photo_count=1,
            )
            new_album = flickr.PublicAlbum(
                title="Synthetic archive",
                url=old_album.url,
                album_id=old_album.album_id,
                photo_count=2,
            )
            args = Namespace(dry_run=False, inventory_output=output)

            with (
                mock.patch.object(flickr, "find_existing_journal", return_value=None),
                mock.patch.object(flickr, "datetime") as mocked_datetime,
            ):
                mocked_datetime.now.return_value.strftime.return_value = "2026-08-04"
                original = flickr.render_inventory_report(
                    flickr.AlbumDiscovery(albums=[old_album]),
                    output,
                )
                curated = original.replace(
                    "- Photos: 1\n",
                    "- Photos: 1\n- Reviewed note: preserve me.\n",
                    1,
                )
                output.write_text(curated, encoding="utf-8")
                mocked_datetime.now.return_value.strftime.return_value = "2026-08-30"

                with redirect_stdout(io.StringIO()):
                    result = flickr.handle_write_inventory(
                        args,
                        flickr.AlbumDiscovery(albums=[new_album]),
                    )

            refreshed = output.read_text(encoding="utf-8")

        self.assertEqual(result, 0)
        self.assertIn("Last checked: 2026-08-30", refreshed)
        self.assertIn("- Photos: 2", refreshed)
        self.assertIn("- Reviewed note: preserve me.", refreshed)

    def test_inventory_render_refuses_duplicate_album_anchor(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "inventory.md"
            album = flickr.PublicAlbum(
                title="Synthetic archive",
                url="https://www.flickr.com/photos/example/albums/999/",
                album_id="999",
                photo_count=1,
            )
            discovery = flickr.AlbumDiscovery(albums=[album])

            with mock.patch.object(
                flickr,
                "find_existing_journal",
                return_value=None,
            ):
                original = flickr.render_inventory_report(discovery, output)
                duplicate = original + original[original.index('<a id="album-999">') :]
                output.write_text(duplicate, encoding="utf-8")

                with self.assertRaisesRegex(
                    flickr.CuratedContentError,
                    "duplicate album anchor",
                ):
                    flickr.render_inventory_report(discovery, output)

    def test_inventory_render_refuses_annotation_outside_album_details(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "inventory.md"
            album = flickr.PublicAlbum(
                title="Synthetic archive",
                url="https://www.flickr.com/photos/example/albums/999/",
                album_id="999",
                photo_count=1,
            )
            discovery = flickr.AlbumDiscovery(albums=[album])

            with mock.patch.object(
                flickr,
                "find_existing_journal",
                return_value=None,
            ):
                original = flickr.render_inventory_report(discovery, output)
                curated = original.replace(
                    "## Summary\n",
                    "## Summary\n\nReviewed preamble note that cannot be mapped safely.\n",
                    1,
                )
                output.write_text(curated, encoding="utf-8")

                with self.assertRaisesRegex(
                    flickr.CuratedContentError,
                    "outside album detail blocks",
                ):
                    flickr.render_inventory_report(discovery, output)

    def test_reconcile_dry_run_leaves_journal_bytes_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            journal = Path(temporary_directory) / "journal.md"
            album_id = "999"
            original = (
                "# Journal\n\n"
                f"- Album URL: https://www.flickr.com/photos/example/albums/{album_id}/\n"
                "- Public photo count: 1.\n"
            )
            journal.write_text(original, encoding="utf-8")
            discovery = flickr.AlbumDiscovery(
                albums=[
                    flickr.PublicAlbum(
                        title="Synthetic archive",
                        url=f"https://www.flickr.com/photos/example/albums/{album_id}/",
                        album_id=album_id,
                        photo_count=2,
                    )
                ],
                source="synthetic public scan",
            )
            args = Namespace(dry_run=True)

            with (
                mock.patch.object(
                    flickr,
                    "find_known_journal_references",
                    return_value=[flickr.JournalReference(album_id, journal)],
                ),
                redirect_stdout(io.StringIO()),
            ):
                result = flickr.handle_reconcile_known(args, discovery)

            preserved = journal.read_bytes()

        self.assertEqual(result, 0)
        self.assertEqual(preserved, original.encode("utf-8"))

    def test_reconcile_stops_flickr_context_at_next_markdown_heading(self):
        album_id = "999"
        journal = Path("journal.md")
        original = (
            "# Journal\n\n"
            "### Primary Flickr Album\n\n"
            f"- Album URL: https://www.flickr.com/photos/example/albums/{album_id}/\n"
            "- Album status: public and visible through the Flickr API\n"
            "- Public photo count: 1\n\n"
            "### Secondary Google Photos Album\n\n"
            "- Album URL: https://photos.example/album\n"
            "- Album status: shared Google Photos album\n"
        )
        public_albums = {
            album_id: flickr.PublicAlbum(
                title="Synthetic archive",
                url=f"https://www.flickr.com/photos/example/albums/{album_id}/",
                album_id=album_id,
                photo_count=2,
            )
        }

        updated, changes = flickr.reconcile_journal_markdown(
            original,
            public_albums,
            journal,
        )

        self.assertEqual(len(changes), 1)
        self.assertIn(
            "- Album status: public and visible through the Flickr API",
            updated,
        )
        self.assertIn(
            "- Public photo count: 2",
            updated,
        )
        self.assertIn("- Album status: shared Google Photos album", updated)

    def test_reconcile_changes_only_mismatched_count_in_album_status_line(self):
        album_id = "999"
        journal = Path("journal.md")
        original = (
            "# Journal\n\n"
            "### Flickr Album\n\n"
            f"- Album URL: https://www.flickr.com/photos/example/albums/{album_id}/\n"
            "- Album status: public API-visible album; latest API review "
            "confirms 514 photos.\n"
        )
        public_albums = {
            album_id: flickr.PublicAlbum(
                title="Synthetic archive",
                url=f"https://www.flickr.com/photos/example/albums/{album_id}/",
                album_id=album_id,
                photo_count=512,
            )
        }

        updated, changes = flickr.reconcile_journal_markdown(
            original,
            public_albums,
            journal,
        )

        expected = original.replace("514 photos", "512 photos")
        self.assertEqual(updated, expected)
        self.assertEqual(
            changes,
            [
                flickr.ReconcileChange(
                    journal_path=journal,
                    line_number=6,
                    before=(
                        "- Album status: public API-visible album; latest API "
                        "review confirms 514 photos."
                    ),
                    after=(
                        "- Album status: public API-visible album; latest API "
                        "review confirms 512 photos."
                    ),
                )
            ],
        )

    def test_reconcile_preserves_public_count_verification_wording_and_date(self):
        album_id = "999"
        journal = Path("journal.md")
        original = (
            "# Journal\n\n"
            "### Primary Flickr Album\n\n"
            f"- Album URL: https://www.flickr.com/photos/example/albums/{album_id}/\n"
            "- Album status: public and visible through the Flickr API\n"
            "- Public photo count: 97, confirmed through the Flickr API on "
            "2026-08-04\n"
        )
        public_albums = {
            album_id: flickr.PublicAlbum(
                title="Synthetic archive",
                url=f"https://www.flickr.com/photos/example/albums/{album_id}/",
                album_id=album_id,
                photo_count=98,
            )
        }

        updated, changes = flickr.reconcile_journal_markdown(
            original,
            public_albums,
            journal,
        )

        expected = original.replace(
            "Public photo count: 97",
            "Public photo count: 98",
        )
        self.assertEqual(updated, expected)
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].before, original.splitlines()[6])
        self.assertEqual(changes[0].after, expected.splitlines()[6])

    def test_reconcile_leaves_correct_counts_and_curated_status_untouched(self):
        album_id = "999"
        journal = Path("journal.md")
        original = (
            "# Journal\n\n"
            "### Primary Flickr Album\n\n"
            f"- Album URL: https://www.flickr.com/photos/example/albums/{album_id}/\n"
            "- Album status: public and visible through the Flickr API\n"
            "- Public photo count: 98, confirmed through the Flickr API on "
            "2026-08-04\n"
        )
        public_albums = {
            album_id: flickr.PublicAlbum(
                title="Synthetic archive",
                url=f"https://www.flickr.com/photos/example/albums/{album_id}/",
                album_id=album_id,
                photo_count=98,
            )
        }

        updated, changes = flickr.reconcile_journal_markdown(
            original,
            public_albums,
            journal,
        )

        self.assertEqual(updated, original)
        self.assertEqual(changes, [])

    def test_flickr_merge_refuses_to_replace_curated_album_section(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            journal = Path(temporary_directory) / "curated.md"
            curated = (
                "# Hand-curated journal\n\n"
                "## Visual Evidence\n\n"
                "### Flickr Album\n\n"
                "- Curator note: preserve this exact interpretation.\n"
            )
            journal.write_text(curated, encoding="utf-8")

            with self.assertRaises(flickr.CuratedContentError) as raised:
                flickr.merge_album_into_journal(
                    journal,
                    self.synthetic_flickr_album(),
                    "archive",
                )

            preserved = journal.read_text(encoding="utf-8")

        self.assertEqual(preserved, curated)
        self.assertIn("# Hand-curated journal", raised.exception.preview)
        self.assertIn("Synthetic archive", raised.exception.preview)


if __name__ == "__main__":
    unittest.main()
