# SEO Readiness — Approved Two-Task Request

Request ID: `WK-WEB-SEO-20261006-01`
Requesting chat: `01a1118b-5382-7490-a139-217004cba7fc`
Receiving hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` — website updates
Date: October 6, 2026, America/Chicago
Coordination delivery: RECEIVED; receiving hub observed ACTIVE
Observed receiving turn: `01a111a8-3cfb-7de0-a3d7-2336e9ab17a6`

The request was sent once under the request ID above. A subsequent
`wait_threads` observation showed the hub's new turn in progress. Child creation,
dispatch, and acceptance are tracked by that hub and are not inferred from
message delivery.

The hub acknowledged both tasks. Shawn then added "let's not over-engineer
this" directly there. The newer active turn is
`01a111a8-e488-7ea3-bbb3-f229828ab024`; its observed response commits to two
small additions using the current layout and content files. The requesting
chat hands implementation coordination to the established hub.

This records the initiating request and audit evidence. It does not replace
the hub-owned [task register](task-register.md), child briefs, or review records.
Only the established hub assigns child IDs and edits its register.

## User Authorization

Shawn explicitly instructed the requesting chat:

> let's tackle the 2 high priority items you identified. use our
> workflow-hub and get started

This authorizes starting both bounded website improvements below through the
invoked workflow-hub procedure. Create user-visible child forks, record the
approval for each, and dispatch each once. Both tasks are approved now; run
them sequentially because the website's existing workflow shares one checkout.
Do not interpret completion as approval for additional work.

## Task 19 — Services and Assessment

Objective: help a homeowner understand suitable work, the preservation approach,
the relevant evidence, and how the normal assessment engagement begins.

- Add compact service and assessment content within the existing website
  design, preferring the homepage/practice area over new routes or redesign.
- Lead with historic wood floors, interior woodwork, and architectural-surface
  restoration. Represent supporting interior painting and shelving accurately
  where useful. Shelving fabrication follows an existing or accepted design;
  original design services are not offered.
- Explain the normal paid assessment and written deliverables using the
  approved service matrix. Do not invent prices, availability, turnaround,
  credentials, consultation guarantees, or free-estimate promises.
- Connect services to relevant existing approved project pages using descriptive
  links. Identify linked residential evidence as Shawn's own-home work. Do not
  imply that photographs prove concealed conditions or regulated-trade services.
- Preserve the disabled inquiry action. Present the assessment process without
  implying that bookings or paid delivery are already open.
- Keep copy editable through established content conventions and preserve the
  existing content validation and review boundary.

Acceptance: the generated candidate visibly explains services, paid assessment,
written deliverables, and relevant project evidence. Verify the service-to-proof
path, accurate claims, working local links, and desktop/mobile presentation.

## Task 20 — Regional Service Context

Objective: let homeowners determine whether their community is within the
practice's intended service focus.

- Add concise visible regional wording in a suitable existing practice area
  and, if useful, the shared footer without duplicative town lists.
- Name Brenham, Somerville, Bastrop, Schulenburg, and La Grange naturally.
- Preserve the qualified regional model: acceptance depends on project fit,
  travel, scheduling, cost, and capacity. The approximately 50-mile planning
  radius is not guaranteed coverage; naming the towns is sufficient if it
  avoids suggesting an unexplained public radius center.
- Do not publish the private center coordinates or home address, imply offices
  or completed jobs in each town, or create town-specific landing pages.
- Keep text consistent with Task 19 and avoid promises that intake is open.

Acceptance: regional wording appears in generated HTML and the rendered page,
reads naturally at desktop and 390-pixel width, and agrees with current approved
territory decisions without private location details or coverage guarantees.

## Sources and Audit Baseline

- Workspace: `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/TradeJournals`.
- Observed branch: `main`; HEAD `41c4dbf2893018a0daff7f917893a0c16298fcfb`.
- Pre-existing unrelated change: `PROJECT_MEMORY.md`; preserve it.
- Website instructions: `website/README.md` and applicable project instructions.
- Implementation sources: `website/src/pages/index.astro`,
  `website/content/home.json`, `website/content/site.json`,
  `website/content/services/historic-floors.json`, and shared frame components.
- Current business authority, read-only, is the sibling
  `restoration-business-operations/OPERATING_CONTROL_ROOM.md` and
  `business_planning/WORKSTREAM_01_SERVICE_BOUNDARY_AND_CLIENT_FIT_MATRIX.md`.
  Transfer only approved public practice facts into website copy.
- Use Toil & Timber Marketing's `tt-content-strategy` and practice context.
  Apply other skills proportionately to the actual implementation.

The October 6 audit built fresh isolated preview and release outputs with scoped
Node 24.21.0. Both passed the existing checker: 20 pages, 60 files, and 363
references. All 20 preview pages had noindex; none of the release pages did.
Homepage, entry project, and archive rendered at 390 pixels without horizontal
overflow. Source/build inspection confirmed that service detail and assessment
process were not rendered and regional service wording was absent.

## Verification and Boundaries

Read current instructions and scripts before editing. Run the established
website tests and candidate build/output check, relevant Markdown lint, and
`git diff --check`. Review the actual rendered changed content on desktop and
mobile. Keep testing proportionate; expand it only for changes or failures.

Leave website changes as a reviewable local candidate. Do not update
`website/content/reviews/pilot.json` or claim the changed copy has received exact
release approval. If the changed content makes the reviewed snapshot stale,
report that expected condition rather than weakening the release gate.

Out of scope: the other SEO findings, image/gallery changes, journal corrections,
new marketing campaigns, domain/hosting decisions, profiles, contact activation,
production deployment, release promotion, Git commit/push, and changes to the
private business repository or its gates. WS08/A-06 remains paused; this fresh
website request does not resume it or unrelated deferred site directions.

The established hub owns task briefs, dispatch records, child acceptance, and
status reconciliation. Children own their assigned implementation and completion
reports. Report the resulting child IDs and actual started/queued states to the
requesting chat as part of this explicitly invoked coordination workflow. Do not
send repeated setup messages or start unrelated work.
