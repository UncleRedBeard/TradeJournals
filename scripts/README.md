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
- `--force` overwrites an existing output file.
- `--merge-existing` updates a matching journal instead of creating a sidecar
  Flickr entry.
- `--output` writes to an explicit Markdown path.
- `--note` supplies the archive note paragraph.
- `--use-api` uses Flickr API methods for full public photo pagination.

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
to require Flickr's lazy-load/API path.

To refresh the tracked public album inventory and gap report, use:

```sh
python3 scripts/import_flickr_album.py \
  --albums-url "https://www.flickr.com/photos/boocher/albums" \
  --use-api \
  --write-inventory
```

Preview it first with `--dry-run` if needed. The inventory report preserves
album IDs already marked as `excluded`, then classifies the rest as `imported`
when a journal reference exists or `gap` when the album still needs review.

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
only updates existing album status and public photo count bullets. If a journal
references an album that is not currently visible through the public API scan,
the script reports it and leaves the journal unchanged.

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
photo-taken time when present.
