# Studio Bay-Window Gallery Addition

Record: `WK-WEB-STUDIO-BAY-20261112-R01`, revision 2.
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` — website updates.
Status: COMPLETE — accepted November 13, 2026. This is a bounded follow-up to
Tasks 25–26 in the hub;
no new child chat was requested or started.

Acceptance: `WK-WEB-STUDIO-BAY-20261113-A01` accepts revision 2. Shawn said
“awesome, that looks great. approved.” in this hub on November 13, 2026
(America/Chicago). This accepts the six-photo gallery and requested lead swap.
Shawn then authorized the established release preparation and Git closeout
with “git er done” in this hub on November 13. Destination: established
`origin/main` at `git@github.com:UncleRedBeard/TradeJournals.git`.
Public deployment and inquiry activation remain separate.

## Approved scope

After reviewing four latest album additions, Shawn said “make it happen cap'n”
to adding only the bay-window photograph as the sixth gallery image. Shawn
then requested that the November 11 barre-and-mirrors photograph replace the
lead, swapping gallery positions one and four. Search-image order follows the
same swap. All six photographs, their captions and completion timeline remain.
The Studio homepage card uses the gallery lead and therefore follows this swap.
No layout, viewer, route or dependency changes. The prior closeout is `97ba80c`.

## Imported photograph

- Source: [November 9 bay-window photograph](https://photos.google.com/share/AF1QipPool3gE7T-_DVHyOZm3jEVm5TSnoL4P5kDdXAhzk-ja22Gbw3rsYOi8cn8EwffLA/photo/AF1QipNY_ZpdaZuScLisrXnoDxrSiB7iJ9tipBaWBTq-?key=S1hjd2FTdE9uTjMzX2NHNHpvYUZiQjA3YmpONTFR).
- Album: `google_photos:af1qippool3ge7t`, Home Reno - Studio.
- Displayed capture date/time: November 9, 2026, 5:05:57 PM.
- Media ID: `studio-3e7c92d16a1d533bb115de45be3a6d30bd35e8c320cd43f157a28bd867cd6777`.
- SHA-256: `3e7c92d16a1d533bb115de45be3a6d30bd35e8c320cd43f157a28bd867cd6777`.
- JPEG: 1488 × 1984 pixels; 587,560 bytes. Google-served display image exported
  from the rendered photo page and inspected locally; bytes unmodified.
- Placement: sixth gallery/search image, role `detail`.
- Caption: “The bay windows, wood display shelves and refinished floor in the
  furnished studio, November 9, 2026.”
- Alt: “Three bay windows with white trim and floral coverings sit beneath wood
  display shelves and a white plank ceiling, with the refinished floor and
  studio equipment below.”

This documents finished-room use. It makes no new material/species, authorship,
window-operability or completion-date claims. The other three new album photos
remain outside the website selection. The album total was not recounted.

## Verification — November 12, 2026

- Full website suite: 125 Node and 37 Python tests passed.
- Preview build and independent output checker: 20 pages, 63 files and 375
  references validated. Repository Markdown lint and whitespace checks pass.
- Initial bay-window review on desktop (1593 pixels) and mobile (390 × 844):
  the new local photograph
  loads at 1488 × 1984, opens with the expected caption, and closes through
  Escape or the close button with focus restored. Six gallery links are present;
  mobile document width equals the viewport, with no horizontal overflow.
- The disclosure retains the exact Google photo link. Actual imported bytes
  match the media ID's SHA-256. No image transformation was performed.
- Revision 2: compared the project against HEAD and confirmed the exact
  first/fourth swap, preserving the original five image records and sixth
  bay-window image. Search-image order matches the gallery; all other project
  fields are unchanged.
- Reloaded the live preview after rebuilding: the November 11 barre-and-mirrors
  image is first, the previous lead is fourth, and the bay-window image remains
  sixth. All six local photographs load. The new lead renders at desktop width
  and loads on mobile (390 × 844), with no horizontal overflow.
- No story or shared component changes were needed. The Studio homepage card
  follows the new gallery lead through its existing component.

At acceptance, the prior release snapshot remained unchanged. The approved
refresh is confined to the Studio project, new media, source journal and album
inventory section. Source records and current image-count guidance are kept
in sync; dated Task 25–26 reports retain their historical five-image checkpoint.

## Release and Git closeout — November 13, 2026

Authorized after visual acceptance. Fresh checks pass under Node 24.21.0:
125 Node and 37 Python tests, preview and guarded release builds, and their
independent output checks (20 pages, 63 files and 375 references each).
Direct inspection of both outputs confirms nine galleries, 40 local photo
links, all six Studio images in the approved order, the updated homepage card,
unchanged Entry hero, exact image bytes and the expected robots state.
The November 12 desktop/mobile review was accepted on November 13.

The reviewed snapshot is current with zero changed keys: 63 records and 58
sources. Changed fingerprints are limited to the Studio project, bay-window
media record/bytes, Studio source journal and Google album inventory section.
Exact `pilot.json` SHA-256:
`5c782fc562c4bf5a3f5b421ce5709d7b126c8253cca611fe7021563f32bae13e`.

The scoped commit includes the gallery and imported photo/provenance, source
records, current image-count guidance/tests, release snapshot and approval
records. Final commit identity, remote synchronization and checkout state are
verified in the hub response after push. Public deployment and inquiries remain
separate.

[Six-photo preview](http://127.0.0.1:8144/work/living-room-studio-restoration/).
At the November 12 review, the previous server was no longer listening. A new
loopback-only server served `website/.preview-dist` on port 8144, exec session
`78568`, and was left available for review. Chrome tab `2084712291` was retained;
the mobile override was reset. Server availability was not rechecked when
recording acceptance.
