# Website 3 - Task 24 Sitewide Gallery Treatment

Brief revision: 1. Execution approval: RECEIVED October 19, 2026.
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` — website updates.
Child: `01a15545-ba05-7420-953c-615c51a1a29b`.
Dispatch: `WK-WEB-T24-D01`. Report: `WK-WEB-T24-R01`, revision 1.
Workspace: TradeJournals shared checkout, `main` at `4864feb`; clean baseline.

## Approval and scope

Shawn directly instructed this hub: “go ahead and expand the gallery treatment
site wide. same as before...don't over engineer...and use the workflow-hub
skill”. This approves starting implementation now; no repeat start question.
Task 23 is accepted and committed. Reuse its approved interaction and style.

Apply local enlargement and secondary source links consistently across all
nine existing `/work/[id]/` project galleries, including restoration, ceramics
and photography. Homepage/archive cards remain navigation into projects; journals
already link to their gallery pages and do not need duplicate galleries.

- Reuse the working native dialog and minimal script. Keyboard activation,
  close/Escape, focus restoration, local-image fallback, image fit, captions
  and mobile behavior remain required. No new viewer library, carousel,
  automatic slideshow, zoom/pan framework, dependency or route.
- Generalize the existing implementation with the smallest shared structure;
  avoid nine duplicated viewers or project-specific scripts. Preserve the
  accepted Entry presentation, its stage labels and two-pass explanation.
- Place the appropriate album link(s) below each gallery and individual photo
  provenance in a quiet disclosure. Preserve all established source URLs and
  source/output validation; support projects with multiple albums accurately.
- Use existing selected images, order, captions and alt text. Add concise
  labels/context only where the record supports them. Do not mechanically
  equate a stored result role with completed work or impose before/progress/
  finish chronology on photography, pottery or unfinished rooms. Existing
  captions may be sufficient. Preserve room distinctions and evidence limits.
- Preserve homepage selections, navigation, journals, own-home attribution,
  metadata, inquiries and the overall design. No new image sourcing/downloads,
  source-journal changes, unapproved selections or broad schema/model redesign.

## Verification and review

Read website/README.md, Task 23 implementation/report, all nine gallery records
and relevant source evidence for any added factual labels. Use applicable coding
and verification skills proportionately; this design is approved for rollout.
No internal agent delegation is needed for this bounded shared-component change.

Check every generated project gallery for correct local-image targets, source
provenance and gallery contents. Check all 20 routes for retained navigation,
metadata and preview behavior. Run established website tests, preview/output,
relevant Markdown lint and git diff --check. Review representative restoration,
ceramics and photography galleries at desktop and 390 pixels, including first
and later images, close/Escape/focus and source links. Recheck Entry for regressions.
Keep tests meaningful and bounded. Record snapshot state without refreshing it.

Produce a reviewable local preview and screenshots. Reuse the Task 23 loopback
preview at port 8143 if it still serves the same output; verify ownership first.
Do not stop another task's server. Save server identity in the report.

Only the hub edits this brief and central register. Preserve concurrent work.
No release promotion, snapshot refresh, commit/push, public deployment, hosting
change, contact activation or successor is authorized by this start request.

## Delivery

Save `docs/website-workflow/reports/task-24-sitewide-gallery.md` with report
`WK-WEB-T24-R01`, revision 1, scope, changed files, checks, preview/screenshots
and limitations. Rename READY FOR REVIEW. The hub observes the saved report
and final response via wait_threads; no callback is required. User acceptance
and Git closeout follow separately after review.
