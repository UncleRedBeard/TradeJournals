# Task 12 — Concept B Shared Frame

Report ID: `WK-WEB-T12-R01`
Revision: 3 — final user approval recorded in child
Date: October 2, 2026
Outcome: COMPLETE — hub accepted as `WK-WEB-T12-H03`
Delivery: Revision 3 RECEIVED and reconciled October 2, 2026
Child: `01a0fed3-08c2-7042-a8ea-f1893d20c24a`
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`
Dispatch: `WK-WEB-T12-D01`

## Authorization And Scope

Implemented revision 1 of the [Task 12 brief](../task-12-concept-b-shared-frame.md),
authorized by Shawn's instruction to start in stages. His October 2 reminder to
avoid over-engineering was retained: two small components and one shared style
file reuse the accepted design. No dependency, framework or configuration system
was added.

Branch remains `codex/concept-b-homepage`; HEAD remains
`6a528e37a2c14b5eb4609f0338f5d0c01b8c7b7b`. Changes are uncommitted.
No push, merge, deployment, archive or successor dispatch occurred.

## Delivered Changes

- `AtelierHeader.astro` and `AtelierFooter.astro` extract the accepted homepage
  markup. `SiteLayout.astro` applies them to every route, along with the local
  font license, shared styles and a focusable skip-link destination.
- Homepage links retain local fragments. Inner-page Selected work, Practice and
  Workshop links lead to the corresponding homepage sections. Workshop remains
  conditional on selected content.
- `atelier-frame.css` holds the extracted frame styles; `tokens.css` holds the
  accepted palette and font definitions. Existing token names remain usable by
  inner-page components. `atelier.css` retains homepage-specific styling.
- The wrapped sticky header receives a 9rem anchor offset at the existing
  tablet breakpoint. Browser measurements showed the previous 8rem offset
  overlapped the destination edge by approximately 1px; the new offset leaves
  about 15px clearance. The phone header remains static.
- All four page files pass the homepage navigation data to the shared layout.
  Homepage body markup, card layout, copy, imagery and selected order are intact.
- Rendering tests cover shared navigation, landmarks, font/license inclusion,
  keyboard target and disabled inquiries across all 18 routes. The synthetic
  candidate fixture also verifies omission of an absent Workshop section.
- `website/README.md` identifies the shared files and later-stage boundary.

Project galleries, journal reading layouts and archive/search presentation
remain later stages. Their content structures and search implementation were
not edited. Historical-home restoration remains primary; clay and film remain
in the quieter workshop section. All room distinctions and disabled inquiries
are preserved.

## Verification

- Regression test failed before implementation on the missing focusable main
  target, then passed with the completed shared frame.
- Full website suite: **119 Node tests and 37 Python tests passed**.
- Candidate/preview and guarded release builds passed. Final retained outputs
  were independently checked using matching prepared models: **18 pages,
  52 files and 270 references each**. Reference count increased from 236 because
  inner pages now carry the shared homepage navigation.
- Both prepared models report review state `current`, with no changed keys.
- Fonts remain bundled inline from existing local WOFF2 files; each rendered
  page includes one OFL license template. No external font source was added.
- A separate read-only code review found no actionable defects.
- Repository Markdown lint: **95 files, zero errors**. `git diff --check` passed.

### Browser Checks

In the Codex browser, inspected homepage, living-room project, its journal and
archive at desktop and phone widths. All four route types measured viewport
width equal to document width at **320px and 390px**, with no horizontal
overflow. Desktop appearance was inspected at **1280px**; the wrapped header and
section destination clearance were checked at **1024px**.

- Homepage appearance and documented-project order matched the accepted layout.
- Project photographs loaded; Cormorant Garamond reported loaded on homepage
  and project. Existing source URLs and gallery links remain present.
- From inner pages, Selected work, Practice and Workshop reached the correct
  homepage sections. At 1024px, Practice starts at 144px below a 129px header.
- Keyboard Tab exposed the visible skip link with a 3px outline. Enter moved
  focus to `main-content`; the next Tab reached archive search with visible
  focus. Inquiry controls remained disabled.
- Search for `original door` returned Entry and Stair Restoration. Search for
  `office` returned Dedicated Office and Barre Studio — Current Room separately.
- Browser console recorded no warnings or errors in the inspected session.

The external photo providers were not re-audited; source links were preserved
and the static checker validated their syntax. No claim of public deployment
or full accessibility certification is made.

## Review Links

Loopback preview server: port 8139, serving `website/.preview-dist`.
Existing servers on ports 8128, 8131, 8132 and 8134 were left running.

- [Homepage](http://127.0.0.1:8139/)
- [Project](http://127.0.0.1:8139/work/living-room-studio-restoration/)
- [Journal](http://127.0.0.1:8139/tradejournals/living-room-studio-restoration/)
- [Archive](http://127.0.0.1:8139/tradejournals/)

Screenshot saved locally at
`/Users/shkelley/.codex/visualizations/2026/10/02/01a0fed3-08c2-7042-a8ea-f1893d20c24a/task12-shared-frame.jpg`.

## Protected And Concurrent Work

The reviewed snapshot remains byte-for-byte unchanged:
`cdc69b8b5c95af1e05677e9a1639287fd5b8886ab0872ce9adc3bc71dcd5699f`.
No website content records, stories, selected assets or source fingerprints
were edited by this task.

The content-review register retains its starting hash
`96ddf67628fec268f62f88eefd69f7e4d350684b00b9be44c159e57d6721a33e`.
Concurrent content-review work changed its Kodakk brief during execution and
also modified `05_the_lens/trade_journals/flickr_kodakk_613_1913.md` and added
`docs/content-review-workflow/reports/task-02-kodakk-camera-film.md`.
Those files were not edited, reverted or included in this implementation.
Hub-owned Task 12 brief and website task register were also left untouched.

## Stage Boundary

Revision 3 records Shawn's direct approval in this child on October 2, 2026:
`i like that. approved`, following delivery of the Work & Craft navigation
wording. No implementation changed after revision 2. Request hub acceptance and
status reconciliation; this approval does not start the next stage or authorize
Git closeout or deployment.

Revision 2 supersedes revision 1 for navigation wording only. Shawn requested
`work & craft`; the shared link now reads **Work & Craft**, without the count.
Its existing destination is unchanged. Preview and guarded release rebuilt
successfully (18 pages, 52 files, 270 references each); the new label was checked
on all 18 pages in both outputs and in the rendered browser. `git diff --check`
passed. Earlier full-suite evidence above applies to the shared-frame change.

Shared-frame implementation is ready for hub review. Detailed project, journal
and archive design work is still outstanding and requires its next staged
instruction. This report requests reconciliation only.
