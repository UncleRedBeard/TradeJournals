# Website 2 - Task 12 Concept B Shared Frame

Workflow status: COMPLETE — hub technical review passed; Shawn's approval verified
Brief revision: 1
Approval: Shawn said `ok, let's get started in stages. you already know our
workflow.` in website updates on October 2, 2026, after receipt of the approved
Concept B direction. This authorizes the first bounded stage; later stages
return to the hub for their own start instruction.
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` / website updates
Child: `01a0fed3-08c2-7042-a8ea-f1893d20c24a`
Dispatch: `WK-WEB-T12-D01` — SENT once October 2, 2026
Register: [task-register.md](task-register.md)
Workspace: `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/TradeJournals`
Branch: `codex/concept-b-homepage`
Baseline: `6a528e37a2c14b5eb4609f0338f5d0c01b8c7b7b`

Exact title and idle state verified before dispatch; fresh wait confirmed turn
`01a0fed5-562d-7193-a48a-ec6d5f50f69a` in progress.

## Approved Direction And Stage Boundary

Hub receipt `WK-WEB-T12-H01`, October 2, 2026: report `WK-WEB-T12-R01`,
revision 1 received. Hub reviewed the implementation diff and new shared
components/styles; independently reran 119 Node and 37 Python tests, 95-file
Markdown lint and whitespace checks. Both retained outputs independently
validate at 18 pages, 52 files and 270 references using matching prepared
models. Review remains current with zero changed keys; snapshot file hash is
unchanged. Hub inspected the live inner project page and shared navigation;
the child's detailed desktop/mobile/keyboard/search QA is recorded in its report.

Hub receipt `WK-WEB-T12-H02`, October 2, 2026: report `WK-WEB-T12-R01`,
revision 2 received. Verified Shawn's direct child instruction `change it to
work & craft` in turn `01a0feef-79b9-7940-8066-cb7c40b10759`. This narrow
amendment replaces the shared navigation label with **Work & Craft**, without
the count; its destination is unchanged. Hub independently checked the label
and destination on all 18 pages in each rebuilt output. Child build and rendered
browser checks passed. Earlier full-suite evidence applies to the shared frame;
visual acceptance remains pending and no next-stage or Git work is authorized.

Hub acceptance `WK-WEB-T12-H03`, October 2, 2026: report `WK-WEB-T12-R01`,
revision 3 received. Verified Shawn's `i like that. approved` in child turn
`01a0fefe-5250-7aa2-ab93-6ee2f42b4f28`, following delivery of the Work & Craft
amendment. No implementation changed after revision 2. Together with the passed
technical review, this completes Task 12's accepted scope. Earlier pending
acceptance statements are historical; no successor or Git work is authorized.

Preview: `http://127.0.0.1:8139/`. Implementation remains uncommitted on
`codex/concept-b-homepage`. Concurrent Kodakk journal, brief/report and
content-review register changes belong to that separate workflow and are
preserved. No implementation fixes or unrelated edits were made by the hub.
Task 12 is accepted and complete; Task 13 has not started.

The Concept B Craftsman's Atelier homepage is accepted. Extend its shared
frame across the existing site: header, footer, palette/font foundations,
navigation, skip link, keyboard focus and review notice. Extract only the
small reusable pieces needed from the accepted homepage. Preserve its visual
appearance and responsive behavior. Avoid a parallel theme system or wholesale
CSS rewrite. Keep long-form content readable while its detailed layout awaits
the next stages.

Current homepage header/footer live in `website/src/pages/index.astro` as named
slots; the remaining routes use defaults in `SiteLayout.astro`. Styling lives
in `atelier.css`, currently scoped in part to `.atelier-home`. Reuse existing
Atelier components and local fonts. Retain the bundled OFL license in generated
output wherever the fonts are used, with no external font requests or new
dependency unless a concrete need is first established.

Navigation must work from both homepage and inner pages: Selected work,
Practice and Workshop must resolve to the actual homepage sections when used
elsewhere. Preserve the TradeJournals link, source links and existing routes.
Make routine implementation choices within this accepted design; do not reopen
settled design approval or ask to start a task already authorized.

Preserve Documented Projects order exactly: Living Room Restoration — Future
Barre Studio, Entry and Stair Restoration, Guest Bath and Dresser Vanity,
Master Bedroom Restoration. Returning to Clay and Agfa Isolette remain under
From the workshop. Inquiry controls stay disabled. Preserve copy, photographs,
captions, gallery order, source identities and search behavior.

Do not implement project-gallery redesigns, TradeJournal reading layouts or
archive/search-card redesigns in this stage. Shared frame changes necessarily
appear on those pages; their page-specific presentation is later work.

## Read First

- `website/docs/concept-b-homepage-review.md` — October 2 closeout supersedes
  its historical failed-test/uncommitted notes.
- `website/docs/pilot-editorial-review.md` — final October 2 section records
  approval of exactly three changed fingerprints.
- `website/README.md`, layout/components/styles and applicable tests.
- Applicable repository instructions and proportionate frontend-design,
  senior-developer, planning and verification skills. Reuse approved design
  decisions; avoid unnecessary design artifacts or approval loops.

## Concurrent Work And Review Boundary

The content-review hub is separate. Preserve these unrelated files byte-for-byte
unless their owner changes them during execution; do not revert their changes:

- `docs/content-review-workflow/task-register.md` — initially modified;
  SHA-256 `96ddf67628fec268f62f88eefd69f7e4d350684b00b9be44c159e57d6721a33e`.
- `docs/content-review-workflow/task-02-kodakk-camera-film.md` — initially untracked;
  SHA-256 `660f482f5936002ef14ea31b864fd0f2c4bcc73d3197396ec966707fbcc869ea`.

Only this child owns website implementation during this stage. The hub owns
this brief and `docs/website-workflow/task-register.md`; preserve their pending
changes and do not edit them. Stay on the current feature branch; no switch to
main, no new checkout required for this nonoverlapping shared-directory stage.

The exact reviewed snapshot file SHA-256 is
`cdc69b8b5c95af1e05677e9a1639287fd5b8886ab0872ce9adc3bc71dcd5699f`.
This presentation-only scope does not require changing public records or source
fingerprints. Preserve the snapshot. If concurrent source edits make review
stale, report the actual gap and continue independent work; do not automatically
refresh fingerprints or weaken the gate. Re-review changed records/sources
before any separately authorized update.

The future living-room studio, current barre studio and Dedicated Office remain
distinct. Do not infer a move. Sealed/non-operable living-room windows and bounded
Office electrical-access source clarifications are accepted; older mixed-room
Office claims remain withheld from the public story.

## Deliverables And Acceptance

- Small reusable shared frame applied consistently to all existing route types,
  retaining the accepted homepage and functional inner-page navigation.
- A loopback preview for review. Inspect existing listeners before selecting a
  port; do not stop other tasks' servers. Show homepage, a project, a journal and
  archive at desktop and phone widths, including 320/390px overflow checks.
- Verify keyboard navigation, visible focus, skip link, disabled inquiries,
  homepage section destinations from inner pages, fonts/license, links, selected
  image loading, search and console output. Do not substitute output counts for
  browser QA. Report any inaccessible checks honestly.
- Proportionate regression checks for shared navigation/layout changes; full
  website Node/Python suite, Markdown lint and `git diff --check`.
- Candidate and guarded release builds with independent output checks using
  matching prepared models. Baseline: 118 Node tests, 37 Python tests, 18 pages,
  52 files, 236 references. Counts may change for legitimate navigation reuse;
  preserve route/file allowlisting and candidate/noindex behavior.
- Use scoped Node 24.21.0 and documented Python runtime. No global-tool changes.

No journal/inventory writes, public copy changes, photo changes, contact
activation, dashboard work, new framework/dependency machinery, commit/push,
merge, hosting/deployment, archival, or successor dispatch is authorized.

## Return

Save `WK-WEB-T12-R01`, revision 1, to
`docs/website-workflow/reports/task-12-concept-b-shared-frame.md`: exact scope,
approval, source state, changed files, tests/browser evidence, preview URLs,
review comparison, preserved unrelated work, and remaining limitations.
Rename the child `Website 2 - Task 12 Shared Frame - READY FOR REVIEW` and report
once to the exact hub for reconciliation. The hub owns acceptance. Stop at the
stage boundary; do not start Task 13. If dispatch D01 was already applied,
report the current result rather than repeating the assignment.
