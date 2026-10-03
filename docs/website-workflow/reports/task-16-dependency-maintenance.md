# Task 16 — Dependency Maintenance

Report ID: `WK-WEB-T16-R01`
Revision: 1
Date: October 3, 2026
Outcome: COMPLETE — compatible patch accepted; remaining findings recorded
Delivery: RECEIVED — hub acknowledged in turn
`01a102b0-677e-7a31-8095-0fdf3654ca9a`; hub reconciliation complete
Child: `01a10290-90df-7271-9f3f-ad82cc5a8739`
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`
Dispatch: `WK-WEB-T16-D01`

## Result

Updated the locked transitive dependency **devalue 5.9.2 → 5.9.4**. Astro stays
at 7.3.2, its declared devalue range `^5.8.1` already permits the patch, and no
override or new dependency was needed. Only that package's version, URL and
integrity changed in `website/package-lock.json`.

The website audit falls from **three high package findings to two**. All six
devalue advisories disappear from the refreshed audit. The remaining two
package findings represent one upstream cache advisory and Astro's inherited
exposure; no released patch exists for that cache package at this checkpoint.
The separate root Markdown-lint installation exposed additional findings,
described below. This is not a clean repository-wide security audit.

The updated fresh and shared builds are byte-identical to the accepted output:
all **52 files** in both preview and release. Website design, content, behavior,
selected media and reviewed snapshot are unchanged.

## Changes And Upstream Evidence

| Dependency | Before | After | Result |
| --- | --- | --- | --- |
| Astro | 7.3.2 | 7.3.2 | Unchanged; inherited cache finding remains |
| devalue | 5.9.2 | 5.9.4 | Six advisory conditions no longer reported |
| http-cache-semantics | 4.2.0 | 4.2.0 | Upstream advisory unresolved |

The [devalue 5.9.3 release](https://github.com/sveltejs/devalue/releases/tag/v5.9.3)
contains the security fixes; [5.9.4](https://github.com/sveltejs/devalue/releases/tag/v5.9.4)
adds a tree-shaking annotation and retains those fixes. Live npm metadata and
the installed Astro manifest confirm the compatible range. Devalue 6.x is
available but unnecessary for this fix.

The [cache advisory](https://github.com/advisories/GHSA-ch52-4w7c-c8xp) still
lists affected versions through 4.2.0 and no patched release. Its
[proposed fix](https://github.com/kornelski/http-cache-semantics/pull/58)
remained open when reviewed. npm's suggested Astro 2.10.9 downgrade is a
breaking framework change, so it was not applied. No forced audit fix,
unmerged fork, finding suppression or transitive override was introduced.

The cache flaw concerns shared cached responses and attacker-controlled
`max-stale` reuse. Installed Astro references it in remote-image build caching,
using `storable()` and `timeToLive()` rather than the affected request-reuse
methods. This website copies selected local images and publishes static files.
No corresponding exploit path was identified in this current build/publication
model. The advisory remains unresolved; reassess before server rendering,
shared proxy caching or untrusted build inputs. This scoped review does not
certify the dependency tree as secure.

## Installation Documentation And Root Tooling

A fresh-checkout check demonstrated that Task 15's root `npm ci` instruction
fails: the repository has no committed root package lock. The website's
separate lockfile and `npm --prefix website ci` work correctly.

The README now uses the existing linter version through npm's package cache:

```sh
npm exec --yes --package=markdownlint-cli2@0.22.0 -- npm run lint:md
```

This exact command passed and creates no root dependency directory or lockfile
in the shared checkout. The website lockfile remains the reproducible website
installation boundary. Root linter tooling is a separate installation: the
cache command pins the top-level linter version, but its transitive dependencies
are not locked and may resolve differently on a future fresh installation.

Installing the root manifest in scratch also reported **eight package findings:
seven high and one moderate**, including inherited findings. A temporary root
lockfile was generated only in scratch to obtain the structured audit:

- High: braces, fast-glob, globby, js-yaml, markdownlint-cli2, micromatch,
  smol-toml.
- Moderate: markdown-it.

These are separate from the two website audit findings. npm suggests
markdownlint-cli2 0.23.3 outside the declared `^0.22.0` range and labels that
change breaking. No linter upgrade, root lockfile or lint-rule migration was
added to this website patch. Their remediation and exposure assessment remain
follow-up for the hub; the findings have not been dismissed or certified safe.
None of this tooling is included in the static website output.

## Verification

Baseline: `f20572a2648cce9d7d386ccc105370d2307cc544` on
`codex/concept-b-homepage`. Website package/source changes were reviewed before
applying the scratch-verified lockfile to the shared checkout.

Scratch checkout: `/private/tmp/tradejournals-task16-evidence/repo`.
It was cloned locally with `--no-hardlinks --single-branch` at the exact
baseline. `npm update devalue --package-lock-only --ignore-scripts` changed only
the one lock entry. A fresh `npm --prefix website ci` installed 194 packages
from that updated lockfile; no shared node_modules was copied or deleted.
The existing scoped Node 24.21.0 binary and npm 11.11.0 were used. This verifies
a clean locked website install, not a fresh installation of the Node runtime.

Fresh scratch verification:

- `npm run test:website`: **121 Node and 37 Python tests passed**, zero failures.
- Preview build/output check and guarded release/output check passed:
  **18 pages, 52 files, 318 references** per mode.
- Installed dependency tree resolves Astro 7.3.2, devalue 5.9.4 and cache 4.2.0.
- Refreshed website audit: two high package findings, no devalue finding.

Shared-checkout verification after installing the same lock:

- Preview and guarded release builds/checks passed.
- Each retained output independently checked against its matching prepared
  model: **18 pages, 52 files, 318 references**, review `current`, zero changed
  keys in both modes.
- Every file in each mode matches both the pre-update output manifest and the
  fresh patched output byte for byte. The framework and output did not change,
  so Task 15's browser evidence remains applicable; no new browser run is
  claimed. Existing automated search/fallback coverage passed in the suite.
- The exact documented npm-cache Markdown lint command and whitespace checks
  passed. No public or repository implementation behavior was added.
- Snapshot SHA-256 remains
  `cdc69b8b5c95af1e05677e9a1639287fd5b8886ab0872ce9adc3bc71dcd5699f`.

The unchanged output contains 18 HTML pages, 31 JPEGs, two authored search
scripts and one search JSON file. No dependency runtime, source journal,
inventory or private Workbench files were added. Preview/release boundaries,
room distinctions and disabled inquiries are preserved.

## Evidence And Ownership

Evidence directory: `/private/tmp/tradejournals-task16-evidence/`.
It retains before/after website audits, registry metadata, updated dependency
tree, install/test/build logs, matching-model results, baseline and updated
per-file SHA-256 manifests, and the separate root audit. The temporary root
lock/dependencies remain only in scratch; they were not copied to the repository.
One later npm-cache lint rerun hit sandbox DNS restrictions; the original
network-authorized command passed, and the installed linter passed all 115
Markdown files. The final authorized rerun is retained separately as
`lint-final-authorized.log`. The command can require registry access even when
some packages are cached. An independent read-only review checked advisories
and the final change scope.

Task-owned files: `website/package-lock.json`, `website/README.md`, and this
report. Task 15's historical report is unchanged. The website hub register and
Task 16 brief belong to the hub. Concurrent La Ciotat Skate Park journal,
content-review register, brief and report changes were preserved.

Return for hub reconciliation and Shawn's acceptance, including the documented
remaining website and root-tooling findings. Changes remain uncommitted. No
Git closeout, merge, deployment, inquiry activation, content promotion,
archival or successor task has been started.

## Hub Acceptance

Shawn said `accepted` in the exact hub on October 3, 2026. Acceptance
`WK-WEB-T16-A01` and reconciliation `WK-WEB-T16-H02` mark this revision COMPLETE.
The hub independently verified tests, both output modes and byte comparisons.
Remaining findings above stay open; no Git closeout or successor is authorized.

## Task 16 Git Closeout Authorization

After acceptance, Shawn said `git er done` in website updates on October 3,
2026. This authorizes validation, commit and push of the accepted website lock
patch, README, Task 16 brief/report and hub register to the established
`origin/codex/concept-b-homepage` branch. Earlier uncommitted/no-closeout
statements describe the pre-closeout checkpoint. Residual findings stay open;
merge, deployment, archival and successor work remain separate. Final commit
and synchronization evidence will be reported in the hub after the push.
