# Website 3 - Task 20 Regional Service Context

Brief revision: 1. Execution approval: RECEIVED, October 6, 2026.
Workflow status: COMPLETE; accepted October 6, 2026 (`WK-WEB-T20-A01`).
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` — website updates.
Child: `01a111aa-b69c-7910-a163-8170fb3fe6a5`.
Dispatch: `WK-WEB-T20-D01` (SENT once; completed idle turn verified by hub).
Report: `WK-WEB-T20-R01`, revision 1.
Workspace: TradeJournals shared checkout, branch `main`, base `41c4dbf` plus
Task 19's reviewed local candidate. Keep Task 19's uncommitted work intact.

## Approval and scope

Shawn authorized both high-priority improvements in chat
`01a1118b-5382-7490-a139-217004cba7fc`: “let's tackle the 2 high priority items
you identified. use our workflow-hub and get started”. See
[the approved request](seo-readiness-request-2026-10-06.md),
`WK-WEB-SEO-20261006-01`. Latest hub instruction: “remember... let's not
over-engineer this”. Task 20 starts on one hub dispatch once Task 19 stops
writing; no repeat start approval is required.

Add a short paragraph in the existing practice area naming Brenham, Somerville,
Bastrop, Schulenburg and La Grange as the intended regional focus. Qualify
acceptance by project fit, travel, scheduling, cost and capacity. Keep it
natural and consistent with Task 19 and the disabled inquiry control.
One clear placement is preferred. Do not repeat town lists in multiple places.
Do not publish a radius center, address or coordinates, imply offices or past
client jobs in each town, or promise coverage or open bookings.

Task 19 is READY FOR REVIEW and idle; the hub checked its implementation,
screenshots, tests and output. Its three service blocks need no schema/model
changes. Preview server: port 8143, PID 28601, serving `website/.preview-dist`.
First consider the existing `home.intro` field for the concise regional text;
only introduce a separate field if actual readability requires it. Do not
misclassify regional coverage as a fourth service card. No new routes, maps,
dependencies, schema markup, campaigns, town pages or framework changes.
Only change rendering/validation if actually required for the small copy field.
This is a bounded copy addition within the approved visual design.

## Read first and preserve

- `website/README.md`, the approved request, Task 19 brief/report, current
  candidate content and the established homepage rendering.
- `tt-content-strategy` and its practice context; `workflow-hub` child procedure.
- Read-only current business authority in sibling
  `restoration-business-operations/OPERATING_CONTROL_ROOM.md` and
  `business_planning/WORKSTREAM_01_SERVICE_BOUNDARY_AND_CLIENT_FIT_MATRIX.md`.
  The flexible planning radius is not a public coverage guarantee. Transfer
  only approved public facts; record a short source note in the report.

Hub owns briefs/register. Preserve the requester-owned request document,
pre-existing `PROJECT_MEMORY.md` edit, all Task 19 files and other tasks' work.
No branch switch, photos, journals, inventory changes, contact activation or
private business-repository edits. WS08/A-06 remains paused. No review-snapshot
refresh, release promotion, Git closeout, deployment or other SEO findings.

## Deliver and verify

Deliver the local candidate and
`docs/website-workflow/reports/task-20-regional-service-context.md`.
Use scoped Node 24.21.0 and run established website tests and candidate
build/output checks, relevant Markdown lint, and `git diff --check`.
Verify all five towns and qualifiers in generated HTML and in the page at
desktop and 390-pixel width. Save final screenshots, verify disabled contact
and service links remain correct, and report expected review staleness without
altering the snapshot. Reuse Task 19's verified preview server if available.
Keep tests proportionate; do not add tests that merely restate the copy.

Save the report, rename to
`Website 3 - Task 20 Regional Service Context - READY FOR REVIEW`, and return
the concise result. Hub observes via `wait_threads`; no callback or successor
task is needed. User review of concrete copy/preview follows implementation.
