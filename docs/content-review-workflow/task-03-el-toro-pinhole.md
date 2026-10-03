# Review 1 - Task 03 El Toro - Pinhole With Lens

This is the preparation snapshot. Shawn approved execution directly in this
child on October 2, 2026: "approved...remember, no over engineering", turn
`01a0ff07-b797-7651-afe6-4d70139cd5eb`. See the
[Task 03 report](reports/task-03-el-toro-pinhole.md) for the scoped result.
The preparation-state fields below are retained as history.
See the [parent register](task-register.md) for hub acceptance and later Git
closeout authorization.

Workflow status: AWAITING APPROVAL
Execution approval: NOT RECEIVED
Prepared: October 2, 2026 (America/Chicago)
Brief revision: 1

Hub: TradeJournals Content Review Parent
Hub thread ID: `01a062b2-cd26-7552-a5f9-3996acac6392`
Child thread ID: `01a0ff06-ae79-75e1-b709-5fbb25c749e0`.
Verified title: Review 1 - Task 03 El Toro - AWAITING APPROVAL.
Runtime: verified idle on October 2, 2026; no dispatch message sent.
Hub register: [Task register](task-register.md)
Environment: same-directory fork, shared TradeJournals checkout.
Preparation branch: `codex/concept-b-homepage`.
Preparation HEAD: `6c48930489851925eb837a2a89f22bb7cec8ccb5`.

## Assignment After Approval

Resolve only the `El Toro - Pinhole With Lens` pending review in the
[Flickr Lomography overlap journal](../../05_the_lens/trade_journals/flickr_lomography_overlap_archive.md).
Review its photographs, select a representative image, and write concise,
evidence-supported prose about subjects, photographic appearance, and source
context. Preserve the distinction between observation and interpretation.

- Inspect the seven recorded Flickr photos if accessible. Record actual coverage
  and any unavailable images; do not claim full coverage after sampling.
- Replace the El Toro pending marker and fill only `Best El Toro representative
  image`. Leave the SXSW sections and shared camera/film-character and
  event/place selections unchanged for their later reviews.
- Use stable Flickr IDs, source labels, and links. Retain Flickr date metadata
  without treating upload or scanner timestamps as verified exposure dates.
- Compare corresponding Lomography images where useful, documenting visual
  matches explicitly rather than assuming identical album contents.
- If evidence is insufficient, report the specific gap instead of inventing
  technique, camera settings, location, or processing history.

## Sources And Known Uncertainties

- [Repository conventions](../../README.md), [project direction](../../PROJECT_MEMORY.md),
  and [lens working guide](../../05_the_lens/README.md).
- [Flickr overlap journal](../../05_the_lens/trade_journals/flickr_lomography_overlap_archive.md).
- [Lomography film catalog](../../05_the_lens/trade_journals/lomography_film_album_catalog.md),
  El Toro album row and shared metadata notes.
- [Flickr El Toro album](https://www.flickr.com/photos/boocher/albums/72157629953268017/).
- [Lomography El Toro album](https://www.lomography.com/homes/texasredd/albums/1838417-el-toro-pinhole-with-lens).

The stored Flickr record lists seven photos, while the Lomography catalog lists
ten. These are saved counts, not fresh external checks; neither implies a
one-to-one match or missing files. Keep platform identities separate.

Flickr's recorded `NORITSU KOKI QSS-32_33` identifies scanner metadata, not the
taking camera. The Lomography catalog attributes Diana F+ camera metadata,
Lomography B&W 100 (120), Austin, 2012/dusk, and a pinhole tag. It also labels the
format 35mm under an existing catalog rule. The 35mm classification and `(120)`
film label are inconsistent; retain attribution and uncertainty, and flag any
needed catalog correction for Shawn rather than silently resolving it.

The album title alone does not establish the optical setup, whether a lens was
attached, exposure settings, or cause of softness or other image characteristics.
Keep Lomography metadata in its catalog unless making an explicit source
comparison in the scoped journal section. No photographs or external source
pages were reviewed during handoff preparation.

## Deliverables And Verification

1. Scoped journal update or precise evidence-gap result.
2. Source-review record with inspected IDs, coverage, selected image, attributed
   metadata, cross-platform matches if established, and unresolved questions.
3. Report at `docs/content-review-workflow/reports/task-03-el-toro-pinhole.md`,
   report ID `TJ-CR-T03-R01`, revision 1, identifying the child, changed paths,
   checks, limitations, and exact Git state.

Visually inspect every selected photograph. Follow local links and verify source
identities and labels. Run `npm run lint:md` and `git diff --check`; distinguish
pre-existing or concurrent failures from task changes. Use workflow-hub for
approval/reporting and art-critic if interpreting photographic qualities.

## Boundaries And Approval

Shawn said "yes" to preparing Task 03's handoff and forking a child while leaving
it awaiting approval. This authorizes preparation only, not source review or
journal edits. Wait for explicit Task 03 execution approval in the hub or exact
child. Do not interpret inherited approvals for Tasks 01-02 as approval here.
After approval, a parent dispatch must include this brief's full path because
the active preparation turn may not be inherited by the fork.

The shared checkout contains unrelated website and website-workflow changes.
Leave them untouched. Refresh branch, worktrees, and current changes before
execution; coordinate isolation if concurrent changes make sharing unsafe.
Do not switch branches or stage anyone else's work.

Tasks 04-11, the Office attribution follow-up, catalog-wide corrections, website
changes, importer code, inventory regeneration, commits, pushes, deployments,
and external publication are outside this approval. Keep this handoff within
TradeJournals craft/public evidence; exclude private business, Oracle, customer,
email, credentials, and private media.

The child must not edit the hub register. After approved work, save the report,
rename the child to `READY FOR REVIEW`, and return the report path to Shawn.
Sending it to the hub requires explicit user messaging authorization; otherwise
leave delivery pending for parent inspection. Hub acceptance and Git closeout
are separate. Completion does not start another task.
