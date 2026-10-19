# Task 23 — Entry Gallery Trial

Report: `WK-WEB-T23-R01`, revision 1. October 19, 2026.
Child: `01a1551b-1022-7c01-bf02-bf4f2a2c0f8f`.
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`.
Dispatch: `WK-WEB-T23-D01`, applied once.
Workflow: READY FOR REVIEW. Hub receipt and user acceptance pending.

## Delivered

Only the Entry project page opts into the trial. It keeps the existing three
local photographs and approved ordering: floor result first, then first-pass
condition/protection and stair finish work. Stage labels and a short introduction
explicitly distinguish the 2024–25 first pass from the late-2025 floor renewal.
Existing captions, alt text, selected images and source content are unchanged.

Photographs open in a native dialog on the same page. Enter activates a link;
Close and Escape dismiss the dialog and restore focus. Local-image links remain
as the no-script/unsupported-dialog fallback. There is no carousel, zoom system,
new dependency, new route or image sourcing.

The full source album link now appears below the Entry gallery. Individual photo
links remain in a quiet “Photograph sources” disclosure: the existing output
checker requires this provenance and has not been weakened. The Entry record
still identifies its sources. Other project galleries and the Entry journal
retain their existing behavior; homepage selections and metadata are unchanged.

## Changed files

- `website/src/components/EntryGallery.astro` (new, Entry-specific composition,
  labels, dialog and minimal scripting)
- `website/src/components/ProjectGallery.astro` (default-off local-viewing option
  and optional stage labels)
- `website/src/components/EvidenceDetails.astro` (default-on album-link option)
- `website/src/pages/work/[id].astro` (explicit Entry-only opt-in)
- `website/tests/rendering.test.mjs`
- `website/README.md`
- This report

Hub register and brief are hub-owned and were preserved after dispatch.

## Verification

- Test-first Entry route check failed initially because the dialog was absent:
  `/tmp/task23-red.log`. Focused tests then passed in `/tmp/task23-focused.log`.
- Full suite passes: 124 Node tests and 37 Python source/HTML tests:
  `/tmp/task23-tests.log`. Tests preserve gallery order, captions and provenance,
  check the Entry local targets/labels/album link, and exclude the dialog from
  Office and the Entry journal. The pre-existing gallery assertion was narrowed
  to gallery figures so the dialog container is not counted as a fourth photo;
  its source-link assertion now recognizes Entry's secondary provenance links.
- Fresh preview and independent output check pass: 20 pages, 60 files,
  366 references; `/tmp/task23-preview.log`.
- Browser review at 1440 × 1000 and 390 × 844: all three photos opened with
  matching captions/alt text; Enter, Escape, close button and focus restoration
  worked. Desktop/mobile widths match scroll widths (1440/390); mobile dialog
  width is 352 pixels. The image fits the dialog without cropping.
- Source disclosure expands to all three original photo links. Album href
  matches the established source. The retained TradeJournal link was followed
  successfully to the unchanged Entry story. External source destinations were
  inspected, not independently audited for remote availability.
- Office direct landing retained all six external image links, no dialog and
  no local-viewer triggers. Its mobile layout has no horizontal overflow.
- No browser console errors were observed. Temporary viewport override reset.
- README/report Markdown lint and `git diff --check` pass. Self-review confirms
  no broad schema, model, content-record or dependency changes.

## Review URL and screenshots

[Entry trial](http://127.0.0.1:8143/work/entry-restoration/#project-photographs)

Temporary Python preview server: PID `29897`, shell session `28856`, loopback
`127.0.0.1:8143`, serving `website/.preview-dist`. The port was free before this
task started it. Left running for review; no other task's server was stopped.

Screenshots in
`/Users/shkelley/.codex/visualizations/2026/10/19/01a1551b-1022-7c01-bf02-bf4f2a2c0f8f/`:

- `task23-desktop-gallery.jpg` (full page)
- `task23-desktop-dialog.jpg`
- `task23-mobile-gallery.jpg`
- `task23-mobile-dialog.jpg`
- `task23-mobile-sources.jpg`

## Checkout and release boundary

Shared branch remains `main` at `b65f0c1`. Changes are uncommitted.
Content review state remains current with zero changed keys because this trial
changes template presentation, not fingerprinted content. `pilot.json` is
unchanged, SHA-256:
`2efb1566680b93491b2f13b389d2ccb368be6e60392cef31bd3027095bdcd841`.
That state does not imply acceptance of the trial or release approval.

No release build, review refresh, commit/push, deployment, contact activation,
other-project rollout, journal rewrite or successor was performed. All required
trial checks are complete. Report delivery uses this artifact and the final
response, observed by the hub; no callback message is sent. Hub owns acceptance
and COMPLETE status after Shawn reviews the concrete result.

## Direct user acceptance

Acceptance `WK-WEB-T23-A01` applies to report `WK-WEB-T23-R01`, revision 1.
On October 19, 2026, Shawn reviewed the delivered Entry gallery trial and said:
“i like it...approved”. This supersedes the pending user acceptance recorded at
submission. The Entry-only gallery trial is accepted; hub reconciliation of
COMPLETE status remains with the website updates hub.

This acceptance does not authorize Git closeout, public deployment, or rollout
to other projects. Release validation and Git closeout remain the next separate
steps.
