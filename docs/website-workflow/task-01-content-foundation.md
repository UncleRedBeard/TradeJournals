# Website 1 - Task 01 Content Foundation

Workflow status: IN PROGRESS
Execution approval: RECEIVED; hub dispatch `WK-WEB-T01-D01` sent and active turn observed.
Hub ID/title: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` / website updates
Child ID: `01a0a5ea-afed-7e92-9938-25b57c1e5b4a`
Hub register: [task-register.md](task-register.md)
Brief revision: 1
Workspace: `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/TradeJournals`
Branch/isolation: `codex/website-updates`; same-directory fork, one website writer
Starting HEAD: `e16be25c6e7d2db3789e080145332b8dc97b771f`

## Assignment

Implement only **Task 1: Validated Records And Offline Source Preparation** in
the [approved plan](../superpowers/plans/2026-09-15-worth-keeping-astro-pilot.md).
Read its global constraints, contracts, file map, and Task 1 before coding;
read the [design](../superpowers/specs/2026-09-15-worth-keeping-website-design.md)
and existing module/website working guides as referenced there.

In scope:

- Project-scoped supported Node runtime, exact website dependencies and lockfile.
- Strict plain JSON schemas, relationships and source/reference validation.
- Scoped source fingerprints and candidate/reviewed comparison.
- Offline preparation of the explicitly selected public model and assets list.
- Focused synthetic tests and unchanged legacy-site baseline checks.
- `.gitignore` additions solely for website runtime/dependencies/generated files.

Out of scope: real Office content migration, Astro pages, gallery styling,
Dashboard changes, edits to original journals/inventories/assets/prototype,
commit/push/deployment, and starting Tasks 02–04. Do not edit the hub register,
brief, or master plan. Record necessary plan deviations in your report.

The current default Node is 25.8.1. The plan specifies scoped Node 24.21.0,
Astro 7.3.2 and Zod 4.5.4; package metadata was checked earlier today. Verify
the installed executable before testing. Keep the global runtime unchanged.
Dependency installation for this scoped approved task is authorized; use the
normal tool approval path if sandbox network access needs escalation.

## Keep It Proportional

Shawn's exact direction: "more tech savy than the average tradesman, but less
flashy than an influencer wanna be site." This is a maintainable craftsman's
site, not an enterprise platform. Prefer small ordinary functions and explicit
data over classes/frameworks that anticipate hypothetical needs. Implement the
approved concrete validation cases; do not add infrastructure, a CMS abstraction,
background services, authentication, deployment machinery, or extra dependencies.

## Completion Criteria

1. Plan Task 1 interfaces are implemented and independently tested with invented
   fixtures, including missing IDs, selected-source changes, path containment,
   and candidate release rejection. The review code never promotes approval.
2. Run the required legacy baseline and focused Node/Python tests. Show exact
   runtime, commands, counts, and any unresolved verification limitations.
3. Public model excludes local source paths and unselected/private records.
   No component/HTML dependency is required by source preparation.
4. Inspect the diff, run Markdown lint and whitespace checks appropriate to
   changed files, and report the actual branch/HEAD and changed paths.
5. Save the completion report, mark READY FOR REVIEW, and request hub review.
   Leave applicable changes uncommitted.

## Skills And Collaboration

Use workflow-hub child procedure and the executing-plans skill to carry out this
bounded written task. Apply senior-developer, Python patterns/testing, and
proportionate verification instructions where relevant. Do not create additional
user-visible tasks. If an applicable skill calls for an internal bounded review,
keep that separate from the hub's own acceptance of this deliverable.

## Approval And Return

Approval source is the exact hub's current user instruction: "then get started
and make sure to use the workflow-hub skill too," following explicit approval
of this implementation plan. Dispatch ID: `WK-WEB-T01-D01`.

Only execute after receiving that hub dispatch, or an explicit current user
instruction in this exact child. Do not request repeat approval for this scope.
Preserve unrelated work; other Dashboard tasks may exist in the same project.
Do not read private Companion storage or private business-operation records.

Save report ID `WK-WEB-T01-R01`, revision 1, at
`docs/website-workflow/reports/task-01-content-foundation.md`. Use the workflow-hub
completion-report structure with exact child ID, approval/dispatch evidence,
results, changed paths, tests, limitations and Git state. Do not edit this register.

Rename the child `Website 1 - Task 01 Content Foundation - READY FOR REVIEW`,
verify the title, and send the report's absolute path and concise result to
hub `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`. This report message is authorized by
the explicitly invoked workflow-hub skill. Request reconciliation only;
do not launch or request automatic launch of another task. Record delivery
separately from task outcome and do not claim receipt without observing it.
