# Task 19 — Services and assessment report

Report ID / revision: `WK-WEB-T19-R01`, revision 1. Supersedes: none.
Child: `01a111aa-6c51-7a50-a0dc-1d6be2c0e65d`.
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` — website updates.
Dispatch: `WK-WEB-T19-D01`; [approved brief](../task-19-services-assessment.md).
Approval: October 6, 2026, in requesting chat
`01a1118b-5382-7490-a139-217004cba7fc`: “let's tackle the 2 high priority items
you identified. use our workflow-hub and get started”.
Workflow status: READY FOR REVIEW; copy acceptance and release remain pending.
Child title: `Website 3 - Task 19 Services and Assessment - READY FOR REVIEW`.
Report delivery: PENDING hub observation through `wait_threads`, as dispatched.

## Result

The homepage now has a compact **Services and assessment** section reached by
the existing Practice navigation link. Three columns become a single column
on mobile: historic floors, woodwork/interior surfaces, and the normal paid
assessment with written deliverables. Supporting painting and shelving stay
secondary; shelving is bounded to restoration or an existing/accepted design.

The section identifies the linked examples as work in Shawn's own home.
Historic floors links to Entry and Stair Restoration. Woodwork links to the
current barre studio and the former living room/future barre studio. These
illustrate documented materials and work, without implying client commissions
or proof of every listed service.

All editable service and assessment copy uses existing service records and
`home.serviceIds`. No schema, model, route, dependency or component abstraction
was needed. A valid empty service selection retains the Practice anchor on
the introductory aside. The existing review gate includes all three records.

## Claim and source ledger

Business authority was read from the sibling `restoration-business-operations`
repository; it was not edited. Only the following approved public practice
facts were transferred.

| Public statement | Authority and evidence |
| --- | --- |
| Historic floors, woodwork and architectural surfaces lead the practice; retain original material where practical | `OPERATING_CONTROL_ROOM.md`, non-negotiables; `business_planning/WORKSTREAM_01_SERVICE_BOUNDARY_AND_CLIENT_FIT_MATRIX.md`, Approved Foundation and Service-Boundary Matrix |
| Interior painting is supporting work; shelving uses an existing/accepted design; original design is excluded | Workstream 01, Approved Foundation and the painting/shelving rows in Service-Boundary Matrix |
| Paid assessment is the normal first engagement, with photographs, observations, risks/unknowns, options, phases and a written recommendation | Workstream 01, Approved Foundation, assessment row, Operating Dispositions, and referral boundaries |
| Entry floor evidence | `website/content/stories/entry-restoration.md`: documented floor renewal within the retained entry assembly |
| Door and interior surface evidence | `website/content/stories/studio-office-restoration.md`: retained door work; `website/content/stories/living-room-studio-restoration.md`: floor, shiplap, ceiling and trim work |
| Inquiries remain closed | Approved task brief, current disabled contact record, and paused WS08/A-06 in the control room |

No private addresses, coordinates, client exceptions, finances, credentials,
pricing, availability, turnaround promises or regulated-trade claims were added.
Room occupancy and project completion claims remain unchanged.

## Verification

Commands used the project-scoped Node 24.21.0 runtime:
`export PATH="$PWD/website/.runtime/node_modules/node/bin:$PATH"`.

| Check | Observed result |
| --- | --- |
| `npm run test:website` | PASS: 121 Node tests and 37 Python tests; `/tmp/task19-tests.log` |
| Focused rendering test after the hub's empty-selection finding | PASS: selected records, escaped text, linked evidence, unselected-record exclusion, and valid empty selection; `/tmp/task19-anchor-green.log` |
| `npm run check:website`, rebuilt after tests and final anchor fix | PASS: 20 pages, 60 files, 366 references; `/tmp/task19-preview.log` |
| Desktop browser, 1440 × 1000 | Three readable columns; existing typography, section framing and project presentation retained |
| Mobile browser, 390 × 844 | Single column; complete text readable; document width and scroll width both 390 pixels; no horizontal overflow |
| Service-to-project links | All three clicked and destination URL/heading verified: entry, current barre studio, future barre studio |
| Contact controls | All rendered Email us — coming soon buttons remain disabled; no form or mail link added |
| Release preparation, read-only `prepareSite({mode: "release", ...})` | Expected rejection `SOURCE_STALE`; no release output or fingerprint update |
| `./node_modules/.bin/markdownlint-cli2 website/README.md docs/website-workflow/reports/task-19-services-assessment.md` | PASS: zero issues |
| `git diff --check` | PASS |

The full suite ran before the one-line empty-selection anchor correction;
the focused rendering test and candidate build/output checks ran afterward.
That regression test first reproduced `BROKEN_FRAGMENT` with no selected
services, then passed with the fallback anchor. The initial service-rendering
test also failed before implementation and passed afterward. An old content
test's sole-service assumption was updated to retain the actual requirement:
historic floors lead the selection, while identity and disabled-contact checks
remain intact. Independent read-only copy review found no claim or source-boundary
concerns.

Review state is stale for exactly `home:home`, `service:historic-floors`,
`service:interior-woodwork`, and `service:paid-assessment`. The unchanged review
record SHA-256 is
`d69779edcd6ded04951bc729d89be0757aa91ebd8b035607ab94c99ad85b9f4f`.

### Browser evidence and preview

- [Preview the section](http://127.0.0.1:8143/#practice).
- [Desktop screenshot](/Users/shkelley/.codex/visualizations/2026/10/06/01a111aa-6c51-7a50-a0dc-1d6be2c0e65d/task-19-desktop.jpg).
- [Mobile services screenshot](/Users/shkelley/.codex/visualizations/2026/10/06/01a111aa-6c51-7a50-a0dc-1d6be2c0e65d/task-19-mobile.jpg).
- [Mobile assessment screenshot](/Users/shkelley/.codex/visualizations/2026/10/06/01a111aa-6c51-7a50-a0dc-1d6be2c0e65d/task-19-mobile-assessment.jpg).

The temporary viewport override was reset after review. The loopback server
remains available for Task 20: PID `28601`, port `8143`, bound to `127.0.0.1`,
serving `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/TradeJournals/website/.preview-dist`.
This task started it after checking that the port was unused; no unrelated
server was stopped. Rebuild and reload after Task 20's changes.

## Changed paths and boundaries

Task 19 owns these changes:

- `website/README.md`
- `website/content/home.json`
- `website/content/services/historic-floors.json`
- `website/content/services/interior-woodwork.json` (new)
- `website/content/services/paid-assessment.json` (new)
- `website/src/pages/index.astro`
- `website/src/styles/atelier.css`
- `website/tests/office-content.test.mjs`
- `website/tests/rendering.test.mjs`
- `docs/website-workflow/reports/task-19-services-assessment.md` (this report)

Shared checkout remains on `main` at
`41c4dbf2893018a0daff7f917893a0c16298fcfb`. Changes are uncommitted.
Pre-existing `PROJECT_MEMORY.md`, hub register/briefs, and requester-owned SEO
request were preserved. Photos, galleries, journals, inventories and project
records were not changed. `website/content/reviews/pilot.json` is untouched.
Generated preview output remains ignored.

No commit, push, deployment, inquiry activation or Task 20 implementation was
performed. No required implementation/browser checks remain unrun. Candidate
copy acceptance, review refresh and release are later hub-owned decisions.

## Hub action requested

Review this report and candidate, reconcile the hub register, and accept only
against the agreed scope. Per dispatch, delivery is through this saved report
and the child's final result observed by the hub; no callback message is sent.
Hub receipt is not yet observed. This report authorizes no successor dispatch,
Git closeout or publication.
