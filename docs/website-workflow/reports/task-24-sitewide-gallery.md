# Task 24 — Sitewide Gallery Treatment

Report: `WK-WEB-T24-R01`, revision 1. October 19, 2026.
Child: `01a15545-ba05-7420-953c-615c51a1a29b`.
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`.
Dispatch: `WK-WEB-T24-D01`. Status: READY FOR REVIEW.

## Delivered

All nine project galleries now use the accepted local photograph viewer.
One shared `GalleryViewer.astro` contains the native dialog, minimal script,
source links and styles. Entry retains its accepted stage labels and two-pass
introduction through its small wrapper. The other projects retain their existing
captions without imposing a restoration chronology on ceramics or photography.

All 37 selected photograph placements retain their order, captions, alt text
and provenance. Album links sit below each gallery; individual sources sit in
a disclosure. The bedroom's two albums retain distinct recorded names.
Homepage/archive navigation, journals, attribution and contact state remain intact.
No dependency, route, content record, schema or source-journal change was needed.

## Changed files

- `website/src/components/GalleryViewer.astro` — shared viewer extracted from Entry.
- `website/src/components/EntryGallery.astro` — accepted Entry context and labels.
- `website/src/pages/work/[id].astro` — shared viewer on every project route.
- `website/tests/rendering.test.mjs` — sitewide local-viewing and provenance checks.
- `website/README.md` — shared gallery maintenance guidance.
- This completion report. Hub-owned brief and register changes were preserved.

## Verification

- `npm run test:website`: 125 Node tests and 37 Python tests passed.
  Log: `/tmp/task24-tests.log`.
- `npm run check:website`: fresh preview and output validation passed for all
  20 pages, 60 files and 366 references. Log: `/tmp/task24-preview.log`.
- Rendering checks cover every project's local image targets, selected order,
  captions, source links, album counts, unchanged journals, navigation and metadata.
- Office, Returning to Clay, Agfa Isolette and Entry checked at 1440-pixel desktop
  and 390-pixel mobile widths. First and last images opened correctly; Enter,
  Escape, close button, caption, image fit and return focus passed. No horizontal
  overflow was observed. Local-image fallback remains in every anchor.
- Bedroom source links and expanded photo provenance checked on mobile; both
  album names/URLs are retained. External album availability was not audited.
- No browser console errors observed. Viewport override reset.
- Initial new test failed against the old non-Entry behavior as expected.
  A later test-only placement assertion mistakenly matched the inline script;
  it was corrected to compare actual gallery anchors before the passing suite.
- A final browser permission check timed out; the permitted single retry
  succeeded. A manually entered bedroom URL omitted its restoration suffix;
  the correct generated route was then verified successfully.
- Self-review found no broader content or dependency changes. README/report
  Markdown lint and `git diff --check` passed.

## Review preview

- [Office](http://127.0.0.1:8143/work/office-restoration/#project-photographs)
- [Returning to Clay](http://127.0.0.1:8143/work/returning-to-clay/#project-photographs)
- [Agfa Isolette](http://127.0.0.1:8143/work/agfa-isolette/#project-photographs)
- [Entry](http://127.0.0.1:8143/work/entry-restoration/#project-photographs)

Reused the verified Task 23 Python server, PID `29897`, shell session `28856`,
at `127.0.0.1:8143`, serving `website/.preview-dist`. Left running for review.
No additional server was started and no other task's server was stopped.

Screenshots are saved under
`/Users/shkelley/.codex/visualizations/2026/10/19/01a15545-ba05-7420-953c-615c51a1a29b/`:

- `task24-office-desktop-dialog.jpg`, `task24-office-mobile-dialog.jpg`
- `task24-clay-desktop-dialog.jpg`, `task24-clay-mobile-dialog.jpg`
- `task24-agfa-desktop-dialog.jpg`, `task24-agfa-mobile-dialog.jpg`
- `task24-entry-desktop-dialog.jpg`, `task24-entry-mobile-dialog.jpg`
- `task24-bedroom-mobile-sources.jpg`

## Review and release boundaries

Shared checkout remains `main` at `4864feb`; implementation is uncommitted.
Read-only snapshot comparison is current with zero changed keys. `pilot.json`
is unchanged, SHA-256:
`2efb1566680b93491b2f13b389d2ccb368be6e60392cef31bd3027095bdcd841`.
Content snapshot currency does not constitute acceptance of this presentation.

No snapshot refresh, release build, commit/push, deployment, contact activation
or successor was performed. User acceptance and Git closeout remain separate.
Report delivery uses this artifact and final response for hub observation;
no callback is sent and hub receipt is not yet claimed. The hub owns acceptance
and COMPLETE status.

## Direct user acceptance

Acceptance `WK-WEB-T24-A01` applies to report `WK-WEB-T24-R01`, revision 1.
On October 20, 2026, after reviewing the reopened preview, Shawn said:
“looks good...approved”.

The sitewide gallery treatment is accepted. This supersedes the pending user
acceptance at submission. Hub reconciliation of the register and COMPLETE
status remains with the website updates hub. Git closeout and public deployment
remain separate; neither was performed by this acceptance update.
