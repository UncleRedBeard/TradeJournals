# Website 3 - Task 19 Services and Assessment

Brief revision: 1. Execution approval: RECEIVED, October 6, 2026.
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` — website updates.
Child: `01a111aa-6c51-7a50-a0dc-1d6be2c0e65d`.
Dispatch: `WK-WEB-T19-D01`. Report: `WK-WEB-T19-R01`, revision 1.
Workspace: TradeJournals shared checkout, branch `main`, base `41c4dbf`.

## Approval and scope

Shawn authorized both high-priority website improvements in chat
`01a1118b-5382-7490-a139-217004cba7fc`: “let's tackle the 2 high priority items
you identified. use our workflow-hub and get started”. The concrete scope is
recorded in [the approved request](seo-readiness-request-2026-10-06.md),
`WK-WEB-SEO-20261006-01`. His latest direct hub instruction is “remember...
let's not over-engineer this”. Both implementation tasks are approved; exact
candidate-copy acceptance and release remain later steps.

Add compact services and assessment content to the existing homepage/practice
area. Reuse current records and visual styles. Lead with historic wood floors,
interior woodwork and architectural surfaces. Include secondary interior
painting and shelving restoration/fabrication from an existing or accepted
design, without offering original design services. Explain the normal paid
assessment and its written record of photographs, observations, risks/unknowns,
options, recommended phases and recommendation. Link to a few appropriate
approved project pages, clearly identifying them as work in Shawn's own home.

The approved design and bounded direction are settled. Make routine copy and
placement choices and deliver a concrete candidate before seeking final-copy
approval. Keep this small: no new routes, dependencies, CMS, abstraction layer,
forms, structured data, town pages, campaigns or broader SEO work. Make only
the validation/model changes necessary to keep the editable copy within the
existing content and review system. Do not add tests that only repeat copy;
use existing checks and focused regression checks if the change needs them.

## Read first

- `website/README.md`, `website/content/home.json`, `website/content/site.json`,
  `website/content/services/historic-floors.json`, `website/src/pages/index.astro`
  and the actual validation/model code affected by your implementation.
- The `workflow-hub` child instructions and `tt-content-strategy` skill plus its
  practice context. Apply implementation skills proportionately.
- Read-only business authority in sibling `restoration-business-operations`:
  `OPERATING_CONTROL_ROOM.md` and
  `business_planning/WORKSTREAM_01_SERVICE_BOUNDARY_AND_CLIENT_FIT_MATRIX.md`.
  Record a short claim/source ledger in your report; transfer only approved
  public practice facts. No private addresses, coordinates, client exceptions,
  finances or operating records belong in the website or report.

## Boundaries and ownership

You are the sole implementation writer while this assignment runs. Task 20
is approved but queued until your work and checks are ready. Preserve the
pre-existing `PROJECT_MEMORY.md` edit and requester-owned request document.
The hub alone edits this brief and `task-register.md`; do not edit them or
switch branches. Leave photos, galleries, journals and inventories unchanged.

Preserve the disabled inquiry control. No prices, booking availability,
turnaround guarantees, credentials, client work, or regulated-trade claims.
WS08/A-06 remains paused. Do not edit the separate business repository.
Do not update `website/content/reviews/pilot.json`, promote a release, commit,
push, deploy or open intake. Expected review staleness must be reported.

## Deliver and verify

Deliver the local candidate plus
`docs/website-workflow/reports/task-19-services-assessment.md`.
Use scoped Node 24.21.0. Run established website tests, candidate build/output
checks, relevant Markdown lint and `git diff --check`. Inspect the actual
changed page at desktop and 390-pixel width and follow the service-to-project
links. Save screenshots of the rendered copy for review; report exact output
counts, commands, changed files and any unrun checks. Keep testing proportionate.

If a loopback preview server is needed, first inspect port ownership, start
your own on an available port, and report its PID/port/directory for Task 20
to reuse. Do not stop an unrelated server. Keep generated outputs ignored.

Save the report, rename this child to
`Website 3 - Task 19 Services and Assessment - READY FOR REVIEW`, and return a
concise result. The hub observes via `wait_threads` and reconciles the report;
no callback or additional task is needed. Do not implement Task 20 yourself.
