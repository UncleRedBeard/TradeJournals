# Toil & Timber Restoration Website

This Astro project builds ordinary static HTML, CSS, JavaScript, and images.
Node and Python are build tools only. Serving the finished site does not require
Astro, Workbench, a database, or an application server.

The current site keeps three rooms distinct:

- Dedicated Office — current room, five selected photographs.
- Barre Studio — Current Room — current home of The Repair Shop, five selected
  photographs.
- Living Room Restoration — Future Barre Studio — future home of The Repair
  Shop, three selected photographs.

Keep the current and future rooms distinct until Shawn explicitly confirms the
move.

## What Lives Where

- `content/` holds the editable public candidate records and selected stories.
  These records are the source for the site pages; journals and inventories
  remain the source for project facts and evidence.
- `lib/` validates records, checks selected sources, compares review snapshots,
  and prepares the allowlisted public model.
- `src/` owns pages, presentation components, browser search controls, and
  shared visual styles.
- `scripts/build.mjs` prepares selected assets, renders Astro, then validates
  every public file and reference. `scripts/check-output.mjs` is the independent
  static-output checker.

The older `site_example/` prototype remains a comparison artifact. It is not
the Astro release package.

## Repository, Runtime, And Installation

Clone the complete TradeJournals repository. The build reads selected journals,
inventories, media, and scripts outside `website/`; copying that directory
alone is insufficient. The website currently lives on
`codex/website-updates`, not the repository's default `main` branch:

```sh
git clone --branch codex/website-updates <repository-url> TradeJournals
cd TradeJournals
```

Prerequisites are npm and Python 3.10 or newer. Install Node 24.21.0 inside the
project rather than changing the Mac's general Node installation. Run commands
from the repository root:

```sh
npm install --prefix website/.runtime --no-save --package-lock=false node@24.21.0
export PATH="$PWD/website/.runtime/node_modules/node/bin:$PATH"
node --version
python3 --version
npm --prefix website ci
```

`node --version` must report `v24.21.0`. Task 08's clean-checkout proof used
Python 3.13.7; the source syntax requires Python 3.10 or newer.

## Test And Build A Candidate

Use the scoped runtime for every website command:

```sh
export PATH="$PWD/website/.runtime/node_modules/node/bin:$PATH"
npm run test:website
npm run check:website
```

`test:website` runs the Node suite and Python source/output checks.
`check:website` builds and validates `website/.preview-dist/`. Serve that
candidate only on loopback for review:

```sh
python3 -m http.server 8126 --bind 127.0.0.1 --directory website/.preview-dist
```

Before reusing a port, identify its current process and directory. Do not stop
another task's server.

## Routine Updates

| Change | Edit | Verify |
| --- | --- | --- |
| Site identity, navigation, or contact action | `content/site.json` | Preview the header, navigation, homepage, and final contact action |
| Project summary or gallery selection | `content/projects/<id>.json`; selected media records | Preview the project, homepage card, and archive search |
| Homepage project order | `content/home.json` → `featuredProjectIds` | First featured project receives the hero link; cards follow the saved order |
| Shared card appearance | `src/components/ProjectCard.astro` | Rebuild and inspect the affected cards; content stays separate |
| Longer story | `content/stories/<id>.md` | Preview its TradeJournal route and review the source evidence |

Run `npm run check:website` after updates. The output gate deliberately accepts
only the site's planned files. New asset types or routes require an explicit
checker update. Styles are explicitly inlined in HTML, including as they grow.
The checker accepts safe HTTPS story citations and verifies required evidence
source-link identities without live Flickr requests;
recorded album counts remain local evidence, not fresh platform counts.

`npm run test:website` includes temporary synthetic builds that change copy,
featured order, and shared styling, then produce an invented reviewed release.
No real journal or review snapshot is changed by those scenarios.

## Review And Release

The candidate/release boundary is deliberate:

- `website/.preview-dist/` is a local candidate with a review notice and
  `noindex, nofollow`.
- `website/content/reviews/pilot.json` fingerprints the exact reviewed records,
  stories, sources, and image bytes.
- `website/dist/` is created only when that reviewed snapshot is current.

Review the [current expanded release](docs/pilot-editorial-review.md), including
the intentionally disabled email placeholder, before replacing the fingerprints
in `pilot.json`. The build never promotes changed content automatically: any
record, story, selected source, or image-byte change makes the reviewed snapshot
stale until that exact revision is approved and recorded.

After that exact snapshot is approved and recorded:

```sh
export PATH="$PWD/website/.runtime/node_modules/node/bin:$PATH"
npm --prefix website run build
node website/scripts/check-output.mjs dist
```

The release command refuses candidate or stale content. A successful run writes
the verified public package to `website/dist/`.

## Eventual Static Hosting

Upload the **contents** of `website/dist/` to the hosting account's document
root. Do not upload the repository, journals, inventories, private Workbench
store, runtime directories, or candidate output.

Current URLs are root-relative, such as `/work/...` and `/media/...`. The
package therefore assumes a domain root. Hosting under a path such as
`example.com/restoration/` requires a separate base-path change and check.

No build command buys hosting, changes DNS, uploads the website, sends a
message, or edits journal records.

## Release Checklist

- [x] The first release uses a disabled `Email us — coming soon` placeholder.
- [ ] Replace the placeholder with an approved `mailto:` action after a public
      address exists.
- [x] The expanded eight-project site is reviewed and approved.
- [x] `pilot.json` contains the matching reviewed snapshot.
- [x] `npm run test:website` passes under scoped Node 24.21.0.
- [x] `npm --prefix website run build` creates `website/dist/`.
- [x] The release output passes its checks and desktop/390-pixel review.
- [x] Only the contents of `website/dist/` form the provider-neutral release
      package; hosting selection and upload remain separate.

## Browser Editing

[TradeJournals Workbench](docs/workbench.md) supports multi-project stories,
room status, album assignment, photo order, captions, alternative text, private
drafts, isolated previews, and explicit local **Publish update**. Structured-file
editing remains available through the same records. Neither path deploys the
site or approves the reviewed snapshot.
