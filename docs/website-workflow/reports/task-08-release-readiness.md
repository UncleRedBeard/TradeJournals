# WK-WEB-T08 — Website Release Readiness Report

Report ID: `WK-WEB-T08-R01` · Revision 2 · September 19, 2026
Supersedes: revision 1 draft
Status: READY FOR REVIEW
Child: `01a0bbcf-a52f-7672-b08e-d69da400c4d7`
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`
Exact child title: `Website 1 - Task 08 Release Readiness - READY FOR REVIEW`
Report delivery: SENT

## Result So Far

The static Astro architecture is portable and the documented setup now works
from a clean clone. A new maintainer can install the project-scoped Node runtime
and locked dependencies, run the complete public-site checks, and build the
candidate without Workbench, a private database, or provider credentials.

Shawn approved the exact 22-record, 18-source snapshot with SHA-256
`ab0a82cd6e9492800f5e2a8b885aee4038d9e96a01cc1f55221b0cd59ed24fce`.
That exact file is saved as `reviewed`, compares as current with zero changed
keys, and passed the guarded release build. The approved first-release contact
treatment is a disabled email placeholder with no address or action.

## Current Maintainer Path

[The website guide](../../../website/README.md) now records one tested route:

1. Clone the complete repository at `codex/website-updates`.
2. Install Node 24.21.0 under `website/.runtime/`.
3. Put that runtime first on `PATH` and install the locked website dependencies.
4. Run `npm run test:website` and `npm run check:website`.
5. Review and approve the exact complete candidate.
6. Record its reviewed snapshot and run the guarded release build.
7. Eventually upload only the contents of `website/dist/` to a domain root.

The guide explicitly explains the full-repository dependency, Python 3.10+
requirement, feature-branch location, candidate/release distinction, root-path
assumption, private Workbench boundary, and eventual upload payload.

## Fresh-Checkout Proof

- Source revision:
  `dd6da4c01476e3ccdcdfbf9b1193b00c5b842d6b` on
  `codex/website-updates`.
- Isolated clone:
  `/private/tmp/tradejournals-task08.OvS7Ya/repo`.
- No `website/.runtime/`, `website/node_modules/`, generated model, or build
  output existed after cloning.
- `node@24.21.0` resolved from the npm registry and installed into the isolated
  project runtime.
- `npm --prefix website ci --no-audit --no-fund --prefer-offline` installed 194
  locked packages in the isolated clone.
- Runtime: Node 24.21.0, npm 11.11.0, Python 3.13.7.
- 115 website Node tests passed.
- 37 Python source/output tests passed.
- Candidate build and independent output check passed: eight HTML pages, 24
  files, and 93 references.

The `--prefer-offline` install option allowed npm to reuse its package cache; no
project runtime, `node_modules` tree, generated website files, or private store
was copied into the clone. Registry resolution and a normal locked install both
succeeded.

## Candidate And Review Snapshot

[The release-candidate packet](../../../website/docs/pilot-editorial-review.md)
now covers all three canonical rooms:

| Project | Status | Selected photographs |
| --- | --- | ---: |
| Living Room Restoration — Future Barre Studio | Future; move unconfirmed | 3 |
| Dedicated Office | Current | 5 |
| Barre Studio — Current Room | Current home of The Repair Shop | 5 |

The exact proposed snapshot covers 22 public records and 18 selected source
fingerprints. With the approved disabled contact placeholder, its serialized
payload hashes to
`ab0a82cd6e9492800f5e2a8b885aee4038d9e96a01cc1f55221b0cd59ed24fce`.
Shawn explicitly approved this digest. The saved review file hashes to the same
value, contains 22 record and 18 source fingerprints, and compares as `current`
with no changed keys.

Before approval, the real release command refused the candidate as designed:

```text
UNREVIEWED_CONTENT: Release requires current reviewed content; state is candidate
```

After approval and exact snapshot recording, the same guarded command completed
and independently validated eight pages, 24 files, and 93 references in
`website/dist/`.

## Browser Verification

The local candidate was served on loopback and inspected in a real browser.

- Desktop: homepage, three work pages, and TradeJournals archive rendered with
  no horizontal overflow or console errors.
- All three work pages showed the correct headings and 3/5/5 selected-image
  counts.
- The candidate review notice and `noindex, nofollow` were present.
- The homepage contact control is intentionally disabled and exposes no email
  address, destination, or form action.
- At a measured 390-pixel content viewport, the same five pages had no
  horizontal overflow and both navigation links remained visible.
- Archive search for `office` returned exactly Dedicated Office and Barre
  Studio — Current Room with the correct separate summaries.
- The built release homepage was then checked at 1280 and 390 pixels. It showed
  the disabled email placeholder, no contact destination or form, no review
  notice or `noindex` metadata, no horizontal overflow, and no console errors.

The Task 07 Playwright skips belonged to the private Workbench application.
Task 08 did not change Companion, and the static public package neither imports
nor runs it. Those private-editor suites were not expanded into a hosting gate;
the public-site browser path above is the release-relevant check.

## Changed Paths

- `website/README.md`
- `website/content/reviews/pilot.json`
- `website/docs/pilot-editorial-review.md`
- `website/docs/task-07-room-source-audit.md`
- `website/content/site.json`
- `website/lib/schema.mjs`
- `website/src/components/ContactInvitation.astro`
- `website/src/pages/index.astro`
- `website/src/styles/base.css`
- `website/tests/office-content.test.mjs`
- `website/tests/rendering.test.mjs`
- this report

The hub-owned Task 08 brief and task register are present in the shared checkout
but remain outside the child's implementation ownership.

## Verification

- Scoped Node 24.21.0 website suite: 116 passed.
- Python suite: 37 passed.
- Fresh-clone candidate: eight pages, 24 files, 93 references.
- Current-checkout candidate: eight pages, 24 files, 93 references.
- Current-checkout guarded release: eight pages, 24 files, 93 references.
- Independent `website/dist/` output check: passing.
- Reviewed snapshot: exact approved digest, `current`, zero changed keys.
- Markdown lint: passing for all Task 08 and hub coordination documents.
- `git diff --check`: passing.

## Remaining Boundaries

No Task 08 release-readiness decision remains. The verified local release folder
is ready for a later static-hosting task.

Hosting choice, domain/DNS, upload, deployment, merge, commit, push, and journal
or inventory correction remain outside Task 08.

## Hub Action Requested

Review this report, reconcile the hub-owned register, and verify title/status
agreement. Accept Task 08 only against its agreed criteria. This report
authorizes no new child, next task, merge, publication, or deployment.

Delivery evidence: the report message was accepted by hub thread
`01a0a263-8d09-7ff2-8144-a71eb6ec16f6`, which entered an active reconciliation
turn. No duplicate delivery was sent.
