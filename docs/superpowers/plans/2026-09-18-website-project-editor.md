# Website Project Editor And Room Separation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Build a private, revisioned Website Workbench editor and use it to prepare an isolated preview that correctly separates the dedicated office, current barre studio, and future barre studio.

**Architecture:** The archive repository remains the authority for public content validation, proposal construction, isolated Astro builds, and canonical file application. The Companion repository stores private website drafts and operation receipts in its existing owner-only SQLite database, exposes a loopback-only service, and renders the editor. A reviewed private revision may be applied to local website source files only through the explicit **Publish update** operation; the real room-separation revision remains private until Shawn separately approves its content and publication.

**Tech Stack:** Node.js 24.21.0 website runtime, Astro 7.3.2, Zod 4.5.4, Node `node:test`, Node `node:sqlite`, vanilla HTML/CSS/JavaScript, Python source inspector.

**Spec:** `docs/superpowers/specs/2026-09-18-website-project-editor-design.md`

## Global Constraints

- Preserve these source identities until Shawn explicitly confirms the move: Flickr `72177720316928566` is the dedicated office; Flickr `72177720306207693` is the current barre studio; Google Photos `af1qippool3ge7t` is the former living room and future barre studio.
- Use stable IDs `office-restoration`, `studio-office-restoration`, and `living-room-studio-restoration` in the proposed room-separation revision.
- Draft save and private preview must not modify `website/content/**`, `website/assets/**`, `website/src/generated/site.json`, `website/.generated/**`, `website/.preview-dist/**`, or `website/content/reviews/pilot.json`.
- **Publish update** means a verified local source update plus a canonical candidate preview. It does not deploy, mark content reviewed, edit journals or inventories, or perform Git operations.
- Do not run the real room-separation **Publish update** during this plan. Leave the exact previewed revision ready for Shawn's separate approval.
- Keep the existing review record in `candidate` state.
- Do not modify or delete original media. Public media promotion is additive and content-addressed.
- Do not edit `FLICKR_PUBLIC_ALBUMS.md`, `GOOGLE_PHOTOS_ALBUMS.md`, `office_restoration.md`, or `ballet_barre_studio_restoration.md`.
- Do not add application dependencies.
- Do not commit or push during task execution. Task 07 reserves Git closeout for a later instruction; each task ends with a diff and test checkpoint.
- If an approved project-ID replacement will remove tracked canonical files, refresh the deletion rule and obtain the task-specific deletion answer before publication.

---

### Task 1: Add Explicit Occupancy And Exclusive Album Ownership

**Files:**

- Modify: `website/lib/schema.mjs`
- Modify: `website/lib/content.mjs`
- Modify: `website/lib/prepare.mjs`
- Modify: `website/src/components/EvidenceDetails.astro`
- Modify: `website/tests/fixtures.mjs`
- Modify: `website/tests/content.test.mjs`
- Modify: `website/tests/prepare.test.mjs`
- Modify: `website/tests/rendering.test.mjs`

**Interfaces:**

- Produces optional project field `occupancy: { state: "current" | "future" | "former", label: string }`.
- `validateContent(raw)` rejects the same `albumKey` on two projects with code `DUPLICATE_REFERENCE`.
- Prepared public projects and search evidence include `occupancy` unchanged when present.

- [x] **Step 1: Write failing schema and ownership tests**

Add focused cases to `website/tests/content.test.mjs`:

```js
test("project occupancy is explicit and album ownership is exclusive", () => {
  const raw = makeFixture();
  raw.projects[0].occupancy = { state: "current", label: "Current barre studio" };
  assert.equal(validateContent(raw).projects[0].occupancy.state, "current");
  raw.projects[1].albumKeys = [...raw.projects[0].albumKeys];
  raw.projects[1].sourceRefs = structuredClone(raw.projects[0].sourceRefs);
  assert.throws(() => validateContent(raw), { code: "DUPLICATE_REFERENCE" });
});
```

Add invalid cases for `{ state: "moved", label: "Moved" }` and a blank label. Add a rendering assertion for `Current barre studio`.

- [x] **Step 2: Run the focused tests and confirm the intended failures**

```bash
npm --prefix website test -- --test-name-pattern="occupancy|album ownership"
```

Expected: strict project validation rejects occupancy, and duplicate album ownership is not yet rejected.

- [x] **Step 3: Implement the model and rendering**

Add this optional field to the project schema:

```js
occupancy: z.strictObject({
  state: z.enum(["current", "future", "former"]),
  label: text
}).optional(),
```

In `validateContent`, keep an `albumOwners` map outside the project loop. Reject a prior different owner with `contentError("DUPLICATE_REFERENCE", ...)`. In `publicProject`, copy occupancy into the public result and search evidence. Render its label once in `EvidenceDetails.astro` while retaining stage and recorded evidence.

- [x] **Step 4: Verify the model and rendered output**

```bash
npm --prefix website test -- --test-name-pattern="occupancy|album ownership|offline preview|candidate preview"
git diff --check
```

Expected: selected tests pass, and no current content record or review snapshot changes.

---

### Task 2: Make Astro Preview Inputs And Outputs Explicit

**Files:**

- Modify: `website/scripts/build.mjs`
- Modify: `website/astro.config.mjs`
- Modify: `website/src/content.config.ts`
- Modify: `website/src/pages/index.astro`
- Modify: `website/src/pages/search.json.js`
- Modify: `website/src/pages/work/[id].astro`
- Modify: `website/src/pages/tradejournals/index.astro`
- Modify: `website/src/pages/tradejournals/[id].astro`
- Modify: `website/lib/prepare.mjs`
- Modify: `website/tests/build.test.mjs`
- Create: `website/tests/private-preview.test.mjs`

**Interfaces:**

- `buildWebsite({ mode, repoRoot, websiteRoot, contentRoot, contentBoundaryRoot, generatedRoot, modelPath, publicRoot, outputRoot, assetOverrides })`.
- `prepareSite({ repoRoot, contentRoot, contentBoundaryRoot, mode, assetOverrides })`.
- `assetOverrides` is a `Map<mediaId, absolutePath>` contained by `contentBoundaryRoot`.
- Canonical callers omit the new options and retain all current paths and output.

- [x] **Step 1: Write a failing private-build isolation test**

Snapshot canonical `src/generated/site.json`, `.generated`, and `.preview-dist`, then call:

```js
const result = await buildWebsite({
  mode: "preview",
  repoRoot,
  websiteRoot,
  contentRoot: privateContent,
  contentBoundaryRoot: privateRoot,
  generatedRoot: path.join(privateRoot, "generated"),
  modelPath: path.join(privateRoot, "site.json"),
  publicRoot: path.join(privateRoot, "public"),
  outputRoot: path.join(privateRoot, "output"),
  assetOverrides: new Map()
});
assert.equal(result.outputRoot, path.join(privateRoot, "output"));
assert.deepEqual(await snapshots(protectedPaths), before);
```

Add a case where an asset override escapes `contentBoundaryRoot`; expect `INVALID_PATH` before Astro starts.

- [x] **Step 2: Run the isolation test and confirm it fails**

```bash
node --test website/tests/private-preview.test.mjs
```

Expected: current build behavior writes canonical generated paths and cannot honor the private options.

- [x] **Step 3: Refactor the build with canonical defaults**

Pass absolute `WK_SITE_MODEL`, `WK_STORY_ROOT`, `WK_PUBLIC_DIR`, and `WK_OUT_DIR` values to Astro. Configure the model alias:

```js
vite: { resolve: { alias: { "@site-model": siteModel } } }
```

Change the five generated-model imports to `import model from "@site-model";`. Use `WK_STORY_ROOT` as the content collection base. Keep Markdown policy unchanged.

Make `prepareSite` require `contentRoot` inside `contentBoundaryRoot`; source references still resolve against canonical `repoRoot`. Validate each asset override ID and contained path before using it for `assetCopies`.

- [x] **Step 4: Verify private isolation and canonical compatibility**

```bash
node --test website/tests/private-preview.test.mjs website/tests/build.test.mjs
npm --prefix website run build:preview
npm --prefix website run check:output
git diff --check
```

Expected: private output passes without changing protected canonical paths, and the ordinary preview still verifies.

---

### Task 3: Replace The Single-Project Adapter With Immutable Change Sets

**Files:**

- Modify: `website/lib/workbench.mjs`
- Create: `website/lib/workbench-files.mjs`
- Replace: `website/tests/workbench.test.mjs`
- Create: `website/tests/workbench-publication.test.mjs`

**Interfaces:**

- `readCatalog(root)` returns `{ projects, albumOwners, reviewState }`.
- `openProject(root, projectId)` returns `{ project, story, media, references, base }`.
- `validateChangeSet(root, changeSet, assets)` returns `{ digest, base, writes, removals, content }`.
- `buildPrivatePreview(root, proposal, { previewRoot, assets })` returns `{ digest, outputRoot, report, urlPath }`.
- `stagePublication(root, proposal, { operationRoot, assets })` returns a durable manifest.
- `applyPublication(root, manifest)` and `inspectPublication(root, manifest)` apply or classify that exact manifest.
- `buildCanonicalPreview(root)` runs the ordinary candidate build after source application and reports its result separately.
- A change set has this exact outer shape:

```js
{
  schemaVersion: 1,
  base: [{ kind, id, sha256 }],
  projects: [{ sourceId, record, story: { id, markdown } }],
  home: null,
  services: [],
  promotions: [{ itemId, hash, record }]
}
```

`sourceId` is the current ID, or `null` for a new project. A changed ID retires `sourceId` only when the replacement and all references validate. `home` is either `null` or a complete home record; `services` contains complete replacement service records. Callers never supply target paths.

- [x] **Step 1: Write failing catalog, stale-scope, and proposal tests**

Use these core assertions:

```js
const catalog = await readCatalog(f.repoRoot);
assert.deepEqual(catalog.projects.map(item => item.id), ["project-one", "project-two"]);

const opened = await openProject(f.repoRoot, "project-one");
const unchanged = {
  schemaVersion: 1,
  base: opened.base,
  projects: [{
    sourceId: opened.project.id,
    record: opened.project,
    story: opened.story
  }],
  home: null,
  services: [],
  promotions: []
};
await f.saveRecord("projects/project-two.json", {
  ...f.raw.projects[1], summary: "Unrelated edit."
});
await assert.doesNotReject(validateChangeSet(f.repoRoot, unchanged, []));
```

Create a three-album fixture and assert one proposal yields exactly:

```js
[
  "living-room-studio-restoration",
  "office-restoration",
  "studio-office-restoration"
]
```

Add rejection cases for unknown keys, duplicate album owners, unsafe IDs, stale touched records, missing stories, invalid promotion hashes, and a reviewed snapshot.

- [x] **Step 2: Run the adapter tests and confirm missing exports fail**

```bash
node --test website/tests/workbench.test.mjs website/tests/workbench-publication.test.mjs
```

- [x] **Step 3: Implement read, validation, and proposal boundaries**

Keep file confinement in `workbench-files.mjs` with these operations:

```js
readTracked(root, descriptor)
fingerprintTracked(root, descriptors)
writeTemporary(root, operationRoot, write)
replaceTracked(root, stagedWrite)
inspectTracked(root, expected)
```

`validateChangeSet` must load complete content, compare only named base descriptors, apply the overlay in memory, validate IDs/references/stories/albums/media/review state, emit sorted writes and removals with before/after SHA-256 values, and digest a canonical JSON representation. Derive paths from validated kinds and IDs.

- [x] **Step 4: Implement private preview and recoverable publication**

`buildPrivatePreview` writes only below `previewRoot`, invokes the Task 2 build interface, and returns the proposal digest with the output report.

`stagePublication` writes an owner-only operation snapshot containing exact before and after bytes plus a manifest shaped as:

```json
{
  "schemaVersion": 1,
  "proposalDigest": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "phase": "staged",
  "writes": [
    { "path": "website/content/projects/example.json", "before": null, "after": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" }
  ],
  "removals": [
    { "path": "website/content/projects/old-id.json", "before": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc" }
  ]
}
```

Synchronize files and directories. `applyPublication` rechecks base hashes, installs additive assets first, replaces records in deterministic order, and performs removals last. `inspectPublication` reports `not-started`, `partial`, or `applied`. Recovery may complete the staged after-state or restore the exact before-state.

After a verified apply, `buildCanonicalPreview` runs the existing candidate build. A build failure does not roll back verified source files; it returns `sourceApplied: true`, `candidatePreview: "failed"`, and a safe rebuild message.

- [x] **Step 5: Test every write interruption and idempotent retry**

Inject a hook after each replacement. For every stop point, reopen the manifest, inspect actual digests, recover, and assert either the complete before-state or complete after-state. Then verify:

```js
const first = await applyPublication(f.repoRoot, manifest);
const retry = await applyPublication(f.repoRoot, manifest);
assert.deepEqual(retry, first);
assert.equal((await loadContent(f.contentRoot)).review.state, "candidate");
```

Run:

```bash
node --test website/tests/workbench.test.mjs website/tests/workbench-publication.test.mjs
git diff --check
```

Expected: all adapter tests pass; private persistence and HTTP concerns remain outside the archive adapter.

---

### Task 4: Upgrade The Private Store To Website Draft Schema Version 3

**Files:**

- Create: `../tradejournals-companion/dashboard/website/schema.mjs`
- Create: `../tradejournals-companion/dashboard/website/upgrade.mjs`
- Modify: `../tradejournals-companion/dashboard/media/schema.mjs`
- Modify: `../tradejournals-companion/dashboard/drafts/store.mjs`
- Modify: `../tradejournals-companion/dashboard/start.mjs`
- Create: `../tradejournals-companion/tests/website-storage.test.mjs`
- Create: `../tradejournals-companion/tests/website-upgrade-crash.test.mjs`

**Interfaces:**

- Produces `WEBSITE_SCHEMA`, `SCHEMA_V3`, and `upgradeWebsiteStore(config, { serverStopped, onProgress })`.
- `openStore` creates v3 databases, opens valid v3 stores, and refuses v1/v2 with the correct explicit offline-upgrade instruction.
- Existing journal and media tables and rows remain unchanged across v2-to-v3 migration.

- [x] **Step 1: Write failing v3 schema and upgrade tests**

Define these strict tables:

```sql
CREATE TABLE website_drafts (
  id TEXT PRIMARY KEY, revision INTEGER NOT NULL,
  status TEXT NOT NULL, json TEXT NOT NULL
) STRICT;
CREATE TABLE website_revisions (
  draft_id TEXT NOT NULL REFERENCES website_drafts(id),
  revision INTEGER NOT NULL, digest TEXT NOT NULL, json TEXT NOT NULL,
  PRIMARY KEY(draft_id, revision)
) STRICT;
CREATE TABLE website_previews (
  draft_id TEXT NOT NULL, revision INTEGER NOT NULL,
  digest TEXT NOT NULL, json TEXT NOT NULL,
  PRIMARY KEY(draft_id, revision),
  FOREIGN KEY(draft_id, revision) REFERENCES website_revisions(draft_id, revision)
) STRICT;
CREATE TABLE website_operations (
  id TEXT PRIMARY KEY, draft_id TEXT NOT NULL, revision INTEGER NOT NULL,
  phase TEXT NOT NULL, json TEXT NOT NULL,
  created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
  FOREIGN KEY(draft_id, revision) REFERENCES website_revisions(draft_id, revision)
) STRICT;
```

Test successful v2-to-v3 backup, refusal while an owner PID is live, rollback after `schema-written`, retained verified backup, and unchanged v2 snapshot on failure.

- [x] **Step 2: Run the new tests and confirm missing modules fail**

From `../tradejournals-companion`:

```bash
node --test tests/website-storage.test.mjs tests/website-upgrade-crash.test.mjs
```

- [x] **Step 3: Implement the additive offline upgrade**

Build `SCHEMA_V3` from exact `SCHEMA_V2` table SQL plus website tables. Extend `assertSchema` to recognize exactly v1, v2, and v3. Model the upgrade on `dashboard/media/upgrade.mjs`: require all servers stopped, validate binding and absent owner, create a mode-0600 backup named with the `backup-v2-` prefix and a generated UUID, verify identity/integrity/full snapshot, add website tables inside `BEGIN IMMEDIATE`, set version 3, and roll back on failure.

Add this command path to `dashboard/start.mjs`:

```bash
node dashboard/start.mjs --upgrade-website --server-stopped --config /absolute/private/companion-config.json
```

- [x] **Step 4: Verify migration and storage regressions**

From `../tradejournals-companion`:

```bash
node --test tests/website-storage.test.mjs tests/website-upgrade-crash.test.mjs tests/media-storage.test.mjs tests/media-upgrade-crash.test.mjs tests/drafts-restart.test.mjs
git diff --check
```

Expected: all selected tests pass, the migration is additive and offline, and its verified backup remains available.

---

### Task 5: Add The Website Draft Service And HTTP Contract

**Files:**

- Create: `../tradejournals-companion/dashboard/website/service.mjs`
- Replace: `../tradejournals-companion/dashboard/website/http.mjs`
- Modify: `../tradejournals-companion/dashboard/drafts/service.mjs`
- Modify: `../tradejournals-companion/dashboard/server.mjs`
- Create: `../tradejournals-companion/tests/website-service.test.mjs`
- Replace: `../tradejournals-companion/tests/website-http.test.mjs`

**Interfaces:**

- `createWebsiteService({ config, store, media, adapter })` returns `listProjects`, `open`, `save`, `preview`, `publish`, `receipt`, `recover`, and `close`.
- `createDraftService` exposes it as `service.website` and closes it before releasing store ownership.
- HTTP routes are `GET /api/website/projects`, `GET /api/website/draft`, `POST /api/website/draft/save`, `POST /api/website/draft/preview`, `POST /api/website/draft/publish`, `GET /api/website/receipt`, `POST /api/website/recovery`, and `GET /api/website/image`.
- Every mutation uses existing same-origin and token checks plus a unique `requestId` receipt.
- Each opened private preview uses its own loopback server on an operating-system-assigned port, bound to one immutable output directory. The receipt identifies draft, revision, digest, and URL; all preview servers close during Workbench shutdown.

- [x] **Step 1: Write failing service tests**

Use a fake archive adapter with the real temporary v3 store:

```js
const saved = await website.save({
  requestId: randomUUID(), draftId, expectedRevision: 0,
  title: "Room separation", changeSet
});
assert.equal(saved.revision, 1);
assert.deepEqual((await website.open(draftId)).changeSet, changeSet);

const previewed = await website.preview({
  requestId: randomUUID(), draftId, expectedRevision: 1
});
assert.equal(previewed.preview.revision, 1);
```

Save revision 2 and assert publication fails with code `preview-required` until that exact revision has a successful preview. Also test restart/reopen, unrelated versus touched canonical changes, duplicate request IDs, capacity bounds, owner loss, interrupted publication recovery, and retained drafts after build failure.

- [x] **Step 2: Run the new service tests and confirm the module is absent**

From `../tradejournals-companion`:

```bash
node --test tests/website-service.test.mjs
```

- [x] **Step 3: Implement persistence and lifecycle**

Store complete validated change-set JSON per immutable revision. Enforce: 1 MiB payload, 100,000-character story, 20 projects per draft, 50 photos per project, and 200 website drafts. Keep selected media bytes in the existing media object store; revisions persist verified hashes and proposed public records.

Use this status sequence:

```text
draft -> previewed -> publishing -> published
                       +-> recovery
```

A new save returns to `draft` and makes older preview receipts ineligible without deleting history. On startup, inspect every `publishing` operation and mark it `published` only when every after digest exists; otherwise mark it `recovery`.

After source application verifies, call `buildCanonicalPreview`. Record `published` when source files are applied even if that build fails, while returning `candidatePreview: "failed"` and the rebuild message. Never replay the source application to repair only the preview.

- [x] **Step 4: Write failing HTTP contract tests**

Cover allowed methods, exact query keys, 64 KiB request limit, same-origin enforcement, token enforcement, safe error bodies, server stopping, and serialized mutations. Assert responses contain no local filesystem paths or private object paths.

- [x] **Step 5: Implement HTTP and server wiring**

Remove the module-level Studio project ID and all Google-specific album, URL, media-prefix, and preview-port assumptions. Validate bounded request shape, then delegate domain validation to `service.website`. Keep image reads confined to adapter-selected public media or verified ready-media hashes.

Shutdown stops new HTTP mutations, drains the website queue, closes the website service, and only then releases shared database ownership.

- [x] **Step 6: Verify service and HTTP regressions**

From `../tradejournals-companion`:

```bash
node --test tests/website-service.test.mjs tests/website-http.test.mjs tests/server.test.mjs tests/drafts-http.test.mjs tests/media-http.test.mjs
git diff --check
```

Expected: selected tests pass, exact preview binding is enforced, and errors retain the private draft.

---

### Task 6: Build The Multi-Project Website Workbench Editor

**Files:**

- Replace: `../tradejournals-companion/dashboard/web/website.html`
- Replace: `../tradejournals-companion/dashboard/web/website.js`
- Modify: `../tradejournals-companion/dashboard/web/styles.css`
- Create: `../tradejournals-companion/tests/website-ui.test.mjs`
- Modify: `../tradejournals-companion/tests/ui.test.mjs`

**Interfaces:**

- The browser consumes only Task 5 HTTP routes.
- One dirty form is retained at a time; project switching never discards edits silently.
- The visible workflow is **Open project → Save draft → Build preview → Publish update**.
- **Move album to new project** and **Replace project ID** create structured operations; the browser never sends filesystem paths.

- [x] **Step 1: Write failing DOM-level tests**

Use the existing fake DOM harness to assert:

```js
assert.deepEqual(projectOptions(), [
  "Dedicated Office",
  "Barre Studio — Current Room",
  "Living Room Restoration — Future Barre Studio"
]);
selectProject("office-restoration");
edit("project-summary", "Conservative Office summary.");
selectProject("studio-office-restoration");
assert.match(statusText(), /save or discard/i);
assert.equal(lastRequest(), undefined);
```

Add cases for reopening a saved revision, album groups, ordered galleries, alt/caption validation, exact current/future labels, preview invalidation after save, disabled publication without the latest receipt, and the local-publication explanation.

- [x] **Step 2: Run the UI test and confirm the current single-project form fails**

From `../tradejournals-companion`:

```bash
node --test tests/website-ui.test.mjs
```

- [x] **Step 3: Implement bounded editor sections**

Create these sections:

1. **Project** — selector, stable ID, title, area, occupancy state and label.
2. **Public summary** — summary, search summary, tags, stage, recorded, source label, introduction, evidence boundary.
3. **Story** — Markdown textarea and character count.
4. **Sources and albums** — grouped albums, inventory reference, **Move album to new project**, and **Replace project ID**.
5. **Photos** — order, caption, alternative text, role, focal point, remove, search-image toggle, and visibly distinct ready Photos Inbox media.
6. **Review** — revision, base status, preview receipt, preview link, and **Publish update** with its local-only explanation.

Render all source copy as text nodes or form values. Preserve keyboard order, labels, focus restoration, status announcements, narrow layout, and current Content Security Policy.

- [x] **Step 4: Add autosave through the same save operation**

After 1.5 seconds of inactivity, autosave only when a draft already exists and the form is valid. Keep **Save draft** visible. A 409 conflict retains every form value and offers **Reopen saved revision** and **Save as separate draft**. Unsaved invalid input blocks project switching until explicitly saved or discarded.

- [x] **Step 5: Verify DOM behavior and available browser automation**

From `../tradejournals-companion`:

```bash
node --test tests/website-ui.test.mjs tests/ui.test.mjs tests/drafts-ui.test.mjs
node --test tests/*.test.mjs
git diff --check
```

If the full command fails only because Playwright or Chrome is absent, record the exact missing dependency and run every non-browser test file. Do not report the browser suites as passing.

Expected: the editor contains no hard-coded Studio album, source URL, or media-ID prefix.

---

### Task 7: Prepare The Corrected Three-Room Draft And Private Preview

**Files:**

- Create: `website/docs/task-07-room-source-audit.md`
- Modify only private Workbench state under the configured `dataDirectory`
- Do not modify canonical `website/content/**` or `website/assets/**`

**Interfaces:**

- Consumes the completed editor and approved source identity map.
- Produces one saved and previewed private change set with an exact revision and digest receipt.
- Produces a source audit separating image observations, album metadata, journal claims requiring correction, and claims withheld from public copy.

- [x] **Step 1: Record the source audit**

Document these ownership facts:

```text
Flickr 72177720316928566 -> dedicated office -> selected flickr-539… media
Flickr 72177720306207693 -> current barre studio -> selected flickr-527… media
Google Photos af1qippool3ge7t -> former living room / future barre studio -> selected studio-… media
```

Withhold the Office floor chronology and reclaimed/charred-door narrative unless independently supported. Record that `flickr-52705240355` shows a stripped door installed before a separately described finish; it does not prove a final installed charred door. Leave conflicting Flickr dates unresolved.

- [x] **Step 2: Create a real private room-separation draft**

Use Workbench to:

1. keep `office-restoration` with album `72177720316928566` and five `flickr-539…` placements;
2. move album `72177720306207693` and five `flickr-527…` placements into new project `studio-office-restoration`;
3. replace `studio-restoration` with `living-room-studio-restoration` while preserving its Google album, three accepted media records, captions, alternatives, roles, and order;
4. update home, navigation, and `historic-floors` references inside the change set; and
5. set explicit occupancy labels for all three rooms.

Use conservative source-backed copy and do not cite the mixed Office journal as already corrected.

- [x] **Step 3: Save, close, reopen, and compare the draft**

Record draft ID, revision, and digest for the task report. Close and reopen Workbench. Compare project IDs, album keys, gallery IDs, story digests, and home/service references with the saved revision.

Expected: the reopened revision is identical and canonical Git state has no Task 07 content or asset changes.

- [x] **Step 4: Build and inspect the exact private preview**

Inspect all three `/work/{project-id}/` and `/tradejournals/{project-id}/` pages, home links, Historic Floors links, search results, occupancy labels, and all thirteen selected image source links.

Confirm the current studio is never called former, the future studio is never called current, and the future status remains explicit. Confirm the preview receipt matches the reopened revision and digest.

- [x] **Step 5: Prove preview isolation**

Before and after the build, compare SHA-256 snapshots of:

```text
website/content
website/assets
website/src/generated/site.json
website/.generated
website/.preview-dist
```

Expected: canonical state is byte-for-byte identical. `website/content/reviews/pilot.json` remains `candidate`; journal and inventory files remain unchanged.

- [x] **Step 6: Stop before real publication**

Leave **Publish update** unused for this draft. Record its status and the exact content approval still required. Do not remove canonical `studio-restoration` files.

---

### Task 8: Documentation, Full Verification, And Workflow Return

**Files:**

- Modify: `website/docs/workbench.md`
- Modify: `../tradejournals-companion/dashboard/website/README.md`
- Modify: `../tradejournals-companion/dashboard/README.md`
- Modify: `../tradejournals-companion/docs/DECISIONS.md`
- Create: `docs/website-workflow/reports/task-07-edit-project.md`
- Do not modify: `docs/website-workflow/task-register.md`
- Do not modify: `docs/website-workflow/task-07-edit-project.md`

**Interfaces:**

- Maintainer docs distinguish private draft, private preview, canonical candidate files, reviewed snapshot, local candidate preview, and eventual hosted output.
- Workflow report identifier is `WK-WEB-T07-R01`.

- [x] **Step 1: Update operating documentation**

Document the user flow, offline v3 upgrade command, recovery states, private preview semantics, **Publish update** scope, and explicit occupancy-confirmation rule. Explain that structured-file editing remains available and that external edits to touched records make a draft safely stale.

- [x] **Step 2: Run archive verification**

From `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/TradeJournals`:

```bash
npm --prefix website test
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_website_sources tests.test_website_html
npm --prefix website run build:preview
npm --prefix website run check:output
npm run lint:md -- docs/superpowers/specs/2026-09-18-website-project-editor-design.md docs/superpowers/plans/2026-09-18-website-project-editor.md website/docs/workbench.md website/docs/task-07-room-source-audit.md docs/website-workflow/reports/task-07-edit-project.md
git diff --check
```

Expected: all available checks pass. Release remains blocked by candidate review state and is verified through its existing protection test.

- [x] **Step 3: Run Companion verification**

From `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/tradejournals-companion`:

```bash
node --test tests/*.test.mjs
git diff --check
```

If Playwright is unavailable, rerun every non-browser test file and report the omitted files and exact reason. Do not install dependencies or count those suites as passing.

- [x] **Step 4: Review privacy and both Git states**

```bash
git status --short --branch
git diff --stat
git -C ../tradejournals-companion status --short --branch
git -C ../tradejournals-companion diff --stat
```

Confirm no private configuration, database, media object, preview output, credential, or machine-specific path entered either worktree. Confirm the hub-owned brief and register remain unedited by Task 07.

- [x] **Step 5: Write the completion report**

Record `WK-WEB-T07-R01`, approved spec/plan paths, behavior in both repositories, room identities, private revision/digest/preview receipt, canonical isolation evidence, exact test totals, changed paths, both Git states, unapplied publication, separate journal proposals, and the absence of commit/push/deployment/review-state change/successor task.

- [x] **Step 6: Return the reviewable result**

Rename this child task to `Website 1 - Task 07 Edit Project - READY FOR REVIEW`, verify the title, and send `WK-WEB-T07-R01` once to hub task `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`. The hub reconciles the report; it does not publish the draft or start another task.

---

## Final Execution Boundary

Implementation ends with a private, exact room-separation preview ready for Shawn's content review. These remain separate decisions:

1. approve or revise the three-room public copy and preview;
2. authorize **Publish update** for that exact revision;
3. answer the task-specific deletion question before retiring old tracked `studio-restoration` files;
4. approve journal or inventory corrections;
5. approve Git closeout; and
6. choose hosting and internet deployment later.
