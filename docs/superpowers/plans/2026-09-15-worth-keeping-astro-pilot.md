# Worth Keeping Astro Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a local, reviewable Worth Keeping pilot in which one Office
Restoration record supplies a project page, featured card, gallery, and search
result, while preserving the existing prototype and archive.

**Architecture:** Validate framework-independent JSON content and resolve its
local source references before Astro renders any HTML. Build only selected
public data and assets, with separate candidate-preview and reviewed-release
outputs. Retain the current prototype as the migration comparison baseline.

**Tech Stack:** Astro 7.3.2; project-scoped Node 24.21.0; Zod 4.5.4; plain
JavaScript modules and CSS; Python standard library for existing archive
parsing; Node's test runner and Python unittest. No UI framework, database,
host adapter, CMS, or network-dependent content loader.

**Spec:** [Approved architecture](../specs/2026-09-15-worth-keeping-website-design.md).

## Execution Direction — September 15, 2026

Shawn approved this plan and then instructed: "then get started and make sure
to use the workflow-hub skill too." The website updates task is the hub;
its [register](../../website-workflow/task-register.md) records individual
assignments, dispatches, and observed outcomes. That later instruction
authorizes the first implementation task and its user-visible workflow child.
Git closeout and publication remain separate.

Shawn's implementation standard is "more tech savy than the average tradesman,
but less flashy than an influencer wanna be site." Keep dependencies and
abstractions small; use ordinary functions and explicit data. Build the checks
needed by this pilot without inventing plugin systems, generic CMS frameworks,
deployment infrastructure, or speculative dashboard integrations. Real craft,
clear photographs, readable type, and straightforward navigation lead.

## Global Constraints

- Development branch: `codex/website-updates` in the current checkout.
- Working identity: **Worth Keeping — Time & Timber Restoration**.
- Exact service line: **Historic floors, interior woodwork, and architectural restoration.**
- "The website will use Astro to generate static files."
- "It will build independently of the private Companion Dashboard."
- "Hosting remains undecided; the core output must work on a conventional static web host with custom-file upload support."
- "Components receive validated data."
- "Only explicitly selected public records and assets are emitted."
- "Generated concept imagery has a separate illustration role and cannot satisfy a project-evidence selection."
- "Original media is preserved. Gallery counts are derived from actual selections."
- "Do not move journals, bulk rewrite the archive, or remove the prototype during this first implementation."
- Do not change the Companion repository or read its private database/media store.
- No commit, push, deployment, external contact, or user-visible task dispatch
  is authorized by this plan alone. The later workflow instruction above
  authorizes scoped child dispatch; it does not authorize Git closeout or
  publication. These constraints override skill commit examples.
- The pilot remains a local review candidate until Shawn accepts its exact copy
  and media selection. Never manufacture a reviewed state to pass a build.

## Plan Scope And Starting Evidence

This plan implements the architecture's **first implementation boundary**.
Full five-pillar migration, final typography/photography approval, contact
processing, Dashboard editing, hosting, and launch remain follow-up work.
They do not require empty modules or placeholder screens in this pilot.

Before execution, refresh Git status and applicable instructions. The planning
snapshot is `e16be25` on `codex/website-updates`, with only the design and plan
documents uncommitted. Preserve any work that appears after this snapshot.

Read these existing records:

- [Module map](../../../MODULE_MAP.md)
- [Website working guide](../../../site_example/README.md)
- [Evidence catalog](../../../site_example/evidence-source.json), Office entry
- [Current page](../../../site_example/index.html), `journal-office`
- [Office journal](../../../01_the_residence_1894/trade_journals/office_restoration.md)
- [Flickr inventory](../../../FLICKR_PUBLIC_ALBUMS.md), the two Office album blocks
- [Source builder](../../../scripts/build_site_evidence.py)
- [Search ranking](../../../site_example/journal-search.js)

Astro and Node versions were resolved from the official npm registry and Node
release index on September 15, 2026. Astro 7.3.2 declares Node `>=22.12.0`;
Astro's installation guidance excludes odd-numbered Node versions. This Mac's
default Node was 25.8.1, so execution must select the supported pinned runtime
locally. Do not replace the global Node used by other projects.

## File Map

Paths below are repository-relative. Only documentation exists at planning time.

| Files | Responsibility |
| --- | --- |
| `website/package.json`, `website/package-lock.json`, `website/.node-version` | Pinned website dependencies, commands, runtime |
| `website/astro.config.mjs` | Static mode, output paths, local preview behavior |
| `website/content/site.json`, `website/content/home.json` | Identity and ordered homepage choices |
| `website/content/services/historic-floors.json` | Pilot offering and supporting project reference |
| `website/content/projects/office-restoration.json` | Public project presentation |
| `website/content/media/flickr-<photo-id>.json` | Ten selected source-to-asset mappings |
| `website/content/stories/office-restoration.md` | Curated optional longer narrative |
| `website/content/reviews/pilot.json` | Candidate/reviewed content snapshot, separate from deployment |
| `website/lib/content.mjs`, `website/lib/schema.mjs` | Load records and enforce the content contract |
| `website/lib/review.mjs`, `website/lib/prepare.mjs` | Compare scoped fingerprints and prepare the public model |
| `scripts/inspect_website_sources.py` | Reuse archive parsing and return requested source facts |
| `website/scripts/build.mjs`, `website/scripts/check-output.mjs` | Ordered build and generated-output verification |
| `scripts/check_website_html.py`, `tests/test_website_html.py` | Parse emitted HTML references and test parser behavior |
| `website/src/content.config.ts`, `website/lib/markdown-policy.mjs` | Selected Markdown stories and non-executable content policy |
| `website/src/layouts/SiteLayout.astro` | Shared document shell and navigation |
| `website/src/components/Hero.astro`, `ServiceSection.astro`, `ProjectCard.astro`, `ProjectGallery.astro`, `EvidenceDetails.astro`, `ArchiveSearch.astro`, `ContactInvitation.astro` | Focused presentation components |
| `website/src/styles/tokens.css`, `base.css` | Shared visual settings and base accessibility styles |
| `website/src/pages/index.astro`, `work/[id].astro`, `tradejournals/index.astro`, `tradejournals/[id].astro`, `search.json.js` | Pilot routes and generated search data |
| `website/src/scripts/archive-search.js` | Browser search controls and result display |
| `website/tests/*.test.mjs`, `website/tests/fixtures.mjs` | Synthetic contract, review, rendering, and output cases |
| `tests/test_website_sources.py` | Network-free Python source-boundary tests |
| `website/README.md`, `website/docs/office-content-review.md` | Workflow, evidence reconciliation, review instructions |
| `.gitignore`, `package.json` | Ignore generated website files; add root convenience commands |

Component filenames after the first item in a row share its directory. Test
filenames are specified per task below. Add no other production module unless
its responsibility is documented and needed to complete the task.

## Content And Build Contracts

### Editable Records

Use strict schemas: reject unknown fields rather than serializing arbitrary
objects into the public output. All records have `schemaVersion: 1` and a stable
`id` that matches their filename. IDs use lowercase letters, digits, and hyphens.

| Record | Required Fields Beyond Version And ID | Optional Fields |
| --- | --- | --- |
| Site | `name`, `descriptor`, `serviceLine`, `navigation: [{label, href}]` | `contact: {label, href}`; omit until agreed |
| Home | `headline`, `intro`, `featuredProjectIds`, `serviceIds` | `heroMediaId` |
| Service | `title`, `description`, `projectIds` | None |
| Project | `title`, `area`, `summary`, `searchSummary`, `tags`, `stage`, `recorded`, `sourceLabel`, `sourceRefs`, `albumKeys`, `gallery`, `searchMediaIds` | `introduction`, `storyId`, `evidenceBoundary` |
| Media | `kind`, `assetPath`, `sourceUrl`, `albumKey`, `alt`, `width`, `height` | None |
| Review | `state`, `records`, `sources` | None |

`searchSummary` may be an empty string, which means use `summary`. Each gallery
placement is `{mediaId, caption, role, focalPoint?, alt?}`; `focalPoint` is a pair
of finite percentages from 0 through 100. Roles are `context`, `condition`,
`process`, `detail`, or `result`. Roles and captions require source/visual review.
An invented fixture may use `result`; no real photo acquires that role by default.

`kind` is `evidence` or `illustration`. Project galleries and search selections
must resolve to `evidence` media. `assetPath` is a repository-relative path to a
selected file; realpath containment must reject traversal and symlink escapes.
Allow only selected JPEG, PNG, WebP, or AVIF media in this pilot. SVG and executable
file types are outside the accepted public-media contract.
`width` and `height` are positive integer pixel dimensions measured from the
selected local file during content preparation.

`sourceRefs` contains `{kind, path, anchor?}` with kinds `journal`, `inventory`,
or `reference`. Inventory references require the exact `album-<id>` anchor.
Journal/reference fingerprints cover file bytes. Inventory fingerprints cover
only the named block, ending at the next album anchor, with normalized newlines.
Selected media fingerprints cover their bytes. Never fingerprint the Git HEAD.

The review record has `state: "candidate" | "reviewed"`, and arrays of
`{key, sha256}` snapshots. `records` covers the selected site/home/service/project/
media JSON and selected story, excluding the review record itself. `sources`
covers explicitly referenced archive material and selected image bytes. Use
SHA-256, deterministic keys, and deterministic JSON serialization for record
digests. Unrelated projects/album blocks must not invalidate the pilot review.

Changing reviewed public copy must invalidate its saved content digest. The
preparation command can print a proposed snapshot but must never update
`state` or accepted digests automatically. Real snapshot acceptance follows
Shawn's exact content review. Synthetic tests create their own reviewed fixtures.

### Public Model And URLs

`prepareSite({repoRoot, contentRoot, mode})` returns
`Promise<{model, report, assetCopies}>`. `mode` is `preview` or `release`.

- `model`: `{site, home, services, projects, searchEntries, reviewNotice}`.
- Public home: `{headline, intro, featuredProjectIds, serviceIds, hero?}`;
  `hero` is the resolved public image for `heroMediaId`, when configured.
- Each public project: `{id, title, area, summary, introduction, stage, recorded,
  sourceLabel, evidenceBoundary, href, archiveHref, storyId, albums, gallery,
  searchImages}`. Optional values become empty text or absent fields as defined
  by consumers, never stringified `undefined`.
- Public album: `{key, label, count, sourceUrl, shown}`; `shown` comes from the
  selected gallery. Count means recorded inventory count, not a live assertion.
- Public image: `{id, src, alt, width, height, sourceUrl, caption?, role?, focalPoint?}`. `src` is
  `/media/<stable-id>.<extension>`; internal asset paths are not emitted.
- `searchEntries` retain the current ranker's input shape:
  `{title, area, summary, tags, source, url, images, evidence}`. Use a public
  archive destination for `source`, not a local journal path. `evidence` is
  `{stage, recorded, sourceLabel}` and `images` is the selected search subset.
- `report`: internal validation and proposed fingerprint data; never published.
- `assetCopies`: validated `{sourceAbsolute, publicRelative}` pairs; never
  serialized into the public model.

Routes for the pilot are `/`, `/work/office-restoration/`, `/tradejournals/`,
`/tradejournals/office-restoration/`, and `/search.json`. The archive index shows
only the pilot selection and does not claim full five-pillar coverage. The
project route displays the concise presentation; the archive route displays
the selected longer story and evidence links. Both are generated from the same
project ID. The existing prototype URLs remain untouched during the pilot.

### Ordered Build

1. Load and schema-check the selected local records.
2. Inspect only their named archive sources and media, then compare review
   fingerprints. Invalid references always fail; candidate/stale review status
   permits a visibly labeled local preview but blocks release.
3. Write the public model to ignored `website/src/generated/site.json` and the
   internal review report to ignored `website/.generated/review.json`. Stage
   only validated selected assets in a fresh directory beneath `.generated/`
   for this run.
4. Invoke Astro with that asset directory as `publicDir`. Components read the
   public model; no component calls Python or external source services.
5. Validate generated pages, assets, local destinations, and output contents.

`build:preview` writes `website/.preview-dist/`; `build` is the release command
and writes `website/dist/`. Preview has a visible review notice and `noindex`.
Release must reject candidate/stale snapshots before producing a fresh release
artifact. A failed build cannot be reported as current based on an old `dist`.

## Task 1: Validated Records And Offline Source Preparation

**Files:** Create the package/runtime files; `website/lib/schema.mjs`,
`content.mjs`, `review.mjs`, `prepare.mjs`; `scripts/inspect_website_sources.py`;
`website/tests/fixtures.mjs`, `content.test.mjs`, `review.test.mjs`;
`tests/test_website_sources.py`. Modify `.gitignore` only for the new website
dependency, runtime, and generated paths.

**Interfaces:**

- `loadContent(contentRoot)` returns the parsed site, home, service, project,
  media, and review records without altering them.
- `validateContent(raw)` returns the schema-checked records and resolved ID
  relationships; failures carry `{code, recordId, field, message}`.
- `inspect_sources(repo_root: Path, requests: list[dict]) -> list[dict]` returns
  `{key, sha256, count?, label?, sourceUrl?}` for explicitly requested sources.
  Each request is `{key, kind, path, anchor?}`. Inspector kinds are `journal`,
  `inventory`, `reference`, and `media`; only inventory requests have anchors.
  The extra `media` kind is generated from selected media records, not accepted
  as a project `sourceRefs` kind.
- `compareReview(review, actual)` returns `{state, changedKeys}` where state is
  `current`, `candidate`, or `stale`.
- `prepareSite(options)` implements the public model contract above.
- `makeFixture()` returns a complete valid invented-content object with two
  projects, three media records, one service, and a candidate review record.
  Tests serialize it beneath a temporary repository when files are needed.

- [ ] Confirm `codex/website-updates`, record the working tree, and run the
  existing `npm run check:site-evidence` and `npm run test:site` baseline. Report
  any failure before changing behavior; do not bypass a failing baseline.
- [ ] Select Node 24.21.0 only for this project. If no suitable runtime is
  available, the scoped npm package below can supply the pinned executable.
  Add the ignored directory before using it; do not run a global upgrade.

  ```sh
  npm install --prefix website/.runtime --no-save --package-lock=false node@24.21.0
  export PATH="$PWD/website/.runtime/node_modules/node/bin:$PATH"
  node --version
  ```

  Expected: `v24.21.0`. Use this shell/runtime for all website commands. Record
  that the existing Dashboard's global runtime was not changed.
- [ ] Create `website/package.json` with `type: "module"`, exact dependencies
  `astro: "7.3.2"` and `zod: "4.5.4"`, `engines.node: "24.21.0"`, and initial
  script `test: "node --test tests/*.test.mjs"`. Write `24.21.0` to
  `website/.node-version`. Run `npm install --prefix website` under the selected
  runtime and retain `website/package-lock.json`.
- [ ] Write the fixtures and failing relationship tests, including this case:

  ```js
  import test from "node:test";
  import assert from "node:assert/strict";
  import { validateContent } from "../lib/content.mjs";
  import { makeFixture } from "./fixtures.mjs";

  test("a missing featured project is a precise content error", () => {
    const raw = makeFixture();
    raw.home.featuredProjectIds = ["missing-project"];
    assert.throws(() => validateContent(raw), error =>
      error.code === "MISSING_REFERENCE" &&
      error.field === "home.featuredProjectIds[0]"
    );
  });
  ```

  Add duplicate IDs, filename/ID mismatch, unsupported schema version, empty
  required values, illustration-as-evidence, invalid focal points, and absent
  search/gallery media relationships. Run `npm --prefix website test`; confirm
  failures reflect the missing behavior, not a malformed test fixture.
- [ ] Implement strict Zod record schemas and explicit ID resolution. Never
  spread raw record objects into the public model. Use this identity rule:

  ```js
  import { z } from "zod";
  export const StableId = z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/);
  export const Version = z.literal(1);
  ```

  Validate local navigation as root-relative paths; external evidence/contact
  URLs must use HTTPS. Do not allow `javascript:`, `data:`, `file:`, protocol-
  relative URLs, or raw local filesystem paths in public URL fields.
- [ ] Add Python tests using synthetic inventories with two album blocks.
  Changing the unreferenced block must leave the requested block fingerprint
  unchanged; changing its count must alter it. Test absent/duplicate anchors,
  nonexistent sources, `../` traversal, and symlink escapes. Reuse the existing
  builder's `parse_inventory_counts` function by importing it from the sibling
  module; do not call `build_manifest`, which depends on existing page HTML.

  ```python
  from hashlib import sha256
  from build_site_evidence import parse_inventory_counts

  def fingerprint_inventory_block(block: str) -> str:
      normalized = block.replace("\r\n", "\n").replace("\r", "\n")
      return sha256(normalized.encode("utf-8")).hexdigest()
  ```

  The CLI accepts JSON requests over stdin and returns JSON facts on stdout;
  diagnostics go to stderr and exit status is nonzero on failure. Resolve
  every requested path against `repo_root` and check its realpath containment.
- [ ] Add review tests for candidate, matching reviewed, changed content,
  changed selected source, changed unselected source, and review-record edits.
  Define deterministic record serialization with recursively sorted object
  keys and preserved array order; record bytes or timestamps must not make
  equivalent JSON serialize differently. SHA-256 helpers use Node `crypto`.

  ```js
  import test from "node:test";
  import assert from "node:assert/strict";
  import { compareReview } from "../lib/review.mjs";

  test("a changed selected source expires its saved review", () => {
    const saved = {
      state: "reviewed", records: [],
      sources: [{ key: "journal:journal-a", sha256: "a".repeat(64) }]
    };
    const actual = {
      records: [],
      sources: [{ key: "journal:journal-a", sha256: "b".repeat(64) }]
    };
    assert.deepEqual(compareReview(saved, actual), {
      state: "stale", changedKeys: ["journal:journal-a"]
    });
  });
  ```

- [ ] Implement preparation with `spawnSync`/`spawn` and an argument array for
  the Python inspector, never a shell string. A malformed inspector response
  or nonzero exit fails preparation. Preview status cannot suppress schema,
  path, or source errors. Release throws `UNREVIEWED_CONTENT` or `SOURCE_STALE`
  for the corresponding review state. Return only the whitelist of public
  fields defined above, plus separate internal report/asset-copy objects.
- [ ] Run `npm --prefix website test` and
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_website_sources -v`.
  Re-run the existing site checks if shared behavior was touched. Review the
  diff and stop at a task review checkpoint; leave changes uncommitted.

## Task 2: Office Content And Evidence Reconciliation

**Files:** Create all pilot JSON/Markdown records from the file map;
`website/docs/office-content-review.md`; `website/tests/office-content.test.mjs`.
No edits to the original Office journal, inventories, assets, or prototype.

**Interfaces:** Consume `loadContent`, `validateContent`, and `prepareSite`.
Produce stable project ID `office-restoration`, service ID `historic-floors`,
and media IDs `flickr-<photo-id>`. The review record starts as `candidate`.

- [ ] Write a migration test for the two separate gallery groups and the
  three-image search subset. Check the mapping table below exactly, including
  source URL, album key, and asset path. The test fails until records exist.

  ```js
  import test from "node:test";
  import assert from "node:assert/strict";
  import { fileURLToPath } from "node:url";
  import { loadContent } from "../lib/content.mjs";
  const contentRoot = fileURLToPath(new URL("../content/", import.meta.url));

  test("Office retains all legacy gallery identities", async () => {
    const records = await loadContent(contentRoot);
    const office = records.projects.find(p => p.id === "office-restoration");
    assert.equal(office.gallery.length, 10);
    assert.deepEqual(office.searchMediaIds, [
      "flickr-53921322250", "flickr-52705240435", "flickr-52705240380"
    ]);
  });
  ```

- [ ] Reconcile the current catalog, full HTML section, and source journal.
  Create the ten media records with `kind: "evidence"` as migration candidates.
  This classification preserves existing use; it is not new image approval.

| Asset Under `site_example/assets/flickr/` | Photo ID | Album ID |
| --- | --- | --- |
| `office/01.jpg` | `53921322250` | `72177720316928566` |
| `office/02.jpg` | `53921322245` | `72177720316928566` |
| `office/03.jpg` | `53921322215` | `72177720316928566` |
| `office/04.jpg` | `53921225999` | `72177720316928566` |
| `office/05.jpg` | `53919981267` | `72177720316928566` |
| `studio-office/01.jpg` | `52705240435` | `72177720306207693` |
| `studio-office/02.jpg` | `52705240380` | `72177720306207693` |
| `studio-office/03.jpg` | `52705240355` | `72177720306207693` |
| `studio-office/04.jpg` | `52704298727` | `72177720306207693` |
| `studio-office/05.jpg` | `52705240320` | `72177720306207693` |

For each row, retain the exact URL pattern observed in the existing page:
`https://www.flickr.com/photos/boocher/<photo-id>/in/set-<album-id>/`.
Album keys are `flickr:<album-id>`; album destinations use the existing
`https://www.flickr.com/photos/boocher/albums/<album-id>/` links.

- [ ] Keep the page introduction and search summary distinct:

  - Introduction: "Two related albums track the former shared office and yoga
    studio through floor refinishing, sanding progression, door reclamation,
    and later dedicated-office use."
  - Search summary: "Office documentation tracks the first floor-refinishing
    method used in the house, sanding progression, hand-applied polyurethane,
    trim work, and reclamation of an original solid-wood door."
  - Proposed concise summary: "Floor refinishing and original-door reclamation
    in the author's 1894 residence."

  Copy existing tags. Use each existing search-image description as that
  media record's base `alt`; a gallery placement can supply its own `alt`
  override. Visually inspect all ten images locally before improving generic
  gallery alternatives or assigning evidence roles. Measure their local pixel
  dimensions with `sips -g pixelWidth -g pixelHeight <selected-asset-path>` and
  record the results as `width` and `height`. Record unresolved image
  interpretations in the review worksheet.
- [ ] Write a short public-story candidate from the journal's supported
  content: shared office/yoga studio to dedicated office; the original floor
  refinishing; original-door reclamation. Preserve the qualification that its
  charred finish was a yakisugi-inspired adaptation, not traditional yakisugi
  or a fire-resistance treatment. Do not copy unfinished journal prompts or
  present the documented finishing schedule as general professional advice.
- [ ] Record the following review qualifications explicitly:

  - Stage can describe the room as restored and returned to use **in the
    documented record**; it is not a new observation of present-day use.
  - Proposed date text: "Floor work documented December 2021–January 2022;
    door reclamation recorded under 2022; planning archive added August 2026."
    The old ending year 2024 needs evidence before reuse as a precise range.
  - August 2026 is documentation intake, not new restoration work.
  - Photo `52705240355` shows the stripped door before its charred treatment.
  - The explicit finished-floor IDs `52704582806` and `52705071273` are outside
    the current ten selections; do not silently fetch or add them.
  - Preserve the main shared-office-to-dedicated-office narrative; flag the
    source's conflicting "office-to-studio" phrase without editing the journal.
  - The master house sketchbook exists and the journal cites page 39. If the
    candidate story discusses that evidence, include the PDF as a source
    fingerprint, inspect page 39 with the PDF skill, and retain the page
    reference. Do not publish the whole master scan by default. Otherwise
    scope the public source label to the two Flickr albums and journal.
  - The inventory counts 276 and 107 are dated recorded values, not a fresh
    external verification. Let source inspection supply actual local counts.

- [ ] Create site/home/service records from the approved identity and concept:
  headline "Keep what makes it home."; the exact service line; ordered
  `featuredProjectIds: ["office-restoration"]`; `serviceIds: ["historic-floors"]`.
  Use a source-backed short service description as a candidate and preserve
  the full three-service positioning in the exact service line. Omit contact
  configuration until Shawn chooses its destination.
- [ ] Generate a proposed fingerprint report for the selected candidate
  records and sources. Record `candidate` in the review record; no code may
  auto-promote it to reviewed. The worksheet lists every migrated item,
  intentional copy difference, and unresolved interpretation for Shawn.

  Run this from the repository root; it prints the internal report without
  changing a review snapshot:

  ```sh
  node --input-type=module <<'JS'
  import path from "node:path";
  import { prepareSite } from "./website/lib/prepare.mjs";
  const result = await prepareSite({
    repoRoot: process.cwd(),
    contentRoot: path.resolve("website/content"),
    mode: "preview"
  });
  process.stdout.write(JSON.stringify(result.report, null, 2) + "\n");
  JS
  ```

- [ ] Run website unit tests and the existing evidence consistency check.
  Verify the source journal and original assets remain byte-identical to the
  task's starting snapshot. Review this task without committing it.

## Task 3: Reusable Astro Pages And Optional Search

**Files:** Create Astro configuration, layout, components, pages, styles,
Markdown policy/content collection, browser search controls, build script,
`website/tests/markdown-policy.test.mjs`, `rendering.test.mjs`, and
`search.test.mjs`. Preserve `site_example/script.js` and `journal-search.js`.

**Interfaces:** Consume the prepared public model and selected media copies.
Use `SiteLayout({site, title, reviewNotice})`,
`ProjectCard({project})`, `ProjectGallery({images})`,
`EvidenceDetails({project})`, `Hero({headline, intro, image?})`,
`ServiceSection({service, projects})`, `ArchiveSearch({entries})`, and
`ContactInvitation({contact?})` as component prop contracts.

- [ ] Write failing Markdown-policy tests. Use Astro's Markdown content
  collection with `glob({pattern: "*.md", base: "./content/stories"})`; story
  frontmatter contains only `schemaVersion: 1` and `id`. Reject unknown metadata,
  raw HTML AST nodes, all Markdown image nodes, executable content, and
  unsupported link protocols. Selected images belong to validated components.
  Do not install MDX. The pilot story uses headings and paragraphs; evidence
  links are rendered by components from validated records.

  ```js
  import test from "node:test";
  import assert from "node:assert/strict";
  import { assertSafeMarkdownTree } from "../lib/markdown-policy.mjs";
  test("raw HTML is rejected before story rendering", () => {
    assert.throws(() => assertSafeMarkdownTree({
      type: "root", children: [{ type: "html", value: "<script>run()</script>" }]
    }), error => error.code === "INVALID_MARKDOWN");
  });
  ```

  `assertSafeMarkdownTree(tree)` walks all child nodes and validates both
  ordinary links and reference definitions. A remark plugin calls it during
  Astro's Markdown processing. Only selected `storyId` entries are rendered.
- [ ] Implement steps 1–4 of the ordered pipeline in `build.mjs`. Task 4 adds
  the output validator and makes it the mandatory final build step. Run Node
  child processes with argument arrays. Set `WK_SITE_MODE` and `WK_PUBLIC_DIR`
  only for the Astro child; do not change global configuration. Wire:

  ```json
  {
    "build": "node scripts/build.mjs release",
    "build:preview": "node scripts/build.mjs preview",
    "test": "node --test tests/*.test.mjs"
  }
  ```

  The Astro config reads those task-specific values and sets `output: "static"`,
  `publicDir` to the validated staging path, and `outDir` to `dist` or
  `.preview-dist`. Fail when required preparation metadata is missing; do not
  let a direct Astro invocation quietly consume stale prepared data.
- [ ] Create semantic server-rendered components and pages. The shared layout
  supplies the exact identity, navigation to real pilot routes, skip link,
  page title, language, and preview notice. Pages resolve all data before
  passing it to components. Example route interface:

  ```astro
  ---
  import model from '../../generated/site.json';
  import SiteLayout from '../../layouts/SiteLayout.astro';
  import ProjectGallery from '../../components/ProjectGallery.astro';
  export function getStaticPaths() {
    return model.projects.map(project => ({
      params: { id: project.id }, props: { project }
    }));
  }
  const { project } = Astro.props;
  ---
  <SiteLayout site={model.site} title={project.title} reviewNotice={model.reviewNotice}>
    <h1>{project.title}</h1>
    <p>{project.introduction || project.summary}</p>
    <ProjectGallery images={project.gallery} />
  </SiteLayout>
  ```

  The prepared public model is written to ignored
  `website/src/generated/site.json` as the importable build input. Keep the
  review report and staging metadata under `.generated/`, outside `src`.
  The snippet illustrates routing; the complete page also includes evidence
  details and the working link to `project.archiveHref`.
- [ ] Use Georgia and a system sans-serif for the pilot, with the accepted
  green/limestone/sage palette in `tokens.css`. Treat these fonts as local
  review choices, not the final approved wordmark. Component-scoped CSS owns
  breakpoints. Use placement `focalPoint` for image positioning, lazy-load
  below-fold media, and keep the hero eager. Set image dimensions from inspected
  local assets to avoid layout shifts. Do not add network font dependencies.
- [ ] Render the configured contact action only when it exists. With no
  configuration, `ContactInvitation` renders nothing; no dead button or
  pretend form. The pilot navigation omits unfinished About/contact routes.
- [ ] Reuse the existing UMD search ranker unchanged. Copy that one explicitly
  named file into the fresh public staging directory as
  `/scripts/journal-search.js`. Load it only on the archive-search page with a
  deferred classic script, then a deferred classic controller. The controller
  uses `window.TradeJournalSearch.searchJournals` after fetching `/search.json`.
  Build the JSON endpoint from `model.searchEntries` at static build time.

  Load both scripts in `ArchiveSearch.astro` in this order. The controller is
  plain browser JavaScript without imports; `?url` emits it as a static asset:

  ```astro
  ---
  import controllerUrl from '../scripts/archive-search.js?url';
  ---
  <script is:inline defer src="/scripts/journal-search.js"></script>
  <script is:inline defer src={controllerUrl}></script>
  ```

- [ ] Keep a server-rendered project list on the archive index. Enhance it
  with search only after data loads successfully. Missing controls or failed
  JSON fetch leave that list usable and display a brief search-availability
  message. Use `textContent` and DOM creation for result text; no raw HTML
  insertion. Search URLs come from validated model destinations.
- [ ] Add search tests using Node `createRequire` to load the existing UMD
  module and synthetic public entries, proving the expected shape still works:

  ```js
  import test from "node:test";
  import assert from "node:assert/strict";
  import { createRequire } from "node:module";
  const require = createRequire(import.meta.url);
  const { searchJournals } = require("../../site_example/journal-search.js");
  test("public search entries resolve to project destinations", () => {
    const entry = {
      title: "Office floors", area: "Residence", tags: ["office", "floor"],
      summary: "Recorded floor refinishing", source: "/tradejournals/office/",
      url: "/work/office/", images: [], evidence: {}
    };
    assert.equal(searchJournals([entry], "office floors")[0].entry.url,
      "/work/office/");
  });
  ```

- [ ] Build the candidate preview and add rendered-output tests that inspect
  the actual generated HTML: exact identity/service line, all ten source URLs,
  three-image search subset, real project/story destinations, preview notice,
  no contact form, and no accidental local paths. Validate two invented projects
  for order changes; do not create a second real project just to test ordering.
- [ ] Run website tests, preview build, and existing search/evidence tests.
  Review the working output and this task's diff; leave it uncommitted.

## Task 4: Static Output Verification And Pilot Review

**Files:** Create `website/scripts/check-output.mjs`,
`website/tests/output.test.mjs`, `scripts/check_website_html.py`,
`tests/test_website_html.py`, `website/README.md`. Modify
`website/scripts/build.mjs`, `website/package.json`, and root `package.json`
with website convenience scripts, and document the pilot in
`site_example/README.md` without changing its existing commands or ownership.

**Interfaces:**

- `checkOutput({outputRoot, model})` returns a success report or throws a
  structured error identifying the file and invalid reference.
- `parse_html(document: str) -> dict` in `check_website_html.py` returns
  `{ids: list[str], references: list[dict]}`; each reference contains
  `{tag, attribute, value}` for `href`, `src`, or `srcset`. Its CLI accepts a
  JSON list of `{path, html}` over stdin and returns parsed records over stdout.
- Root `build:website:preview` runs `npm --prefix website run build:preview`;
  `test:website` runs the website Node tests and both new Python test modules;
  `check:website` builds and verifies the local candidate output.
- Production `npm --prefix website run build` remains the reviewed-release
  path and is not a deployment command.

- [ ] Write output tests on synthetic temporary directories: missing page,
  broken local image, missing fragment target, unexpected raw journal/PDF,
  unsafe source map, private absolute path, and unselected media. Check local
  `href`, `src`, and `srcset` references against actual emitted files. External
  HTTPS links receive syntax/source-identity checks; no automatic live fetch.

  The Python parser's first regression case checks entity decoding and
  fragment discovery independently of the filesystem validator:

  ```python
  import unittest
  from scripts.check_website_html import parse_html

  class WebsiteHtmlTests(unittest.TestCase):
      def test_collects_decoded_links_and_fragment_ids(self):
          result = parse_html(
              '<main id="work"><a href="/search/?a=1&amp;b=2">Work</a></main>'
          )
          self.assertEqual(result["ids"], ["work"])
          self.assertEqual(result["references"], [{
              "tag": "a", "attribute": "href", "value": "/search/?a=1&b=2"
          }])
  ```

- [ ] Implement output validation using a real HTML parser. Reuse Python's
  standard-library `html.parser.HTMLParser` in `check_website_html.py` and
  invoke it with an argument array. Do not use regex as the complete parser.
  Check emitted extensions and asset identities, absence of copied repository
  metadata/private paths, and that only planned project/story routes exist.
  Unexpected output fails validation rather than being silently ignored.
- [ ] Wire `checkOutput` into `build.mjs` after Astro exits successfully and
  before reporting a successful build. Add package script
  `check:output: "node scripts/check-output.mjs .preview-dist"`. The CLI loads
  `src/generated/site.json` and accepts an output directory relative to
  `website/`; the build imports `checkOutput` and passes its current model
  directly. Propagate a structured output failure as a nonzero build result.
- [ ] Verify the preserved-source baseline: no diff in original journals,
  inventories, images, `site_example/index.html`, its catalog/manifest, or
  existing browser scripts. The website-guide documentation change is the
  only planned change inside `site_example/`.
- [ ] Exercise the acceptance scenarios with synthetic data: change a summary,
  reorder two featured IDs, change a component style, remove an image reference,
  change a selected source, and change an unrelated album block. Confirm the
  intended output differences or exact failures. Keep test artifacts temporary;
  never mutate real archive content to demonstrate a failure.
- [ ] Serve the generated `.preview-dist` with a plain loopback static server:

  ```sh
  python3 -m http.server 8126 --bind 127.0.0.1 --directory website/.preview-dist
  ```

  Inspect the owning process/port first; if occupied, select an available port
  and record it. Do not stop another task's server. Use the CUA browser tools
  for rendered verification, not an authenticated public-host setup.
- [ ] Inspect desktop and 390-pixel mobile views of home, project, and archive
  routes. Check keyboard navigation, visible focus, skip link, legibility,
  image cropping, original-source links, and horizontal overflow. Verify core
  content without JavaScript and search behavior when its data request fails.
  Use browser tooling capabilities where available; otherwise record exactly
  which scenario is unverified instead of claiming success.
- [ ] Run the relevant full checks once after the final change:

  ```sh
  npm run lint:md
  npm run check:site-evidence
  npm run test:site
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
  npm --prefix website test
  npm --prefix website run build:preview
  npm --prefix website run check:output
  git diff --check
  ```

  With real content still marked candidate, separately assert that release
  build exits with `UNREVIEWED_CONTENT`. A reviewed synthetic fixture must
  demonstrate a successful release build with no preview notice or `noindex`.
- [ ] Document runtime selection, install/build/preview commands, source and
  component ownership, recorded evidence limitations, and review/release
  distinction in `website/README.md`. Include a spec-acceptance checklist with
  observed results, test commands, and remaining content/visual review items.
- [ ] Present the local pilot and Office content-review worksheet to Shawn.
  Report what works, what was checked, and any unfinished verification. Do not
  mark the working experience accepted on his behalf, change real review
  snapshots without exact approval, or publish/commit/push automatically.

## Spec Coverage And Execution Checkpoints

| Approved Requirement | Delivery |
| --- | --- |
| Content ownership, stable IDs, review fingerprints, public output selection | Task 1 |
| Preserve page/search distinctions and evidence provenance | Task 2 |
| Exact identity, shared components, public visitor structure | Tasks 2 and 3 |
| Optional longer narrative, safe content, separate browser search | Task 3 |
| Independent static build, portable hosting output | Tasks 3 and 4 |
| No-JavaScript reading, responsive/keyboard review, source and route checks | Task 4 |
| Future Dashboard editing | Documented contract only; implementation deferred |
| Full archive migration, final visual approval, contact, hosting, launch | Explicit follow-up decisions in the spec |

Each numbered task has a reviewable deliverable and a focused test cycle. Internal
subagents may assist within this task; they do not create user-visible successor
tasks unless Shawn explicitly requests the workflow-hub process, as recorded
above. The hub register is the current execution record. Work task by task
with review checkpoints and preserve the separate Git and publication boundaries.

## Technical References

- [Astro installation and supported Node versions](https://docs.astro.build/en/install-and-setup/)
- [Astro release metadata](https://registry.npmjs.org/astro/latest)
- [Node release index](https://nodejs.org/dist/index.json)
- [Astro components](https://docs.astro.build/en/basics/astro-components/)
- [Astro content collections](https://docs.astro.build/en/guides/content-collections/)
- [Astro deployment](https://docs.astro.build/en/guides/deploy/)
