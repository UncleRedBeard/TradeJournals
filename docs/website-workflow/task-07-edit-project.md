# Website 1 - Task 07 Edit Project And Room Separation

Workflow status: COMPLETE — approved three-room revision applied locally
Approval: Shawn explicitly said `start task 07` in the hub on September 17, 2026,
after the proposed Edit Project and Room Separation scope and Dashboard handoff.
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` / website updates
Child: `01a0b143-f91d-7142-a68f-85898b4942f7`
Brief revision: 5 — authorized local publication reconciled
Dispatch: `WK-WEB-T07-D01`
Register: [task-register.md](task-register.md)

## Local Publication Checkpoint — September 19, 2026

After reviewing the Workbench controls, Shawn explicitly authorized save, build
and publish in the exact child. Report `WK-WEB-T07-R01` revision 2 records draft
`e9c88bf0-9413-4178-8c7e-b89a09d4a591`, revision 2, as `published`, with digest
`0c86af959f76454e490013e3896806c4d994fdcea3e341366ccbc6115a0c6ef8`.
The child verified completed save/preview/publish receipts with no recovery.

The hub reconciled this as `WK-WEB-T07-H03` at 16:03 UTC. The local canonical
website now has the three distinct room records, correct album ownership,
current/current/future occupancy and 5/5/3 selected photos. The old
`studio-restoration` project/story are unstaged tracked removals, recoverable
from Git. No deletion was performed by the hub during reconciliation.

Hub checks independently confirmed those records and passing output validation
for 8 pages/24 files. Journals, inventories and the candidate review snapshot
remain unchanged; the index is empty and archive HEAD remains `2846ffeb`.
Child reports post-publication 115 Node/37 Python tests and 5 focused assertions
passed, with 93 output references. Earlier browser/runtime limitations remain.

This local application supersedes the earlier unpublished checkpoint below.
There was no hosted deployment, reviewed-snapshot approval, Git closeout,
journal/inventory correction or successor dispatch.

## Earlier Delivery And Acceptance Checkpoint

Report `WK-WEB-T07-R01`, revision 1, was received and reconciled once under
`WK-WEB-T07-H01` at 2026-09-19 02:08 UTC (September 18 in America/Chicago).
The approved design and plan are linked in the
[report](reports/task-07-edit-project.md). They supersede the initial design-only
checkpoint below. The editor implementation is delivered; the proposed room
correction exists only as a private, previewed draft.

- Draft: `e9c88bf0-9413-4178-8c7e-b89a09d4a591`, revision 1.
- Digest: `0c86af959f76454e490013e3896806c4d994fdcea3e341366ccbc6115a0c6ef8`.
- Projects: Dedicated Office (current), Barre Studio — Current Room (current),
  Living Room Restoration — Future Barre Studio (future).
- Publish update was not used. Canonical room records, journals, inventories
  and reviewed snapshot remain unchanged; implementation is uncommitted.
- Child reports 115 website Node tests, 37 Python tests and 258 Companion tests
  passed; 24 Playwright skips and an omitted browser file remain explicit.
  Tests used Node 25.8.1; pinned Node 24.21.0 was unavailable.
- Hub checked report/spec/plan/audit, both Git states and protected content diffs,
  and independently reran canonical output validation: 6 pages/22 files pass.
  This is receipt reconciliation, not a new independent full code or UI review.

Shawn's final approval of the reviewed implementation and private three-room
preview was reported by the exact child on September 19 and reconciled as
`WK-WEB-T07-H02` at 15:33 UTC. COMPLETE title and idle runtime were verified.
Publication/canonical application, retirement of old project files, journal and
inventory corrections, reviewed snapshot changes, Git closeout and hosting
remain separately authorized actions. No new task is dispatched. The child now
reports both local review servers running; the hub did not alter their state.

## Role And Starting Point

You are the executing Task 07 child, not the hub. Begin actual context inspection
and design work; do not end with a promise to start. Do not create another child
or edit this brief or the central register. The hub owns coordination only.

The initial deliverable is a concrete, proportionate Edit Project design based
on the current implementation. Continue through its applicable design review
before implementation. The direction and room identities below are already
agreed; do not ask Shawn to approve them again. Material unresolved choices,
particularly draft isolation and Publish update semantics, need a concrete
recommendation grounded in the existing code.

Repositories, freshly clean at preparation:

- Archive: `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/TradeJournals`,
  `codex/website-updates`, `2846ffebd8c662732d859a630d73e1a3ac994ef9`.
- Companion: `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/tradejournals-companion`,
  `codex/website-workbench`, `31a6ec145582b85b2bf9064c5239f81254877f0c`.

The fork shares the archive directory. Only this child owns implementation work
for this assignment. Inspect applicable instructions, current branch/worktree,
permissions, serving checkout and concurrent edits in both repositories before
any change; do not switch branches or stop someone else's server.

## Confirmed Room Identities

Shawn confirmed three distinct physical rooms in Dashboard Launcher, then
corrected their current/future status directly in Task 07 on September 18.
This revision supersedes the earlier handoff and revision 1 wherever they call
the Flickr barre studio former/earlier or imply the living-room move has occurred.

| Source | Room identity |
| --- | --- |
| Flickr Home Reno - Office, `72177720316928566` | Dedicated Office Restoration; brief earlier yoga use is not a major story point |
| Flickr Home Reno - Studio \| Office, `72177720306207693` | CURRENT barre studio; originally Shawn's office/yoga room, now Haley's barre studio and The Repair Shop's current home |
| Google Photos Home Reno - Studio, `google_photos:af1qippool3ge7t` | Former living room being renovated as the FUTURE home of the barre studio / The Repair Shop; distinct from both rooms above |

Preserve current/future status until Shawn confirms the studio has officially
moved. Do not infer occupancy from renovation progress, album names or photo
dates, or rename projects based on the superseded wording. This correction
changes planning context only; no website or journal content has been corrected.

Names reflect changing use, not shared identity. The current
`ballet_barre_studio_restoration.md` journal and `studio-restoration` website ID
must be inspected against actual source identity before assigning a label or
proposing a correction. Do not repurpose either for the current Flickr studio merely
because its title sounds appropriate.

## Agreed Editing Flow

**Edit project → edit story, album assignments and photos → save draft → preview
→ explicit Publish update.**

- Open the existing website project's current story and photos in Workbench.
- Edit story, album assignments, selected photos, captions, alternative text
  and order. Group photos by source album so room identity remains visible.
- Draft and preview must not change the current published version. Define this
  against the actual local candidate/review/build architecture before promising
  what Publish update does. Hosting is deferred; no remote deployment mechanism
  or broad CMS is required or implicitly authorized.
- Explain the distinction between draft, selected website records, reviewed
  snapshot, generated output and eventual hosted page in the design. Keep the
  product flow simple; avoid exposing implementation bookkeeping unnecessarily.
- Correct the Office/current-barre-studio mash-up through this usable editing workflow,
  not solely through a one-off file repair. Identify how material moves to the
  proper project without losing sources or modifying original media.
- Website editing and journal correction are separate. Propose journal fixes as
  individually reviewable changes; do not silently rewrite journals or inventories.
- Album reassignment does not automatically establish which room owns every
  floor-refinishing, door-restoration, date or completion claim. Audit those
  claims and identify unsupported/conflicting statements explicitly.

## Read First And Inspect

Original handoff, retained at its source (current/future wording is superseded
by the September 18 correction above):
`/Users/shkelley/.codex/visualizations/2026/09/15/01a0a559-f8cd-7191-96b4-77f02e892589/WEBSITE_EDIT_PROJECT_HANDOFF.md`.
Source task: `Dashboard Launcher`, `01a0a559-f8cd-7191-96b4-77f02e892589`.

Read the current website maintainer guide, Workbench instructions, Task 06
report, Office review packets, and public architecture spec. Inspect both room
journals, Office and Studio project/story/media records, album inventory mappings,
`website/lib/workbench.mjs`, Companion `dashboard/website/`, its editor and
existing draft/review infrastructure. Verify actual UI before describing current
capabilities. Handoff observations and old reports are context, not live proof.

## Deliverables And Acceptance

1. A source-to-room and claim audit sufficient to bound the Office correction.
2. A small design and explicit publication semantics, with alternatives only
   where a real tradeoff exists. Include data ownership, draft persistence and
   isolation, source grouping, stale-edit handling, preview behavior and tests.
3. After concrete design approval, implement only that approved plan and prepare
   the Office correction for review through the editor. If this requires a new
   project record for the current Flickr barre studio, specify that in the design first.
4. Keep journal correction proposals separate and unapplied until individually
   approved. Preserve the currently accepted living-room Studio candidate.
5. Verify relevant behavior and record real results, including save/reopen,
   preview isolation, explicit update behavior, source/media identities and
   regression checks. Task 06's missing Playwright browser-suite dependency must
   not be represented as passing; distinguish manual UI verification accurately.

Use workflow-hub child procedure and the brainstorming skill for design, then
applicable implementation skills once the concrete design is approved. Explain
any skill-required review checkpoint by naming/linking its source and requirement.
No Git commit is authorized merely because a skill says to commit a design.

No publication, reviewed snapshot change, journal/inventory rewrite, media
deletion, Git closeout, main merge, hosting choice, new task or unrelated refactor
is authorized by this start instruction. Explicit later user direction can
authorize a concrete scoped action; record it without redundant approval.

## Return

Report `WK-WEB-T07-R01` at
`docs/website-workflow/reports/task-07-edit-project.md`. Clearly distinguish a
design ready for review from implemented functionality and applied corrections.
Report changed paths, checks, open decisions and actual Git state. Rename this
child READY FOR REVIEW when returning a reviewable deliverable, verify readback,
and report once to the exact hub for reconciliation. No automatic successor.
