# Expanded Website Release Review

Current status: Concept B and the subsequent Office, current-studio and La
Ciotat additions are the accepted local release integrated into `main` on
October 4, 2026. Hosting and deployment remain separate. See the dated
[Task 15 report](../../docs/website-workflow/reports/task-15-integrated-release-review.md)
for the earlier integrated candidate and the
[Task 18 report](../../docs/website-workflow/reports/task-18-main-integration.md)
for current integration verification.

The sections below preserve the dated content approvals and earlier release
results. Earlier design descriptions, project ordering and port 8138 links
are historical; the October 3 section records the current presentation.

## September 20 Approved Expanded Snapshot

Earlier approvals remain in force for Toil & Timber Restoration, the restrained
green-and-limestone presentation, the exact service line, the future-studio
story and three photographs, and the Task 07 three-room correction. This packet
brings those approved decisions together as one release candidate. Shawn
approved the exact snapshot with SHA-256
`ab0a82cd6e9492800f5e2a8b885aee4038d9e96a01cc1f55221b0cd59ed24fce`.
That snapshot remains the historical Task 08 baseline. Task 10 added five
approved stories and the craftsman-first homepage; Shawn then started Task 11
to record and verify that expanded release. The September 20 reviewed snapshot covers
50 public records and 47 selected sources with canonical SHA-256
`ec16411478fec3d39b8099e1c366cfe4cedd27af797bcd7217dcd4a1ecff9fcc`.
This approval records the local release state; it does not deploy the site.
The October 2, 2026 review of subsequent changes is recorded at the end of
this document.

## Expanded Release

Historic-home restoration remains primary. The homepage leads with Entry and
Stair Restoration, followed by Guest Bath and Dresser Vanity, Master Bedroom
Restoration, and the future living-room studio. Returning to Clay and Agfa
Isolette remain secondary under **From the workshop**. The dedicated Office and
current Barre Studio remain available as distinct projects. The inquiry action
stays disabled until Shawn supplies a public destination.

During release review, Shawn approved the clearer technical wording
`120-format film` in the Agfa Isolette story. The snapshot above includes that
exact correction.

## Candidate Direction

Keep the approved design, typography, headline **Keep what makes it home.**, and
service line **Historic floors, interior woodwork, and architectural
restoration.** Feature the former living room being prepared as the future
barre studio. Keep it distinct from both the dedicated Office and the current
barre studio. The own-home context remains explicit; no client job is implied.

The story concentrates on three craft decisions: retaining original material,
protecting completed floor work while other trades continue, and bringing
reclaimed ceiling repairs, shiplap, mineral finishes, and crown molding together.
Four short paragraphs provide enough substance without becoming a tutorial.

## Preview Routes

- [Homepage](http://127.0.0.1:8138/)
- [Future barre studio](http://127.0.0.1:8138/work/living-room-studio-restoration/)
- [Current barre studio](http://127.0.0.1:8138/work/studio-office-restoration/)
- [Dedicated Office](http://127.0.0.1:8138/work/office-restoration/)
- [TradeJournals archive](http://127.0.0.1:8138/tradejournals/)

## Current Candidate

| Project | Status | Source | Selected photographs |
| --- | --- | --- | ---: |
| Living Room Restoration — Future Barre Studio | Future home of The Repair Shop; move not confirmed | Google Photos `af1qippool3ge7t` | 3 |
| Dedicated Office | Current dedicated office | Flickr `72177720316928566` | 5 |
| Barre Studio — Current Room | Current home of The Repair Shop | Flickr `72177720306207693` | 5 |

All three projects have separate work and TradeJournals routes, search records,
stories, captions, alternative text, source links, and album ownership. The
site must not imply that the move from the current studio has occurred.

## Photo Selection — Task 06 Candidate

Three photos were inspected in the shared Studio Google Photos album and brought
through Photos Inbox and the Workbench Website editor on September 17, 2026.
The lead is the August 26, 18:42:52 near-completion view identified in the journal.
No Office photographs were substituted. The homepage hero stays text-only; the
Studio project card and gallery use the selected lead.

| Order | Google Photos image ID | Role | Description |
| --- | --- | --- | --- |
| 1 | `AF1QipOYOPMUTUnNJtdnZlBl5Aq_xtg__YaYVun_8a_m` | result | August 26 room, floor, white ceiling and timber wall |
| 2 | `AF1QipO5TK5FXRp97MN26dv5wFBXuLUtEJmB03luGYUW` | condition | March 16 starting room with blue walls and worn floor |
| 3 | `AF1QipO5zjJV4Fdl_JosSyl-9VcRTD99Ailb1PqRU9qS` | process | March 16 scrapers and finish shavings by the floor register |

Exact captions, alternative text, source links and gallery order are saved in
`website/content/projects/living-room-studio-restoration.json` and its three
`studio-*` media records. Review them in the generated preview. The candidate uses inspected
Google display renditions, converted into ordinary local JPEG copies, then
normalized through private intake. These are not full-resolution camera originals.
No source photographs, journal or inventory were edited.

The live album includes later September photographs. This candidate deliberately
uses the dated March/August evidence supporting the already accepted text.
See [Workbench instructions](workbench.md) for intake and maintenance.

## Source Boundaries

- Room identity and current/future status follow Shawn's direct Task 07
  correction, not album names, image dates, or renovation appearance.
- The future-studio public account uses the dated journal record without
  claiming final sign-off, an installed barre, or current occupancy.
- Dedicated Office photographs document the present room but do not establish
  the disputed floor, door, date, or completion claims in the mixed journal.
- Current-studio photographs show an active work state. Current occupancy comes
  from Shawn's correction, not from what is visible in those images.
- Stored album counts are historical. The build makes no live provider request.
- No journal, inventory, or original photograph is changed by this release.

See the [three-room source audit](task-07-room-source-audit.md) for the detailed
evidence boundary.

## Task 08 Verification

- Clean clone at `dd6da4c01476e3ccdcdfbf9b1193b00c5b842d6b` installed the
  scoped Node 24.21.0 runtime and locked dependencies without copied caches.
- The clean-clone baseline passed 115 website Node tests and 37 Python tests;
  the current placeholder candidate passes 116 website Node tests and the same
  37 Python tests.
- Candidate output validated as eight HTML pages, 24 files, and 93 references.
- Desktop and 390-pixel browser checks covered the homepage, all three work
  pages, the archive, navigation, selected-image counts, and archive search.
  No console errors or horizontal overflow were observed.
- The homepage includes a disabled `Email us — coming soon` placeholder. It has
  no address, link, or form action. A later update will replace it with an
  approved `mailto:` action after a public address exists.
- The exact proposed reviewed snapshot covers 22 public records and 18 selected
  source fingerprints. Its serialized SHA-256 is
  `ab0a82cd6e9492800f5e2a8b885aee4038d9e96a01cc1f55221b0cd59ed24fce`.
  The saved snapshot is `reviewed`, matches this digest exactly, and compares
  as current with zero changed keys.

## Release Result

- The guarded release build produced and validated eight HTML pages, 24 files,
  and 93 references in `website/dist/`.
- Desktop and 390-pixel checks of the release homepage found no overflow or
  console errors. Release output has no review notice or `noindex` metadata.
- Hosting selection, domain/DNS work, upload, and deployment remain separate
  work.

## Task 11 Expanded Release Result

- The reviewed snapshot compares as current with zero changed keys.
- Candidate and release builds each validate as 18 pages, 52 files, and 232
  internal references.
- The release package is the contents of `website/dist/`; the repository,
  journals, Workbench data, runtime, and preview output are not upload content.
- Hosting selection, domain/DNS work, public contact destination, upload, and
  deployment remain separate decisions.

## October 2 Concept B And Source Review

Shawn approved the Concept B homepage implementation and then approved the
three changed review items for the exact local revision: the homepage project
order, the living-room journal's clarification that its windows remain sealed
and non-operable, and the Office journal's bounded account of localized
electrical access. The Office journal still contains older mixed-room claims;
the public Office story continues to withhold them.

Only those three fingerprints changed in `content/reviews/pilot.json`. The
reviewed snapshot now matches 50 public records and 47 selected sources with
zero changed keys. The exact `pilot.json` file has SHA-256
`cdc69b8b5c95af1e05677e9a1639287fd5b8886ab0872ce9adc3bc71dcd5699f`.

The full website suite passed 118 Node and 37 Python tests. Candidate and
guarded release builds each validated 18 pages, 52 files, and 236 references.
The candidate retains a review notice and `noindex, nofollow`; the release
output has neither. The inquiry control remains disabled. At that checkpoint,
the rest of the site's Concept B visual update, hosting and deployment were
still pending.

## October 3 Integrated Concept B Review

Tasks 12–14 are accepted COMPLETE: the shared header/footer and local fonts,
project pages and full-image galleries, journal reading layout, and archive
with static and dynamic search results now share the accepted Concept B
presentation. The homepage leads with the future living-room studio, followed
by Entry, Guest Bath and Master Bedroom; clay and film remain secondary.

Task 15 verifies committed baseline
`ef1d5e8303860d49b7ae6131b0596e2bce38660b` as one static release candidate,
including an independent fresh checkout. Its report records the exact runtime,
tests, package checks, browser sample and any remaining limitations. Task 15
does not change the reviewed snapshot, public copy, images or source records.

The future studio, current studio and dedicated Office remain separate; the
move remains unconfirmed. Inquiries remain disabled. Merging the branch,
hosting/domain selection, upload/deployment and any public contact activation
remain separate decisions.

## October 3 Office Access-Detail Release Approval

After reviewing the Office-only candidate at commit `9e2dd6d`, Shawn said
"approved...git er done" in the Content Review Parent. This approves the exact
Office update for the local release snapshot and Git closeout, not deployment.

The snapshot changes are limited to the Office project and story, the new
`flickr-53718846780` media record and image bytes, and the already accepted
Office source-journal attribution correction. All five original Office images
remain, followed by the localized-access detail. No homepage selection, other
project, room occupancy, inquiry control or source journal is changed here.

Verification passed: 84 repository Python tests, 121 website Node tests,
37 website source/HTML tests, five Python and five JavaScript search tests,
Markdown lint and current evidence-manifest checks. The guarded release build
and independent output checker validate 18 pages and 53 files. The snapshot
is current with zero changed keys, covering 51 public records and 48 sources.
The exact `pilot.json` SHA-256 is
`7dd9d7608c8f28b2846ab46451a9ccef40078ed32cfc6af8ee8e061d0940d27e`.

Hosting, upload, deployment, merging to main and the remaining content-promotion
proposals still require separate approval.

## October 3 Studio Retained-Door Release Approval

Shawn approved release-snapshot promotion with "yes" in the Content Review
Parent after accepting and closing out candidate commit `849fbce`.
Only the Current Barre Studio project/story and the selected media records and
image bytes for `52704581571` and `52704058327` changed fingerprints.
The person-visible torch frame remains excluded. Dates and final installation
remain qualified, and the homepage and other projects are unchanged.

This is approval of the local release snapshot, not deployment, a main merge,
inquiry activation or starting the La Ciotat story.

Fresh verification: 121 website Node and 37 source/HTML tests passed. The
guarded release build and independent checker validate 18 pages and 55 files.
The snapshot is current with zero changed keys, covering 53 records and 50
sources. Exact `pilot.json` SHA-256:
`337bb262659e1f82d8e1692472e83e5a8c96d8d27802e1363e503e2b7fe4be03`.

## October 3 La Ciotat Release Approval

Shawn explicitly approved La Ciotat release-snapshot promotion in the Content
Review Parent after accepting candidate commit `f45a020`. New fingerprints
cover only the La Ciotat project/story, its three selected media records and
image bytes, the La Ciotat inventory section, and its France archive source
journal. Existing record and source fingerprints are preserved.

The three-photo story remains available through archive/search and off the
homepage. Approval is for the local release snapshot, not deployment, a main
merge or another content task. Shawn subsequently authorized Git closeout of
this approval record and snapshot with "yup...git er done".

Fresh verification: 121 website Node and 37 source/HTML tests passed. The
guarded release build and independent checker validate 20 pages and 60 files.
The snapshot is current with zero changed keys, covering 58 records and 55
sources. Exact `pilot.json` SHA-256:
`d69779edcd6ded04951bc729d89be0757aa91ebd8b035607ab94c99ad85b9f4f`.

## October 6 Services and Regional Context Release Approval

Shawn reviewed and approved Tasks 19 and 20 in website updates, then said
“make it happen cap'n” to the proposed snapshot refresh and Git closeout.
This approves the accepted services, paid-assessment and regional wording
for the local release and push to the established `origin/main`.

Only four record fingerprints changed: `home:home`, `service:historic-floors`,
`service:interior-woodwork`, and `service:paid-assessment`. All source, image
and project fingerprints are preserved. Inquiries remain disabled.

Fresh verification: 121 website Node and 37 source/HTML tests pass; repository
Markdown lint passes. Preview and guarded release builds independently validate
20 pages, 60 files and 366 references. The snapshot is current with zero changed
keys. Exact `pilot.json` SHA-256:
`2efb1566680b93491b2f13b389d2ccb368be6e60392cef31bd3027095bdcd841`.

This release is repository-ready; hosting, deployment and inquiry activation
remain separate. The unrelated `PROJECT_MEMORY.md` edit is excluded from
this Git closeout. Earlier task reports describe their submission checkpoints.

## October 6 Page Meta Descriptions Release Approval

Shawn accepted Task 21, then replied “reviewed and approved” to the proposed
release validation and Git closeout in website updates. This authorizes the
accepted metadata changes and associated records for `origin/main`.

Fresh verification passes: 122 Node tests, 37 Python source/HTML tests, preview
and guarded release builds (20 pages / 60 files / 366 references). Independent
HTML parsing confirms exactly one nonempty, unique description per page in both
outputs; preview retains noindex and release does not carry that restriction.

The existing content snapshot is current with zero changed keys and remains
byte-identical: template metadata does not change content fingerprints.
No snapshot rewrite is needed. Publication and inquiry activation remain
separate; the unrelated PROJECT_MEMORY.md edit is excluded from this closeout.
