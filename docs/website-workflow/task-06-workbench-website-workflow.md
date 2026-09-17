# Website 1 - Task 06 Workbench Website Workflow

Workflow status: COMPLETE — Workbench workflow and three-photo candidate accepted
Execution approval: RECEIVED directly in this child; Shawn said "start task 06"
on September 17, 2026. Child reported approval to the hub; active execution turn
`01a0b04f-7fc7-7a23-a020-bbb840bf0013` and IN PROGRESS title observed at 17:01 UTC.
Preparation approval: Shawn said "go ahead and get ready for task 06, but don't
start it immediately" in the hub on September 16, 2026.

Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` / website updates
Child: `01a0ac79-2d59-7101-b493-b08da38e407e`
Brief revision: 5 — scoped Git closeout authorization recorded
Reserved dispatch: `WK-WEB-T06-D01`; NOT SENT, superseded by direct child approval
Workspace: `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/TradeJournals`
Branch: `codex/website-updates`; same-directory fork
Preparation HEAD: `98fb1308c927bba6b5b4fd9aa05c63fbac7bc70b`
Register: [task-register.md](task-register.md)

## Explicit Git Closeout Authorization — September 17, 2026

After accepting the delivery, Shawn said `git er done` directly in this child.
The child reported the instruction to the hub, which recorded it at 20:20 UTC.
The child owns validation, scoped staging, commit, push and remote verification:

- TradeJournals: `codex/website-updates` to established
  `git@github.com:UncleRedBeard/TradeJournals.git`, same branch on `origin`.
- Companion: `codex/website-workbench` to established
  `git@github.com:UncleRedBeard/tradejournals-companion.git`, creating the matching
  remote development branch after checking its base and outgoing commits.

Include the accepted Task 05/06 bookkeeping with the applicable archive changes.
Preserve unrelated work and exclude private runtime configuration, credentials,
database and intake storage. Honor the existing scoped closeout checks and report
any unrun checks accurately. Verify remote commit identity, ahead/behind `0 0`
and worktree status after push before claiming synchronization.

This explicit instruction supersedes earlier commit/push exclusions for this
closeout only. It does not authorize force pushes, new remote destinations, a
main merge, publication, reviewed-release snapshot changes or another task.
Git closeout is IN PROGRESS, separate from the accepted COMPLETE task status.
The hub finishes these bookkeeping edits, then stops editing for child staging.
No post-closeout file edits by the hub absent another request; the child will
report the actual resulting commits and synchronization without a duplicate
hub Git operation.

## Delivery Checkpoint — September 17, 2026

Report `WK-WEB-T06-R01`, revision 2, is
[received by the hub](reports/task-06-workbench-website-workflow.md) under
`WK-WEB-T06-H02`, following revision 1 receipt under `WK-WEB-T06-H01`.
The child delivered the Workbench/launcher rename, Studio
authoring controls, explicit candidate save and loopback preview, with three
inspected photos acquired under subsequent direct user album instructions.
Shawn reviewed the working result and flow, then explicitly said `approved`
directly in the child. The hub reconciled acceptance as COMPLETE on September 17
at 20:17 UTC. The assignment below is retained as scope history, not a request
for further execution.

Hub receipt checks confirmed artifacts, both Git states, unchanged candidate
snapshot and passing output validation for six pages/22 files. This closeout
records Shawn's direct acceptance of the delivered local workflow and exact
three-photo candidate; it does not claim a new independent code audit.
The child reports 84 Node/37 Python website tests and 221 non-browser Companion
tests passing; existing browser suites require unavailable Playwright and remain
unrun. No commit, push, deployment or next task is authorized by this delivery.

## Objective

Use the existing private Dashboard as **TradeJournals Workbench**, with the
launcher label **Open TradeJournals Workbench**. Build on its actual capabilities
to support one practical workflow:

**Open Studio → select photos → arrange and caption → save candidate → preview website.**

These names are agreed; no launcher or application rename has been implemented
by preparing this task. The public website remains **Toil & Timber Restoration**.
Keep the tools modest, maintainable and centered on craftsmanship. Leave both
structured-file editing and browser editing viable through the same public records.

## First Step After Approval

Inspect the existing Dashboard before proposing implementation. Resolve its
actual application repository, current instructions, branch/worktree, launcher,
and serving checkout. The existing task `Dashboard Launcher`, ID
`01a0a559-f8cd-7191-96b4-77f02e892589`, is a discovery pointer, not proof of
current functionality. Do not send it a message or start another writer.

Compare observed support for project access, photo intake/selection, lead image,
gallery order, captions/alternative text, candidate saving and website preview.
Record what works, what is absent, and the smallest useful additions. Verify
behavior in the actual interface; configuration and historical notes alone do
not establish capability. No such audit has been performed during preparation.

If the implementation lives outside this checkout, establish its applicable
instructions, write permissions and safe development environment before edits.
Do not assume this branch isolates changes in another repository.

## Proposed Deliverables

1. A short capability assessment with observed evidence and a bounded plan for
   missing functionality. Reuse existing code and dependencies where practical.
2. The agreed Workbench and launcher labels at their verified, relevant locations,
   preserving distinction from the dashboard in Shawn's other project.
3. One working Studio authoring path covering selection, lead image, gallery
   order, captions/alternative text, candidate saving and local website preview.
   Add only the missing pieces justified by the assessment. Material expansion
   beyond this path requires a separate decision.
4. A reviewable Studio photo candidate with durable source identities and
   captions based on inspected images. Preserve the accepted text/layout and
   separate Office work. Record missing access or source evidence explicitly.
5. Concise maintenance instructions and a completion report with actual checks,
   changed paths, environment details and any unresolved review decisions.

This scope is now authorized by direct child approval. The capability assessment
may narrow the implementation needed; it does not authorize broader work.

## Dependencies And Evidence

Task 05's Studio text/layout and Toil & Timber branding are accepted. Studio
currently has no selected photos; the Office project's ten photos are distinct
and must not be substituted. The complete website review snapshot remains
candidate. Task 05's Git closeout does not authorize Task 06 Git operations.

Read after execution approval:

- [Approved architecture](../superpowers/specs/2026-09-15-worth-keeping-website-design.md),
  especially its Dashboard and public-content boundaries
- [Website maintainer guide](../../website/README.md)
- [Studio review packet](../../website/docs/pilot-editorial-review.md)
- [Task 05 report](reports/task-05-pilot-content-review.md)
- `website/content/projects/studio-restoration.json` and
  `website/content/stories/studio-restoration.md`
- Source journal
  `01_the_residence_1894/trade_journals/ballet_barre_studio_restoration.md`
- `GOOGLE_PHOTOS_ALBUMS.md#album-af1qippool3ge7t`; source album key
  `google_photos:af1qippool3ge7t`

The Studio source is distinct from Flickr's Home Reno - Studio | Office.
Preserve original journal facts and identity. A dated near-completion record
does not establish final sign-off or an installed barre.

## Boundaries And Acceptance

- Private drafts and intake remain private. Promotion into public media and
  selection for the public project are deliberate, reviewable operations.
- The Astro build consumes the existing public structured records. It must not
  read the private Dashboard database or managed media store, or require a
  running Workbench to build the website.
- Saving a candidate does not mark it reviewed, publish it or deploy it. Keep
  `website/content/reviews/pilot.json` candidate pending explicit final approval.
- Preserve original journals, inventories, source photos, the old prototype and
  Office candidate. No broad archive import or migration.
- No hosting choice, contact feature, full CMS, unrelated dashboard changes,
  commit, push, deployment, or successor-task dispatch.
- Verify the complete local authoring path in the actual UI and the resulting
  Astro preview. Check selected image identity, saved ordering/captions and
  private-data exclusion. Run proportionate tests for any new behavior plus
  affected application/website checks, output validation, lint and whitespace.
- Only one implementation writer at a time. Refresh live Git state and preserve
  the hub's preparation files and Task 05 acceptance documentation.

## Approval And Return

The preparation-only hold was superseded by Shawn's direct "start task 06"
instruction in this exact child on September 17. The child confirmed reading
revision 1 before beginning. Continue the approved capability assessment and
bounded implementation in that existing turn; no duplicate hub dispatch is
needed. Git closeout, publication and final editorial approval remain excluded.

After approval, apply workflow-hub child procedure and relevant application
skills. Do not edit the central register or fork further user-visible tasks.
Save report `WK-WEB-T06-R01` at
`docs/website-workflow/reports/task-06-workbench-website-workflow.md`, rename
the child READY FOR REVIEW, and report once to the exact hub for reconciliation.
The hub owns acceptance. Completion does not start another task.
