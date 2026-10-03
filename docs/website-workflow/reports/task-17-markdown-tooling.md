# Task 17 — Markdown Tooling

Report ID: `WK-WEB-T17-R01`
Revision: 1
Date: October 3, 2026
Outcome: COMPLETE — locked tooling update accepted; upstream issue remains
Delivery: RECEIVED — hub acknowledged in turn
`01a102f0-278b-7d33-a541-54322a680179`; acceptance recorded below
Child: `01a102e5-9ee6-7281-b41f-8993cc70e4c3`
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`
Dispatch: `WK-WEB-T17-D01`

## Result

Pinned the root Markdown linter to **markdownlint-cli2 0.23.3** and added a
root npm lockfile. A clean `npm ci` now installs the same 87 dependency packages
without relying on an unlocked cache command. Scoped Node 24.21.0 satisfies the
linter's Node 22-or-newer requirement; no global runtime changed.

The fresh root audit improves from **eight package findings (seven high, one
moderate) to five high findings**. All five remaining findings trace to one
unpatched upstream `braces` issue. This is not a clean repository-wide audit.
The website's separate cache/Astro findings remain outside this tooling patch.

Existing Markdown rules pass without any journal reformatting or rule disabling.
Both rebuilt website outputs remain byte-identical to the accepted baseline.

## Change Scope

- `package.json`: replace `^0.22.0` with exact `0.23.3`.
- `package-lock.json`: new version-3 root lockfile, including transitive versions,
  registry URLs and integrity hashes. Website lockfile remains separate.
- `.gitignore`: ignore root `/node_modules/`.
- `.markdownlint-cli2.jsonc`: exclude root `node_modules/**`; retain all existing
  generated/dependency exclusions and `.markdownlint.json` rule settings.
- `README.md`: document the root locked install and supported runtime.
- `website/README.md`: replace the cache-command workaround with tested root
  `npm ci` / `npm run lint:md` instructions and the supported scoped runtime.
- This report. Hub brief/register remain owned by the hub.

The root install exposed that CLI2 does not read the old `.markdownlintignore`.
Before adding the explicit exclusion, both old and new linters scanned installed
dependency Markdown; all resulting errors were in `node_modules`. The narrow
exclusion restores authored-file coverage and does not conceal repository errors.
No bulk formatting, custom rule, override, forced audit fix or new service was added.

## Versions And Advisory Review

Task 16 previously used 0.22.0. The previously unlocked `^0.22.0` manifest now
resolves to **0.22.1** in a fresh baseline install; that current baseline still
reports the same eight package findings. The patched candidate is 0.23.3.

| Package | Fresh old range | Locked candidate |
| --- | --- | --- |
| markdownlint-cli2 | 0.22.1 | 0.23.3 |
| markdownlint | 0.40.0 | 0.41.1 |
| js-yaml | 4.1.1 | 5.4.1 |
| smol-toml | 1.6.1 | 1.8.0 |
| markdown-it | 14.1.1 | 15.0.1 |
| globby | 16.2.0 | 16.2.4 |
| braces | 3.0.3 | 3.0.3 |

[Upstream CLI2 release](https://github.com/DavidAnson/markdownlint-cli2/releases/tag/v0.23.3)
and [registry metadata](https://registry.npmjs.org/markdownlint-cli2/0.23.3)
confirm the version, dependencies and Node requirement. Earlier 0.23 releases
retain vulnerable parser dependencies. The core linter changes some existing
rule behavior but adds no rule IDs; this repository uses supported CLI and
JSON/JSONC configuration, with no custom rules or removed programmatic API use.
See the [core changelog](https://github.com/DavidAnson/markdownlint/blob/main/CHANGELOG.md).

The refreshed audit no longer reports the prior
[YAML](https://github.com/advisories/GHSA-2883-xcg3-v3hh),
[TOML](https://github.com/advisories/GHSA-7w5x-hrqm-74c2) or
[Markdown parser](https://github.com/advisories/GHSA-253c-mchw-3w2r) findings.

### Remaining Root Finding

The [braces advisory](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm) affects
versions through 3.0.3 and currently lists no patched release. Deeply nested
brace patterns can exhaust the Node call stack. The five audit package entries
are braces, micromatch, fast-glob, globby and markdownlint-cli2; these are
inherited paths to the same upstream issue, not five independent root flaws.

The current lint command supplies a fixed `**/*.md` pattern and static local
configuration. No public or visitor-controlled pattern input was identified.
This tool is not included in the static website. That limits the observed
exposure; it does not fix the dependency or establish general safety. Retain
upstream maintenance follow-up and reassess if accepting untrusted glob patterns
or configuration. npm suggests a breaking downgrade to 0.0.4; it was not applied.

## Verification

Baseline: `59d6e31194e4c44a47ee3d36ba2f3ff0888d10ee` on
`codex/concept-b-homepage`. Evidence is retained outside the repository at
`/private/tmp/tradejournals-task17-evidence/`.

Three local `--no-hardlinks --single-branch` clones were used for the old range,
patched candidate and clean-install proof. The clean clone began without root
or website node_modules, and received only the exact candidate manifest/lock,
exclusion files and README. The existing scoped Node binary was used; this is
not another fresh Node-runtime installation test. Initial registry access under
the restricted network failed; approved network access succeeded.

Verified results:

- Fresh root `npm ci`: **87 dependency packages installed**, CLI2 **0.23.3** and
  core **0.41.1**. Clean-install audit matches the candidate's five-high result.
- Root lock bytes are identical before and after clean/shared installs. SHA-256:
  `1deb55153ec00cc2ad01b63d50b050a8699a028f764e0052763b4e922b559b59`.
- Old/new linter actual file lists match exactly: **117 authored Markdown files**
  at the committed baseline. Both pass. The old comparison excluded the newly
  installed root dependencies through its command line; the new tool uses the
  committed candidate exclusion. Saved file lists allow direct comparison.
- Shared root install and full repository lint pass with the new version.
  **121 files, zero issues** after delivery, including concurrent task
  documentation and this report (120 at the earlier implementation checkpoint).
- `npm run check:website` and `npm --prefix website run build`, followed by the
  matching standalone output check, pass. Independently prepared preview and
  release models each validate **18 pages, 52 files, 318 references**, review
  `current`, zero changed keys.
- All 52 files in each rebuilt mode match its pre-update manifest byte for byte.
  Website package/lock and review-snapshot bytes are unchanged. Snapshot SHA-256:
  `cdc69b8b5c95af1e05677e9a1639287fd5b8886ab0872ce9adc3bc71dcd5699f`.
- No application, runtime or generated-output behavior changed. Under the brief's
  proportionate-check boundary, no redundant full website test suite or browser
  run was performed; earlier acceptance evidence is not represented as a new run.

Reproduction from the repository root, after the existing scoped Node setup:

```sh
export PATH="$PWD/website/.runtime/node_modules/node/bin:$PATH"
npm ci
npm run lint:md
npm audit
npm --prefix website ci
npm run check:website
npm --prefix website run build
node website/scripts/check-output.mjs dist
```

`npm audit` currently exits nonzero for the documented upstream issue; install,
lint and build success must not be confused with a clean audit. Root and website
dependency installation remain separate. No dependency runtime enters the
unchanged static release package.

An independent read-only review of the dependency/configuration/documentation
diff and saved verification evidence found no blocking issues. Final Markdown
lint and tracked/new-file whitespace checks passed.

## Ownership And Return

Preserved concurrent Cassis source-review work and both hub-owned records.
No source journal, image, public story, contact destination or reviewed content
fingerprint was edited. Task 16's report is unchanged. Changes remain uncommitted.

Return report revision 1 for hub reconciliation and Shawn's acceptance, including
the remaining upstream issue. No Git closeout, merge, deployment, content
promotion, archival or successor was performed.

## Task 17 Acceptance And Git Closeout

Shawn said `approved and git er done` in website updates on October 3, 2026.
Acceptance `WK-WEB-T17-A01` covers report `WK-WEB-T17-R01`, revision 1;
hub reconciliation `WK-WEB-T17-H02` marks Task 17 COMPLETE. Remaining upstream
findings stay documented and unresolved. Earlier pending/uncommitted statements
record prior checkpoints.

The same instruction authorizes validation, commit and push of the Task 17
manifest/lock, exclusions, installation documentation, brief/report and hub
register to `origin/codex/concept-b-homepage`. Preserve all concurrent Cassis
content-review work. No merge, deployment, archival or successor is included.
Final commit and synchronization evidence will be reported in the hub.
