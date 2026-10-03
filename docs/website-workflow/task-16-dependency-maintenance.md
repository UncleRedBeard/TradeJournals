# Website 2 - Task 16 Dependency Maintenance

Workflow status: COMPLETE — accepted by Shawn; hub review reconciled
Brief revision: 1
Approval: Shawn said `cool...sounds good...let's get back to it and start task 16`
in website updates on October 3, 2026.
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` / website updates
Child: `01a10290-90df-7271-9f3f-ad82cc5a8739`
Dispatch: `WK-WEB-T16-D01` — SENT once; active execution verified
Register: [task-register.md](task-register.md)

## Objective And Scope

Resolve Task 15's dependency-maintenance follow-up with the smallest compatible
change and verify that the accepted static website still builds and behaves
correctly. This is approved execution, not a request to reopen design discovery.

1. Refresh installed and locked dependency versions and obtain a current audit.
   Task 15 reported three high package findings: devalue, http-cache-semantics,
   and Astro's inherited finding. Distinguish package counts from advisories.
   Check upstream advisories, release notes and registry metadata; do not assume
   the old findings, patched versions or remediation suggestions remain current.
2. Apply supported compatible fixes where available. Prefer ordinary dependency
   and lockfile updates with minimal unrelated churn. Do not blindly use forced
   audit fixes, switch framework/runtime major versions, or suppress findings to
   claim a clean audit. A narrow transitive override requires documented upstream
   compatibility and actual verification. If a fix needs a substantial migration,
   report the tradeoff to the hub before expanding scope.
3. Verify the resolved tree after a locked clean install in an isolated scratch
   checkout or copy outside the shared source tree. Do not delete the shared
   node_modules or other owners' files. Preserve exact package changes needed to
   reproduce the result. Record unresolved findings, exposure prerequisites and
   available upstream fixes without implying a comprehensive security audit.
4. Run required website tests, preview and guarded release builds, output checks
   against each matching prepared model, Markdown lint and whitespace checks.
   Compare the release to the accepted baseline; explain any generated-output
   difference and sample representative desktop/phone routes and search if the
   framework or build output changes. Preserve the static fallback behavior.
5. Update current maintainer/release documentation only where needed, and save a
   concise report with before/after versions and audit findings, exact changes,
   command results, package boundary, remaining issues and review links if used.
   Preserve Task 15's dated report as historical evidence.

## Starting State And Ownership

Workspace: `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/TradeJournals`.
Branch: `codex/concept-b-homepage`; baseline
`f20572a2648cce9d7d386ccc105370d2307cc544`.
Task 15 is accepted COMPLETE and committed/pushed. Its closeout verified
HEAD/tracking/FETCH_HEAD equality, ahead/behind `0 0`, and then-clean source.

At Task 16 preparation, concurrent content-review work has modified
`docs/content-review-workflow/task-register.md` and added
`docs/content-review-workflow/task-08-la-ciotat-skate-park.md`. Preserve that work
and refresh status before edits. Website implementation has one owner: this
child. The hub owns this brief and the website task register; do not edit them.

The accepted baseline has 121 Node and 37 Python tests, and both output modes
validate 18 pages, 52 files and 318 references. Scoped Node is 24.21.0; do not
change the global runtime. The reviewed snapshot is current, with zero changed
keys. Saved snapshot SHA-256:
`cdc69b8b5c95af1e05677e9a1639287fd5b8886ab0872ce9adc3bc71dcd5699f`.
Verify these facts afresh rather than copying old success claims.

## Read First

- [Task 15 report](reports/task-15-integrated-release-review.md).
- `website/README.md`, `website/docs/pilot-editorial-review.md`.
- Root and website package manifests/locks, current build and output checker.
- Applicable repository instructions, workflow-hub, senior-developer and
  verification-before-completion guidance. Use additional skills where relevant
  to an actual implementation change; keep the work proportionate.

## Boundaries And Acceptance

- Approved design, content, selected media, routes and source distinctions stay
  intact. Inquiries remain disabled. Do not refresh approved content fingerprints
  to hide source drift; report any changed keys caused by concurrent work.
- The current TradeJournals content-review batch must finish before the hub
  selects website additions. Do not evaluate or promote that new content here.
- No Git commit/push/merge, hosting/domain setup, deployment, contact activation,
  archival, CI/CMS or successor task is authorized by this task start.
- An unresolved upstream finding can be a documented outcome, but cannot be
  called fixed or omitted from the before/after audit summary. The hub and Shawn
  review the actual result and residual limitations before acceptance.
- Required checks must be fresh. Document any check that cannot run and why.
  Keep claims limited to observed behavior; no broad security certification.

## Deliverable And Return

Apply dispatch `WK-WEB-T16-D01` once. Rename this child to
`Website 2 - Task 16 Dependencies - IN PROGRESS` and verify the assignment.
Read this brief first: it is newer than the fork's completed history.
Save report `WK-WEB-T16-R01`, revision 1, to
`docs/website-workflow/reports/task-16-dependency-maintenance.md`.
Rename to `Website 2 - Task 16 Dependencies - READY FOR REVIEW` and report its
path and concise verified outcome to the exact hub using workflow-hub reporting.
Request reconciliation and Shawn's acceptance; do not start another stage.
Keep all material in this authorized personal project environment.

## Dispatch Observation

Exact child was verified idle before dispatch. After the single authorized
message, wait observed active execution turn
`01a10291-85e9-7311-bccd-1c1035c3a1d9` and the child's start acknowledgement.

## Hub Review — October 3, 2026

Report `WK-WEB-T16-R01`, revision 1, RECEIVED once and reconciled as
`WK-WEB-T16-H01`. Exact child title READY FOR REVIEW verified. Shawn's
acceptance remains pending; this reconciliation does not authorize closeout.

Hub inspected the three-line lock entry change, README correction, audit JSON,
fresh-install logs and upstream cache advisory. Independently reran 121 Node
and 37 Python tests: all passed. Both retained outputs pass matching-model
checks (18 pages, 52 files, 318 references each), with current review state and
zero changed keys. All 52 files in each mode independently match both the saved
accepted baseline and fresh patched build byte for byte. No browser rerun is
needed for identical output; Task 15's representative browser evidence stands.

Website audit moves from three to two high package findings; six devalue
advisories are removed by 5.9.4. Remaining cache/Astro findings represent one
unpatched upstream issue. Separately, scratch root tooling audit reports seven
high and one moderate package findings; remediation/exposure review remains
open. This patch does not resolve them or certify a clean repository audit.

Concurrent content-review closeout advanced HEAD to `715b2a1`, with no website
changes. Task 16 website changes and hub records remain uncommitted. Technical
review supports accepting this compatible website patch with the unresolved
findings explicitly retained. No successor, merge, deployment or archival starts.

## Acceptance

Shawn said `accepted` in website updates on October 3, 2026 after the hub's
technical review and disclosure of remaining findings. Acceptance
`WK-WEB-T16-A01` covers report `WK-WEB-T16-R01`, revision 1. Final reconciliation
`WK-WEB-T16-H02` marks Task 16 COMPLETE; earlier pending statements are historical.
The residual website/cache and root-tooling findings remain follow-up. Changes
remain uncommitted; this acceptance does not start Git closeout, merge,
deployment, archival or a successor task.

## Task 16 Git Closeout Authorization

After acceptance, Shawn said `git er done` in website updates on October 3,
2026. This authorizes validation, commit and push of the accepted website lock
patch, README, Task 16 brief/report and hub register to the established
`origin/codex/concept-b-homepage` branch. Earlier uncommitted/no-closeout
statements describe the pre-closeout checkpoint. Residual findings stay open;
merge, deployment, archival and successor work remain separate. Final commit
and synchronization evidence will be reported in the hub after the push.
