# Website 1 - Task 02 Office Content

Workflow status: IN PROGRESS (dispatch sent; active execution observed)
Execution approval: RECEIVED from Shawn: "start task 02" on September 16, 2026.
Hub ID/title: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` / website updates
Child ID: `01a0aa51-2176-75d2-8064-7a89390069c2`
Hub register: [task-register.md](task-register.md)
Brief revision: 1
Workspace: `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/TradeJournals`
Branch/isolation: `codex/website-updates`; same-directory fork, one website writer
Starting HEAD: `e16be25c6e7d2db3789e080145332b8dc97b771f`
Dispatch ID: `WK-WEB-T02-D01`

## Assignment

Implement only **Task 2: Office Content And Evidence Reconciliation** in the
[approved plan](../superpowers/plans/2026-09-15-worth-keeping-astro-pilot.md).
Read its global constraints, contracts and Task 2 in full, together with the
[design](../superpowers/specs/2026-09-15-worth-keeping-website-design.md) and
[accepted Task 01 report](reports/task-01-content-foundation.md).

Task 01 is complete and supplies `loadContent`, `validateContent`, and
`prepareSite`; use the existing implementation. Changes in that foundation,
the design, plan and hub documents are preexisting work. Preserve them.

Create the pilot records under `website/content/`: site, home, historic-floors
service, office-restoration project, ten selected media records, optional longer
story, and candidate review record. Add `website/docs/office-content-review.md`
and `website/tests/office-content.test.mjs` as specified in the plan. Do not
create Astro pages, components, build scripts, or Task 3 functionality.

## Editorial And Evidence Boundaries

- Follow the plan's exact ten-photo mapping and three-photo search subset.
  Retain original Flickr URLs, album identities and intentional differences
  between page and search copy. Reconcile both legacy HTML and catalog.
- Read the Office journal and the two referenced inventory blocks. Visually
  inspect all ten local assets using image viewing tools, and measure actual
  dimensions. Do not infer photographic contents from filenames alone.
- Write concise, supported candidate copy. The project is Shawn's residence;
  do not imply a client commission. Keep source-supported dates distinct from
  later documentation intake, and record unresolved interpretations clearly.
- Follow the plan's specific door-finish, photo identity and date qualifications.
  Avoid unsupported craft or service claims. If using sketchbook evidence,
  inspect the referenced page with the PDF skill and fingerprint that source;
  otherwise scope the public source label to the albums and journal.
- Keep review state `candidate`. Approval to perform this migration does not
  approve the final wording or photo interpretations. A proposed fingerprint
  snapshot is review material; no automatic promotion to reviewed is authorized.
- Preserve original journals, inventories, media and prototype byte-for-byte.
  Do not fetch additional photos or publish the master sketchbook.

## Proportional Implementation

Shawn wants "more tech savy than the average tradesman, but less flashy than an
influencer wanna be site." Keep copy plain and confident, centered on real
craftsmanship and visible work. Use the small existing content contract; do not
add a CMS, elaborate editorial workflow, new dependencies, or speculative features.
Contact configuration remains absent until its destination is chosen.

## Verification And Completion

1. Capture the starting source fingerprints and Git state. Confirm the approved
   branch before edits; if it drifts, ask this hub to reconcile it rather than
   switching branches or continuing on main.
2. Write focused migration tests for exact source/media identities, grouping,
   search subset and independent narrative/search copy. Verify the new records
   through the real `prepareSite` preview path. A release preparation must still
   reject the candidate snapshot.
3. Use the installed scoped Node 24.21.0 runtime for website tests. Run the full
   website suite, existing evidence consistency/site checks, authored Markdown
   lint and tracked/untracked whitespace checks. Verify original source bytes
   and the existing prototype remain unchanged. No visual webpage check is
   expected before Task 3; this task reviews source images and structured copy.
4. The worksheet accounts for each migrated image, original link, dimensions,
   alt text/caption/role decisions, intentional copy differences, and unresolved
   source questions. Identify specific items for Shawn's later content review.
5. Save a report, including exact changed paths, observed tests and limitations.
   Leave changes uncommitted; hub acceptance is separate from content approval.

Use workflow-hub child procedure and executing-plans for this bounded task;
apply relevant code/testing or PDF skills when their scope arises. Do not edit
the hub register or brief. Do not create more user-visible tasks, change the
Companion, or access its private storage. No commit, push or deployment.

## Return To Hub

Report ID: `WK-WEB-T02-R01`, revision 1.
Save to `docs/website-workflow/reports/task-02-office-content.md` using the
workflow-hub completion-report structure. Rename this child to
`Website 1 - Task 02 Office Content - READY FOR REVIEW` and verify readback.
Send its absolute report path and concise results to exact hub
`01a0a263-8d09-7ff2-8144-a71eb6ec16f6`, requesting reconciliation only. Reporting
is authorized by the user-invoked workflow-hub skill. Record delivery separately
from task outcome; do not claim receipt unless observed or launch Task 03.
