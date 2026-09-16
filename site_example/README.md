# Portfolio Publishing And Website Guide

This static prototype presents selected craft journals and their evidence.
Start with the [module map](../MODULE_MAP.md) for archive ownership and shared
dependencies. Journal facts and project status remain in their source journals;
this directory owns their curated portfolio presentation.

The separate [Time & Timber Restoration Astro pilot](../website/README.md)
uses selected structured records for a new public-facing review path. It does
not replace this prototype or alter this directory's ownership and commands.

## Portfolio Publishing

Work on one journal's portfolio selection at a time. The inputs and output are:

| File Or Record | Role |
| --- | --- |
| Source journal and relevant source scans | Supported craft record used during editorial review |
| [Flickr inventory](../FLICKR_PUBLIC_ALBUMS.md) and [Google Photos inventory](../GOOGLE_PHOTOS_ALBUMS.md) | Recorded album identities and counts |
| [Evidence source](evidence-source.json) | Selected journal path, page target, summary, tags, evidence labels, albums, and representative search images |
| [Page](index.html) and referenced image assets | Page narrative, gallery source links, target anchors, and human-readable fallback counts |
| [Evidence builder](../scripts/build_site_evidence.py) | Offline validation and manifest generation |
| [Evidence manifest](evidence-manifest.js) | Generated browser data; rebuild rather than hand-edit |

To publish a reviewed update:

1. Read the journal and confirm what its evidence supports. Find the matching
   `source` entry in the catalog, or explicitly select the journal for a new
   entry. Ordinary journal edits do not require adding them to the portfolio.
2. Curate the summary, tags, stage, recorded date or period, source label, and
   representative images in `evidence-source.json`. Keep the journal path exact
   and use the existing inventory's platform and album IDs. The builder checks
   paths but does not extract prose or update claims from the journal.
3. Review the corresponding section in `index.html`. Its `id` must match the
   catalog's `target`; its gallery, source links, and narrative must support the
   selected presentation. Album fallback counts must match the inventory. Keep
   `shown` counts consistent with the page's galleries; search-result image
   selections can be smaller than those galleries.
4. Confirm that each selected image exists at its referenced path. Keep local
   assets, original-source links, and descriptions aligned. Preserve separate
   platform provenance when the same photograph appears in multiple archives.
5. Build from the reviewed inputs, then check the generated output:

   ```sh
   npm run build:site-evidence
   npm run check:site-evidence
   npm run test:site
   ```

6. Inspect the affected page section and a relevant search result in the
   browser. Follow source links and compare the displayed stage, dates, counts,
   and images with the reviewed records. Inspect the exact diff before closeout.

Run commands from the repository root. The builder reads tracked data offline;
it does not refresh albums or confirm external availability. If album metadata
needs a new review, use the separately scoped
[media workflow](../scripts/README.md#working-guide) first. A stale-manifest or
fallback-count error requires reconciling the owning inputs, then rebuilding.

## Website And Search

The presentation has three focused code areas:

- [index.html](index.html) and [styles.css](styles.css) own page structure and
  visual presentation.
- [script.js](script.js) renders evidence labels, counts, and search-result
  cards from the manifest and connects the page controls.
- [journal-search.js](journal-search.js) owns deterministic keyword ranking.
  [Search tests](../tests/site_search.test.js) exercise representative queries.

For a presentation change, preserve source links and the catalog's target
anchors. Check the affected page at relevant screen sizes. For a search change,
check ranking behavior with a focused query and the existing search tests. The
search uses the selected catalog entries; it does not search all journal prose
or provide a conversational AI service.

Use `npm run test:site` and `npm run check:site-evidence` for these changes,
alongside the applicable [archive checks](../MODULE_MAP.md#existing-validation).
Tests do not replace browser review of layout and displayed evidence.

To serve the prototype locally, run this from the repository root and open the
linked page:

```sh
python3 -m http.server 8123 --bind 127.0.0.1
```

[Open the local portfolio](http://127.0.0.1:8123/site_example/index.html).
Stop the server with `Ctrl+C` when finished. Hosting and deployment are separate
work; the repository currently defines no deployment workflow.
