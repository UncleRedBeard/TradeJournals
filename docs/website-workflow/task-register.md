# Website Updates — Workflow Register

Hub title: website updates
Hub thread ID: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`
Workspace: `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/TradeJournals`
Branch: `codex/concept-b-homepage` (Concept B continuation); `main` retains the prior approved release
Register owner: hub only
Master plan: [Astro pilot implementation](../superpowers/plans/2026-09-15-worth-keeping-astro-pilot.md)
Design: [Approved architecture](../superpowers/specs/2026-09-15-worth-keeping-website-design.md)

Current checkpoint: October 3, 2026. Tasks 12-17 are accepted COMPLETE.
Tasks 12-14 implementation is committed and pushed through `ef1d5e8` on
`codex/concept-b-homepage`; the 11 previously approved completed chats were
archived. Task 15 verified the integrated release and fresh-checkout reproduction;
Shawn approved directly in its child and the hub reconciled that acceptance.
Task 15 documentation and hub bookkeeping were committed and pushed at
`f20572a`; post-push HEAD/tracking/FETCH_HEAD matched with `0 0` and a clean
checkout. Task 16 dependency maintenance is accepted COMPLETE after Shawn said
`accepted` in this hub on October 3, 2026. The verified devalue patch leaves two
high website package findings for one unresolved upstream cache issue, plus
seven high and one moderate findings in separate Markdown tooling. These remain
follow-up; acceptance is not a clean-audit claim. Task 16 changes were committed and pushed at `2d566f0`, with verified
`0 0`. Task 17 Markdown tooling is accepted; scoped Git closeout is authorized.
Independent content-review work advanced HEAD to `715b2a1` without website
changes. Hosting/domain, Git integration, deployment and inquiry activation
remain separate. Earlier checkpoints below are historical.

Integration checkpoint: September 20, 2026. Shawn approved the hub's recommended
flow to update clone instructions, fast-forward the completed website work into
`main`, validate, and push `main`. Local `main` was fast-forwarded from `e16be25`
to `e4fa233` without conflicts, preserving all 16 website commits. The development
branch is retained. Use `main` as the current baseline; the shared-checkout branch
instructions and execution states below describe their historical task contexts.
This integration does not deploy the site or start another implementation task.

Task 11 closeout checkpoint: September 20, 2026. Task 10 Portfolio Expansion is accepted
and committed through `d28f030`; the checkout was clean before Task 11 preparation,
with HEAD matching the local tracking ref and ahead/behind `0 0`. Task 11 Expanded
Release Readiness is accepted COMPLETE: the expanded reviewed snapshot is
current and the portable release is verified. Shawn chose to keep inquiries
disabled. Task 11 implementation is committed and pushed at `46293aa`; hub
observed matching HEAD/tracking/FETCH_HEAD, `0 0`, and a clean checkout before
this final bookkeeping update. The child owns its bookkeeping commit/push.
Hosting and deployment remain separate. Earlier states below are historical.

## Operating Boundary

Shawn approved the written plan and asked this hub to get started using the
workflow-hub skill on September 15, 2026. Apply that start instruction to
Task 01. Later tasks retain their plan approval; record their task-specific
dispatch approval before starting them. Completion of one child alone never
starts another. The original implementation scope excluded Git closeout;
Task 05's later explicit commit/push authorization is recorded below. Deployment
and private Dashboard implementation remain outside current execution scope.
Task 06 received direct child approval on September 17 and delivered its bounded
Workbench candidate, accepted by Shawn directly in the child. Shawn subsequently
authorized scoped Git closeout in both repositories, recorded under Task 06.
Reviewed-release snapshot changes and publication remain outside that approval.

Only one website child writes implementation files at a time. Children share
this checkout to retain the approved uncommitted design and plan. The hub owns
this register and task briefs; children own code within their assignment and
their completion reports. Preserve other tasks' work and do not switch branches.

## Website 1 — Task 01 Content Foundation

- Exact child ID: `01a0a5ea-afed-7e92-9938-25b57c1e5b4a`.
- Exact displayed title: Website 1 - Task 01 Content Foundation - COMPLETE.
- Environment: same directory; branch `codex/website-updates`; base `e16be25`.
- Brief: [Task 01, revision 1](task-01-content-foundation.md).
- Dependencies: approved design and plan, both present.
- Deliverable: validated records, source inspection, review comparison, prepared
  public model, supported scoped runtime, and focused tests (plan Task 1).
- Acceptance: required baseline and Task 1 tests pass; original archive and
  prototype are preserved; no public content is automatically marked reviewed.
- Workflow status: COMPLETE (accepted by hub).
- Runtime state: implementation turn `01a0a7ef-4ab8-7303-8edf-6709ce2dc077`
  completed; idle state observed with COMPLETE title on 2026-09-16 at 02:07 UTC.
  Hub then sent a reporting-only receipt acknowledgement; no further coding
  or acknowledgement loop was requested.
- Approval: RECEIVED in this hub; Shawn approved the plan, then said "then get
  started and make sure to use the workflow-hub skill too."
- Approval scope: create and execute the first bounded implementation child.
- Dispatch ID: `WK-WEB-T01-D01`; state SENT. Messaging returned the exact child
  ID and subsequent wait/read observed its new active execution turn.
- Latest report: `WK-WEB-T01-R01`, revision 1,
  [completion report](reports/task-01-content-foundation.md).
- Report delivery: RECEIVED by exact hub; reconciled once as `WK-WEB-T01-H01`.
- Findings/blockers: shared checkout had returned to `main`. Hub restored
  `codex/website-updates` at the identical `e16be25` commit on 2026-09-16 at
  02:00 UTC; all 18 preexisting modified/untracked files verified byte-identical.
  Branch blocker resolved. Dependency Markdown lint issue resolved with narrow
  generated/dependency ignores; authored website Markdown remains checked.
- Hub review: ACCEPTED on 2026-09-16 at 02:06 UTC (September 15 local time).
  Hub read all four foundation modules and the Python inspector; independently
  reran 41 website tests, 74 Python tests, existing evidence/search checks,
  Markdown lint (50 files), and tracked/untracked whitespace checks: all pass.
  Scoped Node is 24.21.0; global Node remains 25.8.1. Tracked diff is only the
  expected `.gitignore` addition; original archive and prototype remain unchanged.
  New implementation files are within Task 01 scope. No real content or pages
  have been created. Changes remain uncommitted at `e16be25`.
- Final title/register agreement: COMPLETE title freshly read back after hub
  rename on 2026-09-16 at 02:07 UTC; register records the same accepted status.

## Website 1 — Task 02 Office Content

- Exact child ID: `01a0aa51-2176-75d2-8064-7a89390069c2`.
- Exact displayed title: Website 1 - Task 02 Office Content - COMPLETE.
- Environment: same directory; branch `codex/website-updates`; base `e16be25`.
- Brief: [Task 02, revision 1](task-02-office-content.md).
- Dependencies: Task 01 accepted; its implementation is present and uncommitted.
- Deliverable: Office project/story, ten media records, site/home/service records,
  candidate review snapshot, reconciliation worksheet, and migration tests.
- Acceptance: preserve original source identities and page/search distinctions;
  visually inspect selected assets; validate records/preparation; retain candidate
  status; original journal, inventories, assets, and prototype unchanged.
- Workflow status: COMPLETE (hub-recovered and accepted).
- Runtime state: idle; exact COMPLETE title and idle state freshly verified
  on September 16, 2026, 14:48 UTC. Hub recovery history is retained below.
- Approval: RECEIVED; exact current user instruction in this hub: "start task 02".
- Approval scope: create and execute plan Task 2; no Task 3, commit, push, or launch.
- Dispatch ID: `WK-WEB-T02-D01`; state SENT once. Subsequent wait/read confirmed
  active execution on the exact child and expected workspace.
- Latest report: `WK-WEB-T02-R01`, revision 1,
  [completion report](reports/task-02-office-content.md).
- Report delivery: hub-authored recovery report; received locally and reconciled
  as `WK-WEB-T02-H01`.
- Findings/blockers: original child did not produce artifacts while repeatedly
  active. Per Shawn's resume-and-finish instruction, hub paused it and completed
  Task 02 directly. No source or branch blocker remained.
- Hub review: ACCEPTED after direct implementation review and fresh verification:
  44 website tests, 74 Python tests, legacy evidence/site checks, 53-file Markdown
  lint, tracked/untracked whitespace checks, release-candidate rejection, and
  original-source preservation checks all passed. Candidate editorial review remains
  separate and is recorded in `website/docs/office-content-review.md`.
- Final title/register agreement: COMPLETE title and idle runtime read back
  on 2026-09-16 at 14:48 UTC. The earlier stale active indicator has resolved.

## Website 1 — Task 03 Astro Pages

- Exact child ID: `01a0aab2-36e1-78f3-8cff-20a2937e5ccc`.
- Exact displayed title: Website 1 - Task 03 Astro Pages - COMPLETE.
- Environment: same directory; `codex/website-updates`; base `505d34e`.
- Brief: [Task 03, revision 1](task-03-astro-pages.md).
- Dependencies: accepted Tasks 01 and 02 are present; editorial content stays
  candidate while the local pages are built for review.
- Deliverable: reusable Astro layout/components, pilot routes, safe Markdown,
  optional archive search, preview/release build orchestration and focused tests.
- Acceptance: local candidate preview builds and displays the prepared records;
  exact identity and original media links survive; core reading is server-rendered;
  search fails gracefully; release still rejects unreviewed content.
- Workflow status: COMPLETE (hub direct recovery).
- Runtime state: child paused after its dispatched turn ended with no implementation
  artifacts. Hub took over the exact approved Task 03 scope on September 16,
  2026 at 15:00 UTC; safe-Markdown tests and the first Astro preview build now
  have observed passing results. Child title was changed to PAUSED to prevent
  concurrent writers. The hub's active work, not the child title, is authoritative.
- Approval: RECEIVED; Shawn said "ok, let's get started on task 03" in this hub.
- Approval scope: create and execute plan Task 3; no Task 4 dispatch or publication.
- Dispatch ID: `WK-WEB-T03-D01`; state SENT once. Subsequent wait/read confirmed
  active execution on the exact child and expected workspace.
- Latest report: [Task 03 Astro Pages](reports/task-03-astro-pages.md).
- Report delivery: stored in the repository; no external message or task handoff.
- Findings/blockers: the original child dispatch completed without Astro files.
  This is a workflow execution failure, not a source, dependency, or branch
  blocker. Hub recovery is implementing the same user-approved task directly.
- Hub review: 50 focused website tests passed; the existing evidence and search
  suites passed; release correctly refused candidate content. Browser review
  confirmed the home, project, archive search, and mobile project layout with
  no console errors.
- Final task/register agreement: Task 03 is COMPLETE through direct hub work.
  The child is now titled COMPLETE and idle, freshly read back during Task 04
  on September 16, 2026. Direct hub recovery remains the recorded authorship.

## Website 1 — Task 04 Pilot Verification

- Exact child ID: `01a0ab24-db71-75a0-b2d8-d4280528a596`.
- Exact displayed title: Website 1 - Task 04 Pilot Verification - COMPLETE.
- Environment: same directory; `codex/website-updates`; base `7d023b9`.
- Brief: [Task 04, revision 1](task-04-pilot-verification.md).
- Dependencies: accepted pilot committed at
  `7d023b9f06781bdf082acaa2e0c6fc15fbf1479e`; checkout clean before preparation.
- Deliverable: output checker, regression and maintenance tests, build integration,
  browser acceptance checks, and maintenance/preview documentation.
- Workflow status: COMPLETE (accepted by hub).
- Runtime state: child resumed on a direct user follow-up after initial hub
  recovery. That turn has completed and child is idle. The hub owns final review.
- Approval: RECEIVED; Shawn's exact instruction in this hub: "start task 04".
- Approval scope: plan Task 4; no publication, Git closeout, or next task.
- Dispatch ID: `WK-WEB-T04-D01`; SENT once.
- Latest report: `WK-WEB-T04-R01`, revision 2,
  [completion report](reports/task-04-pilot-verification.md).
- Report delivery: RECEIVED locally; revision 2 incorporates hub verification.
- Recovery: child initially ended without code, so hub began approved work.
  When the child resumed, hub stopped overlapping edits and owned browser tests.
  After the child finished, hub reviewed its draft and closed anchor/source-link,
  preview-metadata, hero-selection, and maintenance-test gaps. Internal helper
  supplied the Python HTML parser; independent code review found no remaining Important or Critical issues after fixes.
- Verification: 79 website tests, 84 full Python tests, existing evidence/search
  checks, and a 4-page/17-file/60-reference preview build pass. Actual synthetic
  reviewed release builds; real candidate release rejects. Browser checks include
  desktop/mobile, keyboard skip/focus, script-blocked reading, and search HTTP 503.
- Acceptance: ACCEPTED on September 16, 2026, at 21:47 UTC. Independent review,
  59-file Markdown lint, and tracked/untracked whitespace checks pass. Browser
  preview was reloaded after the final build; no console errors or warnings
  were captured. Final COMPLETE title readback is recorded below.
  No editorial approval is implied.

## Website 1 — Task 05 Pilot Content Review

- Exact child ID: `01a0ac3f-68fd-7771-a652-b16281312adf`.
- Exact displayed title: Website 1 - Task 05 Studio - COMPLETE.
- Environment: same directory; `codex/website-updates`; base `1faa53d`.
- Brief: [Task 05, revision 5](task-05-pilot-content-review.md).
- Initial approval: RECEIVED; Shawn said "start task 05" after the hub proposed
  a focused pilot content and visual review.
- Scope change: direct instruction in this exact child: "i like the direction
  your going with this, but i think the best first candidate is the
  `Home Reno - Studio`". Hub verified the current user-message preview.
- Current scope: feature the distinct Studio / ballet barre project, preserving
  the approved visual direction and Office candidate work. Validate the Studio
  identity and evidence against its local journal, inventory and existing assets.
  Do not conflate Home Reno - Studio with Home Reno - Studio | Office.
- Boundaries: full photo candidate approval and saved reviewed snapshot remain pending.
  No wider archive migration, hosting, contact implementation or publication.
  Scoped Git closeout is now separately authorized as recorded below.
- Workflow status: COMPLETE for accepted Studio text/layout and branding;
  photo curation and approval of the populated candidate are deferred follow-up.
- Runtime state: idle; exact COMPLETE title freshly observed after acceptance
  reconciliation on September 16, 2026. Implementation and Git closeout finished.
- Original dispatch: `WK-WEB-T05-D01`; SENT once. No second dispatch: direct
  child approval authorizes this bounded revision.
- Latest received report: `WK-WEB-T05-R01`, revision 3, at
  `reports/task-05-pilot-content-review.md`; Studio-first candidate with approved
  Toil & Timber Restoration branding. Office packet retained separately.
- Report delivery: revision 1 reconciled as `WK-WEB-T05-H01`; revision 2
  RECEIVED once and reconciled as `WK-WEB-T05-H02`; revision 3 RECEIVED once
  and reconciled as `WK-WEB-T05-H03`.
- Prior hub review: Office draft passed 79 website tests, output validation
  (4 pages/17 files), 62-file Markdown lint and whitespace checks; source and
  rendered-content review completed. Those results are historical and do not
  establish acceptance of the upcoming Studio revision.
- Office questions: room-history confirmation and image 7 selection are deferred
  with the retained Office candidate, not blockers for the Studio-first review.
- Current hub review: read Studio records/story and actual component/test changes,
  checked source-journal support, independently reran 80 website and 37 focused
  Python tests, output validation (6 pages/19 files), 64-file Markdown lint and
  tracked whitespace checks. Inspected the rendered Studio page. Original source
  files, prototype, inventories and saved candidate snapshot have no diff.
- Remaining work: select and bring in actual Studio photographs with durable
  source identities, then choose the lead/gallery, write inspected captions and
  alternatives, and review the populated pages. Studio currently has zero selected
  images; no Office photos are substituted. This is not completed visual curation.
- Acceptance: RECEIVED; exact child reports Shawn's direct `approved` after
  delivery of the Studio text/layout candidate and branding. Its report and
  editorial packet record that bounded acceptance. Hub reconciled this as
  `WK-WEB-T05-H04`. Photos and the complete reviewed snapshot remain pending.
- Git checkpoint before closeout: uncommitted Task 05 changes on
  `codex/website-updates`, HEAD `1faa53d`.
- Git authorization: RECEIVED; Shawn said `git er done` directly in the child,
  which reported that instruction to the hub at 22:51 UTC. The child owns scoped
  validation, staging, commit, push to established `origin/codex/website-updates`,
  and synchronization verification. No force push or new destination is authorized.
- Git closeout status: COMPLETE at `98fb1308c927bba6b5b4fd9aa05c63fbac7bc70b`;
  child reported fetch, matching origin branch, `0 0` and clean worktree after
  push; hub previously verified. HEAD and tracking ref match again at this
  preparation checkpoint. Subsequent acceptance/preparation docs are uncommitted.
- Editorial boundary: Git closeout does not approve Studio photographs, mark the
  candidate reviewed, authorize publication, or dispatch a successor.
- Single writer: child owns website changes; hub edits only brief/register.

- Branding: Shawn directly requested Toil & Timber Restoration in the child.
  Hub verified site/package/test changes, the name on all six generated pages,
  absence of the former name in that output, and the live Studio title/header/footer.
  The child reports 80 website tests rerun for the rename. Current brief updated;
  historical reports retained. This is not editorial or publication approval.

## Website 1 — Task 06 Workbench Website Workflow

- Exact child ID: `01a0ac79-2d59-7101-b493-b08da38e407e`.
- Exact displayed title: Website 1 - Task 06 Workbench - COMPLETE.
- Environment: same-directory fork of this hub; `codex/website-updates`;
  preparation HEAD `98fb1308c927bba6b5b4fd9aa05c63fbac7bc70b`.
- Brief: [Task 06, revision 5](task-06-workbench-website-workflow.md).
- Preparation approval: Shawn said "go ahead and get ready for task 06, but
  don't start it immediately" in this hub.
- Execution approval: RECEIVED directly in the exact child; it reports Shawn
  said "start task 06" on September 17. Workflow status: COMPLETE.
- Runtime state: Git closeout turn `01a0b105-bb6e-76f2-a2c6-372d4cff371b`
  observed active at 20:20 UTC on September 17. Exact COMPLETE title remains
  appropriate for the accepted delivery; Git closeout status is separate.
- Reserved dispatch: `WK-WEB-T06-D01`; NOT SENT, superseded by direct child
  approval. No duplicate execution message or second writer started by the hub.
- Dependencies: accepted Studio text/layout and branding retained; child assessed
  existing Dashboard capability and delivered a three-photo Studio candidate.
- Agreed private tool name: TradeJournals Workbench; launcher label:
  Open TradeJournals Workbench. Child reports both implemented and launcher tested.
- Delivered scope: reused private intake; Studio selection, lead/gallery order,
  captions/alt, explicit promotion, candidate saving and loopback preview.
  Shared-album intake was separately directed by Shawn in the child, per report.
- Acceptance criteria: observed end-to-end local UI and preview behavior, source
  identity and privacy boundaries preserved, proportionate checks. No commit,
  push, hosting, deployment or broader CMS.
- Report: `WK-WEB-T06-R01`, revision 2, at
  [Task 06 report](reports/task-06-workbench-website-workflow.md); RECEIVED once
  and reconciled as `WK-WEB-T06-H02` on September 17 at 20:17 UTC. Revision 1
  receipt remains recorded under `WK-WEB-T06-H01`.
- Hub receipt checks: read report, maintenance guide and photo packet; inspected
  changed paths and both repositories' branch/HEAD state. Independently reran
  output validation: 6 pages/22 files pass. Source journals/inventories, Office
  project and saved candidate review state have no diff. This is receipt review,
  not completed independent implementation or visual acceptance.
- Child verification: 84 website Node tests, 37 Python tests and 221 Companion
  non-browser tests reported passing. UI save/build and restart/reopen reported
  verified. Existing Companion browser suites remain unrun because Playwright
  is unavailable; initial all-suite load failure is explicitly retained.
- Pre-closeout Git: archive remains `98fb1308` on `codex/website-updates`; Companion
  remains `99bddb4` on `codex/website-workbench`. Both have uncommitted changes.
- Acceptance: COMPLETE for the delivered local Workbench workflow and exact
  three-photo Studio candidate. Child reports Shawn reviewed the result and
  easier/more intuitive flow, then explicitly said `approved`; report revision 2
  and the editorial packet record that direct acceptance. Hub reconciles the
  accepted scope without claiming a new independent code audit or passing the
  unavailable browser suites. Reviewed-release snapshot, Git closeout and
  publication remain separate; no new task is authorized.
- Git closeout authorization: RECEIVED; child reports Shawn's direct `git er done`
  after acceptance. Task 06 child owns validation, scoped staging/commit/push,
  and fresh remote/hash/`0 0`/worktree verification in both repositories.
- Authorized destinations, freshly inspected: archive
  `git@github.com:UncleRedBeard/TradeJournals.git`, `codex/website-updates`;
  Companion `git@github.com:UncleRedBeard/tradejournals-companion.git`,
  `codex/website-workbench` as a matching new development branch on existing origin.
- Payload includes accepted Task 05/06 bookkeeping and scoped implementation;
  unrelated work and private runtime data remain excluded. No force push, main
  merge, publication, reviewed-release snapshot change or next task.
- Git closeout status: IN PROGRESS. Resulting commits and synchronization are
  not yet claimed. Hub bookkeeping is ready for child staging; the hub stops
  file edits now and will make no post-closeout file edits absent another request.
- Execution owner: existing child, which confirmed reading brief revision 1
  before beginning assessment. Hub reconciles approval and records only.

## Website 1 — Task 07 Edit Project And Room Separation

- Exact child ID: `01a0b143-f91d-7142-a68f-85898b4942f7`.
- Exact displayed title: Website 1 - Task 07 Edit Project - COMPLETE.
- Brief: [Task 07, revision 6](task-07-edit-project.md).
- Approval: RECEIVED; Shawn said `start task 07` in this hub on September 17,
  following the Dashboard Launcher handoff and proposed design-first scope.
- Workflow status: COMPLETE — editor approved and three-room correction applied
  locally under later explicit save/build/publish authorization. Runtime:
  publication/reporting turn `01a0ba61-2a1e-74d0-ba77-b1f1b296ae67` active at
  receipt; exact COMPLETE title read back September 19 at 16:03 UTC.
- Dispatch: `WK-WEB-T07-D01`; SENT once after idle fork verification.
- Environment: same-directory archive fork, `codex/website-updates` at
  `2846ffebd8c662732d859a630d73e1a3ac994ef9`; Companion remains
  `codex/website-workbench` at `31a6ec145582b85b2bf9064c5239f81254877f0c`.
  Both clean before this task's preparation. No parallel implementation writer.
- Dependency checkpoint: Task 06 closeout `WK-WEB-T06-G02` reported both commits
  pushed, fresh matching remote hashes, `0 0`, clean worktrees; final outcome was
  acknowledged in conversation without post-closeout edits. Its IN PROGRESS Git
  entry above is the committed pre-push history, superseded by that result.
- Objective: Edit Project for website story/album/photo corrections, isolated
  drafts and previews, then an explicit Publish update operation with locally
  defined semantics. Office/current-barre-studio mix-up is the first case.
- Confirmed source identities: Flickr `72177720316928566` = dedicated Office;
  Flickr `72177720306207693` = CURRENT barre studio / The Repair Shop's current
  home; Google `af1qippool3ge7t` = former living room / FUTURE home of the studio.
- Correction authority: Shawn clarified current/future status directly in exact
  Task 07 child on September 18; child reported it for hub reconciliation.
  Brief revision 2 supersedes contradictory handoff/revision 1 language. No move
  is assumed until explicitly confirmed; no project rename or content edit is
  authorized merely by this planning reconciliation. No new dispatch sent.
- Design/implementation authority: report links the approved September 18
  editor spec and plan, now present. Implementation followed that design review.
- Boundaries: local canonical application separately authorized; journal and
  inventory corrections still separate, original media preserved; no hosted
  deployment, reviewed snapshot change, main merge or successor. Subsequent
  explicit Git closeout authorization is recorded below.
- Report: `WK-WEB-T07-R01`, revision 3,
  [Task 07 report](reports/task-07-edit-project.md); RECEIVED once and reconciled
  as `WK-WEB-T07-G01` September 19 at 16:13 UTC. Revision 2 publication receipt
  remains H03; revision 1 receipt/acceptance remain H01/H02.
- Final acceptance: exact child reports Shawn approved the reviewed implementation
  and private three-room preview on September 19. Hub reconciled R01 as approved
  and COMPLETE under `WK-WEB-T07-H02`; no new independent code audit is claimed.
- Delivered: multi-project editing, private immutable draft revisions, isolated
  preview, explicit local Publish update and recovery controls. Room correction
  draft `e9c88bf0-9413-4178-8c7e-b89a09d4a591`, revision 2, is published with
  digest `0c86af959f76454e490013e3896806c4d994fdcea3e341366ccbc6115a0c6ef8`.
- Canonical room correction: APPLIED LOCALLY. Dedicated Office (5 photos), current
  barre studio (5), future living-room studio (3) have separate records and album
  ownership. Child reports Shawn explicitly authorized save, build and publish;
  completed receipts and no recovery were verified by the child. Old
  `studio-restoration` replacement/removals were included in the subsequent
  authorized Git closeout. No deletion or publication performed by the hub.
- Child verification: 115 website Node, 37 Python and 258 Companion tests passed;
  24 explicit Playwright skips and omitted `media-ui.test.mjs` retained. Node
  25.8.1 used because pinned 24.21.0 was unavailable. Child reports final full
  re-review with no Critical/Important findings. Earlier server-shutdown report
  is superseded: child now reports both local review servers running. The hub
  has not independently rechecked or changed their state.
- Hub receipt verification: read report/spec/plan/source audit; inspected both
  branches and changed paths; canonical content/journal/inventory diff empty;
  independently reran output validation (6 pages/22 files) and both whitespace
  checks successfully. User acceptance is now recorded; the hub has not performed
  a new independent full code or UI review during acceptance reconciliation.
- Git authorization: child reports Shawn's explicit `git er done` followed by
  task-scoped `we die like men!` deletion response. Applies to approved Task 07
  implementation, room correction and associated bookkeeping in both repos.
- Implementation closeout: TradeJournals
  `ec61ca9e3ae605f8b969c38674bdd6456d40de46`, `origin/codex/website-updates`;
  Companion `c4a2338584e0137c0a9685a7c964255dee6413af`,
  `origin/codex/website-workbench`. Child verified post-push fetch, exact remote
  hashes, `0 0` and clean status. Hub independently read matching HEAD/tracking
  hashes and `0 0` at 16:13 UTC; Companion clean, archive report revision 3
  modified before hub reconciliation.
- Final bookkeeping closeout: PENDING with child. Report revision 3 plus hub
  brief/register updates follow the implementation commit; do not describe the
  archive as clean until child includes and verifies these changes. Hub stops
  editing after this handback; no competing Git operations.
- Post-publication hub checks: correct three-room records/album/occupancy mapping
  and 5/5/3 selections observed; output validation passes 8 pages/24 files; no
  journal/inventory/review-state diff, no staged changes, archive HEAD unchanged.
  Child reports 115 Node/37 Python tests and focused 5/5 passed, plus canonical
  build with 93 references. These supersede the earlier unchanged-content and
  6-page preview observations; prior browser/runtime limits still apply.
- Hub owns brief/register; child owns its bounded deliverable and report.

## Website 1 — Task 08 Release Readiness

- Exact child ID: `01a0bbcf-a52f-7672-b08e-d69da400c4d7`.
- Exact displayed title: Website 1 - Task 08 Release Readiness - COMPLETE.
- Brief: [Task 08, revision 3](task-08-release-readiness.md).
- Approval: RECEIVED; Shawn said `let's start task 08` in this hub on September
  19, following the release-readiness and portability review.
- Scope: current maintainer instructions, consistent scoped runtime, fresh-checkout
  build proof, outstanding browser verification, contact decision and reviewable
  public release package. This supersedes any tentative Hosting And Launch label.
- Boundaries: no deployment, hosting/domain setup, main merge, journal/inventory
  correction or successor. Original execution excluded Git closeout; subsequent
  child closeout is recorded below. Exact reviewed-snapshot promotion was
  separately approved by Shawn in the child, as recorded in its report.
- Environment: same-directory archive fork on `codex/website-updates`, baseline
  `dd6da4c`; Companion on `codex/website-workbench`, baseline `c4a2338`.
  This child is the sole Task 08 implementation writer.
- Dependency checkpoint: Task 07 accepted and its three-room correction applied
  locally. Final bookkeeping is now committed, superseding the historical
  pending checkpoint above. Candidate review state remains unchanged.
- Workflow status: COMPLETE — accepted release-readiness delivery. Runtime at
  receipt remained active in reporting turn `01a0bc3f-6790-7be1-992f-a39c86b4b8d7`;
  runtime state is separate from accepted delivery status. Final readback confirmed
  the exact COMPLETE title and idle runtime after hub reconciliation.
- Dispatch: `WK-WEB-T08-D01`; SENT once September 19 at 22:37 UTC.
- Acceptance: follow one current guide from fresh checkout to verified public
  release output; distinguish unresolved approval/checks from proven readiness.
  Actual upload remains deferred.
- Report: `WK-WEB-T08-R01`, revision 2, at
  [Task 08 report](reports/task-08-release-readiness.md); RECEIVED once and
  reconciled as `WK-WEB-T08-H01` September 20 at 00:47 UTC.
- Approval evidence: exact child reports Shawn approved the disabled email
  placeholder and snapshot digest
  `ab0a82cd6e9492800f5e2a8b885aee4038d9e96a01cc1f55221b0cd59ed24fce`.
  Hub verified the saved digest and current review with zero changed keys.
- Hub verification: implementation/guide/packet diff review, scoped Node 24.21.0
  suite 116 passed, Python suite 37 passed, independent release output check
  eight pages/24 files/93 references passed. An initial hub CLI check used an
  incorrect duplicated website path; corrected direct output validation passed.
- Child evidence: clean clone at baseline `dd6da4c` installed scoped runtime and
  locked dependencies, passing baseline candidate checks; final approved release
  passed in the working checkout. Desktop and 390-pixel public browser checks
  reported passing. Hub did not repeat clone/browser checks. Private Companion
  browser skips remain explicitly separate from the public static-site gate.
- Git closeout: implementation/report commit
  `ac151076c3d982a20c5da8d49fc708a3a9caf0ba` (`Prepare verified website release`)
  pushed to `origin/codex/website-updates`. Child reports post-push fetch with
  matching hashes, `0 0` and clean status. Hub independently observed matching
  HEAD/tracking ref, `0 0`, clean status and scoped commit files at 00:55 UTC.
  Reconciled once as `WK-WEB-T08-G01`; supersedes the prior uncommitted state.
- Final bookkeeping: these brief/register edits return to the child for its
  final commit/push and synchronization verification. Pending; hub stops edits
  after handback. No hosting/deployment or successor action occurred.
- Hub owns brief/register; child owns implementation and its report.

## Website 1 — Task 09 Content Review And Selection

- Exact child ID: `01a0bf16-d46b-71d3-8d60-03332a6b9267`.
- Exact displayed title: Website 1 - Task 09 Content Selection - COMPLETE.
- Brief: [Task 09, revision 4](task-09-content-review-selection.md).
- Approval: RECEIVED; Shawn said `get started on task 09` in this hub on September
  20 after approving the editorial positioning and proposed review scope.
- Positioning: historic homes/woodwork lead; broader work introduces Shawn as
  craftsman and tradesman and welcomes thoughtful inquiries.
- Scope: consolidate studio-evidence and content-review backlogs, review the
  archive, and produce a prioritized shortlist with proposed placement, candidate
  photographs, evidence gaps and a recommended first publication batch.
- Source sessions: `CURRENT — Ballet Studio Completion Evidence`,
  `01a06e5b-fbaa-7202-8a23-f4f3f570ba34`; `TradeJournals Content Review Parent`,
  `01a062b2-cd26-7552-a5f9-3996acac6392`. Read/capture their work without starting
  either session. Their open items remain unfinished; neither is archived here.
- Environment: same-directory archive fork, `codex/website-updates`, baseline
  `06044320fcdb9f67cbb0c0452ab4e03fbfffd978`. Only this child owns Task 09
  editorial deliverable/report; hub owns brief/register.
- Boundaries: documents-only review; no website implementation/publication,
  reviewed-snapshot changes, journal/inventory correction, media modification,
  hosting, source-session archival or successor dispatch. Subsequent Git closeout
  authorization is recorded below and supersedes the initial no-closeout scope.
- Workflow status: COMPLETE — exact child reports Shawn directly reviewed and
  accepted revision 2. Acceptance reconciled as `WK-WEB-T09-H02` September 20
  at 14:57 UTC. Specific quote placement and final image choices are not inferred
  from general acceptance; those belong to later authorized drafting.
- Dispatch: `WK-WEB-T09-D01`; SENT once September 20 at 13:53 UTC.
- Acceptance: all transferred items retain provenance/status; actual archive
  informs the shortlist; restoration remains primary; recommendations distinguish
  inspected evidence from provisional selections; Markdown/whitespace checks pass.
- Report: `WK-WEB-T09-R01`, revision 2, at
  [Task 09 report](reports/task-09-content-review-selection.md); RECEIVED once,
  reconciled as `WK-WEB-T09-H01` September 20 at 14:27 UTC.
- Deliverable: [Content Review And Selection](../../website/docs/content-review-selection.md).
  Both backlogs retain provenance and next actions; all 11 editorial items remain
  open. Source sessions are unchanged.
- First batch proposed: Entry, Guest Bath dresser vanity, Master Bedroom,
  Returning To Clay: Thirty Years Later, and Agfa Isolette. Restoration leads;
  pottery/photography remain a quieter supporting layer.
- Hub verification: document/report review, source-claim and photo-ID spot checks,
  verified 27-journal inventory, resolved local links, scoped Markdown lint and
  whitespace checks. Requested and verified revision 2 correcting same physical
  wheel to same make/model. Child's visual image review was not repeated by hub;
  provisional image selections remain explicitly marked.
- Git authorization: RECEIVED; exact child reports Shawn directly said
  `git er done` after acceptance. Reconciled as `WK-WEB-T09-G01` September 20
  at 15:00 UTC. Git closeout: IN PROGRESS.
- Destination: established `origin/codex/website-updates` at
  `git@github.com:UncleRedBeard/TradeJournals.git`, freshly read back by hub.
- Owner: Task 09 child validates, stages only applicable files, commits, pushes,
  fetches and verifies fresh hash identity, ahead/behind `0 0` and worktree state.
  Payload is the selection, report and Task 09 hub brief/register bookkeeping.
  Hub stops file edits after this handback; no competing Git operations.
- Pre-staging Git state: HEAD `0604432`; two child documents and two hub files
  uncommitted. No commit/push result yet claimed. No website/journal/inventory/
  media changes, deployment, merge, publication, source-session archival or
  successor dispatch is authorized by closeout.

## Website 1 — Task 10 Portfolio Expansion

- Exact child ID: `01a0bf60-e5e5-7e20-8c3d-65c6a6e3a445`.
- Exact displayed title: Website 1 - Task 10 Portfolio Expansion - COMPLETE.
- Brief: [Task 10, revision 3](task-10-portfolio-expansion.md).
- Approval: RECEIVED; Shawn said `start task 10` in this hub on September 20,
  after the five-story candidate implementation scope was presented.
- Scope: implement Entry, Guest Bath dresser vanity, Master Bedroom, Returning
  to Clay and Agfa Isolette stories; confirm photos, write supported copy, add
  the craftsman/tradesman introduction and inquiry invitation, and build a
  reviewable local preview with restoration clearly primary.
- Dependencies: Task 09 shortlist revision 2 accepted and committed at `9cc3237`;
  preserve provisional-image gaps, room identities and same-wheel-model correction.
- Lint repair handoff: `WK-WEB-T10-L01`; SENT once September 20. Fresh wait
  observed turn `01a0c0a8-1ea1-7b43-92e2-d845615a5e54` in progress. Shawn said
  `handoff this to task 10` after the verified diagnosis. Add a narrow generated
  review-packet lint exclusion, normalize three story final newlines, prevent
  recurrence in the archive-owned writer, and verify full lint plus relevant
  regression checks. Preserve the reviewed snapshot; byte changes make it stale.
  No new task or Git closeout authorization. Details are in brief revision 3.
- Preparation closeout: `ab1bce63e94f7848511e206bc03a2f8447f24756`, pushed to
  `origin/codex/website-updates`; hub verified equal HEAD/tracking/FETCH_HEAD,
  `0 0` and clean status before this handoff. This committed only brief/register,
  not the five-story website implementation. Older baseline below is historical.
- Source correction: `WK-WEB-T10-C01`, September 20 at 21:02 UTC. Exact child
  reports Shawn clarified that the Google Studio shelf planks are unfinished,
  temporarily dry-fitted on low-profile brackets after floating brackets were
  rejected. Planks will later be removed for Danish-oil finishing while brackets
  stay mounted. Brief revision 2 preserves this account without inventing the
  unspecified installation constraint. No completion/move claim or journal/
  inventory edit is authorized; no new dispatch was sent.
- Environment: same-directory archive fork, `codex/website-updates`, baseline
  `9cc32375a6853717c3f0e92459947f0ca2b810d1`. Only this child writes Task 10
  implementation; hub owns brief/register. Exact title and idle state verified
  before dispatch.
- Boundaries: candidate implementation only; no reviewed-snapshot promotion,
  hosted deployment, merge, journal/inventory edits, original-media alteration,
  Companion changes, source-session archival or successor task.
- Workflow status: COMPLETE. Shawn approved the original Task 10 presentation
  after review. The separate tartan mock-up was rejected and permanently removed
  outside the repository under task-scoped deletion authorization.
- Dispatch: `WK-WEB-T10-D01`; SENT once September 20 at 15:14 UTC.
- Acceptance: five supported stories and inspected selections, clear visual
  hierarchy, working discovery/search, preserved existing rooms, actual desktop/
  mobile preview review, relevant automated checks and honest remaining decisions.
- Report: `WK-WEB-T10-R01`, revision 2, at
  [Task 10 report](reports/task-10-portfolio-expansion.md); RECEIVED and accepted.
- Verification: 118 Node and 37 Python tests passed; the candidate built and
  validated at 18 pages, 52 files and 232 references; repository-wide Markdown
  lint and whitespace checks passed. Release correctly refused the stale review
  snapshot with `SOURCE_STALE`.
- Git authorization: RECEIVED; Shawn said `git er done` after approval.
  Implementation commit `6e21460` contains the five-story expansion, selected
  media, homepage changes, maintainability fixes and regression coverage. Final
  bookkeeping, push and synchronization verification complete this closeout.

## Website 1 — Task 11 Expanded Release Readiness

- Exact child ID: `01a0c0f4-617d-70a1-b0b1-da23a7b1f953`.
- Brief: [Task 11, revision 4](task-11-expanded-release-readiness.md).
- Approval: RECEIVED; Shawn said `start task 11` in this hub on September 20,
  after the release snapshot, verification, portability and contact scope was
  proposed. He then explicitly chose `Keep inquiries disabled for now`.
- Scope: refresh the reviewed snapshot for approved Task 10 content, verify the
  expanded static release and browser behavior, prove clean-checkout build
  reproducibility, and update provider-neutral deployment instructions.
- Environment: same-directory fork; `codex/website-updates`; baseline `d28f030`.
  Task 10 is idle and COMPLETE. Only Task 11 writes implementation/release files;
  hub owns brief/register. Clean checkout observed before preparation.
- Exact displayed title: Website 1 - Task 11 Expanded Release Readiness - COMPLETE.
- Workflow status: COMPLETE — accepted by hub September 20 after review and
  independent verification. Initial execution turn was
  `01a0c0f5-57a7-7083-9d22-4a486f770b60`; dispatch history is retained.
- Dispatch: `WK-WEB-T11-D01`; SENT once September 20, 2026.
- Acceptance: current approved snapshot, validated release and protected preview,
  relevant automated and browser checks, reproducible build documentation, and
  honest remaining launch decisions. Existing editorial approval is preserved.
- Boundaries: no new content/design, active inquiry destination, hosted deployment,
  DNS/domain changes, merge, Companion changes, original journal or
  inventory writes, archival, or successor dispatch.
  Scoped Git closeout is separately authorized below.
- Report: `WK-WEB-T11-R01`, revision 2, at
  [Task 11 report](reports/task-11-expanded-release-readiness.md); RECEIVED once
  per revision. Initial acceptance is `WK-WEB-T11-H01`; revision 2 acceptance
  is `WK-WEB-T11-H02`.
- Final editorial approval: `WK-WEB-T11-A02`. Exact child reports Shawn said
  `i like it` after reviewing the corrected release entry, approving revision 2
  and its current snapshot. COMPLETE title and idle runtime freshly verified.
  That editorial approval alone did not authorize Git closeout, deployment or
  archival; subsequent explicit Git authorization is recorded below.
- Hub verification: 118 Node and 37 Python tests, actual release/preview builds,
  independent output checks (each 18 pages, 52 files, 232 references), 87-file
  Markdown lint and whitespace checks passed. Snapshot current, zero changed
  keys, 50 records, 47 sources; canonical SHA-256
  `ec16411478fec3d39b8099e1c366cfe4cedd27af797bcd7217dcd4a1ecff9fcc`
  after the revision 2 correction. Hub independently revalidated both outputs
  and the current snapshot, including the corrected rendered journal wording.
- Hub reviewed rendered release/disabled contact and the child's browser QA and
  clean-clone evidence; all six implementation files match the tested clone.
  Release `http://127.0.0.1:4175/`; protected preview `http://127.0.0.1:4174/`.
  Revision 2 adds only Shawn's directly approved `120-format film` wording in
  the Agfa Isolette story and the corresponding reviewed fingerprint. Design,
  source journals and inventories remain unchanged. Task 11 implementation is
  now committed and pushed as recorded below; no successor or deployment started.
- Git authorization: `WK-WEB-T11-G01`; RECEIVED. Shawn said `git er done` in
  the exact child after approving revision 2. Scoped validation, commit, push
  and sync verification are authorized to established
  `git@github.com:UncleRedBeard/TradeJournals.git`, branch
  `origin/codex/website-updates`. Implementation closeout VERIFIED at
  `46293aab01160f6612f6de49c693f895788f4f17` (`Prepare expanded website release`).
  Child reports fresh fetch after push; hub independently observed matching
  HEAD/tracking/FETCH_HEAD, `0 0`, and clean status before this final bookkeeping.
  Child closeout checks: 118 Node, 37 Python, 87-file Markdown lint, whitespace,
  preview/release builds and validation at 18 pages/52 files/232 references pass.
  Child owns the final brief/register commit and push; that bookkeeping outcome
  remains pending. Hub stops editing after handback. Hosting, deployment, merge,
  archival and successor remain outside scope.

## Website 2 — Concept B Staged Continuation

Approved visual direction: Craftsman's Atelier; homepage implementation accepted
in `Toil & Timber — Concept B Website Redesign`, source task
`01a0fce4-a907-7981-a469-b3b101199a36`. Receipt alone started no work. Shawn then
said `ok, let's get started in stages. you already know our workflow.` here.

| Task | Stage | Execution status |
| --- | --- | --- |
| 12 | Shared header/footer, navigation and styling foundation | COMPLETE |
| 13 | Project pages and galleries | COMPLETE |
| 14 | TradeJournal reading pages and archive/search presentation | COMPLETE |
| 15 | Integrated site verification and release review | COMPLETE |
| 16 | Dependency maintenance | COMPLETE |
| 17 | Markdown tooling cleanup | COMPLETE |

Each child returns for hub review and Shawn's acceptance before the next task
starts. Prior full-site design approval is preserved; each start remains bounded.
Keep existing copy/media/search, room identities and disabled inquiry behavior.
Git closeout, deployment and any changed-source review remain separate decisions.

### Website 2 — Task 12 Shared Frame

- Child: `01a0fed3-08c2-7042-a8ea-f1893d20c24a`.
- Brief: [Task 12, revision 1](task-12-concept-b-shared-frame.md).
- Approval: RECEIVED October 2; direct staged-start instruction above.
- Scope: reuse accepted Concept B header/footer and typography/palette foundations
  on all route types; preserve the homepage; verify inner-page navigation and
  responsive/keyboard behavior. Page-specific body redesigns are deferred.
- Environment: same directory; `codex/concept-b-homepage`; baseline `6a528e3`.
  Other website tasks observed idle. Unrelated content-review work remains.
- Exact title: Website 2 - Task 12 Shared Frame - COMPLETE.
- Workflow status: COMPLETE — hub technical review passed; Shawn's
  direct child approval verified. Initial execution turn was
  `01a0fed5-562d-7193-a48a-ec6d5f50f69a`.
- Dispatch: `WK-WEB-T12-D01`; SENT once October 2, 2026.
- Report: `WK-WEB-T12-R01`, revision 3,
  [Task 12 report](reports/task-12-concept-b-shared-frame.md); received once and
  accepted as `WK-WEB-T12-H03` October 2; earlier receipts remain H01/H02.
- Acceptance: Shawn said `i like that. approved` in child turn
  `01a0fefe-5250-7aa2-ab93-6ee2f42b4f28` after delivery of the Work & Craft
  amendment. User message verified directly; implementation unchanged since
  revision 2. Accepted scope is complete; successor/Git approval is separate.
- Narrow amendment: Shawn directly requested `change it to work & craft` in
  child turn `01a0feef-79b9-7940-8066-cb7c40b10759`. Shared navigation now reads
  **Work & Craft**, without the count. Hub verified the label and unchanged
  destination across all 18 pages in each rebuilt output; child build/browser
  checks passed. Subsequent user acceptance is recorded above.
- Hub checks: full diff/new-component review, 119 Node and 37 Python tests,
  Markdown lint (95 files, zero errors), whitespace checks and both independent
  output checks passed (18 pages, 52 files, 270 references each). Review is
  current with zero changed keys; saved snapshot unchanged. Live inner-page
  shared frame inspected; child's desktop/mobile/keyboard/search evidence read.
- Preview: `http://127.0.0.1:8139/`. Changes remain uncommitted. Separate Kodakk
  journal/brief/report and content-review register work preserved. No successor
  dispatched or Git closeout performed.
- Boundaries: no public content/source/fingerprint change, journal/inventory
  edits, contact activation, Git closeout, merge, hosting/deployment, archive or
  next-stage execution. Hub owns brief/register; child owns implementation/report.

### Website 2 — Task 13 Projects And Galleries

- Child: `01a0ff09-49a5-7cb2-a999-d7dbd073ecba`.
- Brief: [Task 13, revision 1](task-13-project-pages-galleries.md).
- Preparation authorization: Shawn said `handoff task 13` on October 2, 2026.
- Execution approval: RECEIVED directly in child October 2; `WK-WEB-T13-A01`.
  Shawn said `get started...but update the title to reflect status as well` in
  turn `01a0ff11-3c3e-7a13-844d-0ef34b67c21d`; user message verified directly.
- Exact title: Website 2 - Task 13 Projects - COMPLETE.
- Workflow status: COMPLETE; hub technical review passed and Shawn's
  visual acceptance verified. No duplicate hub dispatch sent.
- Scope: extend accepted Concept B styling to project pages/gallery presentation;
  preserve approved content, shared frame, room identities and disabled inquiries.
- Dependency: Task 12 accepted COMPLETE as `WK-WEB-T12-H03`; its uncommitted
  implementation remains the starting point.
- Environment: same-directory fork on `codex/concept-b-homepage`; observed HEAD
  `6c48930489851925eb837a2a89f22bb7cec8ccb5`. Separate El Toro source-review work
  is active; preserve its files and refresh status before execution.
- Report: `WK-WEB-T13-R01`, revision 2, at
  [Task 13 report](reports/task-13-project-pages-galleries.md); RECEIVED and
  accepted as `WK-WEB-T13-H02` October 2; initial receipt remains H01.
- Acceptance: verified Shawn's direct `approved` in child turn
  `01a0ff24-8003-72c3-9b99-f87b22a20315` following delivery. No implementation
  change accompanies approval; the accepted stage is complete.
- Hub review: inspected template/components/test changes and desktop/phone
  screenshots; no blocking issues. Independently passed 120 Node and 37 Python
  tests and both matching-model output checks (18 pages, 52 files, 302 references
  each). Review current with no changed keys; saved snapshot unchanged.
  Child reports live viewport, image loading, keyboard and navigation checks.
- Preview: `http://127.0.0.1:8139/work/living-room-studio-restoration/`.
  Task 12/13 changes remain uncommitted; concurrent content-review work advanced
  HEAD to `0225667` and owns the later SXSW journal/brief/report/register changes.
- Task 14/15, Git closeout, merge, deployment and archival remain outside scope.

### Website 2 — Task 14 Journals And Archive

- Child: `01a0ff4e-a59e-7b02-a44b-d36c0663db18`.
- Brief: [Task 14, revision 1](task-14-journals-archive.md).
- Approval: Shawn said `kick off task 14` in the hub October 2, 2026.
- Dispatch: `WK-WEB-T14-D01` — SENT once; approved scope is journal reading pages
  and archive/search presentation, with existing content and search preserved.
- Runtime: active turn `01a0ff50-6839-7921-b6e9-6fff0dea4bd4` observed after
  dispatch; exact child was idle before sending. No duplicate execution.
- Environment: same-directory fork, `codex/concept-b-homepage` at `6042f00`.
  Tasks 12/13 are committed and synchronized; their earlier uncommitted notes
  are historical. Separate source-review changes remain owned by that workflow.
- Exact title: Website 2 - Task 14 Journals - COMPLETE.
- Workflow status: COMPLETE; hub technical review passed and Shawn's
  visual acceptance received.
- Report: `WK-WEB-T14-R01`, revision 1, at
  [Task 14 report](reports/task-14-journals-archive.md); RECEIVED and reconciled
  once as `WK-WEB-T14-H01` October 2; accepted as `WK-WEB-T14-H02` October 3.
- Acceptance: Shawn said `looks good. approved` directly in the hub after the
  review preview was restarted and its saved pages verified. No implementation
  change accompanies acceptance; Task 15 and Git closeout remain separate.
- Hub review: five-file implementation/test/doc delta and desktop/phone journal
  and actual-search screenshots inspected; no blocking issues. Independent
  121 Node/37 Python tests, 107-file Markdown lint and whitespace checks passed.
  Both outputs validate against matching models (18 pages/52 files/318 references
  each); review current, zero changed keys, snapshot unchanged. Content, search
  scripts and accepted earlier-stage components remain unchanged. Live fallback
  and interaction checks are child-reported.
- Preview: `http://127.0.0.1:8139/tradejournals/` and the Entry journal route.
  Task 14 changes are uncommitted; concurrent source-review work is preserved.
- Task 15, Git closeout, merge, deployment, snapshot refresh and archive remain
  outside this authorization. Hub owns brief/register; child owns implementation.

### Task 14 Git Closeout And Completed-Chat Archival Authorization

On October 3, 2026, Shawn said `git er done...then archive all completed tasks`
after reviewing the exact list of 11 completed chats. This authorizes scoped
Task 14 validation, commit and push to `origin/codex/concept-b-homepage`, followed
by archival of those reviewed chats. Task 14 implementation, README, tests,
brief/report and this hub register are included. Concurrent content-review work
remains excluded. Earlier uncommitted/no-Git statements are historical.

Archive scope: Concept B redesign parent and homepage child; Website 2 Tasks
12, 13 and 14; Content Review Tasks 01 through 06. Preserve website updates,
TradeJournals Content Review Parent, active La Ciotat Task 07, Ballet Studio
Completion Evidence, office storage layout and Dashboard Launcher. Task 15,
merge and deployment are not started by this closeout. Verify push and archival
results in the hub after execution; this entry records authorization only.

### Website 2 — Task 15 Integrated Release Review

- Child: `01a10263-fe12-7673-bb16-067cb5e4f7ff`.
- Brief: [Task 15, revision 1](task-15-integrated-release-review.md).
- Approval: Shawn said `kick off task 15` in the hub October 3, 2026.
- Dispatch: `WK-WEB-T15-D01` — SENT once; child active turn
  `01a10265-f4d4-7e71-9475-8e4261b9216b` observed after dispatch.
- Scope: integrated browser/build verification, fresh-checkout reproduction,
  bounded fixes for observed failures, and current maintainer/release docs.
- Environment: same-directory fork on `codex/concept-b-homepage` at `ef1d5e8`;
  Tasks 12-14 accepted and pushed, latest sync verified `0 0`. Completed-chat
  archival verified for all 11 approved IDs. Active La Ciotat work is preserved.
- Report: `WK-WEB-T15-R01`, revision 1, RECEIVED once at
  [integrated release review](reports/task-15-integrated-release-review.md).
- Acceptance: Shawn directly said `looks good...approved` in the exact child,
  turn `01a10277-dae3-71a3-bc1c-4da9945ad307`; hub verified the user message.
  Acceptance `WK-WEB-T15-A01`; reconciliation `WK-WEB-T15-H01`.
- Workflow status: COMPLETE. Exact child title:
  Website 2 - Task 15 Release Review - COMPLETE.
- Hub review: inspected docs, screenshots, fresh-checkout proof, audit assessment
  and logs recording 121 Node / 37 Python tests in both checkouts. Independently
  checked both retained outputs: 18 pages, 52 files, 318 references each; current
  review and zero changed keys. Compared every output file with the fresh
  checkout: both modes byte-identical. No website implementation changes.
- Remaining follow-up: three high build-dependency package findings; dependencies
  absent from the verified static package. Task 15 documents remain uncommitted.
  Concurrent La Ciotat commit `082520c` changes no website files.
- No deployment, Git closeout/merge, snapshot refresh, contact activation,
  archival or next task is authorized by this start.

## Remaining Decisions After The Pilot — Updated Direction

### Completed Task Archival

On September 16, 2026 at 23:14 UTC, Shawn requested archiving completed tasks
after checking actual completion. The hub inspected the five completion reports,
acceptance records, current implementation artifacts and Git history, and reran
`npm run test:website`: 80 website tests and 37 Python tests passed, including
build/output checks. Tasks 01–04 delivered their accepted implementation scope;
Task 05 delivered its explicitly accepted text/layout and branding. Its remaining
photo work is carried into the prepared Task 06, not treated as finished.

The exact Task 01–05 IDs above were archived on host `local`. A fresh active
listing contained none of those IDs; the archived listing contained all five.
This hub and Dashboard Launcher remain available. Task 06 was freshly observed
idle with AWAITING APPROVAL; it was neither dispatched nor archived. Archival
changes task organization only. Existing uncommitted documentation remains.

The original four-task implementation plan is complete. Shawn separately
authorized Task 05 for content and visual review. Contact destination, additional
projects, hosting/domain and deployment remain later decisions.

## Event Log

| Time (UTC) | Task | Event ID | Evidence | Result |
| --- | --- | --- | --- | --- |
| 2026-09-15 16:31 | 01 | WK-WEB-T01-A01 | Explicit plan approval followed by get-started/workflow-hub instruction in exact hub | Approval recorded; child preparation started |
| 2026-09-15 16:34 | 01 | WK-WEB-T01-F01 | Exact same-directory child resolved; fresh read shows intended title and idle runtime | Ready for approved dispatch |
| 2026-09-15 16:35 | 01 | WK-WEB-T01-D01 | Single approval message sent; new active turn and exact IN PROGRESS title observed | Assignment running; implementation acceptance pending |
| 2026-09-16 02:00 | 01 | WK-WEB-T01-B01 | Child reported branch drift after direct user continue instruction; hub verified equal branch tips, switched back, and checked 18 content fingerprints | Approved branch restored without content changes; existing Task 01 may continue |
| 2026-09-16 02:07 | 01 | WK-WEB-T01-H01 | Received R01 revision 1; reviewed code and independently reran required checks; exact COMPLETE title read back | Accepted; no successor dispatch or Git closeout authorized by this report |
| 2026-09-16 13:02 | 02 | WK-WEB-T02-A01 | Shawn's exact instruction in this hub: start task 02 | Task-specific approval recorded; branch and accepted foundation verified |
| 2026-09-16 13:05 | 02 | WK-WEB-T02-D01 | Same-directory child created and approved dispatch sent once | Task started |
| 2026-09-16 13:20 | 02 | WK-WEB-T02-H01 | Child repeatedly remained active without artifacts; hub paused child and completed approved records/tests directly | Candidate content accepted as implementation; editorial review remains pending |
| 2026-09-16 13:05 | 02 | WK-WEB-T02-D01 | Same-directory child created and verified idle; approved brief dispatched once; active turn and exact IN PROGRESS title observed | Office content task running |
| 2026-09-16 14:48 | 03 | WK-WEB-T03-A01 | Shawn explicitly requested starting Task 03; clean development branch and accepted dependencies verified | Approved for scoped child creation and execution |
| 2026-09-16 14:51 | 03 | WK-WEB-T03-D01 | Same-directory child verified idle before single approved dispatch; active turn and exact IN PROGRESS title observed | Astro pages task running |
| 2026-09-16 15:00 | 03 | WK-WEB-T03-R01 | Child dispatch ended without implementation; Shawn required actual work. Hub paused the child and began the same approved scope directly | Markdown safety test and Astro preview build now have real artifacts |
| 2026-09-16 15:10 | 03 | WK-WEB-T03-R02 | Hub completed the approved Astro scope and browser review; focused tests and existing evidence/search checks passed | Task complete; Task 04 remains unstarted |
| 2026-09-16 16:53 | 04 | WK-WEB-T04-A01 | Shawn explicitly said start task 04; clean development branch and committed pilot verified | Task-specific approval recorded |
| 2026-09-16 16:56 | 04 | WK-WEB-T04-D01 | Same-directory child created and verified; approved brief dispatched once | Pilot verification running |
| 2026-09-16 16:58 | 04 | WK-WEB-T04-H01 | Child turn ended without verification code; hub paused child and took over existing approved scope | Direct implementation in progress |
| 2026-09-16 17:44 | 04 | WK-WEB-T04-H02 | Hub reconciled resumed child work and superseded its premature acceptance entry with report revision 2 | Final acceptance review pending; no publication or Git closeout authorized |

| 2026-09-16 21:47 | 04 | WK-WEB-T04-H03 | Independent review findings fixed; 79 website tests, 84 Python tests, legacy checks, browser review, lint and whitespace pass | Accepted; COMPLETE title set and verified; no next task or publication |

| 2026-09-16 22:04 | 05 | WK-WEB-T05-A01 | Shawn explicitly said start task 05; clean committed pilot and idle Task 04 verified | Scoped review child created; dispatch being prepared |

| 2026-09-16 22:05 | 05 | WK-WEB-T05-D01 | Approved brief dispatched once to exact child; new execution turn observed active | Content and visual review running |

| 2026-09-16 22:16 | 05 | WK-WEB-T05-H01 | Received R01 revision 1 once; source/diff review, 79 tests, output gate, lint, whitespace and rendered candidate verified | READY FOR REVIEW; editorial decisions and snapshot approval pending |

| 2026-09-16 22:34 | 05 | WK-WEB-T05-A02 | Direct child instruction selects Home Reno - Studio as first candidate; active turn and user wording verified | Brief revision 2 recorded; Studio work IN PROGRESS; no duplicate dispatch |

| 2026-09-16 22:45 | 05 | WK-WEB-T05-H02 | Received R01 revision 2 once; Studio source/diff review, 80 Node and 37 Python tests, output gate, lint and rendered page verified | Text/layout READY FOR REVIEW; Studio photo selection and editorial acceptance remain unfinished |

| 2026-09-16 22:50 | 05 | WK-WEB-T05-H03 | Received R01 revision 3; approved Toil & Timber rename verified in actual output and live page; current brief/register reconciled | READY FOR REVIEW; Studio photos and reviewed snapshot still pending |

| 2026-09-16 22:51 | 05 | WK-WEB-T05-G01 | Child reports Shawn's direct git er done instruction; established origin/codex/website-updates destination | Scoped Git closeout authorized and running in child; hub brief/register ready to stage; editorial acceptance unchanged |

| 2026-09-16 23:08 | 05 | WK-WEB-T05-H04 | Child reports direct user approval; report and editorial packet record acceptance; exact COMPLETE title and idle runtime read back | Text/layout and branding accepted; photos deferred; subsequent documentation uncommitted |

| 2026-09-16 23:08 | 06 | WK-WEB-T06-F01 | Explicit preparation-only instruction; brief saved; same-directory fork resolved and idle state read back | AWAITING APPROVAL; no execution dispatch; brief panel queued |

| 2026-09-17 17:01 | 06 | WK-WEB-T06-A01 | Exact child reports Shawn's direct start task 06 instruction and brief read; active execution turn and IN PROGRESS title verified | Direct approval recorded; brief revision 2; existing child owns work; no duplicate dispatch |

| 2026-09-17 20:11 | 06 | WK-WEB-T06-H01 | R01 revision 1 received; artifacts, both Git states and candidate boundary inspected; output check passes 6 pages/22 files; READY FOR REVIEW title and idle runtime verified | Receipt reconciled once; acceptance and photo review pending; missing browser-suite dependency recorded; no further dispatch |

| 2026-09-17 20:17 | 06 | WK-WEB-T06-H02 | R01 revision 2 and editorial packet record Shawn's direct approved after reviewing workflow and three-photo candidate | Accepted scope COMPLETE; unchanged implementation/check evidence and browser-suite limitation retained; no Git, snapshot change or next task |

| 2026-09-17 20:20 | 06 | WK-WEB-T06-G01 | Child reports direct git er done after acceptance; both established origin URLs and development branches inspected; closeout turn active | Scoped two-repository Git closeout authorized; Task 05/06 bookkeeping included; hub edits stop before staging |

| 2026-09-17 21:28 | 07 | WK-WEB-T07-D01 | Shawn explicitly said start task 07; same-directory child verified idle; brief dispatched once; new active turn, exact title and workspace observed | Edit Project and Room Separation running, design first; no journal correction, publication or Git closeout |

| 2026-09-18 14:29 | 07 | WK-WEB-T07-C01 | Exact child reports Shawn's correction: Flickr Studio Office is current barre studio; Google Studio is former living room and future home; idle state observed | Brief revision 2 and register reconciled; contradictory handoff wording superseded; design review continues without new dispatch or content edits |

| 2026-09-19 02:08 | 07 | WK-WEB-T07-H01 | R01 revision 1 received; spec/plan/audit and Git state inspected; canonical content untouched; output validates 6 pages/22 files; READY FOR REVIEW title read back | Private revision 1 delivered unpublished; exact review and publication remain pending; runtime and browser-test limitations retained; no new dispatch |

| 2026-09-19 15:33 | 07 | WK-WEB-T07-H02 | Exact child reports Shawn's final approval of implementation and private three-room preview; COMPLETE title and idle runtime verified | Accepted delivery COMPLETE; canonical room correction remains unapplied; no publication, deletion, Git, journal/inventory correction or successor authorized |

| 2026-09-19 16:03 | 07 | WK-WEB-T07-H03 | R01 revision 2 reports explicit save/build/publish approval and published draft revision 2; hub verifies three-room canonical records and 8-page/24-file output | Local application reconciled; review state and journals/inventories unchanged; tracked removals unstaged; no hosted deployment or Git closeout |

| 2026-09-19 16:13 | 07 | WK-WEB-T07-G01 | Child reports git er done and task-scoped deletion approval; implementation commits pushed; hub confirms both HEAD/tracking hashes and 0 0 | Implementation synchronized; report revision 3 and two hub files handed back for authorized bookkeeping closeout; hub edits stop |

| 2026-10-03 15:54 | 15 | WK-WEB-T15-H01 | R01 revision 1 received; direct child approval A01 verified; documentation, screenshots, test logs, matching-model output checks and byte-identical fresh outputs reviewed | Accepted COMPLETE; dependency maintenance retained; no Git closeout, merge, deployment, archival or successor |

## Task 15 Git Closeout Authorization

After Task 15 acceptance and hub reconciliation on October 3, 2026, Shawn said
`git er done` in website updates. This authorizes validation, commit and push of
the Task 15 brief/report, hub register, website README and release-review document
to the established `origin/codex/concept-b-homepage` branch. Earlier statements
that these documents remain uncommitted or that Git closeout is unauthorized
record the pre-closeout checkpoint. No merge, deployment, inquiry activation,
archival or successor task is included. Final commit and synchronization evidence
will be reported in the hub after the push.

## Website 2 — Task 16 Dependency Maintenance

- Child: `01a10290-90df-7271-9f3f-ad82cc5a8739`.
- Brief: [Task 16, revision 1](task-16-dependency-maintenance.md).
- Approval: Shawn said `cool...sounds good...let's get back to it and start task 16`
  in website updates on October 3, 2026.
- Scope: recheck dependency advisories; apply minimal compatible fixes; verify
  locked installation, tests and static output; document remaining findings.
- Environment: same-directory fork on `codex/concept-b-homepage` at `f20572a`.
  Task 15 accepted, committed and pushed. Content Review Task 08's register and
  brief are independently owned and preserved.
- Dispatch: `WK-WEB-T16-D01` — SENT once; idle child verified beforehand.
  Wait observed active turn `01a10291-85e9-7311-bccd-1c1035c3a1d9` and start
  acknowledgement.
- Workflow: COMPLETE. Shawn said `accepted` in this hub on October 3, 2026.
  Acceptance `WK-WEB-T16-A01`; final reconciliation `WK-WEB-T16-H02`.
  Exact child title: Website 2 - Task 16 Dependencies - COMPLETE.
- Report: `WK-WEB-T16-R01`, revision 1, RECEIVED once and reconciled as
  `WK-WEB-T16-H01`: [dependency maintenance](reports/task-16-dependency-maintenance.md).
- Hub checks: reviewed lockfile/README diff, audit evidence and upstream advisory;
  independently reran 121 Node and 37 Python tests, both output checks
  (18 pages / 52 files / 318 references each), and complete byte comparisons to
  baseline and fresh patched output. All pass; review current, zero changed keys.
- Result: devalue 5.9.2 to 5.9.4 only; six advisories removed. Website audit now
  has two high package findings for the unresolved cache issue/inherited Astro
  finding. Separate root-tooling audit has seven high and one moderate package
  findings. Those need remediation/exposure assessment; no clean-audit claim.
- Current HEAD `715b2a1` includes independent content-review work without website
  changes. Task 16 files remain uncommitted.
- Keep design/content unchanged and inquiries disabled. No Git closeout, merge,
  deployment, archival or successor is authorized. Wait for the current journal
  review batch to finish before selecting future website content additions.

## Task 16 Git Closeout Authorization

After acceptance, Shawn said `git er done` in website updates on October 3,
2026. This authorizes validation, commit and push of the accepted website lock
patch, README, Task 16 brief/report and hub register to the established
`origin/codex/concept-b-homepage` branch. Earlier uncommitted/no-closeout
statements describe the pre-closeout checkpoint. Residual findings stay open;
merge, deployment, archival and successor work remain separate. Final commit
and synchronization evidence will be reported in the hub after the push.

## Website 2 — Task 17 Markdown Tooling

- Child: `01a102e5-9ee6-7281-b41f-8993cc70e4c3`.
- Brief: [Task 17, revision 1](task-17-markdown-tooling.md).
- Approval: Shawn said `kick off task 17` in this hub on October 3, 2026.
- Scope: evaluate and update root linter, add locked reproducible installation,
  preserve lint coverage and verify documentation/website compatibility.
- Environment: same-directory fork on `codex/concept-b-homepage` at `59d6e31`;
  clean checkout at preparation. Task 16 accepted and pushed at `2d566f0`.
- Dispatch: `WK-WEB-T17-D01` — SENT once; child idle verified beforehand.
  Active execution turn `01a102e6-7709-7242-9181-39da57ce8234` observed.
- Workflow: COMPLETE; Shawn approved in the hub October 3, 2026. Exact title:
  Website 2 - Task 17 Markdown - COMPLETE.
- Report: `WK-WEB-T17-R01`, revision 1, RECEIVED once; reconciled as
  `WK-WEB-T17-H01`: [Markdown tooling](reports/task-17-markdown-tooling.md).
- Hub verification: current lint 121 files/zero issues, whitespace, both output
  gates (18 pages/52 files/318 references), current snapshot and byte-identical
  outputs pass. Old/new saved coverage matches 117 authored baseline files.
  Root lock hash and clean-install logs agree; no website dependency changes.
- Result: pinned CLI2 0.23.3 with root lock and install documentation. Root audit
  eight findings to five high package findings for one unpatched braces issue.
  Website cache/Astro issue stays separate. Changes uncommitted; no clean-audit
  claim. Acceptance recorded below.
- No content promotion, website redesign, inquiry activation, Git closeout,
  merge, deployment, archival or successor start. Preserve concurrent reviews.

## Task 17 Acceptance And Git Closeout

Shawn said `approved and git er done` in website updates on October 3, 2026.
Acceptance `WK-WEB-T17-A01` covers report `WK-WEB-T17-R01`, revision 1;
hub reconciliation `WK-WEB-T17-H02` marks Task 17 COMPLETE. Remaining upstream
findings stay documented and unresolved. Earlier pending/uncommitted statements
record prior checkpoints.

The same instruction authorizes validation, commit and push of the Task 17
manifest/lock, exclusions, installation documentation, brief/report and hub
register to `origin/codex/concept-b-homepage`. Preserve all concurrent Cassis
content-review work. No merge, deployment, archival or successor is included.
Final commit and synchronization evidence will be reported in the hub.

## Website 2 — Task 18 Main Integration

- Child: `01a1078d-069e-77d2-8db1-9d0cfb51fd16`.
- Brief: [Task 18, revision 1](task-18-main-integration.md).
- Approval: Shawn said `start task 18` October 4, 2026 after the explicit
  main integration, documentation, validation and push proposal.
- Scope: review the full accepted branch payload, safely integrate into main,
  update release instructions, run checks and push/verify origin/main.
- Baseline: clean `codex/concept-b-homepage` at `0fa6bc9` before preparation.
  All three content promotions and release snapshots are approved and committed;
  current preview/release check: 20 pages/60 files/363 references, zero changed keys.
- Dispatch: `WK-WEB-T18-D01` — SENT once; child idle verified beforehand.
  Active turn `01a1078e-4235-73a1-9e0d-2df2b9984cc1` observed.
- Workflow: IN PROGRESS. Expected report `WK-WEB-T18-R01` at
  `reports/task-18-main-integration.md`.
- Child may include hub-prepared brief/register in the authorized Git closeout;
  only hub edits those files. No deployment, archival or successor authorized.
