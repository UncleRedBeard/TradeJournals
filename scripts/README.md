# Scripts

Utility scripts for maintaining the TradeJournals archive.

## Flickr Album Import Prototype

`import_flickr_album.py` imports a public Flickr album into a Markdown journal
entry using Flickr's public oEmbed endpoint, album page metadata, and public
photoset feed. It does not require a Flickr API key.

Example:

```sh
python3 scripts/import_flickr_album.py \
  --url "https://www.flickr.com/photos/boocher/albums/72157626216393933/" \
  --title "East Side Locos" \
  --format "35mm film" \
  --section lens \
  --update-readme
```

Useful flags:

- `--dry-run` prints the generated Markdown without writing files.
- `--force` overwrites an existing output file.
- `--merge-existing` updates a matching journal instead of creating a sidecar
  Flickr entry.
- `--output` writes to an explicit Markdown path.
- `--note` supplies the archive note paragraph.

## Flickr Albums Directory Scan

Use `--albums-url` to scan a public Flickr `/albums` page before importing
anything:

```sh
python3 scripts/import_flickr_album.py \
  --albums-url "https://www.flickr.com/photos/boocher/albums" \
  --limit 10
```

The scan report lists album titles, IDs, photo counts, view counts, and whether
an existing journal already appears to reference the album. Flickr may advertise
more total albums than it exposes in the initial public HTML; the report calls
that out when the remaining albums appear to require Flickr's lazy-load/API
path.

Batch import is opt-in and still requires a project classification:

```sh
python3 scripts/import_flickr_album.py \
  --albums-url "https://www.flickr.com/photos/boocher/albums" \
  --section machines \
  --format "machine archive" \
  --import-discovered \
  --merge-existing \
  --dry-run \
  --limit 3
```

After importing, run:

```sh
npm run lint:md
```
