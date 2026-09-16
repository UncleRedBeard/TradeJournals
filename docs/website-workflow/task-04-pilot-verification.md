# Website 1 - Task 04 Pilot Verification

Workflow status: IN PROGRESS (dispatch sent; execution underway)
Execution approval: RECEIVED; Shawn said "start task 04" on September 16, 2026.
Hub ID/title: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` / website updates
Child ID: `01a0ab24-db71-75a0-b2d8-d4280528a596`
Hub register: [task-register.md](task-register.md)
Brief revision: 1
Workspace: `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/TradeJournals`
Branch/isolation: `codex/website-updates`; same-directory fork, one website writer
Starting HEAD: `7d023b9f06781bdf082acaa2e0c6fc15fbf1479e`
Dispatch ID: `WK-WEB-T04-D01`

## Assignment

Execute **Task 4: Static Output Verification And Pilot Review** in the
[approved plan](../superpowers/plans/2026-09-15-worth-keeping-astro-pilot.md).
Read its contract and Task 4 in full, the
[Task 03 report](reports/task-03-astro-pages.md), current build implementation,
and the [Office content worksheet](../../website/docs/office-content-review.md).

Task 03's current committed identity is **Time & Timber Restoration**, matching
`website/content/site.json`, its tests and the updated Task 03 brief. Preserve
that identity; do not restore older Worth Keeping wording from the original
architecture/plan. Preserve the exact service line and the existing understated
design. This is a practical quality pass, not a redesign or enterprise platform.

## Bounded Deliverables

1. Implement `website/scripts/check-output.mjs` and its focused tests, using
   `scripts/check_website_html.py` and Python `HTMLParser` for HTML references.
   Match the plan's exported interfaces. Verify actual emitted pages, images,
   local links/fragments and expected asset identities. Unexpected private/raw
   source files or unselected media must fail with a useful file/reference error.
2. Integrate the checker as the final build step, and add the planned root and
   website convenience commands. Successful Astro rendering alone must not
   declare a successful validated build. Keep the current scoped runtime.
3. Demonstrate the plan's maintenance scenarios with synthetic fixtures: changed
   summary, featured order and shared style; missing selected image; selected
   source change versus unrelated inventory change. Do not mutate real journals
   or accepted content to demonstrate failures.
4. Review the local static pilot in the browser at desktop and 390-pixel mobile
   widths, including home, project and archive. Check keyboard focus/skip link,
   legibility, cropping, overflow, source links, reading without JavaScript, and
   graceful search-data failure. Record exactly what was observed versus what
   tooling could not verify. Focused fixes for actual acceptance failures are
   in scope; unrelated features or visual redesign are not.
5. Document scoped Node setup, update ownership, build/preview commands and
   review/release boundaries in `website/README.md`; add the planned short
   pointer to `site_example/README.md`. Include an acceptance checklist with
   evidence and remaining content/visual decisions.

The existing local preview was served on loopback port 8126. Inspect its owning
process and directory before reusing it; use another available loopback port
if necessary and never stop another task's server. Return a working local
preview URL for Shawn's review. Use CUA browser tools for visual verification.

## Limits And Verification

Keep dependencies small; use existing Astro, Node and Python standard-library
facilities. No CMS, backend, authentication, analytics, deployment configuration,
paid services, new stock imagery, or private Companion access. Preserve the
original journal/inventory/media/prototype and leave source editorial questions
in the existing review worksheet. Keep components and visitor copy practical.

The real content remains candidate. Confirm release rejection and use an
invented reviewed fixture to prove the successful release path without a preview
notice or `noindex`. Do not mark Shawn's content approved on his behalf.

Run the full Task 4 checks once after the final changes: Markdown lint, legacy
evidence/search checks, Python suite, website tests, preview build, output checker
and tracked/untracked whitespace checks. Use scoped Node 24.21.0. Capture counts,
results and any remaining limitations. Confirm source preservation and branch.
Do not switch branches, commit, push, deploy or edit this hub register/brief.

Use workflow-hub child procedure, executing-plans, and applicable coding,
Python/testing and verification skills. Start actual implementation after the
approved dispatch; do not end with only a plan or acknowledgement. If blocked,
report the concrete failure to the hub with the last observed state.

## Return

Save report `WK-WEB-T04-R01`, revision 1, at
`docs/website-workflow/reports/task-04-pilot-verification.md`. Include exact
changed paths, commands/results, browser observations, preview access, remaining
review items and Git state. Leave work uncommitted for hub review.

Rename the child `Website 1 - Task 04 Pilot Verification - READY FOR REVIEW`
and verify readback. Send its absolute report path and concise results to exact
hub `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` for reconciliation only. Reporting is
authorized by the user-invoked workflow-hub skill. Keep delivery state separate
from acceptance; the hub owns COMPLETE. No next task is authorized.
