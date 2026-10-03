# Content Cleanup 1 - Task 04 SXSW Part 2

Brief revision: 1. Execution approval: Shawn's "kick off task 4" in the parent
hub on October 3, 2026 authorizes creation and scoped execution.

- Hub: `01a062b2-cd26-7552-a5f9-3996acac6392`, TradeJournals Content Review Parent.
- Child: `01a1037b-4747-7e43-a553-d72b1f4a70f6`.
- Workspace: existing TradeJournals checkout; same-directory fork/shared files.
- Branch: `codex/concept-b-homepage`.
- Baseline: `7f462a6626b1828698c15a181d2a824aeb988059`, clean before preparation.
- Dispatch: `TJ-CC-T04-D01`.
- Register: `docs/content-review-workflow/task-register.md`, hub-owned.

## Assignment

Resolve or accurately qualify SXSW 2011 Part 2's Diana Mini 35mm classification
versus `(120)` film label, and its 2010 metadata versus 2011 album title.
Keep this lean: bounded source review and prose correction, no new tooling.

Read current instructions, `PROJECT_MEMORY.md`, workflow-hub instructions,
`docs/content-review-workflow/reports/task-05-sxsw-part-2.md`, and Part 2 material
in `05_the_lens/trade_journals/lomography_film_album_catalog.md` and
`05_the_lens/trade_journals/flickr_lomography_overlap_archive.md`.

The reviewed representative is Flickr `5556961580`, visually matched to
Lomography `12915508` in album `1689993-sxsw-2011-part-2`. Recorded metadata
lists Diana Mini, Kodak Ektachrome 64T (120), Austin, 2010/night, with upload
date 2011-03-24. Both albums displayed seven images at the old review checkpoint.
Verify relevant public metadata read-only as needed; separate capture year,
upload date, album title, source film label, and user-confirmed physical format.
Do not infer capture dates from uploads or film format from image shape/scanner.
Shawn's Diana F+ to 120 clarification explicitly depends on the plus sign and
does not apply to Diana Mini. Preserve it and the accepted El Toro/Part 1 work.
If evidence cannot settle either question, ask Shawn the precise missing fact
rather than guess or silently replace source metadata.

Authorized edits: Part 2-specific classification and explanatory prose in the
two journals above, plus this task's report. Preserve accepted visual critique,
representative image, platform identities, URLs, and unrelated album content.
No broad camera rule changes, historical report edits, inventories, external
album writes, website changes, parent brief/register edits, or new journal.

## Deliverables and checks

- Evidence-supported resolution or explicitly attributed uncertainty for each
  conflict, with exact remaining questions where needed.
- Report `docs/content-review-workflow/reports/cleanup-04-sxsw-part-2.md`,
  ID `TJ-CC-T04-R01`, revision 1: sources, decisions, scope, uncertainties,
  checks, branch/HEAD, and worktree state.
- Run `npm run lint:md`, `npm run check:site-evidence`, and `git diff --check`;
  inspect actual diffs for preservation of unrelated content and accepted work.

No commit/push, merge, deployment, successor, dependency changes, or private
business/customer data. Preserve other chats' changes in this shared tree.

## Return

Save the report and rename the exact child to
`Content Cleanup 1 - Task 04 SXSW Part 2 - READY FOR REVIEW`.
Show Shawn the result and ask permission before messaging the exact hub.
Kickoff does not authorize report delivery. If clarification is necessary,
report BLOCKED with the narrow questions. Content acceptance, report delivery,
Git closeout, and later tasks remain separate gates.
