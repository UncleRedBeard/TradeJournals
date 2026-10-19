# Website 3 - Task 23 Entry Gallery Trial

Brief revision: 1. Execution approval: RECEIVED October 19, 2026.
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` — website updates.
Child: `01a1551b-1022-7c01-bf02-bf4f2a2c0f8f`.
Dispatch: `WK-WEB-T23-D01`. Report: `WK-WEB-T23-R01`, revision 1.
Workspace: TradeJournals shared checkout, `main` at `b65f0c1`; clean baseline.

## Approval and objective

Shawn directly instructed this hub: “let's run that test/trial on the existing
project you mentioned, Entry and Stair Restoration...don't over engineer and
follow our workflow established in workflow-hub”. This approves implementation
of the small trial proposed immediately beforehand. No repeat start approval
is needed. This is a local candidate for user review, not a site-wide rollout.

Improve the existing `/work/entry-restoration/` page so visitors can understand
the work and view its photographs without being sent away to an image host.
Use the current selected, locally stored images and the accepted site design.

## Bounded design

- Lead with the strong result/current-state photograph, then present starting
  condition and work/process with concise, useful captions or labels. Existing
  selection has three photographs with result, condition and process roles.
  Preserve truthful evidence: the entry records two restoration passes, so do
  not invent a single chronological before/after sequence or imply photographs
  prove more than they show. Existing images are sufficient for this first trial.
- Clicking a gallery image should enlarge it within the site. Use the smallest
  accessible implementation: keyboard activation, clear close action, Escape,
  focus restoration and a usable mobile fit. No carousel library, zoom/pan
  system, new dependency, automatic slideshow or broader gallery framework.
  A native dialog with minimal scripting is a reasonable implementation choice.
- Put a quiet “View the full source album” link below the Entry gallery rather
  than making the image or repeated original-source links the primary exit.
  Keep source provenance available and retain the TradeJournal link.
- Reuse the existing project page. Do not add another route or change homepage
  selections, the Entry journal presentation, other projects or their clicks.
  Shared components may accept a small explicit opt-in if needed; avoid global
  behavior changes or broad schema changes.

## Verification and boundaries

Read website/README.md, existing gallery/project/evidence components, the Entry
record and its referenced journal before editing. Apply relevant implementation
and verification skills proportionately; the user has approved the trial design
above. No internal subagents are needed for this small assignment.

Verify the Entry flow directly at desktop and 390 pixels: enlargement, close,
Escape/focus, source album link and retained journal navigation. Check one
non-trial project remains unchanged. Add proportionate behavior/regression
coverage and run established website tests, preview/output checks, relevant
Markdown lint and git diff --check. Record content snapshot state; do not
refresh reviewed fingerprints. Save screenshots and a usable local preview URL
for Shawn. An available loopback preview server is authorized for this review;
inspect ports before starting and do not stop another task's server.

No new image sourcing/downloads, source-journal edits, homepage changes, business
copy changes, contact activation, other-project rollout, release promotion,
commit/push, hosting purchase, DNS changes or deployment. Preserve concurrent
work if any appears. Only the hub edits its brief and central task register.

## Delivery

Save `docs/website-workflow/reports/task-23-entry-gallery-trial.md`, report
`WK-WEB-T23-R01`, revision 1, with changes, verification, screenshot paths,
preview URL, server identity and any limitations. Rename the child READY FOR
REVIEW. Use the final response and saved report for delivery; the hub observes
via wait_threads, so no callback is required. Acceptance remains with Shawn and
the hub; do not launch another task or perform Git closeout automatically.
