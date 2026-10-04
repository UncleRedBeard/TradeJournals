# Toil & Timber Restoration Website

This Astro project builds ordinary static HTML, CSS, JavaScript, and images.
Node and Python are build tools only. Serving the finished site does not require
Astro, Workbench, a database, or an application server.

The current site keeps three rooms distinct:

- Dedicated Office — current room, six selected photographs in the candidate
  (five room/use views and one localized-access detail).
- Barre Studio — Current Room — current home of The Repair Shop, seven selected
  photographs in the candidate (five room/door views and two finish details).
- Living Room Restoration — Future Barre Studio — future home of The Repair
  Shop, three selected photographs.

Keep the current and future rooms distinct until Shawn explicitly confirms the
move.

The La Ciotat Lens story is a three-photo archive and search entry. It does
not change the homepage's featured or workshop selections.

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

The [approved Concept B homepage](docs/concept-b-homepage-review.md) adapts the
reviewed Stitch direction into the existing Astro site. Its presentation lives
in `src/styles/atelier.css` and `src/components/AtelierProjectCard.astro`.
`SiteLayout.astro` reuses `AtelierHeader.astro` and `AtelierFooter.astro` on every
route. Shared frame styles and local fonts live in `src/styles/atelier-frame.css`;
palette and font tokens live in `src/styles/tokens.css`. Inner-page navigation
links back to the homepage sections. Project presentation lives in
`src/pages/work/[id].astro` and `ProjectGallery.astro`: full-image matte frames,
captions, a photo jump link and links to the journal. `EvidenceDetails.astro`
uses its opt-in `projectPage` record panel on project and journal pages.
Journal reading styles live with `src/pages/tradejournals/[id].astro`; their
Markdown selectors are explicitly global beneath `.journal-story`.
`ArchiveSearch.astro` owns search controls and both static and dynamic result
presentation. Its entry selectors deliberately reach runtime-created children;
the existing text-safe search script, ranking and fallback remain unchanged.

## Repository, Runtime, And Installation

Clone the complete TradeJournals repository. The build reads selected journals,
inventories, media, and scripts outside `website/`; copying that directory
alone is insufficient. The accepted Concept B candidate is on
`codex/concept-b-homepage`; `main` still contains the previous release.
Task 15 verifies candidate baseline `ef1d5e8303860d49b7ae6131b0596e2bce38660b`.
To obtain that candidate branch:

```sh
git clone --branch codex/concept-b-homepage <repository-url> TradeJournals
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

`node --version` must report `v24.21.0`. The clean-checkout verification uses
Python 3.13.7; the source syntax requires Python 3.10 or newer.
Install the repository Markdown tooling separately from the repository root,
using the same scoped Node runtime:

```sh
npm ci
npm run lint:md
```

The root manifest pins `markdownlint-cli2` 0.23.3, and the root lockfile fixes its
transitive versions. It requires Node 22 or newer; the scoped Node 24.21.0 above
satisfies that requirement. Root `node_modules/` is ignored by Git and lint.
The existing Markdown rules and authored-file coverage are preserved.

Website dependencies remain separately locked and installed with
`npm --prefix website ci`. The [Task 17 report](../docs/website-workflow/reports/task-17-markdown-tooling.md)
records the tooling update and remaining upstream finding; Task 16 records the
separate website dependency findings.

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
| Homepage card appearance | `src/components/AtelierProjectCard.astro` | Rebuild and inspect desktop and stacked mobile cards |
| Other shared card appearance | `src/components/ProjectCard.astro` | Rebuild and inspect the affected cards; content stays separate |
| Longer story | `content/stories/<id>.md` | Preview its TradeJournal route and review the source evidence |

Run `npm run check:website` after updates. The output gate deliberately accepts
only the site's planned files. New asset types or routes require an explicit
checker update. Styles are explicitly inlined in HTML, including as they grow.
The checker accepts safe HTTPS story citations and verifies required evidence
source-link identities without live Flickr requests;
recorded album counts remain local evidence, not fresh platform counts.
Every page embeds its Cormorant Garamond fonts in the CSS and includes their
license in an inert HTML template. Font files and the original license live in
`src/styles/fonts/`; visitors make no external font requests.

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

The standalone checker reads the prepared model from the most recent build.
Run it immediately after the matching build: `check:website` does this for the
preview; the two commands above do it for the release. To inspect both retained
outputs independently, prepare each mode's model and pass it to `checkOutput`,
as recorded in the [Task 15 report](../docs/website-workflow/reports/task-15-integrated-release-review.md).

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

The [release review](docs/pilot-editorial-review.md) records the content approval
and accepted Concept B homepage, shared frame, project galleries, journals and
archive. The [Task 15 report](../docs/website-workflow/reports/task-15-integrated-release-review.md)
records integrated verification of the candidate branch. The
[Task 16 report](../docs/website-workflow/reports/task-16-dependency-maintenance.md)
records the subsequent dependency patch and remaining upstream findings.
These are local
readiness records; they do not mean the branch is merged or the site deployed.

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
