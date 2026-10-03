# Content Cleanup 1 - Task 02 El Toro Film Format

Brief revision: 1. Execution approved October 3, 2026 by Shawn's "start task 2"
in hub turn `01a10326-b1f3-77a2-8bdf-bee7aeaac81d`.

- Hub: `01a062b2-cd26-7552-a5f9-3996acac6392`, TradeJournals Content Review Parent.
- Child: `01a10326-eb2a-72c3-842d-4eaf224f98f2`.
- Workspace: existing TradeJournals checkout; same-directory fork, shared files.
- Branch: `codex/concept-b-homepage`.
- Baseline: `20201aa8bc1fa5b21b9141938b0b2619d7a2f558`, clean before preparation.
- Dispatch: `TJ-CC-T02-D01`.
- Hub register: `docs/content-review-workflow/task-register.md`, hub-owned.

## Assignment

Resolve or accurately qualify the El Toro 35mm classification versus `(120)`
film-label conflict. Keep this lean: evidence review and narrowly scoped prose,
not tooling, bulk catalog changes, or a new research framework.

Read current instructions, `PROJECT_MEMORY.md`, workflow-hub instructions,
`docs/content-review-workflow/reports/task-03-el-toro-pinhole.md`, and the El Toro
material in `05_the_lens/trade_journals/lomography_film_album_catalog.md` and
`05_the_lens/trade_journals/flickr_lomography_overlap_archive.md`.

Trace whether the 35mm classification reflects Shawn's explicit correction or
another source. Do not override a user-confirmed film format with a platform
label. Camera model, scanner metadata, image shape, and album titles alone do
not settle film format. Verify relevant public source metadata read-only where
useful, preserving attribution and uncertainty. If authoritative evidence is
insufficient, ask Shawn the specific question needed rather than guess.

Authorized edits: El Toro-specific classification and explanatory prose in the
two journals above, plus this task's completion report. Preserve other albums,
accepted visual critique, source identities, and the seven-versus-ten album
coverage distinction. Do not rewrite historical review reports. Do not edit
inventories, external albums, website files, hub register, or parent brief.

## Deliverables and checks

- A supported resolution, or explicit source-attributed uncertainty with the
  exact missing fact needed from Shawn. Do not claim resolution without evidence.
- Report `docs/content-review-workflow/reports/cleanup-02-el-toro-film-format.md`,
  ID `TJ-CC-T02-R01`, revision 1: evidence, decision, exact scope, checks, gaps,
  branch/HEAD and Git status.
- Run `npm run lint:md`, `npm run check:site-evidence`, and `git diff --check`.
  Review the diff to ensure unrelated albums and accepted image reviews survive.

No Git commit/push, deployment, merge, next task, dependency changes, or private
business/customer data. Preserve all other chats' changes in this shared checkout.

## Return

When review-ready, save the report and rename the exact child to
`Content Cleanup 1 - Task 02 El Toro Film Format - READY FOR REVIEW`.
Show Shawn the result and ask permission before sending a completion message to
the exact hub. Kickoff is not return-message authorization. If clarification is
needed, report BLOCKED with the narrow question. Acceptance, report delivery,
Git closeout, and future tasks remain separate gates.
