# Task 26 Studio Website Refresh — Report

Report ID: `WK-WEB-T26-R01`, revision 1. Date: November 12, 2026.
Status: COMPLETE — directly accepted by Shawn in this child.
Acceptance: `WK-WEB-T26-A01`, November 12, 2026: “reviewed and approved.”
Deliverable revision remains 1; this records acceptance only.
Hub register reconciliation remains hub-owned; no callback sent.
Child: `01a1d0aa-7b06-7d11-8e18-608ac75048c1`.
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` — website updates.
Dispatch: `WK-WEB-T26-D01`, brief revision 2.
Input: accepted Task 25 report `WK-WEB-T25-R01`, revision 1.
Delivery: report saved for hub observation through wait_threads; no callback.

## Delivered

The restored living-room Studio now has five local gallery photographs: the
November 7 finished-room lead, the retained March condition and floor-preparation
views, and the November 11 barre/mirrors and shiplap-doorway details. The old
August photograph and media record remain archived intact.

Project and story copy separates August/September 2026 restoration completion
from later furnishing and the November 7 reopening/student appreciation event.
The restored living room is current; the earlier Flickr Studio is former.
No exact completion/move day or subsequent use of the earlier room is invented.
The dedicated Office, prior door evidence, unresolved door dates, routes,
featured ordering, inquiry state and shared gallery design remain unchanged.

## Files

- `website/README.md` — current room mapping.
- `website/content/projects/living-room-studio-restoration.json`.
- `website/content/projects/studio-office-restoration.json`.
- `website/content/stories/living-room-studio-restoration.md`.
- `website/content/stories/studio-office-restoration.md`.
- `website/tests/build.test.mjs` — selected count updated from three to five.
- `website/tests/studio-content.test.mjs` — current/former occupancy and revised
  evidence expectations; existing album separation and door checks retained.
- Three new JPEGs in `website/assets/workbench/` and matching JSON records in
  `website/content/media/`, identified below.
- This report.

Task 25 source edits and hub-owned briefs/register were preserved. No hub
register edits were made by this child. No new dependencies or features.

## Imported media provenance

Only the three accepted photo URLs were visited and downloaded through the
browser's rendered-page asset export. Each image was inspected visually after
export. These are Google-served display JPEGs, not claimed original camera files.
All three are 1488 × 1984 pixels; bytes were preserved without transformation.
IDs use the existing `studio-<SHA256 of bytes>` convention. Exact durable photo
URLs and album ownership are in the JSON records; capture dates are in captions
and the accepted selection report. Signed delivery URLs are not site sources.

| View | Media ID suffix / SHA256 | Bytes | Album display date |
| --- | --- | ---: | --- |
| Finished room | `e4b40175312eeb5a3760ad9100b81b85c8134c118cdd113c98f638b7ee786884` | 602419 | November 7, 2026, 2:01:55 PM |
| Barre/mirrors | `28cf5df28ed481448bac91bb685ac271d3f0b1f00897caeb9fbe7eb93a272843` | 835668 | November 11, 2026, 5:11:16 PM |
| Shiplap doorway | `b40288d6786cc72cf6dfd3d68674d132e4f782d7957e8fd2f0a5b64087cfb929` | 629029 | November 11, 2026, 5:11:46 PM |

## Verification

Using the repository-scoped Node runtime:

- `npm run test:website`: passed, 125 Node tests and 37 Python tests.
- First test run exposed two obsolete three-photo assertions; their associated
  future/current expectations were reconciled to the approved update. The full
  rerun passed, including unchanged room/album separation assertions.
- `npm run check:website`: passed, 20 pages, 62 files, 372 references; independent
  output checker validated 20 pages and 62 files.
- Scoped Markdown lint and `git diff --check`: passed.
- Reviewed actual content/test diff and new media records/bytes.
- Generated affected work/journal pages retain noindex; no stale Future Barre
  Studio title remains anywhere in generated HTML.
- Live Chrome: homepage card, Studio story and earlier Studio heading verified.
  Archive search for studio returns two distinct, correctly named rooms with
  revised descriptions.
- Desktop at 1593 pixels and mobile at 390 × 844: gallery opens all five images,
  captions match, close/Escape work and focus returns to the opening link.
  All five enlarged images loaded with nonzero natural dimensions on mobile.
  Document widths equal viewport widths; no horizontal overflow observed.
- Full source-album link remains below the local gallery. New media records
  retain exact photo source links. Inquiry buttons remain disabled.

## Preview and screenshots

[Studio preview](http://127.0.0.1:8144/work/living-room-studio-restoration/).
[Homepage](http://127.0.0.1:8144/).

Loopback-only Python preview server: PID `77077`, exec session `14606`.
Command: `python3 -m http.server 8144 --bind 127.0.0.1 --directory website/.preview-dist`.
Verified process working directory: TradeJournals repository. Port was free
before launch; no existing server was stopped. Preview left running for review.
Chrome tab `2084712291` is marked as a review deliverable. Mobile override reset.

Screenshots:

- Desktop: `/Users/shkelley/.codex/visualizations/2026/11/12/01a1d0aa-7b06-7d11-8e18-608ac75048c1/studio-desktop.jpg`.
- Mobile: `/Users/shkelley/.codex/visualizations/2026/11/12/01a1d0aa-7b06-7d11-8e18-608ac75048c1/studio-mobile.jpg`.

The full-page desktop capture places the fixed header at the capture scroll
position; the normal viewport presentation was separately visually checked.

## Review and release boundary

Branch remains `main`, baseline HEAD
`68469b700326e6aac48e8fc96418ca7d1bcd9b79`. Changes remain uncommitted.
No staging, commit, push, release promotion or deployment performed.
The approved snapshot remains untouched, SHA256
`2efb1566680b93491b2f13b389d2ccb368be6e60392cef31bd3027095bdcd841`.
Expected review drift is displayed on the candidate; it was not cleared to
bypass acceptance. After Shawn accepts the candidate, snapshot refresh, portable
release validation and Git closeout need the separately authorized next step.
