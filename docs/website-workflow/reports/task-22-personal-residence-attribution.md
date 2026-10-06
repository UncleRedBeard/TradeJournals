# Task 22 — Personal Residence Attribution

Report: `WK-WEB-T22-R01`, revision 1. October 6, 2026.
Child: `01a1128e-058e-7763-a61b-c9283775222d`.
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`.
Dispatch: `WK-WEB-T22-D01`, applied once.
Workflow: READY FOR REVIEW. Hub receipt and acceptance pending.

## Delivered

The visible line **Restoration work in my own home.** now appears near each
residential project and journal introduction. A small shared Astro component
contains the six verified IDs; ownership is not inferred from a category.
Existing type, color and spacing conventions are reused. No schema, dependency,
route, broad ownership framework or source-content change was needed.

The six projects are entry, guest bath/dresser vanity, living room/future studio,
master bedroom, dedicated office and current barre studio. Their paired project
and journal routes show the line exactly once. Returning to Clay, Agfa Isolette
and La Ciotat routes do not show it. Current/future studio distinctions,
metadata, stories, evidence limits, images and contact state are preserved.

## Files changed by this task

- `website/src/components/ResidenceAttribution.astro` (new)
- `website/src/pages/work/[id].astro`
- `website/src/pages/tradejournals/[id].astro`
- `website/tests/rendering.test.mjs`
- `website/README.md`
- This report

## Verification

- Test-first route assertion failed on missing entry attribution before the
  implementation; `/tmp/task22-red.log` records the expected failure.
- Full tests pass: 123 Node and 37 Python source/HTML tests. Log:
  `/tmp/task22-tests.log`. The added check covers all 12 applicable routes and
  all six unrelated project/journal routes. Existing metadata and navigation
  checks continue to pass.
- Fresh preview/output check passes: 20 pages, 60 files, 366 references.
  Log: `/tmp/task22-preview.log`.
- Direct Office project and current-studio journal landings reviewed at
  1440 × 1000 and 390 × 844. The attribution is visible near the introduction;
  mobile project/journal and desktop journal width measurements match their
  viewport widths, with no horizontal overflow. Desktop project screenshot
  also shows the layout intact. Temporary viewport override reset afterward.
- README/report Markdown lint and `git diff --check` pass. Self-review confirms
  no additional production changes beyond the component and its two placements.

## Review evidence

Preview server started for this task on loopback port 8143, serving
`website/.preview-dist`; available for review. Shell session: `6034`.

- [Office project](http://127.0.0.1:8143/work/office-restoration/)
- [Current studio journal](http://127.0.0.1:8143/tradejournals/studio-office-restoration/)

Screenshots are in
`/Users/shkelley/.codex/visualizations/2026/10/06/01a1128e-058e-7763-a61b-c9283775222d/`:

- `task22-project-desktop.jpg`
- `task22-project-mobile.jpg`
- `task22-journal-desktop.jpg`
- `task22-journal-mobile.jpg`

## Boundary and delivery

Shared checkout remains `main` at `da081cd`. Changes are uncommitted.
The hub register/brief, requester-owned request and pre-existing
PROJECT_MEMORY.md edit were preserved; the child did not edit those files.

Observed content review state: current, zero changed keys. The snapshot remains
byte-identical, SHA-256
`2efb1566680b93491b2f13b389d2ccb368be6e60392cef31bd3027095bdcd841`.
Template changes do not alter the content fingerprints; this does not constitute
acceptance of the new visible wording or release approval.

No release build, snapshot refresh, Git closeout, deployment, contact activation,
private-repository change or successor was performed. All required task checks
are complete. Report delivery is through this artifact and the final response,
observed by the hub with wait_threads; no callback is sent. Hub acceptance and
any later release/Git action remain separate.

## Direct user acceptance — October 6, 2026

Shawn said “reviewed. approved” in this Task 22 child after reviewing the
completed candidate. Acceptance evidence: `WK-WEB-T22-A01`, covering report
`WK-WEB-T22-R01`, revision 1, and the delivered visible attribution.
The earlier pending-acceptance statements describe the submission checkpoint.
Hub reconciliation and COMPLETE status remain hub-owned. This acceptance does
not authorize Git closeout, release promotion, deployment or a successor.
