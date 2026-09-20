# Website 1 - Task 08 Release Readiness

Workflow status: COMPLETE — release-readiness delivery accepted by hub
Approval: Shawn explicitly said `let's start task 08` in the website updates
hub on September 19, 2026, following the release-readiness and portability review.
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` / website updates
Child: `01a0bbcf-a52f-7672-b08e-d69da400c4d7`
Brief revision: 2 — accepted release-readiness delivery
Dispatch: `WK-WEB-T08-D01`
Register: [task-register.md](task-register.md)

Dispatch was sent once September 19 at 22:37 UTC after exact-title/idle readback.
Fresh runtime observation showed execution turn
`01a0bbd1-89f2-7c91-b195-dc0b623ac87b` in progress. No readiness result is yet claimed.

## Acceptance Checkpoint — September 20, 2026, 00:47 UTC

Report `WK-WEB-T08-R01`, revision 2, was received once and reconciled under
`WK-WEB-T08-H01`. This checkpoint supersedes the starting candidate state and
pending decisions below. The exact child reports Shawn approved the disabled
email placeholder and reviewed snapshot SHA-256
`ab0a82cd6e9492800f5e2a8b885aee4038d9e96a01cc1f55221b0cd59ed24fce`.

Hub inspected the changed implementation, guide and editorial packet; confirmed
the saved digest, current review with zero changed keys, and independent release
output validation: eight pages, 24 files, 93 references. Fresh scoped Node 24.21.0
checks passed 116 Node and 37 Python tests. Child reports clean-clone baseline
installation/candidate proof and actual desktop/390-pixel browser verification.
Hub did not repeat those browser or clean-clone checks. The clone proof used
committed baseline `dd6da4c`; the final approved release was built in the working
checkout. Private Companion browser skips remain outside this static-site gate.

Accepted scope is the verified local release and documented reproducible setup.
Task 08 changes remain uncommitted; GitHub does not yet contain this updated
guide, contact placeholder or reviewed snapshot. Companion remains clean.
No commit, push, merge, deployment or successor task is authorized by acceptance.

## Assignment And Authority

You are the executing Task 08 child. Read this brief and begin actual work;
do not prepare another child or stop at a promise to start. This is website
release readiness. It supersedes any earlier tentative Hosting And Launch
label for Task 08. Hosting selection and deployment remain deferred.

Make the existing static website reproducibly buildable and straightforward
to hand off from its Git repository. Keep the implementation proportionate to
an understated tradesman's website. Preserve the approved Astro architecture,
branding, room identities and editorial work. Do not redesign or grow a CMS.

The user has authorized readiness work and necessary bounded fixes. Do all
independent authorized preparation before seeking any final concrete decision.
Ask early for the preferred public contact destination if it cannot be resolved
from current approved artifacts; continue independent work while awaiting it.
Do not invent an address, contact form service or backend.

## Starting State And Ownership

- Archive: `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/TradeJournals`, branch
  `codex/website-updates`, HEAD `dd6da4c01476e3ccdcdfbf9b1193b00c5b842d6b`.
- Companion: `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/tradejournals-companion`,
  branch `codex/website-workbench`, HEAD
  `c4a2338584e0137c0a9685a7c964255dee6413af`.
- Both were clean at preparation; the hub is adding only this brief/register.
  Task 07 bookkeeping is now committed at `dd6da4c`; its earlier pending entry
  is historical. Refresh current state before changing files.
- This is a same-directory fork. You are the sole implementation writer for
  Task 08. The hub owns this brief and the register; do not edit them. Preserve
  other work, branches and existing servers. Inspect applicable instructions
  and permissions in each repository. Companion is outside the archive's
  writable root; obtain required filesystem authorization before writes there.

## Deliverables

1. Reconcile the maintainer guide and related instructions with the actual
   three-room site, current Workbench workflow and candidate/release distinction.
   Give one clear host-neutral path from clone to checked output, including
   prerequisites, exact install/build/check commands and what to upload later.
2. Resolve the runtime inconsistency: the project pins Node 24.21.0, whereas
   Task 07 used global Node 25.8.1 because the scoped version was unavailable.
   Verify actual availability and supported versions; use a project-scoped
   runtime and consistent documentation/configuration. Do not change global Node.
   Establish and document the Python requirement used by build/check scripts.
3. Prove the documented process in a fresh isolated checkout without existing
   node_modules, generated output, private Workbench stores or copied runtime
   caches. Record exact source revision, any applied uncommitted patch, runtime
   versions, commands and results. Do not call a warm-cache build a fresh install.
4. Close the outstanding browser verification gaps relevant to release
   confidence. Task 07 reported 115 website Node and 37 Python tests passing;
   Companion had 258 passing, 24 Playwright skips and an omitted media-ui suite
   that could not import Playwright. Verify current reality, install scoped test
   dependencies when permitted, and run relevant suites and actual browser checks.
   Report any still-unavailable verification explicitly, with its release impact.
5. Prepare a reviewable release package and concise readiness report. Validate
   all intended pages, local links/assets, public-only output, responsive layout,
   selected photos and the agreed contact action. Keep synthetic release tests
   distinct from a real approved-content release build.

## Build And Publication Boundaries

The site is static Astro. Node and Python are build-time requirements, not
hosting requirements. The public site must remain independent of the private
Workbench application, SQLite database and runtime configuration.

The build reads selected journals, inventories, local media and scripts outside
`website/`; document cloning the full repository. The website currently lives
on `codex/website-updates`, not default `main`. Explain that branch explicitly;
do not merge or change the default branch. Current URLs assume deployment at a
domain root. Document this; subdirectory support is not an automatic expansion.

Only validated generated public output is an eventual upload payload, never the
repository or private source archive. Candidate output is `website/.preview-dist/`;
release output is `website/dist/`. Confirm these against current code.

`website/content/reviews/pilot.json` is still a candidate with empty record/source
snapshots. Its real release gate intentionally refuses release. Task 07's local
Publish update applied approved content to canonical sources and produced a
candidate preview; it was not approval of a reviewed release snapshot or hosting.
Prepare an exact snapshot for review and request Shawn's explicit approval before
promoting it. Prior editorial approvals remain valid; do not reapprove identical
copy or room identities. Complete other readiness work while that decision waits.
Never bypass the gate or claim real release success using only synthetic data.

No hosting purchase, domain/DNS work, upload, hosted deployment, external
publication, new remote, commit/push, main merge, journal/inventory correction,
original-media alteration, or successor-task dispatch is authorized here.
Avoid speculative CI/provider integrations. Refresh the durable deletion rule
before any deletion; Task 07's deletion authorization does not carry forward.

## Preserve These Room Identities

- Dedicated Office: `office-restoration`, Flickr `72177720316928566`, current,
  five selected photos.
- Barre Studio — Current Room: `studio-office-restoration`, Flickr
  `72177720306207693`, current home of The Repair Shop, five selected photos.
- Living Room Restoration — Future Barre Studio:
  `living-room-studio-restoration`, Google Photos `af1qippool3ge7t`, former living
  room and future home of The Repair Shop, three selected photos.

Never infer that the move occurred from names, renovation progress or dates.
Do not restore unsupported floor/door/date/completion claims from source journals.
Preserve Toil & Timber Restoration and the approved restrained presentation.

## Read And Verify

Read `website/README.md`, `website/docs/workbench.md`, the current build/review
scripts and package manifests, `website/docs/task-07-room-source-audit.md`,
`docs/website-workflow/reports/task-07-edit-project.md`, and the approved
architecture at `docs/superpowers/specs/2026-09-15-worth-keeping-website-design.md`.
Apply workflow-hub and relevant implementation/testing skills as appropriate;
avoid repeating settled design approvals for this bounded readiness scope.

Run required repository checks, proportionate regression/browser tests, Markdown
lint and `git diff --check`. Existing candidate output was eight HTML pages,
24 files and 93 references; verify actual current output rather than assuming
these counts prove correctness. Record evidence and limitations accurately.

Acceptance target: a fresh checkout follows one current guide and produces a
verified public release folder suitable for later upload to ordinary static
hosting. Actual upload is deferred. If contact or snapshot approval or a required
verification remains unresolved, distinguish completed preparation from remaining
release blockers; do not mark the website release-ready prematurely.

## Return

Save report `WK-WEB-T08-R01`, revision 1, at
`docs/website-workflow/reports/task-08-release-readiness.md`. Include delivered
files, checks, exact environment/source state, approval evidence, remaining
decisions and a practical release checklist. At the review checkpoint rename
your task to `Website 1 - Task 08 Release Readiness - READY FOR REVIEW` and send
the report location and concise outcome once to the exact hub. Request receipt
reconciliation only. Hub acceptance is separate; do not auto-launch another task.
