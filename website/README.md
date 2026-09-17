# Toil & Timber Restoration Website Pilot

This Astro project produces a static local review site for selected
TradeJournals records. It is intentionally small: structured content selects
the work, Astro renders the pages, and ordinary static files are the output.
It does not require a Dashboard, database, CMS, or application server.

## What Lives Where

- `content/` holds the editable public candidate records and the selected story.
  These records are the source for the pilot pages; journals and inventories
  remain the source for project facts and evidence.
- `lib/` validates records, checks selected sources, compares review snapshots,
  and prepares the allowlisted public model.
- `src/` owns pages, presentation components, browser search controls, and
  pilot visual styles.
- `scripts/build.mjs` prepares selected assets, renders Astro, then validates
  every public file and reference. `scripts/check-output.mjs` is the independent
  static-output checker.

The older `site_example/` prototype remains separate during this migration.
See its [working guide](../site_example/README.md) for updates to that existing
presentation.

## Runtime And Commands

This Mac's general Node installation is not the website runtime. Use the scoped
Node 24.21.0 runtime supplied by `website/.runtime`. Run commands from the
repository root. On a fresh checkout, install the scoped runtime and locked
website dependencies first (Python 3 must also be available):

```sh
npm install --prefix website/.runtime --no-save --package-lock=false node@24.21.0
export PATH="$PWD/website/.runtime/node_modules/node/bin:$PATH"
npm --prefix website ci
```

For routine verification:

```sh
export PATH="$PWD/website/.runtime/node_modules/node/bin:$PATH"
node --version
npm --prefix website test
npm --prefix website run build:preview
npm --prefix website run check:output
```

The root convenience commands are:

```sh
npm run test:website
npm run build:website:preview
npm run check:website
```

`build:preview` writes `website/.preview-dist/`. Serve that directory with a
loopback-only static server for review:

```sh
python3 -m http.server 8126 --bind 127.0.0.1 --directory website/.preview-dist
```

Before reusing a port, identify its current process and directory. Do not stop
another task's server. Static hosting later means uploading the reviewed `dist/`
contents to the host's document root; it does not mean running Node on the host.

## Routine Updates

| Change | Edit | Verify |
| --- | --- | --- |
| Project summary or gallery selection | `content/projects/<id>.json`; selected media records | Preview the project, homepage card, and archive search |
| Homepage project order | `content/home.json` → `featuredProjectIds` | First featured project receives the hero link; cards follow the saved order |
| Shared card appearance | `src/components/ProjectCard.astro` | Rebuild and inspect the affected cards; content stays separate |
| Longer story | `content/stories/<id>.md` | Preview its TradeJournal route and review the source evidence |

Run `npm run check:website` after updates. The output gate deliberately accepts
only the pilot's planned files. New asset types or routes require an explicit
checker update. Styles are explicitly inlined in HTML, including as they grow.
The checker accepts safe HTTPS story citations and verifies required evidence
source-link identities without live Flickr requests;
recorded album counts remain local evidence, not fresh platform counts.

`npm run test:website` includes temporary synthetic builds that change copy,
featured order, and shared styling, then produce an invented reviewed release.
No real journal or review snapshot is changed by those scenarios.

## Review And Release

The pilot review currently has `state: "candidate"`. Studio is the first featured
project; the Office project and its ten photographs remain separate prior work. Preview output
therefore shows a review notice and includes `noindex, nofollow`. The release
command deliberately refuses candidate or stale content:

```sh
npm --prefix website run build
```

To prepare a real release, first review the exact public copy, image selections,
captions, and evidence limitations in
[the active Studio review](docs/pilot-editorial-review.md). A later explicit approval
is required to save a reviewed snapshot. The build never promotes a candidate
record automatically.

## Pilot Acceptance Checklist

- [x] Structured records select Studio and Office; the ten local photographs belong
  to Office. Studio now has a separate three-photo review candidate.
- [x] Build-time validation rejects unknown IDs, unsafe paths, and stale sources.
- [x] Generated output is checked for planned pages, media, links, fragments,
  source links, private paths, and preview metadata.
- [x] Core reading is server-rendered; archive search enhances the existing list.
- [x] Candidate preview and reviewed-release behavior have focused automated tests,
  including an actual synthetic Astro release build.
- [x] Desktop and 390-pixel layouts, keyboard skip/focus, and archive search were
  checked in the browser. Pages remained readable with page scripts blocked;
  a simulated search-data failure preserved the project list.

Full command results and browser limits are recorded in the
[Task 04 report](../docs/website-workflow/reports/task-04-pilot-verification.md).

Remaining review:

- [ ] Shawn reviews the candidate wording, captions, photo roles, and final visual
  treatment.
- [ ] A contact destination, domain, hosting choice, and publication procedure are
  decided in separately approved work.

No build command publishes the website, sends a message, or changes journal
records. Inspect the generated preview and exact Git diff before any later closeout.

## Browser Editing

[TradeJournals Workbench](docs/workbench.md) supports the Studio photo selection,
lead image, gallery order, captions, alternative text, candidate save, and local
preview. Structured-file editing remains available through the same records.
