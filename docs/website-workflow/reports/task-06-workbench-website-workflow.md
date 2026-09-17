# Task 06 — Workbench Website Workflow

Report ID: `WK-WEB-T06-R01` · Revision 2 · September 17, 2026
Status: COMPLETE — approved by Shawn and reconciled by the hub
Report delivery: Revision 2 RECEIVED and reconciled by the exact hub.
Revision 2 records Shawn’s direct “approved” after reviewing the working flow;
implementation and verification evidence are unchanged.
Child: `01a0ac79-2d59-7101-b493-b08da38e407e`
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`
Authority: direct child instruction “start task 06”; subsequent direction to use
selected images from the shared Google Photos album. Brief revision 2 reconciles
that direct approval without changing implementation scope.

## Delivered

TradeJournals Workbench now supports the bounded Studio path:
**select staged photos → arrange lead and gallery → caption and describe → save
candidate → build and open the local Astro preview**.

- [Website editor](http://127.0.0.1:8125/website)
- [Studio preview](http://127.0.0.1:8126/work/studio-restoration/)
- [Maintenance instructions](../../../website/docs/workbench.md)
- [Photo review packet](../../../website/docs/pilot-editorial-review.md)

Shawn approved the Task 06 workflow and three-photo Studio candidate. Nothing is published. The existing
Toil & Timber design and accepted Studio prose remain; the evidence note now
accurately describes the selected photographs. The homepage hero stays text-only,
while the Studio project card uses the selected near-completion view.

## Capability Assessment And Smallest Additions

Observed the actual serving Companion checkout, private configuration and UI
before implementation. Archive coverage was complete: 27 journals read out of
27 expected. No saved drafts were present.

| Capability | Observed starting behavior | Delivered addition |
| --- | --- | --- |
| Project access | Existing journal browser/search worked | Website nav opens Studio directly |
| Photo intake | Local file preview, staging and private originals existed | Reused those controls and ready photos |
| Google Photos | No account integration; link intake supported other sources | Selected inbound downloads, individual source links, local intake |
| Lead/order/captions/alt | No website authoring interface | Small standalone Website page using existing styles |
| Candidate save | Public JSON existed, no browser writer | Archive-owned schema adapter; explicit promotion and revision checks |
| Website preview | Existing Astro build, no Workbench control | Build button and loopback preview listener |
| Names | TradeJournals - Dashboard / Start launcher | TradeJournals Workbench / Open TradeJournals Workbench |

No new package dependency or general CMS was added. Scope is Studio photographs;
structured files still handle prose and other projects.

## Photo Evidence

Inspected all three selected Google album photographs before writing captions.
Preserved individual source URLs in media records and exact order/captions/alt in
`website/content/projects/studio-restoration.json`.

| Order | Public media ID suffix | Source image ID | Evidence |
| --- | --- | --- | --- |
| 1 | `c721a809f0e722d6d0178585601aa6ca564b6d7ef95094505284f7f5788c85f6` | `AF1QipOYOPMUTUnNJtdnZlBl5Aq_xtg__YaYVun_8a_m` | August 26, 18:42:52 near-completion room |
| 2 | `a400ee37342a3a2d58cf36631811b65f2d466e5f0608db2810bab20ef93e86b2` | `AF1QipO5TK5FXRp97MN26dv5wFBXuLUtEJmB03luGYUW` | March 16, 10:41:18 starting condition |
| 3 | `705eb089635f352fc52889dfb21495f96c762ea01dfe83a6c5aca62c4a2bbfce` | `AF1QipO5zjJV4Fdl_JosSyl-9VcRTD99Ailb1PqRU9qS` | March 16, 10:46:35 floor scraping tools |

IDs have the `studio-` prefix and hash the promoted JPEG bytes. Assets live under
`website/assets/workbench/`; corresponding records are in `website/content/media/`.
The images are Google display renditions, 1012–1080 pixels wide, not original
camera files. Source downloads contained MPF auxiliary image data and were
rejected by the existing importer. Ordinary JPEG copies made with macOS `sips`
passed its existing checks, were staged and inspected, then explicitly promoted.
The three failed intake outcomes remain private and were not deleted.

The live album extends into September; selected March/August photos support the
accepted journal account through August 30. No later completion claim, installed
barre, or final sign-off was inferred. Office's ten photos remain separate.

## Boundaries And Implementation

Archive additions: `website/lib/workbench.mjs`, four focused authoring tests,
three media records/assets, Studio selection and evidence note, two updated
content/build assertions, review packet and maintenance documentation.

Companion additions: `dashboard/website/http.mjs`, its README, standalone
`dashboard/web/website.html` and `website.js`, existing stylesheet additions,
server route/shutdown integration, navigation/branding, two HTTP guard tests.

Public promotion selects only ready normalized JPEG previews and allowlisted
public fields. No private paths, intake IDs, notes, database or credentials are
copied. Origin/token checks, opt-in configuration, candidate state, revision
checks and existing schemas gate saves. Additive assets precede one atomic
project replacement; interrupted saves can leave unselected assets for later
inspection. No cleanup runs automatically. Concurrent file editing should use
reopen after a revision conflict.

Astro uses the same public records and works without the Workbench. The build
never imports the authoring adapter or reads its private store. Build output
validation retains the existing strict page/media allowlist and private-path
checks. Preview binds only to loopback and refuses an occupied port.

## Environment And Git

- Archive: `codex/website-updates`, HEAD
  `98fb1308c927bba6b5b4fd9aa05c63fbac7bc70b`.
- Companion: new `codex/website-workbench`, HEAD
  `99bddb45788ecb6b1805166b94d38f4d9e13067f`, at
  `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/tradejournals-companion`.
- Private launcher:
  `~/Library/Application Support/TradeJournals Dashboard/Open TradeJournals Workbench.command`.
  The old launcher is a forwarding wrapper; folder/storage identity is retained.
- Private config has `allowWebsiteWrites: true`; `allowJournalWrites: false`.
- Node 25.8.1 runs Companion; the website uses its scoped Node 24.21.0 runtime.
- Renamed launcher was executed; serving checkout and 27-journal coverage were
  observed. Final app restarted successfully, candidate reopened/saved again,
  then preview rebuilt. Listeners: Workbench 8125 and its preview 8126.
- No commit, push, deployment or new task dispatch. Hub register/brief and prior
  Task 05 acceptance edits were preserved; this child did not edit those files.

## Verification

- Website Node suite: **84 passed**, zero failed/skipped.
- Website source/HTML Python suites: **37 passed**.
- Companion non-browser suite: **221 passed**, zero failed/skipped.
- Initial all-suite Companion attempt: 220 passed, 24 browser cases skipped,
  one suite failed to load because `playwright` is unavailable. After adding the
  second website guard test, the 221 available non-browser tests passed.
  The existing browser suites were not represented as passing or installed.
- Markdown lint: archive 66 files and Companion 25 files, zero errors; report
  separately linted after creation. JavaScript syntax checks and both Git
  whitespace checks passed.
- Actual UI: imported three JPEG copies, selected/staged them, opened Studio,
  entered source links/captions/alt/roles, moved the room view to lead, explicitly
  promoted and saved. Reload and server restart preserved selection and text.
- Actual UI build: success notice and preview link; all three generated images
  loaded with expected dimensions and source links. Desktop gallery inspected.
  Editor and preview each checked at 390 pixels with no horizontal overflow;
  temporary viewport override reset afterward.
- Existing public output checker passed during the preview build. Git diff
  confirms no changes to source journals, inventory, Office project or candidate
  review-state file. Current candidate content still cannot release as reviewed.

## Review Decisions Remaining

Shawn approved the delivered workflow and the saved Studio photo candidate in
this child after reviewing its presentation and flow.
This is a deliberately small candidate; more details or higher-resolution assets
can follow a concrete need. Full reviewed-snapshot approval, Git closeout, hosting
and publication remain separate decisions. The hub owns acceptance.

## Authorized Git Closeout

Shawn subsequently said `git er done` in this child on September 17. This
authorizes scoped commit/push to the established origins on
`codex/website-updates` (archive) and `codex/website-workbench` (Companion).
Earlier no-Git statements describe the implementation/acceptance checkpoint.

Fresh closeout checks: 84 website Node tests, 37 Python tests and 221 available
Companion tests passed; both Markdown lint runs and whitespace checks passed.
The public output validator accepted 6 pages and 22 files. Existing Playwright
suites remain unavailable as recorded above. Source journals, Office content,
private Workbench storage and the release-review state are unchanged.

Final commit identities and post-push synchronization are reported in the child
and to the hub after both pushes, without another bookkeeping edit cycle.
