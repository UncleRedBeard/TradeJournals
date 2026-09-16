# Task 05 — Pilot Content And Visual Review

Report ID: `WK-WEB-T05-R01`

Revision: 3 — adds the business rename after the Studio-first revision 2

Status: READY FOR REVIEW — Studio text/layout candidate; photo selection pending

Child: `01a0ac3f-68fd-7771-a652-b16281312adf`

Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`

## Scope And Result

Shawn directly selected **Home Reno - Studio** as the first candidate in this
child. The hub recorded that instruction in brief revision 2. The existing
visual direction and prior Office edits are preserved.

The [active review packet](../../../website/docs/pilot-editorial-review.md)
contains the Studio copy, photo-selection proposal, source boundaries, routes,
and remaining decisions. The
[Office review](../../../website/docs/office-editorial-review.md) retains the
original ten-photo proposal separately; its homepage recommendation is historical.

- [Homepage](http://127.0.0.1:8126/) now features Studio.
- [Studio project](http://127.0.0.1:8126/work/studio-restoration/) has its own record.
- [Studio story](http://127.0.0.1:8126/tradejournals/studio-restoration/) covers
  retained materials, work sequence, and finish integration in four paragraphs.
- [Archive](http://127.0.0.1:8126/tradejournals/) contains both projects.

## What Changed

- Shawn requested the business name **Toil & Timber Restoration**. Updated the
  site record, homepage label, package metadata, maintainer heading and brand
  test assertions. The service line and project content stay as reviewed.

- Added Studio project and story records, selecting the dedicated ballet barre
  journal and `google_photos:af1qippool3ge7t` inventory identity.
- Homepage feature, Work navigation, and first historic-floors project link now
  point to Studio. The Office photograph is no longer the homepage hero.
- Studio gallery and search-image selections are empty. No Studio media IDs,
  captions, alternative text, or visual claims were invented. No images fetched.
- The source journal has no selected durable image identifiers and the prototype
  has no Studio assets. Existing `studio-office` photos belong to Office.
- Current account is explicitly dated to the journal through August 30. The
  room's present completion state was not independently checked. The differing
  polyurethane coat counts are avoided without changing the journal.
- Image-free cards use the available text width. The earlier shared gallery
  proportional-image improvements and optional hero sizing fix remain.
- Office records, ten photos, captions, alternatives, story and routes remain.
  Office-specific history and personal-image questions are deferred.
- Updated maintainer documentation and preserved the Office review separately.

## Verification

Runtime: scoped Node 24.21.0.

Revision 3 rename verification: all 80 website tests reran successfully, including
the preview build; output validation passed for six pages and 19 files. All six
generated pages contain Toil & Timber and no old brand. The live homepage title,
header, hero label and footer show the new name. Markdown lint and whitespace
checks passed. The 37 Python checks below were run for revision 2; the rename did
not change their source/output parser code.

- `npm --prefix website test`: **80 tests passed**. One old integration assertion
  assumed a single project; it now verifies both exact project IDs, separate
  gallery counts, and both new Studio routes. Office evidence identities remain
  tested. A new Studio test verifies its album source, homepage target, empty
  images, and retained Office gallery.
- `npm run check:website`: build and independent output checker passed for
  **6 HTML pages, 19 public files, 72 references**.
- Python source/output checks: **37 tests passed**.
- Markdown lint and whitespace checks pass; final checks include the revised
  report and newly added files.
- Original journals, inventories, source media, prototype, and saved review
  snapshot have no diff. Review remains candidate with empty records/sources.

Desktop 1280 and mobile 390-pixel browser checks covered homepage, Studio project,
and story. Text, navigation and the exact service line remain readable; no
horizontal overflow was observed. The correct Google Photos album link and
explicit missing-photo boundary render on the Studio pages. The archive lists
both projects; searching `shiplap` returns Studio alone. No browser warnings or
errors were reported. The temporary viewport override was reset.

Existing loopback preview server PID 35118 was rechecked at port 8126 with this
checkout as its working directory and reused. Rendered changes were observed.
The Studio preview tab is retained. No server was stopped or replaced.

## Remaining Work And Decisions

This delivery is **not completed photo curation or editorial acceptance**.

1. Review the Studio text and story.
2. Select and bring in actual Studio photographs with durable source identities.
   The brief explicitly prohibits automatically fetching new photos. The packet
   proposes a lead composition and seven evidence roles; exact selections,
   captions and alternatives remain pending direct image inspection.
3. Review the populated gallery and homepage lead, then explicitly approve the
   complete candidate and recording its reviewed snapshot.

The earlier source checkpoint identifies August 26 near-completion views as
possible leads. These are not claimed as newly inspected or selected images.
Final barre installation or current room completion is not asserted.

## Changed Paths And Pre-closeout Git State

Studio revision adds or changes:

- `website/content/projects/studio-restoration.json`
- `website/content/stories/studio-restoration.md`
- `website/content/home.json`, `site.json`, `services/historic-floors.json`
- `website/src/components/ProjectCard.astro`
- `website/tests/studio-content.test.mjs`, `build.test.mjs`, `office-content.test.mjs`
- `website/README.md`, `website/package.json`, `website/package-lock.json`
- Brand expectations in `website/tests/fixtures.mjs` and `rendering.test.mjs`
- `website/docs/pilot-editorial-review.md`, `office-editorial-review.md`,
  `office-content-review.md`
- This report

Prior Office changes remain in its project/story records, ten media alternative
texts, and shared `Hero.astro` / `ProjectGallery.astro` sizing.

Branch: `codex/website-updates`. HEAD:
`1faa53d6a502665a823ea168f058960fa0fb0ed2`. Changes remain uncommitted.
The hub-owned register and brief were not edited by this child. No commit,
push, deployment, contact feature, hosting choice, private Dashboard access,
source edits, or reviewed snapshot occurred.

Delivery state: Revision 3 SENT once to the exact hub; the response returned the
expected hub ID. Acceptance is not assumed. Revision 2 was previously sent.
The hub owns reconciliation; no next task is authorized by this rename.

## Authorized Git Closeout

Shawn subsequently instructed `git er done` in this child, authorizing the scoped
commit and push to established `origin/codex/website-updates`. This supersedes the
initial no-Git boundary for this closeout only. It does not approve publication
or change the candidate review snapshot.

Fresh closeout checks passed: 80 website tests, all 84 Python tests (including
37 focused website tests), five legacy search tests, the legacy evidence manifest
check, and generated-output validation for six pages and 19 files. Git whitespace
and Markdown checks are required on the final staged tree. The original source
journals, inventories, photographs, prototype, and review snapshot remain intact.

The child will report the resulting commit and observed remote synchronization
after the push. Earlier Git descriptions above are pre-closeout checkpoints.
