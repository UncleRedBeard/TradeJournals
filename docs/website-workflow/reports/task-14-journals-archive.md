# Task 14 — Journals And Archive

Report ID: `WK-WEB-T14-R01`

Revision: 1

Date: October 2, 2026

Outcome: COMPLETE — accepted by Shawn and hub as `WK-WEB-T14-H02` October 3

Delivery: RECEIVED as `WK-WEB-T14-H01`; acceptance recorded in the hub register

Child: `01a0ff4e-a59e-7b02-a44b-d36c0663db18`

Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`

Dispatch: `WK-WEB-T14-D01`

## Authorization And Delivery

Shawn said `kick off task 14` in the website hub. The approved dispatch and
[brief, revision 1](../task-14-journals-archive.md) authorized this stage. The
IN PROGRESS title and active child were verified before implementation.

- Journal pages now use a measured reading column, existing Atelier typography,
  a project-record panel and links back to the project and archive. The original
  Markdown story remains intact; a storyless fixture still renders its title
  and summary. Styles are contained in the journal template and explicitly
  reach rendered Markdown descendants.
- The archive has a consistent heading, search panel, labelled field, status
  area and two-column entries that stack on phones. Runtime-created results
  receive the same styling as static entries. An explicit hidden-state rule
  keeps fallback entries and results from appearing together.
- Search scripts, query matching/ranking, result destinations, summary data,
  text-safe rendering and existing empty/error behavior are unchanged.
- `website/README.md` records the component/style ownership. Rendering coverage
  verifies a single story heading, matching project destination, archive return
  link and one evidence record on every journal, plus the storyless fixture.

No dependency, new runtime JavaScript, content record, gallery or source-journal
change was introduced. Accepted homepage, shared frame and project pages are
unchanged. Work & Craft and disabled inquiry controls remain in place.

## Verification

- The new journal navigation test first failed on the absent archive-return
  link, then passed with implementation. The storyless fixture passed too.
- Full website suite: **121 Node tests and 37 Python tests passed**.
- `npm run check:website` and guarded release build passed using scoped Node
  24.21.0. Independent checks against matching prepared models validated both
  outputs at **18 pages, 52 files and 318 references each**.
- Both review states are `current`, with no changed keys. Snapshot SHA-256 is
  unchanged: `cdc69b8b5c95af1e05677e9a1639287fd5b8886ab0872ce9adc3bc71dcd5699f`.
- Final Markdown lint passed across **107 files, zero errors**. Tracked and
  new-report whitespace checks passed.
- A separate read-only reviewer inspected the five implementation/test/doc
  files and found no actionable correctness, accessibility or scope issues.

### Browser Checks

- Archive and long Entry journal fit at 320, 390, 768, 1024 and 1280px without
  horizontal overflow. The short Office journal was also inspected at 390px.
  Desktop reading width is capped at 704px; phone content fits its viewport.
- `original door` returns Entry and Stair Restoration. `office` returns
  Dedicated Office and Barre Studio — Current Room as separate entries.
- Static and inserted result headings both use Cormorant Garamond at the same
  computed size. Hidden fallback has `display: none` after a successful search.
- A nonmatching query shows the existing no-match message; an empty query
  retains the existing first-three-results behavior.
- Temporary loopback QA servers returned an intentional search-data 503 or
  empty script responses. With unavailable data, the status explains the
  failure and all eight static entries remain visible. With no scripts, the
  complete archive remains browsable before and after normal GET submission.
  These QA servers were stopped; the existing preview server was preserved.
- Keyboard navigation reveals a 3px skip-link focus outline, moves through the
  main content to the archive-return link, and reaches the search button from
  its field with visible focus. Journal/project/archive navigation was used.
- The accepted homepage and Living Room project were inspected in the browser.
  Room distinctions, shared navigation and disabled inquiries remain intact.
  No warnings or errors were reported in the normal preview tab.

External source-provider availability was not re-audited. Source destinations
remain unchanged; there is no claim of deployment or full accessibility audit.

## Preview And Screenshots

The existing loopback preview on port 8139 serves `.preview-dist` and was
verified against the rendered new layout. Its archive tab is retained for review.

- [Archive](http://127.0.0.1:8139/tradejournals/)
- [Entry journal](http://127.0.0.1:8139/tradejournals/entry-restoration/)
- [Office journal](http://127.0.0.1:8139/tradejournals/office-restoration/)

Screenshots are in
`/Users/shkelley/.codex/visualizations/2026/10/03/01a0ff4e-a59e-7b02-a44b-d36c0663db18/`:

- `task14-journal-desktop.jpg`
- `task14-journal-phone.jpg`
- `task14-archive-search-desktop.jpg`
- `task14-archive-phone.jpg`

## Shared Workspace And Return

Branch remains `codex/concept-b-homepage`; observed HEAD remains
`6042f00416a2d04382dbc57f249bbd15c1d315b8`. Task 14 changes are uncommitted.
Starting hashes confirm changes only to the archive component, two journal
templates, rendering tests and README. All website content, shared-frame,
homepage, project, gallery, search-script and snapshot files are unchanged.

Concurrent source-review work owns the Lomography overlap and France travel
journals, its register, and SXSW/Mini Diana briefs/reports. Those files were not
edited or staged here. The hub owns and updated the website brief/register;
this child did not edit either one.

Return is for hub reconciliation and Shawn's visual acceptance. Task 15, Git
closeout, snapshot refresh, merge, deployment and archival are not authorized
by this report.
