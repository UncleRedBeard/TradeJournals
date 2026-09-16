# Website 1 - Task 03 Astro Pages

Workflow status: COMPLETE (hub direct recovery; child remained paused)
Execution approval: RECEIVED; Shawn said "ok, let's get started on task 03".
Hub ID/title: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` / website updates
Child ID: `01a0aab2-36e1-78f3-8cff-20a2937e5ccc`
Hub register: [task-register.md](task-register.md)
Brief revision: 1; September 16, 2026
Workspace: `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/TradeJournals`
Branch/isolation: `codex/website-updates`; same-directory fork, one website writer
Starting HEAD: `505d34e44457e4d0b207b19620ad5489afbec349`
Dispatch ID: `WK-WEB-T03-D01`

## Assignment And Inputs

Implement only **Task 3: Reusable Astro Pages And Optional Search** in the
[approved plan](../superpowers/plans/2026-09-15-worth-keeping-astro-pilot.md).
Read its contracts, file map, Task 3 and the
[design](../superpowers/specs/2026-09-15-worth-keeping-website-design.md).
Tasks 01 and 02 are accepted and committed at the starting HEAD. Consume their
prepared public model and the existing records in `website/content/`.
Read the [Office content worksheet](../../website/docs/office-content-review.md);
its copy and selections remain candidate, not approved for release.

Create Astro configuration, semantic layout and focused components, style
tokens/base styles, pilot pages, safe Markdown policy/content collection,
browser search controller, build orchestration and focused tests from Task 3.
Routes are `/`, `/work/office-restoration/`, `/tradejournals/`,
`/tradejournals/office-restoration/`, and `/search.json`.

Implement ordered build stages 1–4. The dedicated output validator and full
acceptance sweep are Task 4; do not implement that task automatically. Task 3
still requires working-output inspection and generated-HTML regression tests.

## Presentation Direction

Shawn's standard is "more tech savy than the average tradesman, but less flashy
than an influencer wanna be site." Build a restrained craftsman's website:
real work and clear photographs, readable typography, straightforward navigation,
useful spacing, and minimal interaction. Avoid animation for decoration, generic
dashboard cards, marketing claims, or elaborate new abstractions/dependencies.

Use the approved Time & Timber Restoration identity and exact service line, green/limestone/
sage palette, Georgia and system sans-serif pilot fonts. Final wordmark typography
remains a later review choice. The earlier Horizon demo is not the design brief.

Inspect the accepted visual reference if helpful:
`/Users/shkelley/.codex/generated_images/01a0a20e-066f-75c3-bd48-667231c21a5f/exec-0286d5a3-6052-4427-8399-eec6533496c9.png`.
Its imagery is generated concept material. Do not copy it into project evidence
or replace selected real Office images with invented restoration photographs.

Keep technical implementation details out of visitor copy. Show the required
candidate preview notice clearly but quietly; preview metadata must include
`noindex`. Render no contact action or unfinished navigation destination when
its configuration is absent.

## Build And Content Boundaries

- Use scoped Node 24.21.0 and existing pinned Astro/Zod dependencies. Keep the
  global runtime and original prototype unchanged. No Dashboard or live-source
  dependency, UI framework, MDX, CMS, server adapter, or remote fonts.
- Components receive validated public data. Only selected assets enter fresh
  ignored staging; internal reports and source paths never enter public output.
- Reject unsafe Markdown before rendering; images and evidence links are
  controlled by validated components. Render only selected story IDs.
- Build preview under `.preview-dist`; release remains blocked by the current
  candidate snapshot. Do not mark content reviewed to make a release pass.
- Reuse the existing search ranker without editing it. Server-render the archive
  list; enhance it only when search is available. On failure preserve useful
  content. Use safe DOM text creation and validated destinations.
- Preserve journals, inventories, assets, original site, Tasks 01/02 content,
  and unrelated work. Report a necessary narrow integration adjustment rather
  than expanding scope. Never change branches; ask the hub to reconcile drift.

## Verification And Return

Use executing-plans for the approved bounded task and apply frontend-design,
senior-developer, and relevant test/verification skills. Do not reopen settled
design approval. Verify current Astro APIs against installed code or official
docs where needed. Run the website suite, candidate preview build, existing
evidence/search checks, Markdown lint and whitespace checks. Use synthetic
fixtures for reviewed release/order tests; keep real content unchanged.

Inspect the local generated pages in a browser when available, including a
mobile-width view and working archive search. Record observed results and any
unverified behavior precisely; Task 4 owns the comprehensive acceptance sweep.
Serve only on loopback, verify port ownership first, and preserve other servers.
The deliverable should include a usable local preview URL for Shawn to review.

Save report `WK-WEB-T03-R01`, revision 1, to
`docs/website-workflow/reports/task-03-astro-pages.md`. Include exact changed paths,
runtime, test/build results, preview access, limitations, and Git state. Leave
changes uncommitted. Do not edit the hub register/brief or start another task.
No commit, push, deployment or private Companion access is authorized.

Rename the child `Website 1 - Task 03 Astro Pages - READY FOR REVIEW` and verify
readback. Send its absolute report path and concise results to exact hub
`01a0a263-8d09-7ff2-8144-a71eb6ec16f6` for reconciliation only. Reporting is
authorized by the user-invoked workflow-hub skill. Keep delivery state distinct
from acceptance; the hub owns COMPLETE and future task dispatch.
