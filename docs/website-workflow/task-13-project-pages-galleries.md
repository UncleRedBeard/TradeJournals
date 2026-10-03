# Website 2 - Task 13 Projects and Galleries

Workflow status: COMPLETE — hub technical review passed; Shawn's acceptance verified
Execution approval: RECEIVED directly in child; reconciled as `WK-WEB-T13-A01`
Brief revision: 1
Date: October 2, 2026
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` / website updates
Child: `01a0ff09-49a5-7cb2-a999-d7dbd073ecba`
Register: [task-register.md](task-register.md)

## Assignment

Extend the accepted Concept B Craftsman's Atelier style to individual project
pages and their galleries. Make the introduction, project details, photographs,
captions and link to the journal clear and comfortable to browse on desktop and
phones. Historic-home restoration and woodwork lead; other craft remains a
quieter supporting layer. Keep the result practical and understated.

Reuse the approved shared frame, typography and charcoal/brass/parchment palette.
Make small, maintainable template/component/style changes. Avoid adding a new
theme system, gallery framework, carousel, CMS or dependency without a concrete
need. Work & Craft is the approved navigation label, without a count.

### Scope

- Project route template `website/src/pages/work/[id].astro`.
- `ProjectGallery.astro`, `EvidenceDetails.astro` and narrowly scoped styling
  needed for project presentation. Inspect other consumers before changing a
  shared component; preserve their behavior and defer their redesign.
- Clear heading/intro hierarchy, readable details, balanced image sizing and
  spacing, captions and usable links to the original images/journal.
- Preserve selected images, order, captions, alt text, approved copy and evidence
  distinctions. Show portrait and landscape work without hiding relevant detail.

### Boundaries

Task 12's shared frame and homepage are accepted. Reuse them. Task 14 owns
TradeJournal reading pages and archive/search presentation; Task 15 owns final
integrated release review. No new content selection, source-journal/inventory
edits, contact activation, deployment, Git closeout, merge or archival here.

The former living room is the future barre studio; moving remains unconfirmed.
The current barre studio and Office are different rooms. Preserve approved
window and Office evidence wording. Keep inquiries disabled; invent no contact
destination. Do not refresh the reviewed snapshot to hide source drift.

## Environment And Dependencies

- Same-directory fork in
  `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/TradeJournals`.
- Branch `codex/concept-b-homepage`; observed HEAD
  `6c48930489851925eb837a2a89f22bb7cec8ccb5` (Kodakk evidence closeout).
- Accepted homepage commit `6a528e3`. Task 12 is COMPLETE and approved, but its
  implementation and hub records remain uncommitted in this checkout. Retain
  those changes as the starting point; do not reset or recreate them.
- A separate El Toro content-review child is active in the same directory.
  Preserve `docs/content-review-workflow/` and source journals/inventories;
  refresh status before edits and before reporting. Do not stage other work.
- Preview last observed at `http://127.0.0.1:8139/`, serving `.preview-dist`.
  Verify the server and output before using it as evidence.

## Read Before Starting

- [Task 12 brief](task-12-concept-b-shared-frame.md) and its
  [report, revision 3](reports/task-12-concept-b-shared-frame.md).
- `website/docs/concept-b-homepage-review.md`: approved direction; its older
  failure/status narrative is superseded by the parent closeout and Task 12.
- `website/README.md`, `website/docs/pilot-editorial-review.md`, current project
  content records, the project template and its components.
- `SiteLayout.astro`, `atelier-frame.css`, `tokens.css`, `atelier.css` and
  `AtelierProjectCard.astro` for existing visual conventions.
- Applicable repository instructions and workflow-hub, frontend-design and
  senior-developer skills. Reuse settled design decisions; routine details do
  not require reopening the approved whole-site direction.

## Deliverables And Verification

1. A consistent project-page and gallery presentation using existing content.
2. A working local preview with representative project links and screenshots
   showing desktop and phone layouts for user review.
3. Proportionate rendering/regression coverage for any changed behavior; run
   `npm run test:website`, `npm run check:website`, the guarded release build,
   `npm run lint:md` and `git diff --check` with the repository's scoped runtime.
   Read `website/README.md` for exact current commands.
4. Verify image loading, captions, full-image/journal links, keyboard focus and
   no horizontal overflow at narrow widths. Inspect portrait/landscape and
   shorter/longer project content. Confirm the accepted homepage/shared frame
   remains intact and room identities/inquiry controls remain correct.
5. Check each retained output against its matching prepared model; release and
   preview can differ. Report source-review drift separately if concurrent
   source work causes it; do not claim a gate passed if it did not.

Task 12's baseline checks passed: 119 Node and 37 Python tests; both outputs
contained 18 pages, 52 files and 270 checked references. These are prior evidence,
not a substitute for checks after Task 13. Avoid tests that merely mirror CSS.

## Approval And Return

Hub receipt `WK-WEB-T13-H01`, October 2, 2026: report `WK-WEB-T13-R01`,
revision 1 received. Hub reviewed the project template, component/test delta and
desktop/full-page/phone screenshots; no blocking issue found. Independently
reran 120 Node and 37 Python tests and checked both retained outputs against
matching models: 18 pages, 52 files, 302 references each. Both review states are
current with zero changed keys; snapshot hash remains unchanged. Detailed live
browser interactions and viewport checks are child-reported in the report.
Shawn's visual acceptance is pending. Task 14 has not started; changes remain
uncommitted. Concurrent source-review work remains with its owner.

Review: `http://127.0.0.1:8139/work/living-room-studio-restoration/`.

Hub acceptance `WK-WEB-T13-H02`, October 2, 2026: report `WK-WEB-T13-R01`,
revision 2 received. Verified Shawn's direct `approved` in child turn
`01a0ff24-8003-72c3-9b99-f87b22a20315` after delivery. No implementation changed
with this approval. Passed technical review plus user acceptance completes
Task 13. Earlier pending-acceptance statements above are historical. Task 14
and Git closeout remain separate; neither has been started by this receipt.

Shawn initially requested `handoff task 13` in the hub, preparing an idle fork.
On October 2, he then said `get started...but update the title to reflect status
as well` directly in the child, turn `01a0ff11-3c3e-7a13-844d-0ef34b67c21d`.
Hub verified that user message, the IN PROGRESS title and active execution.
Approval is recorded as `WK-WEB-T13-A01`; the child owns this implementation.
No duplicate dispatch was sent. Assignment scope remains revision 1.

After approval, refresh the workspace, implement this scope and return for
visual acceptance. Do not edit the hub register. Save report `WK-WEB-T13-R01`,
revision 1, to `docs/website-workflow/reports/task-13-project-pages-galleries.md`.
Record changes, checks, preview, remaining issues and concurrent work. Rename
the child `Website 2 - Task 13 Projects - READY FOR REVIEW` and
send the report to the exact hub for reconciliation only. No next stage starts
automatically. Keep all project material in this authorized workspace.
