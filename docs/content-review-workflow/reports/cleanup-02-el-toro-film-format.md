# Content Cleanup 1 - Task 02 El Toro Film Format Report

- Report ID: `TJ-CC-T02-R01`, revision 4; adds personal purchase provenance to
  revision 3 and supersedes the blocked revision 1.
- Child: `01a10326-eb2a-72c3-842d-4eaf224f98f2`.
- Hub: `01a062b2-cd26-7552-a5f9-3996acac6392`.
- Date: October 3, 2026 (America/Chicago).
- Dispatch: `TJ-CC-T02-D01`; approved [brief](../cleanup-02-el-toro-film-format.md).
- Status: READY FOR REVIEW; film-format clarification received.
- Report-send approval: Shawn's "yes" on October 3, 2026, in this child's turn
  `01a10345-1986-74e0-8b4f-91d4c368c029`, authorizes delivery to the parent hub.
- Report delivery: SENT once as `TJ-CC-T02-DEL01`; parent active review turn
  `01a10346-0679-75c0-9604-60eefb2b1777` observed. Hub acceptance is pending.

## Evidence And Decision

The catalog's original commit `201e25d33c0d08d94178e29cb2728eaf924bbe87`
already contained both the blanket Diana F+ 35mm rule and the El Toro
`Lomography B&W 100 (120)` label. Later catalog commit `71a6692` added the
best-of selections, not substantiation for the rule. A bounded provenance check
did not recover an explicit user confirmation of the rule; that does not prove
it was an assistant inference or revoke any earlier user instruction.

Read-only browser inspection of
[Lomography photo 15964487](https://www.lomography.com/homes/texasredd/albums/1838417-el-toro-pinhole-with-lens/15964487)
on October 3 confirmed the displayed Diana F+ camera and
`Lomography B&W 100 (120)` film fields. The page showed position 10/10. This was
a metadata check of one representative page, not a new review of every image
or a fresh Flickr count check. The web-reading tool could not access the page;
the public in-app browser page provided the observable fields.

Revision 1 preserved uncertainty and asked Shawn which format applied. In this
exact child on October 3, Shawn answered: **"El Toro is a 120 format camera."**
El Toro is now classified as 120 on that direct authority, superseding its
earlier 35mm placement under the catalog rule. The Lomography camera and film
labels remain intact as source metadata. No exposure settings or scan-based
inference was added. The format question is resolved
for this album only; other albums' classifications are not reassessed.

Shawn subsequently supplied edition background and
[a video reference](https://www.youtube.com/watch?v=QfFr5-S8nOA).
Lomography's [edition history](https://www.lomography.com/magazine/331216-the-diana-f-over-the-years)
confirms that El Toro is a red, Spain-themed Diana F+ edition honoring bulls
and matadors. Its [Diana F+ product specifications](https://shop.lomography.com/world/diana-f-camera-flash)
confirm 120 film, 12/16 square-frame options, a removable 75mm lens, pinhole
capability, and normal/Bulb shutter modes. A short catalog note records those
capabilities without inferring the actual settings used in the album. The
generic Diana F+ metadata is consistent with the El Toro edition identity.

Shawn also recalled in this child: "i bought mine in paris during my trip
there." The catalog records that personal purchase provenance separately from
the album's Austin location metadata. No purchase date, store, trip year, or
claim that this camera made any particular Paris photograph was inferred.

The supplied [secondary camera history](https://filmphotography.eu/en/camera/diana-f-el-toro/)
was readable and describes the 2009 tour association; the exact launch/tour
claim was not independently corroborated in the manufacturer sources reviewed
and was not added to the catalog. The video and Light Leak Club page were not
accessible to the web-reading tool; no video viewing or transcript review is
claimed. The catalog relies on the manufacturer sources for camera context.

## Exact Scope

- Corrected only El Toro's format in the
  [Lomography catalog](../../../05_the_lens/trade_journals/lomography_film_album_catalog.md)
  and [Flickr overlap journal](../../../05_the_lens/trade_journals/flickr_lomography_overlap_archive.md).
- Moved its catalog row from 35mm to 120, removed it from the 35mm list, and
  recorded the album-specific exception, source metadata, and user correction.
- Added only El Toro's concise, source-backed camera-edition context; no full
  specification sheet or historical research expansion.
- Preserved the accepted visual critique, representative image, source links,
  platform identities, and historical seven-Flickr/ten-Lomography distinction.
- Other albums, historical reports, inventories, website files, parent brief,
  and hub register were not edited by this child.
- No new journal structure, tooling, external album writes, or successor task.

## Verification And Git State

- `npm run lint:md`: passed, 127 files, zero issues.
- `npm run check:site-evidence`: passed; checked-in manifest remains current.
- `git diff --check`: passed.
- Exact journal diff reviewed: only the El Toro classification and source
  provenance changed; accepted visual observations and SXSW sections are intact.
- No application code changed, so application test suites were not run.

Branch `codex/concept-b-homepage`, HEAD
`20201aa8bc1fa5b21b9141938b0b2619d7a2f558`. Child changes are the two journals
and this report, uncommitted. Parent brief/register changes are separate and
preserved. No staging, commit, push, fetch, deployment, or remote-sync claim.

Content acceptance, report delivery, and Git closeout remain separate gates.
