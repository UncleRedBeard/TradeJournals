# Content Cleanup 1 - Task 03 SXSW Part 1 Film Format

Brief revision: 1. Execution approval: Shawn's "kick off task 3" in the parent
hub on October 3, 2026. Creation and scoped execution are authorized.

- Hub: `01a062b2-cd26-7552-a5f9-3996acac6392`, TradeJournals Content Review Parent.
- Child: `01a10354-9e64-7620-954d-0feabdda7a31`.
- Workspace: existing TradeJournals checkout, same-directory fork/shared files.
- Branch: `codex/concept-b-homepage`.
- Baseline: `aa9d4c8f8d0ec8d02cd2e4a48b627e6f6b4e76d5`, clean before preparation.
- Dispatch: `TJ-CC-T03-D01`.
- Register: `docs/content-review-workflow/task-register.md`, hub-owned.

## Assignment

Resolve or accurately qualify the SXSW 2011 Part 1 Diana F+ 35mm classification
versus Kodak Ektachrome 64T `(120)` metadata conflict. Keep it lean: bounded
source review and prose correction, no tooling or catalog-wide reassessment.

Read current instructions, `PROJECT_MEMORY.md`, workflow-hub instructions,
`docs/content-review-workflow/reports/task-04-sxsw-part-1.md`, the current Part 1
material in `05_the_lens/trade_journals/lomography_film_album_catalog.md` and
`05_the_lens/trade_journals/flickr_lomography_overlap_archive.md`, and the accepted
El Toro cleanup report for the limits of that separate correction.

The reviewed representative is Flickr `5556099221`, visually matched to
Lomography `12915139` in album `1689964-sxsw-2011-part-1`. Recorded metadata
lists Diana F+ and Kodak Ektachrome 64T (120). The historical review did not
refresh the catalog's nine/eight camera-count split. Verify public metadata
read-only as needed; distinguish physical film format from platform labels and
scanner metadata. Do not extrapolate Shawn's El Toro clarification to SXSW.
If reliable evidence cannot settle the format, ask Shawn the narrow question
needed rather than guess. Preserve existing Agfa Isolette attribution and
qualify any unverified count instead of inventing a new split.

Authorized edits: SXSW Part 1-specific format/classification prose in the two
journals above and this task's report. Preserve accepted visual observations,
representative image, source identities, and unrelated albums, including El
Toro and SXSW Part 2. No external album writes, inventories, website changes,
historical report rewrites, parent brief/register edits, or broad rule changes.

## Deliverables and checks

- Supported resolution or explicit source-attributed uncertainty and the exact
  missing fact for Shawn. Do not claim a format resolved without evidence.
- Report `docs/content-review-workflow/reports/cleanup-03-sxsw-part-1-film-format.md`,
  ID `TJ-CC-T03-R01`, revision 1, recording evidence, decision, scope, gaps,
  checks, branch/HEAD, and worktree state.
- Run `npm run lint:md`, `npm run check:site-evidence`, and `git diff --check`;
  inspect the diff for preservation of accepted critique and unrelated albums.

No commit, push, merge, deployment, successor task, dependency changes, or
private business/customer data. Preserve other chats' changes in the shared tree.

## Return

Save the report and rename the exact child to
`Content Cleanup 1 - Task 03 SXSW Part 1 Film Format - READY FOR REVIEW`.
Show Shawn the result and ask permission before messaging the exact hub.
Kickoff does not authorize report delivery. If clarification is needed, report
BLOCKED with the narrow question. Content acceptance, report delivery, Git
closeout, and future tasks remain separate gates.
