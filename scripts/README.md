# Scripts

Utility scripts for maintaining the TradeJournals archive.

## Flickr Album Import Prototype

`import_flickr_album.py` imports a public Flickr album into a Markdown journal entry using Flickr's public oEmbed endpoint, album page metadata, and public photoset feed. It does not require a Flickr API key.

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
- `--output` writes to an explicit Markdown path.
- `--note` supplies the archive note paragraph.

After importing, run:

```sh
npm run lint:md
```
