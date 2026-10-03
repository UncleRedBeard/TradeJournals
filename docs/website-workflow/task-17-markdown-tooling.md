# Website 2 - Task 17 Markdown Tooling

Workflow status: COMPLETE — accepted by Shawn
Brief revision: 1
Approval: Shawn said `kick off task 17` in website updates on October 3, 2026.
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` / website updates
Child: `01a102e5-9ee6-7281-b41f-8993cc70e4c3`
Dispatch: `WK-WEB-T17-D01` — SENT once; active execution verified
Register: [task-register.md](task-register.md)

## Assignment

Resolve the separate root Markdown-tooling findings discovered by Task 16 with
a small, maintainable update and reproducible installation. Preserve existing
lint coverage and avoid unrelated formatting churn.

- Refresh the root tool's audit, upstream advisories and release notes. Task 16
  found seven high and one moderate package findings in the scratch-installed
  root dependency tree. Its suggested markdownlint-cli2 0.23.3 is a candidate,
  not a predetermined version; confirm current availability and compatibility.
- Evaluate and apply the smallest supported linter update that resolves findings
  where possible. Inspect changed defaults, Node requirements and rule behavior.
  Do not use forced audit fixes, broad dependency overrides or disable checks
  simply to claim success. Record unresolved issues and actual exposure limits.
- Add a root package lock and verify a fresh root `npm ci` in isolated scratch
  outside the shared checkout. Use the existing scoped Node 24.21.0; do not
  change the global runtime. Keep the website package/lock boundary unchanged.
- Run the existing repository Markdown lint against the full intended file set,
  preserving generated/dependency exclusions. Make only necessary narrow config
  adjustments or formatting fixes; report substantial rule migration or bulk
  journal rewriting needs to the hub before expanding scope. No mass auto-fix.
- Update relevant installation documentation to the verified locked workflow.
  Task 16's dated report remains historical evidence, not rewritten history.
- Verify whitespace, lockfile/manifests, actual resolved tool version, and
  before/after audit. Ensure root dependency installation does not interfere
  with website scripts. Run existing proportionate checks; website output
  validation and unchanged reviewed snapshot are required, full website tests
  if runtime/build behavior changes. Do not add implementation-mirroring tests
  for a package-only change or repeat browser review of identical output.

## Environment And Ownership

Same-directory fork in
`/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/TradeJournals`.
Branch `codex/concept-b-homepage`, baseline `59d6e31` (resolve full hash).
Checkout was clean at preparation. Task 16 was accepted and pushed at `2d566f0`,
with matching HEAD/tracking/FETCH_HEAD and `0 0`; subsequent Marseille review
commit is separate content work. Refresh Git state before edits and return.

Child owns root dependency manifest/lock, necessary lint configuration and
maintainer documentation edits, and its report. Hub owns this brief and website
register. Preserve any concurrent content-review files and edits. Use scratch
for clean-install testing; do not delete shared dependencies or user files.

## Read First And Boundaries

Read Task 16 report, root package.json and lint config, website README, relevant
repository instructions, workflow-hub, senior-developer and verification guidance.
This is approved bounded maintenance; no new product design is needed.

The website devalue patch remains accepted. The two website cache/Astro findings
are separate unresolved upstream work, not part of root-tool remediation.
No website design, public content, media, route, fingerprint or inquiry change.
Do not promote new TradeJournals content; selection waits until the current review
batch is finished. No CI, new service, CMS, hosting, deployment, Git commit/push/
merge, archival or successor is authorized. Report genuine blockers without
broadening the task. No claim of a clean repository-wide audit unless supported.

## Deliverables And Return

Save report `WK-WEB-T17-R01`, revision 1, to
`docs/website-workflow/reports/task-17-markdown-tooling.md`, covering exact versions,
changed files, locked clean install, lint coverage/results, website checks,
audit delta and residual findings. Include reproducible commands and limitations.

Apply dispatch `WK-WEB-T17-D01` once. Read this brief before work; it is newer
than the fork history. Rename to `Website 2 - Task 17 Markdown - IN PROGRESS`.
On delivery rename to `Website 2 - Task 17 Markdown - READY FOR REVIEW`, return
the report path and concise evidence to the exact hub through workflow-hub,
and request reconciliation and Shawn's acceptance. Do not start another stage.

Active execution turn `01a102e6-7709-7242-9181-39da57ce8234` observed after
the single dispatch; exact child was idle before dispatch.

## Hub Review

Report `WK-WEB-T17-R01`, revision 1, RECEIVED once on October 3, 2026;
reconciliation `WK-WEB-T17-H01`. Exact READY FOR REVIEW title and idle runtime
verified. Hub inspected the dependency/config/docs diff, clean-install log,
lock hash, before/after audit and current upstream braces advisory.

Independent hub checks: current Markdown lint passes 121 files, whitespace
passes, and both matching-model output gates pass 18 pages/52 files/318
references with current review and zero changed keys. Both modes' 52 files
match the accepted baseline byte for byte. Saved old/new baseline file lists
match exactly (117 authored files); root lock hash matches clean-install proof.
No application behavior changed, so no redundant full-suite or browser run.

Root audit improves from eight findings to five high inherited package findings
for one unpatched braces issue. Website cache/Astro findings remain separately
open. Acceptance is pending and does not imply a clean audit. Task changes
remain uncommitted; concurrent content-review work is preserved. No Git closeout,
merge, deployment, archival or successor is started.

## Task 17 Acceptance And Git Closeout

Shawn said `approved and git er done` in website updates on October 3, 2026.
Acceptance `WK-WEB-T17-A01` covers report `WK-WEB-T17-R01`, revision 1;
hub reconciliation `WK-WEB-T17-H02` marks Task 17 COMPLETE. Remaining upstream
findings stay documented and unresolved. Earlier pending/uncommitted statements
record prior checkpoints.

The same instruction authorizes validation, commit and push of the Task 17
manifest/lock, exclusions, installation documentation, brief/report and hub
register to `origin/codex/concept-b-homepage`. Preserve all concurrent Cassis
content-review work. No merge, deployment, archival or successor is included.
Final commit and synchronization evidence will be reported in the hub.
