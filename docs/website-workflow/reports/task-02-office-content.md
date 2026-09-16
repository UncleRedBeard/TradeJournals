# WK-WEB-T02 — Office Content Report

Report ID / revision: `WK-WEB-T02-R01` / 1
Supersedes: none
Hub thread ID: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`
Workflow child ID: `01a0aa51-2176-75d2-8064-7a89390069c2`
Approval / dispatch: `WK-WEB-T02-A01` / `WK-WEB-T02-D01`
Workflow status: READY FOR REVIEW
Execution note: the hub completed this bounded task after pausing the child
session when it remained active without producing artifacts.
Verified: September 16, 2026, America/Chicago

## Result

Created the first Worth Keeping candidate content set for Office Restoration.
One structured project record now drives the title, concise summary, distinct
search summary, longer story, ten-image gallery, and three-image search subset.
The records retain the original Flickr photo URLs and source album identities.

The candidate does not claim a current observation, client work, or a release.
It records the Office as the author's 1894 residence, uses dated journal support
for floor work and door reclamation, and calls August 2026 documentation intake
rather than new restoration work. The original door treatment remains described
as yakisugi-inspired material reclamation, not traditional yakisugi or a
fire-resistance treatment.

The content remains `candidate` with no saved review fingerprints. Local preview
preparation succeeds with a visible review notice; release preparation fails with
`UNREVIEWED_CONTENT` as intended.

## Artifacts And Verification

| Deliverable / criterion | Artifact or check | Observed result |
| --- | --- | --- |
| Structured site/project content | `website/content/` | One Office project, one service, site/home records, story, review record, and ten selected media records |
| Exact legacy image mapping | `website/tests/office-content.test.mjs` | All ten asset paths, photo IDs, album keys, and Flickr URLs verified |
| Search and page distinctions | Candidate record and Office test | Three established search selections; page introduction and search summary remain distinct |
| Visual evidence review | [Office review worksheet](../../../website/docs/office-content-review.md) | All ten local images inspected; dimensions and conservative candidate captions recorded |
| Candidate gate | `prepareSite(..., "preview")` and release preparation | Preview: one project, ten gallery images, three search images; release: `UNREVIEWED_CONTENT` |
| Website tests | `npm --prefix website test` with scoped Node 24.21.0 | 44 tests pass |
| Python suite | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | 74 tests pass |
| Existing evidence/site checks | `npm run check:site-evidence`; `npm run test:site` | Manifest current; 5 Python and 5 JavaScript legacy-site tests pass |
| Markdown and whitespace | `npm run lint:md`; `git diff --check`; untracked-file whitespace scan | 53 Markdown files and whitespace checks pass |
| Source preservation | `git diff --name-only HEAD -- 01_the_residence_1894 FLICKR_PUBLIC_ALBUMS.md site_example scripts/build_site_evidence.py` | No original journal, inventory, asset, prototype, catalog, or evidence-builder changes |

## Changed Paths

- `website/content/site.json`
- `website/content/home.json`
- `website/content/services/historic-floors.json`
- `website/content/projects/office-restoration.json`
- `website/content/reviews/pilot.json`
- `website/content/stories/office-restoration.md`
- `website/content/media/flickr-*.json` (ten selected records)
- `website/tests/office-content.test.mjs`
- `website/docs/office-content-review.md`
- `docs/website-workflow/reports/task-02-office-content.md`

All Task 01 files remain uncommitted alongside this task. The branch is
`codex/website-updates` at `e16be25c6e7d2db3789e080145332b8dc97b771f`.

## Items For Shawn's Content Review

1. Candidate summary and longer-story level of detail.
2. Two inherited broad search alternatives for the first two door images.
3. The gallery captions and role assignments for the ten selected images.
4. The source journal's conflicting "office-to-studio" phrase, which remains
   visible in the worksheet while the candidate follows its main
   shared-office-to-dedicated-office account.

No contact action, Astro page, deployment output, commit, push, or publication
occurred. Task 03 is not authorized by this report.

## Hub Action Requested

Reconcile the workflow register and accept this implementation task only after
checking the delivered candidate records and verification evidence. Candidate
content itself still awaits Shawn's exact editorial review. This report does not
authorize Task 03, a reviewed snapshot, Git closeout, publication, or deployment.
