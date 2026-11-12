# Website 3 - Task 26 Studio Website Refresh

Workflow status: COMPLETE — accepted by Shawn November 12, 2026.
Execution approval: RECEIVED November 12, 2026; Task 25 verified by the hub.
Brief revision: 2, updated November 12, 2026.
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` — website updates.
Child: `01a1d0aa-7b06-7d11-8e18-608ac75048c1`.
Dispatch: `WK-WEB-T26-D01` — completed.
Report `WK-WEB-T26-R01`, revision 1, RECEIVED; accepted as `WK-WEB-T26-A01`.
Hub reconciliation: `WK-WEB-T26-H01`.
Subsequent release/Git closeout authorized in the hub November 12; original
implementation exclusions below describe the submitted candidate checkpoint.
Task 25 report `WK-WEB-T25-R01` revision 1 accepted as `WK-WEB-T25-H01`.
Register: [website task register](task-register.md).
Workspace: TradeJournals shared checkout; refresh state at dispatch and preserve
other work. Only one website child writes implementation files at a time.
Dependency: Task 25 verified by the hub. Shawn authorized both remaining tasks
on November 12 in hub turn `01a1d0a5-9e99-7d02-980d-99f6ac3e2058`: “use
workflow-hub and start the remaining tasks.” This supersedes the November 11
pause and the proposed separate start-approval gate. No repeated start approval
is needed; the hub dispatches this child after Task 25 verification.

## Objective and approach

Apply the accepted Studio history and selected photographs using the existing
Astro content records and shared gallery. Keep the restoration, floors and
woodwork central; use the reopening as concise project context. No redesign,
new page, gallery feature, dependency, dashboard work or bulk album import.

## Approved work after dependency verification

1. Read Task 25's accepted report, current website README, selected-media
   examples and existing importer guidance. Refresh Git state and inspect the
   approved input files. Do not treat this prepared brief as start approval.
2. Bring only the three accepted new photographs into the established local
   asset/media-record structure. Keep durable photo IDs, album provenance,
   capture dates and appropriate captions/alt text. Use existing image sizing
   conventions; verify the actual output images load. Preserve older assets.
3. Update `website/content/projects/living-room-studio-restoration.json` and
   its story. Present five selected images: the two retained condition/process
   views and three accepted result/details. Distinguish late-summer restoration
   completion from subsequent decoration and the November 7 reopening.
4. Reconcile the earlier studio's project and story labels so they no longer
   contradict the new studio record. Proposed labels are “Barre Studio —
   Restored Living Room” and “Earlier Barre Studio,” subject to Task 25 review.
   The existing occupancy values already support `current`, `future`, and
   `former`; use the accepted evidence without changing the schema. Preserve
   both project IDs/routes, separate album ownership, dedicated Office record,
   older door evidence and unresolved historical door dates.
5. Check the affected homepage card, project pages, journal pages, archive
   search and derived descriptions for consistent room names and dates. Update
   current maintenance guidance as needed; retain dated historical reviews.
   Keep the existing source-album links secondary to the local gallery.
6. Deliver a local candidate and representative desktop/mobile screenshots for
   review. Do not refresh the approved release snapshot during implementation.

## Acceptance and verification

- Five Studio images load in the existing gallery and enlarged view; captions,
  source links, Escape/close and focus restoration work on desktop and mobile.
- Source-backed late-summer completion and later reopening appear consistently.
  There is no invented exact move date or claim about the earlier room's new use.
- Current public copy does not retain contradictory “future studio” / “move
  has not occurred” statements. Historical source observations remain dated.
- Existing routes, historic-home focus, own-home attribution, other project
  selections, inquiry state and gallery design are preserved.
- Using the scoped Node runtime from the README, run `npm run test:website`,
  `npm run check:website`, applicable Markdown lint and `git diff --check`.
  Add or adjust tests only for a meaningful behavior affected by the update.
- Inspect generated affected pages and search results, plus desktop and
  390-pixel views. Record snapshot drift as expected pending review; do not
  mark changed content approved to make release checks pass.

Verify any existing local preview server's ownership and output before reuse;
never stop another task's server. Record the preview URL and server identity.

## Return and later gates

Save `reports/task-26-studio-website-refresh.md`, report `WK-WEB-T26-R01`,
revision 1, with changed files, checks, preview/screenshots and review state.
Use READY FOR REVIEW and return to the exact hub. Only the hub edits the
register. The hub observes the report via wait_threads; no callback is needed.

After Shawn accepts the exact candidate, separately obtain authorization to
refresh the release snapshot, validate the portable release, and complete Git
closeout to the established destination. No release promotion, commit/push,
public deployment, hosting change or inquiry activation is authorized now.
