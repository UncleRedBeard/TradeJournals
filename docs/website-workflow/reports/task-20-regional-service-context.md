# Task 20 — Regional service context report

Report ID / revision: `WK-WEB-T20-R01`, revision 1. Supersedes: none.
Child: `01a111aa-b69c-7910-a163-8170fb3fe6a5`.
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` — website updates.
Dispatch: `WK-WEB-T20-D01`; [approved brief](../task-20-regional-service-context.md).
Approval: Shawn authorized both high-priority improvements October 6, 2026,
in requesting chat `01a1118b-5382-7490-a139-217004cba7fc`; request
`WK-WEB-SEO-20261006-01`. His latest direction was to avoid over-engineering.
Workflow status: READY FOR REVIEW; exact-copy acceptance remains pending.
Child title: `Website 3 - Task 20 Regional Service Context - READY FOR REVIEW`.
Report delivery: PENDING hub observation through `wait_threads`, as dispatched.

## Result

Added two sentences to the existing `home.intro` paragraph:

> The intended regional focus is Brenham, Somerville, Bastrop, Schulenburg,
> and La Grange. Acceptance will depend on project fit, travel, scheduling,
> cost, and capacity.

The regional context appears once in the existing **A craftsman's practice**
aside. The original introductory sentence and Task 19's three service selections
are preserved. No rendering, schema, model, style, route, dependency, or new
content field was necessary.

## Claim and source ledger

The current sibling business records were refreshed read-only on October 6.
Only approved public regional facts were transferred.

| Public statement | Authority | Treatment |
| --- | --- | --- |
| Five focus towns | `restoration-business-operations/OPERATING_CONTROL_ROOM.md`, Non-Negotiable Operating Boundaries; `business_planning/WORKSTREAM_01_SERVICE_BOUNDARY_AND_CLIENT_FIT_MATRIX.md`, Approved Foundation | Intended focus, without implying a local office or completed client jobs |
| Fit, travel, scheduling, cost, and capacity govern acceptance | The same approved territory paragraphs | Qualified future acceptance, without promising coverage or open bookings |
| Inquiries remain closed | Task 19 assessment text, disabled site contact, and current Control Room paused-work record | Existing statement and disabled control preserved |

Private center coordinates, home address, client exceptions, finances and
operating details were not transferred. WS08/A-06 remains paused.

## Verification

All commands used project-scoped Node 24.21.0. Full checks ran after the copy
change; a fresh candidate was built after the test suite.

| Check | Observed result |
| --- | --- |
| `npm run test:website` | PASS: 121 Node tests and 37 Python tests; `/tmp/task20-tests.log` |
| `npm run check:website` | PASS: 20 pages, 60 files, 366 references; `/tmp/task20-preview.log` |
| Generated homepage HTML | Exact intro present; each town and acceptance qualifier appears once |
| Desktop browser, 1440 × 1000 | Full regional paragraph readable within the existing aside; document width and scroll width both 1440 |
| Mobile browser, 390 × 844 | Full regional paragraph readable; document width and scroll width both 390; no horizontal overflow |
| Service-to-proof links | Current DOM retains Entry and Stair Restoration, Current Barre Studio, and Future Barre Studio links; full output checker validates references |
| Contact controls | All three existing Email us — coming soon controls remain disabled |
| Independent read-only copy review | PASS: all towns and qualifications, limited scope, no coverage/intake or private-location claims |
| Read-only release preparation | Expected `SOURCE_STALE` rejection; review fingerprints and release output not updated |
| Report Markdown lint and `git diff --check` | PASS |

Review state remains stale for `home:home`, `service:historic-floors`,
`service:interior-woodwork`, and `service:paid-assessment`. The review-record
SHA-256 remains `d69779edcd6ded04951bc729d89be0757aa91ebd8b035607ab94c99ad85b9f4f`.

### Preview evidence

- [Local homepage preview](http://127.0.0.1:8143/).
- [Desktop screenshot](/Users/shkelley/.codex/visualizations/2026/10/06/01a111aa-b69c-7910-a163-8170fb3fe6a5/task-20-desktop.jpg).
- [Mobile screenshot](/Users/shkelley/.codex/visualizations/2026/10/06/01a111aa-b69c-7910-a163-8170fb3fe6a5/task-20-mobile.jpg).

The existing loopback preview server was reused: PID `28601`, port `8143`,
bound to `127.0.0.1`. The served page was reloaded after the fresh build.
The temporary viewport override was reset. Automatic approval review rejected
marking the temporary browser tab as a persistent deliverable for lack of
explicit authorization. That optional action was omitted; screenshot saving
and viewport reset succeeded separately. The preview URL remains available.

## Changed paths and boundaries

Task 20 changes only `website/content/home.json`'s intro and this report.
The same home record also contains Task 19's preserved service selections.
All other Task 19 changes, the hub-owned register/briefs, requester-owned request,
and pre-existing `PROJECT_MEMORY.md` edit were preserved.

Shared checkout remains on `main` at
`41c4dbf2893018a0daff7f917893a0c16298fcfb`; changes are uncommitted.
No photos, journals, inventory, private repository, review record, contact
destination, or other SEO item was changed. No commit, push, release promotion,
deployment, or successor start occurred. No required checks remain unrun.

## Hub action requested

Review the concrete copy and preview, reconcile the hub-owned register, and
retain READY FOR REVIEW pending acceptance. Delivery is through this report
and the child's final result observed by the hub; no callback is sent.
Hub receipt is not yet observed. This report does not authorize Git closeout,
release approval, publication, or any further task.
