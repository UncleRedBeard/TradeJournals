# Task 13 — Project Pages And Galleries

Report ID: `WK-WEB-T13-R01`
Revision: 2 — direct user acceptance recorded
Date: October 2, 2026
Outcome: COMPLETE — hub accepted as `WK-WEB-T13-H02`
Delivery: Revision 2 RECEIVED and accepted as `WK-WEB-T13-H02`
Child: `01a0ff09-49a5-7cb2-a999-d7dbd073ecba`
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`

## Authorization And Scope

Implemented the [Task 13 brief](../task-13-project-pages-galleries.md), revision 1.
Shawn directly said `get started...but update the title to reflect status as well`
in child turn `01a0ff11-3c3e-7a13-844d-0ef34b67c21d`. Hub reconciliation
`WK-WEB-T13-A01` records that approval. The child title was updated to IN PROGRESS
and read back before implementation.

The approved Concept B palette, typography and shared frame are reused. This
stage changes project presentation only; approved content and photographs remain
unchanged. No dependency, carousel, framework or runtime JavaScript was added.

## Delivered

- `website/src/pages/work/[id].astro`: project introduction and record sit side
  by side on desktop and stack on smaller screens. A labelled project navigation
  offers a focusable photograph-section jump and the journal link. Return links
  lead to Work & Craft. The eight existing project routes retain their identity.
- `website/src/components/ProjectGallery.astro`: matte photo frames, an opening
  image with an adjacent desktop caption, responsive supporting images and
  readable original-source links. Portrait, landscape and square photographs
  remain uncropped. Order, captions, alt text and source destinations are retained.
- `website/src/components/EvidenceDetails.astro`: an opt-in `projectPage` style
  presents the existing evidence in a quiet record panel. Its default journal
  appearance and content remain unchanged.
- `website/tests/rendering.test.mjs`: one rendering test checks working gallery
  navigation plus every selected image, caption, alt text, original-source link
  and journal destination across all eight projects.
- `website/README.md`: records ownership of the project styles/components and
  the remaining journal/archive stage.

## Verification

- New regression test failed on the missing photograph jump before implementation
  and passed afterward. The existing occupancy fixture also passed.
- Full website suite: **120 Node tests and 37 Python tests passed**.
- `npm run check:website` and guarded release build passed under scoped Node
  24.21.0. Both retained outputs were independently checked against their matching
  prepared model: **18 pages, 52 files, 302 references each**.
- Review state is `current`, with no changed keys in either mode. The saved
  snapshot file retains SHA-256
  `cdc69b8b5c95af1e05677e9a1639287fd5b8886ab0872ce9adc3bc71dcd5699f`.
- Repository Markdown lint (101 files, zero errors) and `git diff --check` passed.
- A separate read-only reviewer inspected the Task 13 delta against saved
  starting copies and found no actionable defects. The reviewer did not rerun
  tests or duplicate browser checks.

### Browser Review

- No horizontal overflow on Living Room, Guest Bath, Office and Agfa projects
  at 320px and 390px; each lead image loaded. Living Room also fits at 768px.
- Inspected desktop project introduction and photo layouts at 1280px. Living
  Room portraits, Guest Bath square images and Current Studio landscape/portrait
  images use `contain` sizing. All images on those three inspected galleries
  loaded as they were scrolled into view.
- At 1024px the Current Studio gallery target starts at 144px beneath a 129px
  wrapped header. At 1280px the target starts at 128px beneath a 90px header.
- Gallery jump transfers focus to its section. Tab then reaches the original
  image source with a visible 3px focus outline.
- The Living Room journal link opens the matching journal and retains the
  existing evidence presentation. Current/future studio wording stays distinct.
- Inspected the accepted homepage and shared navigation; inquiry controls remain
  disabled. The browser reported no warnings or errors.
- External Flickr/Google Photos availability was not re-audited. Source URLs
  remain unchanged; output and rendering checks verify their identities.

## Review Links

Existing loopback preview on port 8139 serves the rebuilt candidate; the browser
shows the new project output. The listener was reused without restarting it.

- [Living Room project](http://127.0.0.1:8139/work/living-room-studio-restoration/)
- [Guest Bath project](http://127.0.0.1:8139/work/guest-bath-dresser-vanity/)
- [Current Studio project](http://127.0.0.1:8139/work/studio-office-restoration/)
- [Agfa project](http://127.0.0.1:8139/work/agfa-isolette/)

Screenshots in
`/Users/shkelley/.codex/visualizations/2026/10/02/01a0ff09-49a5-7cb2-a999-d7dbd073ecba/`:
`task13-desktop.jpg` (full page), `task13-overview.jpg` (desktop introduction),
and `task13-phone.jpg` (phone gallery).

## Protected Work And Return

Branch: `codex/concept-b-homepage`. Task 13 started at `6c48930`; a separate
El Toro content-review closeout advanced HEAD to
`0225667b59339ea2a8bb82e00d59b3c98e886aca` during this work. No Git writes were
performed by Task 13. Its changes and the accepted Task 12 foundation remain
uncommitted.

Starting-file hashes confirm only the three intended source components/template
changed under `website/src/`; no file under `website/content/` changed. Task 12
shared frame, homepage, fonts and tokens were preserved. The hub alone updated
its brief/register. Concurrent content-review journals, register and later
SXSW brief remain owned by that workflow and were not edited or staged here.

Revision 2 records Shawn's direct `approved` in this child on October 2, 2026,
turn `01a0ff24-8003-72c3-9b99-f87b22a20315`, after the review delivery. The hub
register independently records passed technical review as `WK-WEB-T13-H01`.
No implementation change accompanies this approval. Request hub acceptance and
status/title closeout only.

This report requests reconciliation only. User acceptance is received.
Task 14, Git closeout, snapshot changes, merge, deployment and archival remain
outside this stage.
