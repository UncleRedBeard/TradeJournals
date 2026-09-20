# WK-WEB-T11-R01 — Expanded Website Release Readiness

Revision: 2
Status: COMPLETE
Date: September 20, 2026
Branch: `codex/website-updates`
Baseline: `d28f0305b164cb1f9214b2b129b4e2c46bca8d0f`
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` / website updates
Child: `01a0c0f4-617d-70a1-b0b1-da23a7b1f953`

## Result

The approved Task 10 website is now recorded as the current reviewed release.
The snapshot contains 50 public record fingerprints and 47 selected source
fingerprints. Its canonical SHA-256 is
`ec16411478fec3d39b8099e1c366cfe4cedd27af797bcd7217dcd4a1ecff9fcc`.
Fresh comparison reports `current` with zero changed keys.

Revision 2 records Shawn's direct release-review correction from `120 film` to
the clearer and technically accurate `120-format film` in the Agfa Isolette
story. No other public copy or selection changed.

The inquiry action remains the disabled `Email us — coming soon` button, as
Shawn directed during Task 11 preparation. No address, link, form, message, or
backend was added.

## Release Package

The guarded release and protected preview both build and validate as 18 pages,
52 files, and 232 internal references.

- Release review: [http://127.0.0.1:4175/](http://127.0.0.1:4175/)
- Protected preview: [http://127.0.0.1:4174/](http://127.0.0.1:4174/)
- Eventual hosting payload: the contents of `website/dist/` only.

The release has no review notice or robots exclusion. The preview retains
`noindex, nofollow` and the notice `Local preview — reviewed content; this
preview is not a deployment.` Neither output contains journals, inventories,
Workbench data, runtime files, or private source paths.

## Browser Verification

- The release homepage rendered the restoration portfolio before the quieter
  workshop section, with the disabled inquiry button and no horizontal overflow
  at desktop or a calibrated 381-pixel content viewport.
- Full-page loading confirmed all seven homepage images had positive natural
  dimensions. Browser logs contained no warnings or errors.
- Archive search for `dresser` returned exactly `Guest Bath and Dresser Vanity`.
- The preview showed its review notice and robots protection; the release showed
  neither. Both navigation links remained visible at the narrow viewport.

## Fresh-Checkout Proof

An isolated clone of committed baseline `d28f030` was created at
`/private/tmp/tradejournals-task11.J63neO/repo`. Only the Task 11 website patch
was overlaid; no runtime, dependencies, generated model, or build output was
copied from the working checkout.

The documented setup installed Node 24.21.0, npm 11.11.0, Python 3.13.7, and
194 locked website packages. That clean checkout then passed 118 Node tests and
37 Python tests and produced an independently checked 18-page, 52-file release
with 232 references.

## Changed Implementation Files

- `website/content/reviews/pilot.json`
- `website/content/stories/agfa-isolette.md`
- `website/README.md`
- `website/docs/pilot-editorial-review.md`
- `website/tests/build.test.mjs`
- `website/tests/office-content.test.mjs`
- `website/tests/rendering.test.mjs`
- this report

The hub-owned Task 11 brief and register remain separate shared-checkout changes.
No source journal, album inventory, original media, site content, design,
Workbench data, hosted service, DNS record, or remote repository was changed.

## Verification

- Current checkout: 118 Node tests and 37 Python tests passed.
- Clean checkout with Task 11 patch: 118 Node and 37 Python tests passed.
- Candidate and guarded release builds: 18 pages, 52 files, 232 references.
- Independent release output check: 18 pages and 52 files validated.
- Repository Markdown lint: 87 files, zero errors.
- `git diff --check`: passed.
- Snapshot: `current`, zero changed keys, 50 records, 47 sources.
- Source journals and album inventories: no Task 11 changes.

## Remaining Decisions

Hosting provider, domain/DNS, upload/deployment, and a future public inquiry
destination remain separate decisions. They do not block the provider-neutral
release package. After approving revision 2, Shawn authorized scoped Git
closeout with `git er done`; that authorization does not include deployment or
any of the remaining decisions above.

## Hub Action Requested

Review this report and the release preview, then reconcile Task 11. This report
does not authorize Git closeout, hosting, deployment, archival, or a successor.
