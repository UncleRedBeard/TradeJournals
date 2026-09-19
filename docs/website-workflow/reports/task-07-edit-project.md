# WK-WEB-T07 — Website Project Editor And Room Separation Report

Report ID: `WK-WEB-T07-R01` · Revision 2 · September 19, 2026
Status: COMPLETE — approved revision applied to the local canonical website
Child: `01a0b143-f91d-7142-a68f-85898b4942f7`
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`

## Hub Acceptance — September 19, 2026

The exact child reported Shawn's final approval of the reviewed Workbench
implementation and private three-room preview. The hub reconciled report
`WK-WEB-T07-R01` revision 1 as accepted under `WK-WEB-T07-H02` at 15:33 UTC.
The COMPLETE title and idle runtime were independently read back. Implementation
and previously reported test evidence are unchanged by this bookkeeping.

This approval does not authorize Publish update, canonical source application,
retiring the old `studio-restoration` files, reviewed snapshot changes, Git
commit/push, deployment, journal/inventory corrections or a successor task.
The child reports both local review servers running for now; this supersedes
the earlier shutdown checkpoint and was not independently rechecked by the hub.

## Local Publication Addendum — September 19, 2026

After reviewing the Workbench button behavior, Shawn explicitly authorized
save, build, and publish. That later authorization supersedes the acceptance
boundary above only for applying the approved revision to the local canonical
website and rebuilding its candidate output. It does not authorize Git
commit/push, hosted deployment, reviewed-snapshot approval, journal or inventory
edits, or a successor task.

Approved design:
[Website Project Editor Design](../../superpowers/specs/2026-09-18-website-project-editor-design.md)

Approved plan:
[Website Project Editor Implementation Plan](../../superpowers/plans/2026-09-18-website-project-editor.md)

## Result

TradeJournals Workbench now supports private, revisioned, multi-project website
editing. One change set can edit stories and project fields, move an album to a
new project, replace a project ID, update validated references, arrange photos,
save an immutable draft, and build an isolated Astro preview. The archive owns
the content schemas, proposal, source application, and builds. Companion owns
private revisions, receipts, lifecycle state, and the browser editor.

The Task 07 room correction was saved as a new immutable revision, built in the
private preview, and applied to the local canonical website:

- Draft: `e9c88bf0-9413-4178-8c7e-b89a09d4a591`
- Revision: `2`
- Status: `published`
- Proposal and preview digest:
  `0c86af959f76454e490013e3896806c4d994fdcea3e341366ccbc6115a0c6ef8`
- Receipts: completed `save`, `preview`, and `publish`; no recovery required

**Publish update was used for the approved local application.** Canonical
website source and candidate output now contain the three-room correction. No
hosted output, reviewed snapshot, journal, inventory, Git index, commit, or
remote branch changed.

## Confirmed Room Identities

| Stable project ID | Room | Occupancy | Source | Media |
| --- | --- | --- | --- | ---: |
| `office-restoration` | Dedicated Office | current | Flickr `72177720316928566` | 5 |
| `studio-office-restoration` | Barre Studio — Current Room | current | Flickr `72177720306207693` | 5 |
| `living-room-studio-restoration` | Living Room Restoration — Future Barre Studio | future | Google Photos `af1qippool3ge7t` | 3 |

The current barre studio remains the current home of the barre studio and The
Repair Shop. The former living room remains their future home until Shawn
explicitly confirms the move. Album names, dates, renovation progress, and room
appearance do not override that distinction.

The source audit binds all 13 selected records to their albums and separates
direct observations, metadata, journal claims, conflicts, and withheld claims:
[Task 07 Three-Room Source Audit](../../../website/docs/task-07-room-source-audit.md).

## Private Preview Evidence

The reopened revision matched the saved change set for all three IDs, album
keys, ordered galleries, stories, occupancy values, and references. The preview
inspection covered:

- all three Work pages and all three paired TradeJournals pages;
- the home feature, primary Work navigation, and TradeJournals index;
- all three search records and stable IDs;
- the `Historic floors` reference;
- explicit current, current, and future occupancy labels; and
- all 13 external image-source links.

The old `studio-restoration` routes were absent from navigation, links, and
search. The current studio copy says the move has not occurred. The future
studio copy says the move is unconfirmed and the room is not currently occupied
as the studio.

The project-ID replacement derives exact home, service, and navigation remaps
from validated rename operations. The adapter rejects caller-supplied site
content, ghost source IDs, stale touched records, unsafe paths, duplicate album
ownership, and unreviewed promotion bytes.

## Pre-Publication Canonical Isolation

The same deterministic snapshot ran before and after the private preview. Every
protected root remained byte-for-byte identical:

| Protected root | Files | SHA-256 before and after |
| --- | ---: | --- |
| `website/content` | 21 | `6ac06e97b33e087d4e09cc32eb845a79c83eed2f2c92ad2adad43efaa4c9ceae` |
| `website/assets` | 3 | `76bfb59769382da72f4f84194e40aa6c55d02cb524e15eec3e3e06bd2ce995b4` |
| `website/src/generated/site.json` | 1 | `7b961b2b3390513597c29124df748e85ed7b6ce6aaf3085b6283e70ac035abb2` |
| `website/.generated` | 16 | `554c7ee0da694c7a2ceb6566c94decf5fa4af54acbc7d01a5e5af9aac0591194` |
| `website/.preview-dist` | 22 | `8300b8695f016a2495de9fdeb54b73c64d7682b1508de1c8a7ea7f94a6ae03ca` |

`website/content/reviews/pilot.json` remains `candidate` at SHA-256
`465d327c886b20dd8693baa8e117ed911573b4eaa6abe704614292971f8cde91`.
The two source journals and both album inventories have no Task 07 content diff.

After publication, the canonical website contains the three approved stable
project IDs and no longer contains the old `studio-restoration` project or
story files. Those tracked removals remain recoverable through Git because this
task did not stage, commit, or push them. The journals, album inventories, and
candidate review state remain unchanged.

## Behavior By Repository

### Archive

- Adds explicit project occupancy and exclusive album ownership validation.
- Makes all private preview roots and outputs explicit while preserving ordinary
  canonical build defaults.
- Replaces the single-project authoring adapter with immutable change sets,
  touched-record fingerprints, deterministic proposals, confined private
  previews, durable publication manifests, and exact recovery inspection.
- Rechecks each tracked target against its recorded before-digest immediately
  before replacement or removal, so a supported direct edit made while an
  operation is preparing stops publication and remains intact.
- Derives navigation changes from a validated project-ID replacement without
  expanding the caller-supplied change-set contract.
- Records the three-room source and claim audit.

### Companion

- Adds schema-version-3 tables for website drafts, immutable revisions,
  previews, and operation receipts, with a verified offline v2-to-v3 upgrade.
- Adds the Website Draft service and guarded HTTP contract for save, reopen,
  preview, publish, receipt lookup, and recovery.
- Adds the multi-project browser editor with a four-step workflow rail,
  autosave, explicit discard/reopen, revision-conflict handling, and exact
  preview gating.
- Opens a retained recovery draft before the canonical catalog, keeps normal
  editing and publication locked, and exposes only the explicit recovery action
  when an interrupted rename makes that catalog temporarily invalid.
- Serializes source mutations, retains uncertain operations for recovery, and
  keeps internal paths and object names out of public errors.

## Publication And Recovery Boundary

Private states are `draft`, `previewed`, `publishing`, `recovery`, and
`published`. A matching preview receipt for the current revision and digest is
required before **Publish update**. The operation applies local canonical source
and then attempts the ordinary candidate build. It does not deploy, approve the
reviewed snapshot, edit journals or inventories, or perform Git operations.

Startup inspects interrupted durable manifests. It finalizes publication only
when the expected after-image is verified. Otherwise it retains `recovery` and
does not replay uncertain source application. If source application is verified
but the canonical candidate build fails, source remains `published` and the
candidate preview is marked failed for a rebuild without source reapplication.

The real private store was upgraded offline from version 2 to version 3 with a
verified backup while no server owned it. No private configuration, database,
backup, media object, preview output, credential, or local endpoint entered
either repository.

## Structured-File And Stale-Edit Paths

Direct editing remains available through `website/content/projects/*.json`,
matching `website/content/stories/*.md`, `website/content/home.json`,
`website/content/services/*.json`, `website/content/site.json`, and public media
records. These paths use the same archive schemas and build checks as Workbench.

External edits to unrelated canonical records do not invalidate a saved draft.
An external edit to any touched project, story, home, service, navigation, or
media record makes the draft safely stale. Preview and publication stop without
discarding the saved revision; the editor must reopen current canonical content,
reconcile the change, and save a new revision.

## Separate Journal Proposals

Journal and inventory correction remains outside this website revision and
requires separate review and approval:

1. Split the mixed Office journal's two-room account. Keep Flickr
   `72177720316928566` with the Dedicated Office. Reassign the December 2021
   floor and door claims associated with Flickr `72177720306207693` only after
   the current-studio chronology and conflicting dates are reconciled.
2. Keep the Ballet Barre Studio journal tied to Google Photos
   `af1qippool3ge7t`, but preserve former-living-room and future-studio wording.
   Do not claim current occupancy, final sign-off, or an installed barre without
   new evidence and Shawn's confirmation.
3. Update either album inventory only as a separately reviewed routing change;
   do not treat inventory labels as evidence of room identity.

No journal or inventory proposal was applied.

## Changed Paths

### Archive implementation and documentation

- `website/lib/schema.mjs`
- `website/lib/content.mjs`
- `website/lib/prepare.mjs`
- `website/lib/workbench.mjs`
- `website/lib/workbench-files.mjs`
- `website/scripts/build.mjs`
- `website/astro.config.mjs`
- `website/src/content.config.ts`
- `website/src/components/EvidenceDetails.astro`
- `website/src/pages/index.astro`
- `website/src/pages/search.json.js`
- `website/src/pages/work/[id].astro`
- `website/src/pages/tradejournals/index.astro`
- `website/src/pages/tradejournals/[id].astro`
- `website/tests/build.test.mjs`
- `website/tests/content.test.mjs`
- `website/tests/fixtures.mjs`
- `website/tests/prepare.test.mjs`
- `website/tests/rendering.test.mjs`
- `website/tests/private-preview.test.mjs`
- `website/tests/office-content.test.mjs`
- `website/tests/studio-content.test.mjs`
- `website/tests/workbench.test.mjs`
- `website/tests/workbench-publication.test.mjs`
- `website/docs/workbench.md`
- `website/docs/task-07-room-source-audit.md`
- this report and the approved Task 07 design and plan

The hub-owned task register and Task 07 brief contain hub coordination changes
and are excluded from this child's implementation ownership.

### Companion implementation and documentation

- `dashboard/drafts/service.mjs`
- `dashboard/drafts/store.mjs`
- `dashboard/media/schema.mjs`
- `dashboard/server.mjs`
- `dashboard/start.mjs`
- `dashboard/website/http.mjs`
- `dashboard/website/schema.mjs`
- `dashboard/website/service.mjs`
- `dashboard/website/upgrade.mjs`
- `dashboard/website/README.md`
- `dashboard/web/website.html`
- `dashboard/web/website.js`
- `dashboard/web/styles.css`
- `dashboard/README.md`
- `docs/DECISIONS.md`
- `tests/drafts.test.mjs`
- `tests/media-storage.test.mjs`
- `tests/ui.test.mjs`
- `tests/website-http.test.mjs`
- `tests/website-service.test.mjs`
- `tests/website-storage.test.mjs`
- `tests/website-ui.test.mjs`
- `tests/website-upgrade-crash.test.mjs`

## Final Verification

- Archive focused adapter and publication suite after navigation hardening:
  **27 passed**, zero failed.
- Full website Node suite: **115 passed**, zero failed.
- Website source and HTML Python suites: **37 passed**, zero failed.
- The first post-publication full website suite exposed four stale assertions
  that still described the former two-project, ten-photo Office layout. The
  three affected test files were updated to the approved three-room mapping;
  the focused rerun passed **5/5**.
- Post-publication canonical candidate build: **8 pages**, **24 files**, and
  **93 source references**; the output check accepted all 8 pages and 24 files.
- Companion editor DOM suite: **14 passed**, zero failed.
- All 22 available non-browser Companion files: **258 passed**, zero failed,
  with **24 explicit Playwright skips** inside the otherwise available suites.
  `tests/media-ui.test.mjs` remains omitted because this checkout cannot import
  Playwright; no omitted browser test is represented as passing.
- The final two-repository re-review approved the recovery UI, publication
  conflict checks, and Task 8 evidence with no Critical or Important finding.
  Its focused checks passed archive adapter/publication **27/27**, Companion UI
  **14/14**, service **11/11**, and HTTP **6/6**.
- Actual browser inspection verified save, reload/reopen, all six room pages,
  references, search, occupancy labels, and 13 source links.
- Runtime limitation: verification used Node 25.8.1 because the plan's pinned
  Node 24.21.0 runtime was unavailable.
- Markdown lint for the five Task 8 operating documents and report: zero errors.
- `git diff --check`: passed in both repositories.

No file is staged, committed, or pushed by this report.

## Decisions Still Required

1. Review and approve journal or inventory corrections separately.
2. Authorize Git closeout separately. Until then, the removed tracked files
   remain recoverable through Git as unstaged working-tree changes.
3. Choose hosting and deployment later.

No successor task is started by this report.
