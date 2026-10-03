# Task 15 — Integrated Release Review

Report ID: `WK-WEB-T15-R01`

Revision: 1

Date: October 3, 2026

Outcome: COMPLETE — local release verification accepted by Shawn and reconciled by hub

Delivery: RECEIVED — hub acknowledged the report in turn
`01a10274-d339-7741-a332-8ee4cfec9735`; reconciled as `WK-WEB-T15-H01`

User acceptance: Shawn said `looks good...approved` directly in this child on
October 3, 2026. Acceptance ID: `WK-WEB-T15-A01`. Hub reconciliation complete;
this approval covers report revision 1 and its local release-review result.

Child: `01a10263-fe12-7673-bb16-067cb5e4f7ff`

Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`

Dispatch: `WK-WEB-T15-D01`

## Result And Scope

Shawn's `kick off task 15` authorized [brief revision 1](../task-15-integrated-release-review.md).
The accepted Concept B site builds reproducibly as a standalone static package.
No implementation failure was demonstrated; this task changes only the
maintainer README, existing release-review document and this report.

The README now points to `codex/concept-b-homepage`, distinguishes the prior
release on `main`, explains the matching-model checker and root lint install,
and records that fonts and their license are shared by every page. The release
review preserves earlier approvals as dated history and records the accepted
shared frame, galleries, journals and archive from Tasks 12–14.

Verified revision: `ef1d5e8303860d49b7ae6131b0596e2bce38660b` on
`codex/concept-b-homepage`. Task 15 documentation remains uncommitted. No
content, image, source, dependency, snapshot or website implementation changed.

## Checks

Both the shared checkout and an independent fresh checkout passed:

- Node **24.21.0**, npm **11.11.0**, Python **3.13.7**.
- `npm run test:website`: **121 Node tests and 37 Python tests**, no failures.
- `npm run check:website`: preview build and output gate passed.
- `npm --prefix website run build`: guarded release passed.
- `node website/scripts/check-output.mjs dist`: release output passed.
- Independent checks with each mode's freshly prepared model:
  **18 pages, 52 files, 318 references** in both retained outputs.
- Review state `current`, **zero changed keys**, **50 records / 47 sources**.
- Saved snapshot bytes remain unchanged, SHA-256:
  `cdc69b8b5c95af1e05677e9a1639287fd5b8886ab0872ce9adc3bc71dcd5699f`.

The shared repository's final `npm run lint:md` passed across 111 files with
zero errors; tracked and new-report whitespace checks also passed.
The fresh checkout also finished with a clean source tree and whitespace check.

To check both retained outputs without accidentally using the last build's
model for the other mode, run from the repository root with the scoped Node:

```sh
node --input-type=module <<'JS'
import { prepareSite } from './website/lib/prepare.mjs';
import { checkOutput } from './website/scripts/check-output.mjs';
const repoRoot = process.cwd();
for (const [mode, directory] of [['preview', '.preview-dist'], ['release', 'dist']]) {
  const { model, report } = await prepareSite({
    repoRoot, contentRoot: `${repoRoot}/website/content`, mode
  });
  const result = await checkOutput({
    outputRoot: `${repoRoot}/website/${directory}`, model
  });
  console.log(mode, report.state, report.changedKeys, result);
}
JS
```

## Fresh-Checkout Proof

Retained scratch: `/private/tmp/tradejournals-task15.8Olcsz/repo`.
The adjacent `commands.txt`, `initial-state.json`, `final-proof.json`, test and
build logs, mode-specific models/reviews and SHA-256 manifests retain evidence.

An isolated `git clone --no-hardlinks --single-branch --branch
codex/concept-b-homepage` from the local committed repository was detached at
the exact revision above. Before installation, runtime, dependencies, generated
data and both output directories were absent. No working-tree patch was needed
or overlaid. The documented scoped runtime install and
`npm --prefix website ci` installed **194 locked website packages**; npm's
package cache was allowed. No runtime, node_modules or generated files were
copied from the shared checkout.

The initial restricted-network npm attempt failed resolving the registry. The
same install succeeded with narrowly approved network access. This is a local
clean-clone proof, not a fresh GitHub authentication/network availability test.

Every file in the fresh preview and release is byte-identical to its matching
shared output. The release is **6,488,732 bytes** across 52 files. SHA-256 of
the sorted `hash`, two spaces, relative-path and newline manifest:

- Preview: `290246c521c1a1b9ddf838303aa169979121cc74e9e14a0fd0cd2c4507b262e9`
- Release: `6662a67b59c26dcbd3499c62836fde6923a8d7864f127a3ca27ed943bea37405`

## Browser Review

The normal release was inspected in the in-app browser at **1280×900** and
**390×844**, covering the homepage, Living Room project/gallery, long Entry
journal, short Office journal and archive/search. Guest Bath's square gallery
was also inspected at phone width through the no-script preview server.

- No horizontal overflow on the sampled routes at either reviewed width.
  The desktop journal reading column is 704px; phone text fits its viewport.
- All six homepage images loaded after scrolling. The sampled three-image
  Living Room and Guest Bath galleries loaded fully with `object-fit: contain`;
  headings, captions and source links remained readable.
- Homepage-to-project, photo jump, journal-to-archive and fallback-to-project
  navigation worked. The release skip link has a visible 3px focus outline and
  Enter focuses `main-content`. Search field-to-button keyboard navigation
  also shows the 3px focus outline.
- `office` returns **Dedicated Office** and **Barre Studio — Current Room**
  separately. Static and inserted headings use the same Cormorant Garamond
  styling; static entries are hidden after a successful search.
- `original door` returns Entry and Stair Restoration. A nonmatching query
  shows `No matching selected projects.` Empty submission retains the existing
  first-three-results behavior.
- An intentional `/search.json` 503 shows `Search is unavailable. The project
  list remains below.` and preserves all eight static entries.
- Empty responses for the two search scripts leave all eight entries browsable
  before and after ordinary GET submission. A fallback project link works.
- Normal preview/release browsing produced no captured console warnings or
  errors. The expected 503 belongs only to the temporary failure simulation.

The fallback servers on 8140/8141 were stopped after testing. Review servers
8139/8142 remain available. Temporary viewport overrides were reset.
This is a representative visual/keyboard sample, not a full accessibility,
cross-browser, physical-device or external-source-provider audit.

## Package Boundary

The verified release contains **18 HTML pages, 31 JPEGs, two authored JavaScript
files and one search JSON file**, with no symlinks. It contains no source
journals, inventory files, private Workbench store, Node/runtime dependencies,
generated build models or local filesystem paths. Text scans and the existing
allowlist/output gate passed. Only the archive uses scripts; their bytes match
the existing authored search sources. All 18 pages retain the local font
license and require no external font service.

All 18 preview pages contain the review notice and `noindex, nofollow`; all 18
release pages contain neither. Disabled inquiry controls and the separate
future studio/current studio/Office accounts remain intact. The move is still
unconfirmed; no public contact destination was added.

The build needs the complete repository, Node/npm and Python. Serving it needs
only static hosting at a **domain root**. Upload only the **contents of
`website/dist/`**; a subdirectory deployment needs a separate base-path change.

### Dependency Maintenance Follow-Up

The clean install's npm audit reports **three high package findings**:
`devalue@5.9.2`, `http-cache-semantics@4.2.0`, and Astro's inherited cache finding.
These are build dependencies and none ships in the verified static output.

The [cache advisory](https://github.com/advisories/GHSA-ch52-4w7c-c8xp) requires
shared cross-user response caching and attacker-controlled `max-stale`;
Astro uses it in remote-image build caching, while this site copies local media.
The devalue advisories involve [shared-buffer disclosure](https://github.com/advisories/GHSA-j22f-vq7h-c4qm),
[parse-to-uneval amplification](https://github.com/advisories/GHSA-mcm9-63f2-9j32)
or [asynchronous rejection timing](https://github.com/advisories/GHSA-x5rw-q4pp-hg5g).
No corresponding visitor-facing execution path was found in this static site.
This is a scoped assessment, not a claim that the dependency tree is clean.

Retain dependency maintenance as follow-up; no lock change or automatic
`npm audit fix` was applied. Reassess before introducing server rendering,
remote/untrusted build inputs or a publicly accessible builder. The raw audit
and assessment remain with the fresh-checkout evidence.

## Review Links And Screenshots

- [Release homepage](http://127.0.0.1:8142/)
- [Release project gallery](http://127.0.0.1:8142/work/living-room-studio-restoration/)
- [Release Entry journal](http://127.0.0.1:8142/tradejournals/entry-restoration/)
- [Release archive/search](http://127.0.0.1:8142/tradejournals/)
- [Existing preview with review notice](http://127.0.0.1:8139/)

HTTP response bytes matched the respective output files. Port 8139's existing
process was preserved; Task 15 started the separate loopback release on 8142.
The release homepage tab is retained for review. These local URLs depend on
their review processes remaining running.

Screenshots are in
`/Users/shkelley/.codex/visualizations/2026/10/03/01a10263-fe12-7673-bb16-067cb5e4f7ff/`:

- `task15-home-desktop.jpg` and `task15-home-phone.jpg`
- `task15-gallery-desktop.jpg` and `task15-gallery-phone.jpg`
- `task15-journal-desktop.jpg` and `task15-journal-phone.jpg`
- `task15-office-phone.jpg`
- `task15-search-desktop.jpg` and `task15-search-phone.jpg`
- `task15-unavailable-phone.jpg`

## Ownership And Return

Concurrent La Ciotat work owns the France travel journal, content-review
register and Task 07 brief/report. The hub owns the website register and Task 15
brief. Those existing edits were preserved; no files were staged or committed.
Concurrent source work did not change any selected website review key.

Shawn accepted this local release-review result directly in the child. The hub
verified that approval and reconciled Task 15 as COMPLETE. Branch integration/Git closeout,
hosting and domain selection, upload/deployment and inquiry activation remain
separate. No successor task, merge, deployment or archival starts from this
report.

## Task 15 Git Closeout Authorization

After Task 15 acceptance and hub reconciliation on October 3, 2026, Shawn said
`git er done` in website updates. This authorizes validation, commit and push of
the Task 15 brief/report, hub register, website README and release-review document
to the established `origin/codex/concept-b-homepage` branch. Earlier statements
that these documents remain uncommitted or that Git closeout is unauthorized
record the pre-closeout checkpoint. No merge, deployment, inquiry activation,
archival or successor task is included. Final commit and synchronization evidence
will be reported in the hub after the push.
