# WK-WEB-T01 — Content Foundation Report

Report ID / revision: `WK-WEB-T01-R01` / 1
Supersedes: none
Child thread ID: `01a0a5ea-afed-7e92-9938-25b57c1e5b4a`
Hub thread ID: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`
Approval / dispatch: `WK-WEB-T01-A01` / `WK-WEB-T01-D01`
Workflow status: COMPLETE (accepted by hub under `WK-WEB-T01-H01`)
Submission status: READY FOR REVIEW; original submitted title was Website 1 - Task 01 Content Foundation - READY FOR REVIEW
Exact child title: Website 1 - Task 01 Content Foundation - COMPLETE (verified by fresh task readback)
Report delivery: RECEIVED
Delivery flag: cleared by explicit hub acknowledgement
Verified: September 15, 2026, 9:03 p.m. America/Chicago (September 16, 02:03 UTC)

## Result

Implemented Task 1's content foundation using four small JavaScript modules and
one offline Python source inspector. No real project records or visitor pages
have been added in this task.

- JSON records have strict schemas, stable IDs, relationship checks, contained
  paths, and precise errors. Project JSON files form the deliberately curated
  public catalog; unrelated archive journals are never discovered automatically.
- The source reader reuses the existing inventory count parser, reads only
  requested local files/album blocks, and returns fingerprints and recorded
  album facts. It does not require page HTML or network calls.
- Review comparison detects selected content/source changes without changing
  the saved approval record. Candidate/stale content cannot pass release
  preparation. Unrelated inventory blocks and unselected media do not invalidate
  the selected snapshot.
- Preparation returns a public model, a separate internal report, and an
  explicit asset-copy list. Local source paths and fingerprint bookkeeping do
  not enter the public model. It preserves separate gallery/search alternatives,
  original media URLs, recorded counts, and public project/archive destinations.
- All preview modes remain visibly labeled, including previews of reviewed
  content. A reviewed release model has no preview notice.

## Artifacts And Verification

Run commands from the repository root. Select the website runtime in the shell:

```sh
export PATH="$PWD/website/.runtime/node_modules/node/bin:$PATH"
```

| Deliverable / Criterion | Command Or Observation | Observed Result |
| --- | --- | --- |
| Scoped runtime | `website/.runtime/node_modules/node/bin/node --version` | `v24.21.0` |
| Global runtime preserved | `node --version` outside the scoped shell | `v25.8.1` |
| Website dependencies | `npm --prefix website ls --depth=0` under scoped runtime | Astro `7.3.2`, Zod `4.5.4`; lockfile retained |
| Content, review, source integration | `npm --prefix website test` under scoped runtime | 41 tests pass |
| Focused source reader | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_website_sources -v` | 27 tests pass |
| Python regression suite | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | 74 tests pass using Python `3.13.7` |
| Existing website evidence | `npm run check:site-evidence` | Existing manifest is current |
| Existing website behavior | `npm run test:site` | 5 Python and 5 JavaScript tests pass |
| Authored Markdown | `npm run lint:md` | 50 files pass, including this report |
| Whitespace | `git diff --check` plus `git diff --no-index --check /dev/null` for each untracked file | No whitespace diagnostics |
| Original archive/prototype preservation | `git diff --name-only HEAD` scoped to all five pillars, inventories, existing site, and existing source builder | No differences |
| Review fixes | Focused failing-then-passing HTTPS and reviewed-preview tests, followed by the full website suite | Both findings resolved |

The tests use invented records and temporary files. Reviewed fixtures establish
the release-preparation success path without marking any real public content
approved. Actual Astro rendering is Task 3 work, not a claim of this report.

## Changed Paths

- `.gitignore`
- `.markdownlint-cli2.jsonc`
- `website/.node-version`
- `website/package.json`
- `website/package-lock.json`
- `website/lib/schema.mjs`
- `website/lib/content.mjs`
- `website/lib/review.mjs`
- `website/lib/prepare.mjs`
- `website/tests/fixtures.mjs`
- `website/tests/content.test.mjs`
- `website/tests/review.test.mjs`
- `website/tests/prepare.test.mjs`
- `scripts/inspect_website_sources.py`
- `tests/test_website_sources.py`
- `docs/website-workflow/reports/task-01-content-foundation.md`

Dependencies and the scoped runtime are installed in ignored website directories.
The design, plan, task brief, and hub register were already present and remain
hub-owned. This child did not modify them.

## Review And Implementation Notes

Independent read-only review found two actionable issues: incomplete HTTPS
authority strings could pass validation, and reviewed previews lacked a label.
Both are fixed and regression-tested. The reviewer found no other actionable
containment, privacy, or fingerprint problems within Task 1's scope.

Two small file-map additions support the approved work:

1. `website/tests/prepare.test.mjs` keeps the subprocess/model integration cases
   separate from record and review unit tests.
2. `.markdownlint-cli2.jsonc` excludes only website dependencies and generated
   directories. Installing the runtime exposed that the existing CLI2 command
   otherwise scanned dependency documentation. The hub explicitly authorized
   this integration fix. Authored website content remains in the lint scope.

There is no image decoder in this foundation. The plan assigns real-image
inspection and pixel-dimension measurement to Task 2. Synthetic image fixtures
intentionally contain test bytes; their tests verify selection and fingerprints,
not image authenticity or visual quality. Markdown story bytes are contained
and fingerprinted here; safe Markdown rendering belongs to Task 3.

## Repository State And Limits

Repository: `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/TradeJournals`
Branch: `codex/website-updates`
HEAD: `e16be25c6e7d2db3789e080145332b8dc97b771f`
Applicable changes: uncommitted and unstaged.

During interruptions, the shared checkout changed to `main` at the same commit.
The child paused code edits and requested hub reconciliation. The hub restored
the approved branch under `WK-WEB-T01-B01` and verified the then-existing 18
modified/untracked files were byte-identical across the switch. The child then
verified the branch and finished the fixes above.

No commit, push, deployment, content migration, Companion modification, or next
task dispatch occurred. No required Task 1 checks remain unrun. Real Office
content review, full pages, browser verification, and launch remain later scope.

## Hub Action Requested

Review the delivered Task 1 implementation and this report, reconcile the
hub-owned register, and verify title/status agreement. The hub owns acceptance
and COMPLETE. This report authorizes no next task, merge, push, or deployment.

Delivery evidence: exact hub `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`
acknowledged receipt and acceptance in `WK-WEB-T01-H01`. The hub independently
reviewed the implementation and reran the recorded checks successfully, updated
its register, and renamed this task COMPLETE. The child verified the final title
through a fresh task read. The original review request above is retained as
submission history; no further acknowledgement dispatch or implementation is due.
