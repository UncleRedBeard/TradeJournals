# Website 2 - Task 15 Integrated Release Review

Workflow status: COMPLETE — accepted by Shawn; hub review reconciled
Brief revision: 1
Approval: Shawn said `kick off task 15` in website updates on October 3, 2026.
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` / website updates
Child: `01a10263-fe12-7673-bb16-067cb5e4f7ff`
Dispatch: `WK-WEB-T15-D01` — SENT once; active execution verified
Register: [task-register.md](task-register.md)

Exact idle child verified before dispatch. Fresh wait confirmed active turn
`01a10265-f4d4-7e71-9475-8e4261b9216b` after dispatch.

## Objective

Verify the complete accepted Concept B website as one coherent static release
and leave a concise, reproducible readiness record. Confirm the repository can
produce the site without private dashboard services or local-only generated
files. Make only bounded fixes for concrete verification failures and update
the existing maintainer/release documentation where it is stale.

This is approved execution. Reuse the settled design and existing verification
tools; do not restart design discovery or build enterprise release machinery.
The site should stay practical, understated and maintainable.

## Starting State And Ownership

Same-directory fork in
`/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/TradeJournals`, on
`codex/concept-b-homepage` at `ef1d5e8303860d49b7ae6131b0596e2bce38660b`.
Tasks 12-14 are approved COMPLETE; their implementations are committed and
pushed. Hub verified HEAD/tracking/FETCH_HEAD equality and `0 0` after Task 14.
The 11 approved completed chats are archived, with files and reports retained.

The content-review workflow is independently running La Ciotat Task 07 and owns
its register, brief and any source-journal changes. Refresh Git state before
editing and reporting. Preserve other work; do not stage, revert or rewrite it.
Only the hub edits this brief and the website task register.

## Read First

- `website/README.md` and `website/docs/pilot-editorial-review.md`.
- Task 12-14 briefs and reports in this workflow directory.
- Task 08/11 release-readiness reports for the existing fresh-checkout method.
- Current package scripts, output checker and review comparison implementation.
- Applicable repository instructions and workflow-hub and verification guidance.
  Use senior-developer guidance only if implementation fixes are needed.

Prior baseline: 121 Node and 37 Python tests passed. Preview and release contain
18 pages, 52 files, 318 checked references. The review snapshot file hash was
`cdc69b8b5c95af1e05677e9a1639287fd5b8886ab0872ce9adc3bc71dcd5699f`, current
with zero changed keys. Verify fresh; do not copy old results as current proof.

## Verification Scope

1. Run full website tests, preview build/check and guarded release build using
   scoped Node 24.21.0 and documented Python requirements. Independently check
   both retained outputs against their matching prepared models. Confirm review
   state and saved snapshot bytes. Run Markdown lint and whitespace checks.
2. Inspect representative homepage, project/gallery, long/short journal and
   archive/search routes together in the browser on desktop and phone widths.
   Check image loading, full-image presentation, readable headings/body/captions,
   no horizontal overflow, shared navigation and keyboard focus/skip links.
   Use the output checker to cover routes/links beyond the representative UI
   sample. Document actual sample and limitations; do not claim a full audit.
3. Verify matching, empty and no-match searches plus the static fallback when
   scripts/data are unavailable, using the existing lightweight approach.
   Confirm dynamically inserted results are styled and Office/current studio
   remain distinct. Keep query matching/ranking and text-safe rendering intact.
4. Verify both preview and release behavior: preview notice and noindex stay in
   preview; release has neither. Inspect the actual release package for private
   journals, inventories, Workbench data, runtime files or local filesystem paths.
   Keep local fonts and their license intact. No hosting-provider setup is needed.
5. Reproduce a release from a fresh isolated checkout of the committed baseline
   using documented installation and locked dependencies. Do not copy runtime,
   node_modules, generated data or build output from this shared checkout.
   An npm package cache is acceptable. If fixes are needed, overlay only the
   exact reviewed patch and identify it. Keep scratch work outside the shared
   checkout; do not delete user files or unrelated worktrees.
6. Correct documentation that could mislead a new maintainer. In particular,
   the new Concept B work is on `codex/concept-b-homepage`; `main` still has the
   prior release. Document how to obtain the current candidate without implying
   it is merged. Confirm full-repository, runtime, domain-root and dist-only
   upload requirements. Reuse existing docs instead of duplicating a runbook.

Fix small, demonstrated issues within this scope and recheck affected behavior.
If a fix needs new content decisions, substantial redesign or broader features,
report it to the hub rather than expanding the assignment.

## Preserved Decisions

- Craftsman first; historic homes/woodwork lead; other work stays secondary.
- Approved homepage, shared frame, project and journal/archive design remains.
- Keep Work & Craft navigation, existing routes, selected media and story copy.
- Future barre studio/former living room, current studio and Office remain
  separate; move is unconfirmed. Preserve approved window and evidence wording.
- Inquiries stay disabled. No email address, form service or backend invented.
- Do not update source journals, inventories or the reviewed fingerprints.
  If concurrent source work makes the snapshot stale, identify exact changed
  keys and return that decision to the hub; do not conceal it by refreshing.
- No hosting purchase/configuration, DNS, upload/deployment, CI, CMS, new runtime
  framework, Git commit/push/merge or archival is authorized by this task.

## Deliverables And Return

Produce a concise report distinguishing verified local release readiness from
remaining hosting/domain/inquiry decisions. Include exact revision, changes,
test/build results, snapshot state, clean-checkout proof, package boundaries,
desktop/phone screenshots, working review links and any limitations/blockers.
Use the existing loopback preview at `http://127.0.0.1:8139/` if it is serving
the correct output. Inspect listeners before reuse; leave other servers alone.
Provide a separate loopback release review if needed.

Apply dispatch `WK-WEB-T15-D01` once and update title to
`Website 2 - Task 15 Release Review - IN PROGRESS`. Read this brief before work;
it is newer than the fork's completed history. Save report `WK-WEB-T15-R01`,
revision 1, to `docs/website-workflow/reports/task-15-integrated-release-review.md`.
Rename to `Website 2 - Task 15 Release Review - READY FOR REVIEW`, send the
report to the exact hub, and request reconciliation and Shawn's acceptance.
No next-stage work starts automatically. Keep all material in this authorized
project environment.

## Acceptance And Hub Reconciliation

Report `WK-WEB-T15-R01`, revision 1, received once and reconciled as
`WK-WEB-T15-H01` on October 3, 2026. Shawn directly said `looks good...approved`
in the exact child, turn `01a10277-dae3-71a3-bc1c-4da9945ad307`;
the hub read and verified that approval (`WK-WEB-T15-A01`).

The hub reviewed the documentation diff, clean-checkout proof, test logs,
dependency assessment and representative screenshots. Child verification records
121 Node and 37 Python tests passing in both checkouts. Hub independently checked
both retained outputs with matching models: 18 pages, 52 files and 318 references
each; review state current with zero changed keys. All 52 files in each output
match the fresh checkout byte for byte. No implementation fix was needed.

Concurrent La Ciotat closeout advanced HEAD to `082520c`; it changes no website
files. The release proof remains anchored to `ef1d5e8`. Task 15 documentation
and hub bookkeeping remain uncommitted. Three high audit package findings in
build dependencies remain a maintenance follow-up; none ships in the verified
static artifact. Hosting/domain, Git integration, deployment and inquiry
activation remain separate. No successor or archival is started.

## Task 15 Git Closeout Authorization

After Task 15 acceptance and hub reconciliation on October 3, 2026, Shawn said
`git er done` in website updates. This authorizes validation, commit and push of
the Task 15 brief/report, hub register, website README and release-review document
to the established `origin/codex/concept-b-homepage` branch. Earlier statements
that these documents remain uncommitted or that Git closeout is unauthorized
record the pre-closeout checkpoint. No merge, deployment, inquiry activation,
archival or successor task is included. Final commit and synchronization evidence
will be reported in the hub after the push.
