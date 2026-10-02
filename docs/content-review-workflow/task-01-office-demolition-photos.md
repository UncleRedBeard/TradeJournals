# Review 1 - Task 01 Office Demolition

This is the October 1 preparation snapshot. Task 01 was subsequently approved
and accepted COMPLETE on October 2. See the [task register](task-register.md)
for current approval, acceptance, and Git closeout records. The original scope
and approval boundary below are retained as history.

Workflow status: AWAITING APPROVAL
Execution approval: NOT RECEIVED
Prepared: October 1, 2026 (America/Chicago)

Hub: TradeJournals Content Review Parent
Hub thread ID: `01a062b2-cd26-7552-a5f9-3996acac6392`
Child thread ID: `01a0f8f2-763b-7f02-ad52-1af2e344b1f3`
Hub register: [Task register](task-register.md)
Brief revision: 1
Environment: same-directory fork in the TradeJournals checkout, branch `main`.
Preparation baseline: `d63a4a08db1884fb81e8690a6962b1c4e8930224`.
The worktree was clean before these handoff documents were created.

## Assignment After Approval

Resolve the remaining photo-review marker under `Visual Evidence` / `Demolition
And Opening` in the [Office restoration journal](../../01_the_residence_1894/trade_journals/office_restoration.md).
Prepare a concise account of what the reviewed photographs establish about
opening, removal, investigation, and revealed conditions, with specific evidence
links. The goal is to document physical work and preservation judgment.

Execution scope proposed for Shawn's approval:

- Read the current journal, project instructions, and prior Office reviews.
- Inspect relevant photographs from the two existing Office Flickr albums,
  starting with local evidence and using read-only public source access as needed.
- Record which images were actually viewed, their stable Flickr IDs, source
  albums, supported dates, and what each image shows.
- Replace the pending marker with supported evidence and concise interpretation.
  Fill the corresponding empty `Demolition and opening` key-photo entry only
  when the selected evidence supports it.
- If the inspected material does not establish this phase, document the bounded
  review and the specific evidence gap. Do not invent demolition work or claim
  full album coverage after examining only a selection.
- Preserve existing journal prose except for the scoped evidence update. Record
  broader contradictions or proposed corrections for Shawn's decision.

No execution has been authorized yet. Preparing this brief and creating the fork
are the only actions authorized by the current request. The fork has been created
and observed idle; no execution message has been sent.

## Sources And Context

- [Office journal](../../01_the_residence_1894/trade_journals/office_restoration.md):
  pending marker was at line 111 when this brief was prepared.
- [Project direction and evidence rules](../../PROJECT_MEMORY.md).
- [Repository conventions](../../README.md).
- [Flickr inventory](../../FLICKR_PUBLIC_ALBUMS.md).
- [Earlier Office migration review](../../website/docs/office-content-review.md)
  and [Office editorial review](../../website/docs/office-editorial-review.md).
  Read current wording and later decisions; historical candidate notes are not
  authority to undo newer approved content.
- [Home Reno - Office](https://www.flickr.com/photos/boocher/albums/72177720316928566/).
- [Home Reno - Studio | Office](https://www.flickr.com/photos/boocher/albums/72177720306207693/).

The journal records 276 and 107 photos respectively. Those are stored counts,
not a fresh external verification. Room-use wording has had historical conflicts;
correlate the correct room, album, chronology, and latest user clarification before
assigning restoration stages. Do not confuse the dedicated Office with the
separate Ballet Barre Studio.

Use human-readable capture timestamps for timestamp-style Flickr titles. Preserve
source titles or state date uncertainty when capture metadata is unreliable.
Separate visible facts, existing project notes, and interpretation. An image of
surface preparation alone does not prove demolition or concealed conditions.

## Deliverables And Acceptance

1. A bounded review record listing inspected sources, selected IDs, evidence
   interpretations, and unresolved questions.
2. The scoped journal update, or a documented evidence gap if source material is
   insufficient. Report the exact coverage and avoid an unsupported completion
   claim.
3. A completion report at
   `docs/content-review-workflow/reports/task-01-office-demolition-photos.md`,
   with report ID `TJ-CR-T01-R01`, child ID, changed paths, verification results,
   remaining gaps, and exact Git state.

After approval, refresh the shared checkout and preserve concurrent changes.
Visually inspect every selected image; metadata alone is insufficient. Check
source identity, date labels, and link targets. Run `npm run lint:md` and
`git diff --check` for the journal update and report. If Git closeout is later
authorized, follow the current repository-required checks and Shawn's global
`git er done` instructions.

No skill is required solely because photos are involved. Use the workflow-hub
skill for task state and reporting; use relevant image/source tools for the
evidence review. Apply PDF or art-analysis skills only if the actual work needs
them.

## Boundaries And Approval

Shawn's current instruction:

> create a handoff for task 1 fork it and give it an appropriate label...wait for
> my approval before starting the newly forked task

Do not start the review, fetch photographs, or edit the journal until Shawn
explicitly approves this task. Approval may be given in the parent hub or directly
in the exact child. The parent must pass this brief's path when dispatching
because an active hub turn is not copied into a fork.

Website records, review snapshots, media inventories, importer code, other
journals, and Tasks 02-11 are outside this task. Do not publish to Flickr, deploy
the website, commit, or push under preparation-only approval. A later explicit
instruction controls any expanded authority.

Keep craft evidence in this existing project environment. Do not copy Oracle,
customer, email, private business-planning, credential, or private media content
into the handoff or public repository.

The child does not edit the hub register. At the end of approved work, save the
report and rename the child to `READY FOR REVIEW`. Return the report location to
Shawn. A message to another thread requires Shawn's explicit messaging authority;
if that is absent, retain report delivery as PENDING for hub inspection. Completion
does not start another task.
