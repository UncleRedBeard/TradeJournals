# Release Candidate Review — Three Rooms

Status: APPROVED — exact reviewed snapshot recorded September 19, 2026.

Earlier approvals remain in force for Toil & Timber Restoration, the restrained
green-and-limestone presentation, the exact service line, the future-studio
story and three photographs, and the Task 07 three-room correction. This packet
brings those approved decisions together as one release candidate. Shawn
approved the exact snapshot with SHA-256
`ab0a82cd6e9492800f5e2a8b885aee4038d9e96a01cc1f55221b0cd59ed24fce`.
This approval records the local release state; it does not deploy the site.

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
