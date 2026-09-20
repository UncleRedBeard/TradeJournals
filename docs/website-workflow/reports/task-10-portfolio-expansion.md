# WK-WEB-T10-R01 — Task 10 Portfolio Expansion

Revision: 2
Status: COMPLETE
Date: September 20, 2026
Branch: `codex/website-updates`
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` / website updates
Child: `01a0bf60-e5e5-7e20-8c3d-65c6a6e3a445`

## Approval And Source State

Shawn approved Task 10 by saying `start task 10`. The Markdown repair was later
handed into the same task by the hub. The implementation started from commit
`ab1bce63e94f7848511e206bc03a2f8447f24756`.

After reviewing the result, Shawn said the updates looked good and approved
them. He later rejected the separate tartan landing-page mock-up and confirmed
that the approved original should remain. The mock-up was permanently removed
under his task-scoped `we die like men!` authorization; it never entered this
repository. Shawn then authorized Git closeout with `git er done`. The approved
website implementation is commit `6e21460` on `codex/website-updates`.

## Implemented Candidate

The candidate adds five evidence-led stories while keeping all three existing
room records available:

1. [Entry and Stair Restoration](http://127.0.0.1:4173/work/entry-restoration/)
2. [Guest Bath and Dresser Vanity](http://127.0.0.1:4173/work/guest-bath-dresser-vanity/)
3. [Master Bedroom Restoration](http://127.0.0.1:4173/work/master-bedroom-restoration/)
4. [Returning to Clay](http://127.0.0.1:4173/work/returning-to-clay/)
5. [Agfa Isolette: A Working Eye](http://127.0.0.1:4173/work/agfa-isolette/)

The homepage now leads with the entry project and separates four restoration
projects from a quieter `From the workshop` section for pottery and film. It
introduces the approved craftsman-first positioning, includes the jack-of-all-
trades quote without attribution, and invites thoughtful inquiries while
retaining the disabled email placeholder.

The Work navigation now opens Entry and Stair Restoration. The current barre
studio, dedicated office, and future living-room studio remain distinct. No
shelf completion claim was added; the Google-album shelf planks remain
understood as unfinished, temporarily dry-fitted work.

## Selected Images

- Entry: three Flickr images covering protected work, the retained stair and
  rail, and the renewed floor.
- Guest Bath: dresser preparation, vessel-sink fitting, and the verified final
  room image.
- Master Bedroom: the limited electrical investigation, protected 2024 finish
  work, and the room returned to use. The 2023 and 2024 passes remain separate.
- Pottery: the strongest historical jar and functional bowl from the circa
  1994–1995 Brookhaven work, plus one clearly identified unfired current form.
- Agfa Isolette: the full six-image editorial sequence from coast to workshop,
  including the intentional double exposure and Lockerbie Model K bridge.

All 18 new media records retain the Flickr photo identity, album provenance,
source link, dimensions, and meaningful alternative text. Four newly selected
source images were downloaded without alteration and verified as JPEG files.

## Maintainability Changes

- Added explicit `workshopProjectIds` to the existing home schema and public
  model rather than introducing a taxonomy or CMS.
- Enforced that a project cannot appear in both restoration and workshop
  homepage groups.
- Added a small reusable craftsman introduction component and bounded homepage
  styling for the secondary section.
- Normalized Workbench story saves to exactly one final newline while
  preserving Markdown hard breaks, with regression coverage.
- Excluded only generated `.superpowers/sdd/**` packets from Markdown lint and
  fixed final newlines in the three authored pilot stories.

## Verification

- `npm run test:website`: 118 Node tests and 37 Python tests passed.
- `npm run check:website`: candidate built and independently validated at 18
  pages, 52 files, and 232 references.
- `npm run lint:md`: 85 Markdown files, 0 errors.
- `git diff --check`: passed.
- Release build: refused as designed with `SOURCE_STALE`; the old reviewed
  snapshot was preserved byte-for-byte.
- Browser QA: homepage and all five new work routes opened on loopback; every
  selected gallery image loaded with its declared dimensions; `dresser`
  returned exactly the Guest Bath result; desktop and 390-by-844 mobile checks
  showed no horizontal overflow; browser console showed no warnings or errors.

The current review preview is available at
[http://127.0.0.1:4173/](http://127.0.0.1:4173/).

## Review Outcome And Remaining Release Decision

- Shawn approved the five new stories, titles, captions, image order, and the
  understated homepage placement of the jack-of-all-trades quote.
- Supply a public contact destination when ready; the candidate does not invent
  an address, form, or phone number.
- Refreshing the exact reviewed release snapshot remains a separate release
  step; this closeout preserves the intentional `SOURCE_STALE` gate.

No journal, album inventory, hosted site, DNS record, dashboard, or private
source was changed by this implementation.
