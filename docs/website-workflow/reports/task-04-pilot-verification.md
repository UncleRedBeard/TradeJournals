# Task 04 Pilot Verification Report

Report ID: `WK-WEB-T04-R01`
Revision: 2
Status: COMPLETE — accepted by hub

This hub revision supersedes revision 1's incomplete browser and maintenance
verification. The child resumed after the hub began recovery and supplied the
checker/documentation draft. The hub reconciled those edits, corrected review
findings, and completed the build and browser scenarios. The internal parser
helper contributed the Python parser and its focused tests.

## Result

The Time & Timber Restoration Astro pilot validates actual emitted static
files after Astro renders them. Candidate content remains preview-only; a
release stops with `UNREVIEWED_CONTENT` until an approved review is recorded.

The homepage's "See the work" link now follows the first featured project.
A synthetic two-project build exposed its previous hardcoded Office URL.
This is a maintenance fix; the real pilot's appearance and destination remain
unchanged because Office is still its first featured project.

## Delivered

- Python standard-library HTML parser for IDs, links, image attributes, entities,
  robots metadata, and a strict stdin/stdout contract.
- Output checker for exact planned pages/assets, local links and fragments,
  source identities and required project source links, search JSON, private
  paths, preview metadata, unsafe URLs, unexpected files, and symlinks.
- Build integration: a successful Astro render alone cannot pass the build.
- Explicit inline styles keep ordinary stylesheet growth within the pilot's
  small output contract. A larger-than-4-KB synthetic stylesheet is exercised.
- Empty image URLs fail; valid HTTPS story citations pass while required
  evidence-source links retain exact identity checks.
- Root preview/test/check commands, maintenance guide, and prototype-guide pointer.
- Regression cases for same-page anchors, duplicate targets, relative links,
  selected homepage heroes, missing source links, and leftover preview notices.

## Verification

All commands used the scoped Node 24.21.0 runtime where applicable.

| Check | Observed result |
| --- | --- |
| `npm run test:website` | 79 Node tests and 37 focused Python tests passed. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | 84 Python tests passed. |
| `npm run check:site-evidence` | Existing evidence manifest is current. |
| `npm run test:site` | 5 evidence tests and 5 legacy search tests passed. |
| `npm run check:website` | Preview rendered and validated 4 pages, 17 files, and 60 references. |
| Real candidate release | Nonzero exit with `UNREVIEWED_CONTENT`; saved review remains candidate with empty snapshots. |
| Synthetic reviewed release | Actual Astro release built 6 pages and passed the output gate; no preview notice or noindex in those pages. |

Final acceptance on September 16, 2026: Markdown lint checked 59 files with
zero errors; tracked and untracked whitespace checks passed. Independent review
findings were fixed and rechecked with no remaining Important or Critical
issues. The normal preview was reloaded after the final build, with no captured
console errors or warnings. Task title and register were reconciled to COMPLETE.

### Maintenance Scenarios

All altered records and styles were temporary synthetic fixtures.

- A summary edit appeared on the homepage, project page, and search JSON.
- Reordering two featured IDs reordered the homepage cards and hero destination,
  while the project page stayed byte-identical.
- Changing the shared card border changed generated presentation while the
  prepared public content model stayed identical.
- Missing selected image IDs fail `MISSING_REFERENCE`; missing emitted images
  fail `MISSING_OUTPUT` with their paths.
- Selected journal/photo changes invalidate review. An unrelated inventory
  block and unselected image changes preserve the reviewed state.
- Candidate release failed; after recording an invented reviewed snapshot, the
  complete synthetic release build succeeded.

## Browser Review

Normal preview: [Time & Timber Restoration](http://127.0.0.1:8126/).
The loopback server serves this checkout's `website/.preview-dist` directory.
The previous preview server stopped during task coordination; the hub restarted
it after verifying port 8126 was free.

- Desktop 1280 pixels and mobile 390 pixels: home, Office project, and archive
  remained readable with no horizontal overflow. The mobile gallery stacked
  into one column. Sampled gallery crops and captions were legible; final photo
  and crop choices remain Shawn's editorial decision.
- The longer TradeJournal story rendered as readable paragraphs at narrow and
  desktop widths, with its source-album links and project return link.
- Keyboard Tab exposed the skip link. Enter reached `#main-content`; the next
  Tab focused "See the work" with a visible solid outline, bypassing the header.
- Normal archive search for `door` returned one Office result and its distinct
  search summary.
- Ten selected images, ten photo-source links, and two album links were present
  on the project page. Source identities are checked locally; remote Flickr
  availability was not fetched or claimed.
- A temporary loopback server on port 8127 sent a verified
  `Content-Security-Policy: script-src 'none'` header. Home, archive, Office
  project, and longer story remained readable; archive-to-project navigation
  worked. This blocks page scripts, not the browser's global JavaScript engine.
- A separate temporary server returned HTTP 503 for `/search.json`. The browser
  showed "Search is unavailable. The project list remains below." and kept the
  original project list visible with the results list hidden.

These are focused checks in the Codex in-app browser, not a full cross-browser
or assistive-technology certification. Temporary viewport overrides were reset and fault servers stopped; the normal
preview remains available.

## Changed Paths

- `scripts/check_website_html.py`
- `tests/test_website_html.py`
- `website/scripts/check-output.mjs`
- `website/tests/output.test.mjs`
- `website/tests/maintenance.test.mjs`
- `website/scripts/build.mjs`
- `website/astro.config.mjs`
- `website/src/components/Hero.astro`
- `website/src/pages/index.astro`
- `website/package.json` and root `package.json`
- `website/README.md`
- `site_example/README.md`
- Task 04 brief, this report, and the hub-owned workflow register

## Git And Review Boundary

Branch: `codex/website-updates`; HEAD remains
`7d023b9f06781bdf082acaa2e0c6fc15fbf1479e`. Changes are uncommitted.
Original journals, inventories, source images, public candidate records,
prototype HTML/catalog/manifest, and existing browser scripts have no diff.
Only the planned guide pointer changed inside `site_example/`.

Editorial approval of the candidate copy and photos, a contact destination,
and hosting/domain decisions remain outside this task. No public release,
deployment, commit, or push was performed. There is no automatic Task 05.
