# Website Project Editor And Room Separation Design

- Date: 2026-09-18
- Status: Written specification approved by Shawn on 2026-09-18
- Workflow: Website 1 - Task 07 Edit Project And Room Separation
- Development branches: `codex/website-updates` and `codex/website-workbench`

## Purpose

Extend TradeJournals Workbench from its current Studio photo selector into a
small project editor. Shawn should be able to open a website project, edit its
story and presentation, save a private draft, inspect the exact draft in an
isolated website preview, and explicitly apply that reviewed revision to the
local website records.

The first real use of this workflow is to untangle three rooms that the current
Office page partly combines. The editor must preserve source identity and make
the room correction reviewable before any tracked website file changes.

The public Astro website remains a static build that consumes structured files
from the archive repository. It must not depend on Workbench, its database, or a
running local service.

## Goals

1. List and open every website project rather than hard-code one project.
2. Edit project copy, story Markdown, source albums, selected photographs,
   captions, alternative text, roles, focal points, and ordering.
3. Save revisions privately without modifying tracked website records, selected
   public assets, the review snapshot, generated files, or preview output.
4. Build a private preview from one immutable saved revision.
5. Apply the exact previewed revision to canonical local website files through
   an explicit **Publish update** action.
6. Detect stale canonical records before preview or publication and retain the
   private draft when a conflict or interruption occurs.
7. Separate the Office, current barre studio, and future barre studio while
   preserving their distinct evidence.

## Non-Goals

- Hosting, internet deployment, domains, analytics, authentication, or a public
  content-management system.
- Git staging, commits, pushes, merges, or release approval.
- Changing `website/content/reviews/pilot.json` to `reviewed`.
- Editing journals, album inventories, or original source media.
- Inferring that the barre studio has moved from renovation progress, album
  names, photographs, or dates.
- A general-purpose page builder or arbitrary component editor.

## Authoritative Room Identities

The following identity map overrides earlier wording that called the Flickr
studio former or treated the former living room as the current studio.

| Stable project ID | Approved public label | Source album | Meaning |
| --- | --- | --- | --- |
| `office-restoration` | Dedicated Office | Flickr `72177720316928566` | The separate dedicated office |
| `studio-office-restoration` | Barre Studio — Current Room | Flickr `72177720306207693` | The current barre studio and current home of The Repair Shop; originally Shawn's office/yoga room |
| `living-room-studio-restoration` | Living Room Restoration — Future Barre Studio | Google Photos `af1qippool3ge7t` | The former living room being renovated as the future barre studio |

The stable IDs describe physical source identity rather than a temporary label.
When Shawn explicitly confirms that the move has occurred, a later edit may
change the public labels and occupancy values without reassigning the source
albums or reusing another project's ID.

The existing `studio-restoration` record becomes
`living-room-studio-restoration` as part of the reviewed room-separation change
set. Its three accepted Google Photos selections and their durable media IDs are
preserved. The current barre studio receives the new
`studio-office-restoration` identity.

## Public Content Model

Add an optional `occupancy` object to project records:

```json
{
  "state": "current",
  "label": "Current barre studio"
}
```

`state` accepts `current`, `future`, or `former`; `label` is nonblank public
copy. The three room projects use explicit occupancy values during this
transition. The project page, archive page, and search evidence display the
label. The label is descriptive context and does not replace the restoration
`stage` field.

One album key may belong to only one project. Content validation rejects a
duplicate album owner across the public project collection. Selected media must
still belong to one of the owning project's album keys. Moving an album in a
change set therefore transfers its matching inventory reference and all
selected placements from the old owner or requires the editor to remove those
placements explicitly.

Story Markdown remains a separate file identified by `storyId`. Project copy
and story copy are editable together in one draft, but the public website keeps
the existing file boundaries:

- `website/content/projects/<id>.json` owns structured project presentation.
- `website/content/stories/<storyId>.md` owns the long narrative.
- `website/content/media/<id>.json` owns durable public media identity.
- `website/assets/**` owns selected public renditions.
- home and service records own project listings and references.

## User Flow

### Open Or Start A Draft

The Website Workbench opens with a project selector. Each entry shows its public
title, stable ID, occupancy label when present, source albums, and whether a
private draft exists.

Opening a project reads its canonical project record, story, matching source
media, and only the home/service references that name it. The editor records
individual SHA-256 base fingerprints for those records. Unrelated website
changes do not make the draft stale.

The editor may start a draft for one project or use **Move album to new
project**. That focused operation collects a new stable ID and public title,
creates a blank story within the private change set, and moves the chosen album,
matching inventory reference, and chosen placements. It does not create tracked
files. Project ID replacement is represented as one multi-record change set so
the old record, story, home references, and service references change together.

### Edit And Save Draft

The editor exposes these bounded fields:

- title, area, summary, search summary, tags, stage, recorded evidence,
  source label, introduction, evidence boundary, and occupancy;
- story Markdown;
- album ownership and inventory source references;
- gallery membership, order, caption, alternative text, role, and focal point;
- search image selection;
- existing public media and inspected ready photos from Photos Inbox.

Saving creates a new immutable private revision. Autosave may call the same save
operation after a short idle period, but the visible **Save draft** control
remains available. Revision conflicts preserve the browser text and ask the user
to reopen or save a separate draft.

### Preview

**Build preview** validates one saved revision against its stored base
fingerprints, materializes a complete content overlay in an owner-only private
workspace, and runs the existing Astro preparation and output checks with
revision-specific generated-model, public-media, and output paths.

Preview never writes:

- `website/content/**`;
- `website/assets/**`;
- `website/src/generated/site.json`;
- `website/.generated/**`;
- `website/.preview-dist/**`; or
- `website/content/reviews/pilot.json`.

The preview URL identifies the draft revision. Saving another revision does not
change the older preview. Prior private previews remain untouched until a
separate cleanup policy is approved.

### Publish Update

The button label is **Publish update**. In this local workflow, publication means
applying the exact previewed revision to canonical website source files and
rebuilding the ordinary local candidate preview. It does not deploy to the
internet, approve a release, edit a journal, or perform a Git operation. The UI
states this beside the button.

Publication is enabled only when:

1. the latest saved revision has a successful private preview receipt;
2. the preview receipt matches the exact draft revision and content digest;
3. every touched canonical record still matches its stored base fingerprint;
4. the complete proposed public content validates; and
5. the review record remains in `candidate` state.

Publication writes only the files named in the immutable proposal. New media
records and public renditions are additive. Multi-record replacements use a
durable operation receipt, temporary files, file synchronization, and ordered
atomic renames. The operation then rereads every expected file and verifies its
digest before marking the revision published. Retrying a verified publication
returns the same receipt without applying it twice.

After the canonical write verifies, Workbench runs the existing candidate build
into the ordinary local preview. A build failure leaves the verified source
update recorded as applied and reports that the local preview needs rebuilding;
it does not attempt to reverse already verified source files.

## Private Persistence

Use additive version-3 tables in the existing owner-only
`<dataDirectory>/drafts.sqlite` store. This reuses its archive binding, single
writer ownership, WAL mode, `synchronous=FULL`, revision pattern, receipts, and
recovery handling instead of creating another configuration surface.

The added tables have distinct website-specific names:

- `website_drafts`: current revision and summary for each private change set;
- `website_revisions`: immutable JSON payload and digest for every revision;
- `website_previews`: successful preview receipt keyed by draft and revision;
- `website_operations`: publication request, phase, expected writes, and result.

The schema upgrade is additive. Before upgrading a version-2 database, the
store creates and verifies its existing backup copy using the same guarded
migration boundary. A failure leaves the version-2 database usable and intact.
Private website payloads have the same owner-only directory and archive-checkout
binding as journal drafts.

## Component Boundaries

### Archive Repository

`website/lib/workbench.mjs` becomes the canonical adapter for reading public
website records, validating a complete proposed overlay, calculating
record-specific fingerprints, and applying a verified immutable proposal. It
does not own private draft persistence or HTTP behavior.

A separate preview helper accepts an explicit content root, model output path,
public staging path, and output path. The ordinary `website/scripts/build.mjs`
continues to supply the existing canonical paths. Workbench supplies private
paths. Astro pages import a configured generated-model alias so a private build
does not rewrite `src/generated/site.json`.

The public schema and preparation code own occupancy rendering and exclusive
album ownership validation. They do not know about private draft IDs or database
records.

### Companion Repository

`dashboard/website/service.mjs` owns website draft revisions, preview receipts,
publication receipts, stale checks, and recovery. It calls the archive adapter
through a narrow interface.

`dashboard/website/http.mjs` authenticates local requests, validates bounded
payloads, serializes mutations, and exposes project list, draft, preview, and
publish operations. It no longer hard-codes `studio-restoration`, the Google
Photos album, a media-ID prefix, or one source URL pattern.

`dashboard/web/website.js` owns browser editor state and rendering. It does not
write files or infer room identity. `dashboard/web/website.html` provides the
project selector, edit sections, draft status, preview link, and publication
summary. Existing Workbench styling is extended rather than introducing a new
visual system.

## Room-Separation Change Set

Task 07 prepares, previews, and leaves ready for Shawn's review one private
change set with these effects:

1. `office-restoration` retains only Flickr album `72177720316928566` and its
   five `flickr-539…` selections. Copy is limited to what that album and its
   inspected images support. The 2021–2022 floor sequence and reclaimed/charred
   door claims are removed from the Office presentation unless separately
   supported by Office evidence.
2. `studio-office-restoration` receives Flickr album `72177720306207693` and its
   five `flickr-527…` selections. It is labeled as the current barre studio.
   Floor and door wording remains conservative: the selected door photograph
   shows a stripped door installed before a separately described finish, not a
   final installed charred door. Conflicting Flickr dates are not converted into
   a confident chronology.
3. `studio-restoration` is replaced by
   `living-room-studio-restoration`. Its Google Photos album, three accepted
   selections, captions, alternatives, and source identity remain intact. Its
   title and occupancy state clearly state that the former living room is the
   future barre studio and that final occupancy has not been confirmed.
4. Home and service references are updated to the stable project IDs within the
   same change set. No redirect is required before the site has a public hosting
   contract; the old ID is removed only when all local references validate.

The new current-studio story and revised Office story use conservative,
source-backed prose. Journal corrections are documented separately and remain
unapplied. The public records may cite the corresponding album inventory without
claiming that a mixed journal has already been corrected.

## Stale Edits, Failures, And Recovery

- A draft becomes stale only when a record in its base-fingerprint set changes.
  Unrelated project edits do not block it.
- Preview rechecks the complete overlay and current base. A stale draft remains
  saved and receives no new preview receipt.
- Publication rechecks the base immediately before the first canonical write.
- Expected target paths are fixed in the reviewed proposal; IDs and paths are
  validated before any write.
- If publication stops between renames, the durable operation and the actual
  file digests determine which writes landed. Workbench blocks further edits to
  that draft until recovery verifies completion or safely restores the exact
  pre-operation bytes from its private operation snapshot.
- Original source media are never moved or deleted. Public image promotion is
  additive, content-addressed, and verified before a project may reference it.
- A private preview or ordinary candidate-build failure reports the exact stage
  and keeps the saved draft and receipts available.

## Verification

Archive tests cover:

- occupancy schema and rendering;
- exclusive album ownership;
- project creation, project-ID replacement, and complete reference updates;
- record-scoped fingerprinting;
- overlay validation without canonical writes;
- private build paths that leave all canonical generated and preview paths
  byte-for-byte unchanged;
- exact multi-project publication, idempotent retry, and interrupted-write
  recovery;
- unchanged `candidate` review state;
- the three corrected room identities and source albums; and
- release protection and existing output validation.

Companion tests cover:

- version-2 to version-3 private-store migration and backup;
- save/reopen of immutable website draft revisions;
- project listing without a hard-coded Studio ID;
- stale-edit behavior limited to touched records;
- preview-receipt binding to the exact revision;
- disabled publication before preview or after a new save;
- authenticated, serialized, bounded HTTP mutations;
- publish receipts and recovery after failures at each write phase; and
- browser-editor state for project switching, unsaved changes, album transfer,
  and current/future labels.

Manual verification uses the actual Workbench UI to reopen a saved draft, inspect
all three room projects, build the private preview, compare its room pages and
search results, and exercise **Publish update** only after the change set receives
separate content approval. If Playwright remains unavailable, report browser
automation as unrun and record the manual checks; do not count missing suites as
passing.

## Acceptance Criteria

The implementation is ready for content review when:

- all three projects appear with the approved stable identities and explicit
  current/future labels in a private saved draft;
- closing and reopening Workbench restores the exact draft revision;
- the private preview shows the corrected separation and does not alter any
  canonical website or review file;
- the preview receipt names the exact revision and content digest;
- an unrelated project edit does not create a false conflict;
- a touched-record edit blocks preview and publication without losing the draft;
- publication remains a separate explicit action and states its local scope;
- the candidate review snapshot remains unchanged;
- journals, inventories, and source media remain unchanged; and
- automated and manual results distinguish passed, failed, and unavailable
  checks accurately.

Actual publication of the room-separation change set requires Shawn's separate
approval after he reviews the private preview. Git closeout, internet deployment,
release approval, and journal corrections require their own instructions.
