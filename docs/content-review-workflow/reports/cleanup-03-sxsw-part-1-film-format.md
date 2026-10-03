# Content Cleanup 1 - Task 03 SXSW Part 1 Film Format Report

- Report ID: `TJ-CC-T03-R01`, revision 3; adds Shawn's catalog-wide Diana F+
  clarification to revision 2 and supersedes blocked revision 1.
- Child: `01a10354-9e64-7620-954d-0feabdda7a31`.
- Hub: `01a062b2-cd26-7552-a5f9-3996acac6392`.
- Date: October 3, 2026 (America/Chicago).
- Dispatch: `TJ-CC-T03-D01`; approved [brief](../cleanup-03-sxsw-part-1-film-format.md).
- Status: READY FOR REVIEW; album-specific and catalog-wide clarifications received.
- Report-send approval: Shawn's "you can now send the update to the hub" on
  October 3, 2026, child turn `01a10360-ae7c-7280-98d1-41c84bf310f4`.
- Report delivery: SENT once as `TJ-CC-T03-DEL01`; parent active review turn
  `01a10361-93c5-7110-a10a-52ae3fe61960` observed. Hub acceptance is pending.

## Evidence And Decision

The live [representative Lomography page](https://www.lomography.com/homes/texasredd/albums/1689964-sxsw-2011-part-1/12915139)
displayed Diana F+, Kodak Ektachrome 64T (120), Austin, 2011/night, `sxsw`,
uploaded 2011-03-24, and position 17/17 on October 3, 2026. The public browser
provided these fields after the text web reader could not retrieve the page.
This is a one-page metadata check, not a new image review, Flickr count check,
or recount of the catalog's camera split.

Bounded read-only Git provenance review found that commit
`201e25d33c0d08d94178e29cb2728eaf924bbe87` already contained the nine-Diana/eight-
Isolette tally, Diana F+ to 35mm rule, and conflicting `(120)` label together.
The committed evidence does not substantiate the rule with a cited user
statement, physical-film record, or frame-by-frame inventory. That does not
prove the rule was an assistant inference or negate an earlier user instruction.
Later `71a6692` added portfolio selections; `aa9d4c8` corrected only El Toro.
The accepted Task 04 report explicitly did not refresh the nine/eight split.

Revision 1 qualified the classification as provisional and asked Shawn whether
the SXSW Part 1 Diana photographs were shot on 35mm or 120 film. In this exact
child on October 3, 2026, Shawn answered **"120 film"**, turn
`01a1035a-a04e-7a11-9ffb-b2690ff5f849`. That direct clarification resolves the
conflict for this album.

The catalog now places Part 1 under 120 rather than mixed formats, and the
overlap journal records the same correction. Existing Agfa Isolette 120 attribution is preserved;
the nine/eight camera split remains a historical tally, not freshly verified.
El Toro's separate correction is not the basis for this decision. Physical
exposure settings and capture dates are not reassessed.

Shawn then broadened the format correction in this exact child, turn
`01a1035c-9d27-7f33-9eff-eb3ac6dc11b0`: anything labeled `Diana F+`, specifically
the plus sign, means 120 film. This later direct clarification supersedes the
brief's earlier album-only limit for applying the catalog format rule. It does
not authorize website, inventory, external source, Git, or hub-register changes.

The catalog-wide rule is now Diana F+ to 120, leaving Diana Mini unchanged.
Nine additional album rows and their format notes moved from 35mm to 120:
Caveau de la Huchette, East Side Locos, East Side Showroom, Night Shots,
Paris en Rouge, Queer Bomb Austin 2012, queer bomb pt 2, South 1st Performance
Auto, and Street Style. South 1st's earlier 35mm project note is explicitly
superseded. El Toro's accepted 120 classification and purchase provenance remain.

Original platform camera/film labels, counts, dates, locations, and URLs are
preserved. Caveau and Paris en Rouge retain their conflicting recorded
`Lomography Color Negative 35 mm ISO 100` labels, now identified as source
metadata rather than governing format. No replacement stock is invented and no
fresh source check of those nine albums is claimed. SXSW Part 2's Diana Mini
format/date conflict remains outside this correction.

## Scope And Verification

- Edited Part 1 classification/provenance passages in the
  [film catalog](../../../05_the_lens/trade_journals/lomography_film_album_catalog.md)
  and [overlap journal](../../../05_the_lens/trade_journals/flickr_lomography_overlap_archive.md),
  plus the catalog-wide Diana F+ format classification on Shawn's later direct
  clarification, and this report.
- Accepted visual observations, representative frame, source identities,
  El Toro, Part 2, and non-Diana-F+ classifications are preserved in the reviewed diff.
- Parent brief/register, historical reports, inventories, and website untouched.
- Report-inclusive checks passed: `npm run lint:md` (129 files, zero issues),
  `npm run check:site-evidence` (manifest current), and `git diff --check`.
- No application code changed; application tests were not run.

Branch `codex/concept-b-homepage`, baseline HEAD
`aa9d4c8f8d0ec8d02cd2e4a48b627e6f6b4e76d5`. Child changes are uncommitted;
parent-owned brief/register changes remain separate. No staging, commit, push,
fetch, external album write, deployment, or successor task. No synchronization
claim is made. User clarification is received; content acceptance, report
delivery, and Git closeout remain separate gates.
