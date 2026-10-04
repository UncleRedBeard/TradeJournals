# Task 18 — Main Integration

Report ID: `WK-WEB-T18-R01`
Revision: 1
Date: October 4, 2026 (America/Chicago)
Child: `01a1078d-069e-77d2-8db1-9d0cfb51fd16`
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`
Dispatch: `WK-WEB-T18-D01`
Outcome: local fast-forward integration verified; final remote identity is
reported to the hub after the authorized push.

## Integrated Scope

Fetched `origin/main` and `origin/codex/concept-b-homepage`. Before integration,
local and remote `main` both pointed to
`b45445ed384c290a98bf28a65e564ec5d91e822b`; local and remote development
branch both pointed to `0fa6bc9b0b4bdf6e212c2f6e158410cf7e6a2033`.
`origin/main` was an ancestor of the development branch and neither remote had
new commits. The shared checkout held only the hub-owned Task 18 brief/register
changes. No unrelated changes were staged.

Reviewed all 24 development commits and the 108-file main-to-development diff.
It contains the accepted Concept B presentation and tests; root and website
locked tooling; five corrected source journals; content-review and website
workflow records; six selected local photographs; the accepted Office access,
current-studio door, and La Ciotat website additions; and the reviewed release
snapshot. No unexpected top-level directory, new service, contact destination,
hosting configuration, or deployment artifact appeared in that delta. Individual
editorial acceptance and release-snapshot approvals are retained in the content
review register and website editorial review. La Ciotat remains in archive/search
and off the homepage.

Updated `website/README.md` to direct a new maintainer to clone `main` and
clarified that the development branch records earlier work. Updated the current
header of `website/docs/pilot-editorial-review.md` to identify the integrated
local release while retaining dated historical approval sections. Committed those
documentation edits with the hub-prepared brief/register as `cb6cd8b` on the
development branch, then switched to `main` and used
`git merge --ff-only codex/concept-b-homepage`. Local `main` advanced from
`b45445e` to `cb6cd8b` without a merge commit or conflict. The development
branch was retained. This report is a final main-only bookkeeping addition.

## Integrated Verification

Checks ran on the scoped Node **24.21.0** and Python **3.13.7**. The same complete
suite passed before the fast-forward, and the following checks passed again on
local `main` after integration:

- `npm run test:website`: **121 Node tests and 37 Python tests**, no failures.
- `python3 -m unittest discover -s tests`: **84 tests**, no failures.
- `npm run test:site`: **five Python and five JavaScript tests**, no failures.
- `npm run check:site-evidence`: checked-in manifest current.
- `npm run lint:md`: **141 Markdown files**, zero issues.
- Preview build/output check and guarded release build/output check: each
  **20 HTML pages, 60 total files and 363 checked references**.
- Independent matching-model checks: preview and release each `current`, zero
  changed keys, **58 reviewed records and 55 selected sources**.
- Root and website lockfiles preserve the accepted pinned linter 0.23.3 and
  devalue 5.9.4. No dependency version changed in Task 18.
- `git diff --check` passed. Release output contains 20 HTML files, 37 JPEGs,
  two authored JavaScript files, and one search JSON file; no symlinks.

The static package is ready for domain-root hosting under the existing
instructions. Inquiries remain disabled. The unpatched root `braces` and website
cache/Astro audit findings remain documented follow-ups; these checks do not
claim a clean audit. No hosting account, DNS, upload, public deployment, branch
deletion, archive, or successor work is included.

## Git Completion Boundary

This report is included in the authorized main closeout. Its own commit and
post-push HEAD/tracking/FETCH_HEAD identity, ahead/behind counts, and worktree
status are reported in the Task 18 chat to avoid a self-referential commit edit.
If remote push is rejected, this report alone does not establish published main
integration; the child must resolve the actual remote state and report it.
