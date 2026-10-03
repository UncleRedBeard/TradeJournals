# Content Cleanup 1 - Task 05 Cassis Paris Attribution Report

- Report ID: `TJ-CC-T05-R01`, revision 2; supersedes blocked revision 1.
- Child: `01a10398-207a-7121-8bee-fc4986363864`.
- Hub: `01a062b2-cd26-7552-a5f9-3996acac6392`.
- Date: October 3, 2026 (America/Chicago).
- Dispatch: `TJ-CC-T05-D01`; approved [brief](../cleanup-05-cassis-paris-attribution.md).
- Status: READY FOR REVIEW; Shawn confirmed both photos were taken in Cassis.
- Report-send approval: Shawn's "yes" in this child on October 3, 2026.
- Report delivery: RECEIVED after one send as `TJ-CC-T05-DEL01`; the parent hub's active review turn was observed. Hub acceptance is pending.

## Source Inspection And Attribution

The live public Flickr pages for [photo 5483335414](https://www.flickr.com/photos/boocher/5483335414/in/album-72157626010685451/) and [photo 5483340298](https://www.flickr.com/photos/boocher/5483340298/in/album-72157626010685451/) were inspected individually on October 3, 2026, including the displayed images and each page's metadata and album list. Both source titles are `cassis`. Both pages list the photo in the Cassis album (27 items) and the Paris album (45 items), show `Canon PowerShot SD780 IS`, and give February 26, 2011 as taken and February 27, 2011 as uploaded. These are page-display observations, not a fresh EXIF audit or proof of physical location.

At normal page-display size, `5483335414` shows a narrow paved lane bounded by buildings, with plants and distant figures. `5483340298` shows small boats and masts beside a stone quay, waterfront buildings, and hills. Neither image visibly identifies a unique city or explains its membership in two albums. The source title and album placement alone do not establish where Shawn took either picture.

In this child on October 3, 2026, Shawn answered "yes" to the question of whether both photos were taken in Cassis. His direct recollection settles city attribution for these two images. It does not explain their Paris-album membership or identify the exact lane or quay. The journal now attributes both to Cassis on Shawn's authority, keeps the Flickr title and dual membership separate, and excludes them as Paris-location evidence. The three accepted Cassis candidates remain unchanged. The reason for dual membership is an explicitly unresolved provenance detail, not a blocker to the city correction.

## Scope And Verification

Child edits are limited to the two-image attribution/provenance notes in the Cassis and Paris sections of the [France travel journal](../../../05_the_lens/trade_journals/flickr_france_travel_archive.md) and this report. The three accepted Cassis candidates, four accepted Paris candidates, their critique, source URLs and metadata, and all other journal sections remain unchanged. No external Flickr album, inventory, film catalog, website file, historical report, or parent-owned brief/register was edited by this child.

- `npm run lint:md`: 133 files, zero issues.
- `npm run check:site-evidence`: manifest current.
- `git diff --check`: passed.
- Diff review: only the Cassis note addition and Paris attribution-caution replacement in the journal; all accepted selections and other sections are preserved. The parent-owned register change is unrelated and untouched.

Branch `codex/concept-b-homepage`; baseline HEAD `a9fbf07a65e2540d73d346f25a138455db9fe8d2`. The shared checkout also contains parent-owned edits to the task register and Task 05 brief, which this child has left untouched. Child changes are uncommitted and unstaged. No fetch, commit, push, merge, deployment, or successor task was performed. Content acceptance, report delivery, and Git closeout remain separate gates.
