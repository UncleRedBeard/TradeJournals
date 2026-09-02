# Scripts

Utility scripts for maintaining the TradeJournals archive.

## Flickr Album Import Prototype

`import_flickr_album.py` imports a public Flickr album into a Markdown journal
entry. The default path uses Flickr's public oEmbed endpoint, album page
metadata, and public photoset feed. That path does not require a Flickr API key.

For more reliable album discovery and full public photo pagination, use
`--use-api` with the API key in the environment:

```sh
export FLICKR_API_KEY="your-api-key"
```

You can also copy `.env.example` to `.env`; the importer reads
`FLICKR_API_KEY` from that gitignored file when it is not already exported.

The Flickr API secret is not needed for the public-read workflow and should not
be committed to the repo.

Repeated Flickr photo IDs are collapsed deterministically after feed or API
pagination. The first public record keeps its original position and metadata.

Example:

```sh
python3 scripts/import_flickr_album.py \
  --url "https://www.flickr.com/photos/boocher/albums/72157626216393933/" \
  --title "East Side Locos" \
  --format "35mm film" \
  --section lens \
  --use-api \
  --update-readme
```

Useful flags:

- `--dry-run` prints the generated Markdown without writing files.
- `--force` requests regeneration of an existing output file. If the proposed
  Markdown differs, the importer fails closed and prints a reviewable preview
  instead of overwriting potentially curated metadata.
- `--merge-existing` updates a matching journal instead of creating a sidecar
  Flickr entry.
- `--output` writes to an explicit Markdown path.
- `--note` supplies the archive note paragraph.
- `--use-api` uses Flickr API methods for full public photo pagination.

### Public Metadata Preview

Use the dedicated metadata preview to review public Flickr metadata without
writing a journal, inventory, cache, sidecar, or other repository file:

```sh
python3 scripts/import_flickr_album.py \
  --url "https://www.flickr.com/photos/boocher/albums/72177720335033061/" \
  --use-api \
  --metadata-preview \
  --metadata-limit 12
```

This mode requires `FLICKR_API_KEY` to be exported in the process environment;
it does not use the repo-local `.env` fallback. It prints a time-stamped,
review-only report to standard output. Existing import and `--dry-run` behavior
is unchanged.

For persistent Bash availability, export the key from `~/.bashrc` and source
that file from `~/.bash_profile`. Automation or app-launched checks can use
`bash -lc 'python3 ...'` to run through the verified login-shell path. Confirm
inheritance without printing the key itself:

```sh
bash -lc 'python3 -c '\''import os; print("SET" if os.getenv("FLICKR_API_KEY") else "UNSET")'\'''
```

Without a metadata scope flag, the preview makes only bulk album requests.
Use a positive `--metadata-limit` to expand the first N photos in Flickr album
order, or repeat `--metadata-photo-id ID` to expand specific public photo IDs.
The two scope controls are mutually exclusive, and there is no unbounded
per-photo expansion mode.

Missing required responses, invalid or non-advancing pagination, count
disagreement, and unexpected detail-request failures produce an incomplete
preview and a nonzero exit status. Incomplete previews retain safe partial
diagnostics but do not propose candidate journal additions.

Expanded photos use public `flickr.photos.getInfo` and
`flickr.photos.getExif` calls. EXIF is labeled `Digital-file EXIF` because film
scans may describe the scan or copy workflow rather than the original camera.
Only camera make/model, lens model, exposure time, aperture, ISO, focal length,
and EXIF original date/time are allowed through. GPS, serial numbers, personal
fields, unique IDs, maker notes, binary values, and unknown EXIF tags are
excluded. Flickr date-taken and date-posted values are preserved without
timezone conversion or historical-date inference.

## Flickr Albums Directory Scan

Use `--albums-url` to scan a public Flickr `/albums` page before importing
anything:

```sh
python3 scripts/import_flickr_album.py \
  --albums-url "https://www.flickr.com/photos/boocher/albums" \
  --use-api \
  --limit 10
```

The scan report lists album titles, IDs, photo counts, view counts, and whether
an existing journal already appears to reference the album. Without
`--use-api`, Flickr may advertise more total albums than it exposes in the
initial public HTML; the report calls that out when the remaining albums appear
to require Flickr's lazy-load/API path. The seven user-approved exclusions are
omitted from scan, batch-import, and reconciliation candidates. Inventory mode
still lists them explicitly as `excluded` so the reviewed classification stays
visible.

To refresh the tracked public album inventory and gap report, use:

```sh
python3 scripts/import_flickr_album.py \
  --albums-url "https://www.flickr.com/photos/boocher/albums" \
  --use-api \
  --write-inventory
```

Preview it first with `--dry-run` if needed. The inventory report preserves
album IDs already marked as `excluded`, then classifies the rest as `imported`
when a journal reference exists or `gap` when the album still needs review. A
changed existing inventory preserves reviewed annotation lines inside each
album-detail block, keyed by the stable Flickr album anchor and their position
after an importer-owned field. Generated fields can then refresh safely. The
importer fails closed if anchors are missing or duplicated, an annotation's
field position no longer exists, or non-generated content appears outside the
album-detail blocks. Keep annotations out of the generated summary and table.

Batch import is opt-in and still requires a project classification:

```sh
python3 scripts/import_flickr_album.py \
  --albums-url "https://www.flickr.com/photos/boocher/albums" \
  --section machines \
  --format "machine archive" \
  --import-discovered \
  --merge-existing \
  --use-api \
  --dry-run \
  --limit 3
```

To reconcile journals that already reference Flickr albums against the latest
public API-visible counts, use:

```sh
python3 scripts/import_flickr_album.py \
  --albums-url "https://www.flickr.com/photos/boocher/albums" \
  --use-api \
  --reconcile-known \
  --dry-run
```

Remove `--dry-run` after reviewing the proposed line updates. Reconciliation
only replaces a mismatched numeric photo count in an existing album status or
public photo count bullet; it preserves the rest of the line verbatim. If a
journal references an album that is not currently visible through the public
API scan, the script reports it and leaves the journal unchanged.

After importing, run:

```sh
npm run lint:md
```

## Google Photos Album Import Workflow

`import_google_photos_album.py` records Google Photos shared albums and imports
image-level evidence from durable local inputs.

Google Photos shared album pages are not treated as a stable public metadata
API in this project. The preferred durable sources are:

- a small project JSON manifest
- a local Google Photos or Google Takeout export folder
- a future authenticated Google Photos importer

To record a shared album source before image-level metadata is available:

```sh
python3 scripts/import_google_photos_album.py \
  --share-url "https://photos.google.com/share/..." \
  --title "Album title" \
  --section residence
```

To generate a journal from a manifest:

```sh
python3 scripts/import_google_photos_album.py \
  --manifest google_photos_album_manifest.json \
  --section residence \
  --output 01_the_residence_1894/trade_journals/example.md
```

Manifest shape:

```json
{
  "album": {
    "title": "Album title",
    "share_url": "https://photos.google.com/share/..."
  },
  "photos": [
    {
      "title": "IMG_0001",
      "url": "https://photos.google.com/share/.../photo/...",
      "date_taken": "2026-07-09 10:15",
      "description": "Short evidence note."
    }
  ]
}
```

To list a local export folder as evidence:

```sh
python3 scripts/import_google_photos_album.py \
  --local-dir "/path/to/exported/album" \
  --title "Album title" \
  --section residence
```

The local export path also checks for simple sidecar JSON files beside images,
including `image.jpg.json` and `image.json`, and uses title, description, and
photo-taken time when present. When manifest and local-export records share an
explicit `id`, `photo_id`, or media-item ID, the first record keeps its stable
position and metadata while the generated evidence line records both source
provenance labels. Changed existing Google Photos journals are likewise
previewed and rejected rather than overwritten, even with `--force`.
