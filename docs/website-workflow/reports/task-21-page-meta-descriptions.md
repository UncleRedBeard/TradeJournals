# Task 21 — Page Meta Descriptions

Report: `WK-WEB-T21-R01`, revision 1. October 6, 2026.
Child: `01a11244-b428-73c2-a870-621a495540b8`.
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6`.
Dispatch: `WK-WEB-T21-D01`, applied once.
Workflow: READY FOR REVIEW. Hub receipt/acceptance pending.

## Delivered

One description prop and tag in the shared layout, supplied by all four page
families. Home summarizes the practice and selected work; archive summarizes
its restoration, pottery and photography records. Overviews identify the
project-and-photographs destination; journals identify the TradeJournal.
Both reuse the approved project summary without dropping its uncertainty.
No new content schema, field, dependency, route or visible design was needed.

## Changed files

- `website/src/layouts/SiteLayout.astro`
- `website/src/pages/index.astro`
- `website/src/pages/work/[id].astro`
- `website/src/pages/tradejournals/index.astro`
- `website/src/pages/tradejournals/[id].astro`
- `website/tests/rendering.test.mjs`
- `website/README.md`
- This report

## Verification

- Test-first all-route check initially failed because the homepage had zero
  descriptions. After implementation, the full suite passes: 122 Node tests
  and 37 Python source/HTML tests. Log: `/tmp/task21-tests.log`.
- Existing fixture also checks quoted text and ampersands in metadata.
  Astro escapes attribute delimiters; angle brackets remain safely within
  the quoted attribute. The initial assertion incorrectly expected text-node
  escaping there and was corrected to match valid attribute serialization.
- Fresh `npm run check:website` passes: 20 pages, 60 files, 366 references.
  Log: `/tmp/task21-preview.log`.
- Independent Python HTMLParser inspection of all 20 generated pages confirms
  exactly one non-empty description each, no duplicate descriptions, and
  unchanged `noindex, nofollow` on every preview route.
- Reviewed all generated descriptions below against the existing summaries
  and page purposes. Current/future studio distinctions and qualified dates
  remain; no client, availability, coverage or ranking claims were introduced.
- Existing shared-frame tests cover navigation, disabled inquiry controls and
  titles/content behavior. Only head metadata changed in production templates;
  no new browser visual review was needed for this nonvisual change.
- README/report Markdown lint and `git diff --check` pass.

## Review boundary and checkout

`main` remains at `cedebf8`; implementation is uncommitted. No release build,
snapshot refresh, Git closeout, deployment or successor was performed.
`pilot.json` remains byte-identical, SHA-256:
`2efb1566680b93491b2f13b389d2ccb368be6e60392cef31bd3027095bdcd841`.
Observed content review state is `current`, zero changed keys: template code
is not fingerprinted by that content snapshot. This does not mean the new
metadata wording has received user acceptance or release approval.

The unrelated `PROJECT_MEMORY.md`, hub register/brief and requester-owned
request are preserved. Titles, navigation, visible content, source journals,
images, contact state and private business files were not edited.

## Generated descriptions for review

### `/`

Historic floors, interior woodwork, and architectural restoration. Project records and workshop studies from a craftsman's practice.

### `/tradejournals/agfa-isolette/`

TradeJournal: A compact body of square medium-format photographs uses a 1961 folding camera to study coastal structure, material, atmosphere, and the workshop.

### `/tradejournals/entry-restoration/`

TradeJournal: Two careful passes renewed the public threshold of the house while keeping its front door, transom, stair, balustrade, and original floor legible.

### `/tradejournals/guest-bath-dresser-vanity/`

TradeJournal: A compact old-house bath was brought back into service around an antique dresser adapted as a vessel-sink vanity.

### `/tradejournals/`

Selected project records from historic-home restoration, pottery, and photography: visible evidence and the decisions that led to it.

### `/tradejournals/la-ciotat/`

TradeJournal: Three photographs move between La Ciotat's working harbor and a narrow street, then return to the waterfront through a contrasting 35mm film scan.

### `/tradejournals/living-room-studio-restoration/`

TradeJournal: Original floors, exposed shiplap, and a repaired plank ceiling in the former living room being prepared as the future barre studio.

### `/tradejournals/master-bedroom-restoration/`

TradeJournal: Two distinct restoration passes kept the original floor, board walls and ceiling, tall windows, trim, and built-in cabinet at the center of the room.

### `/tradejournals/office-restoration/`

TradeJournal: A dedicated office in the 1894 residence, documented through its current room layout, trim, finishes, and continued use.

### `/tradejournals/returning-to-clay/`

TradeJournal: A return to wheel-thrown pottery connects current greenware studies to surviving wood-fired work from a Brookhaven apprenticeship three decades earlier.

### `/tradejournals/studio-office-restoration/`

TradeJournal: The current barre studio and Repair Shop home, including the decision to retain and refinish an original solid-wood door.

### `/work/agfa-isolette/`

Project overview and photographs: A compact body of square medium-format photographs uses a 1961 folding camera to study coastal structure, material, atmosphere, and the workshop.

### `/work/entry-restoration/`

Project overview and photographs: Two careful passes renewed the public threshold of the house while keeping its front door, transom, stair, balustrade, and original floor legible.

### `/work/guest-bath-dresser-vanity/`

Project overview and photographs: A compact old-house bath was brought back into service around an antique dresser adapted as a vessel-sink vanity.

### `/work/la-ciotat/`

Project overview and photographs: Three photographs move between La Ciotat's working harbor and a narrow street, then return to the waterfront through a contrasting 35mm film scan.

### `/work/living-room-studio-restoration/`

Project overview and photographs: Original floors, exposed shiplap, and a repaired plank ceiling in the former living room being prepared as the future barre studio.

### `/work/master-bedroom-restoration/`

Project overview and photographs: Two distinct restoration passes kept the original floor, board walls and ceiling, tall windows, trim, and built-in cabinet at the center of the room.

### `/work/office-restoration/`

Project overview and photographs: A dedicated office in the 1894 residence, documented through its current room layout, trim, finishes, and continued use.

### `/work/returning-to-clay/`

Project overview and photographs: A return to wheel-thrown pottery connects current greenware studies to surviving wood-fired work from a Brookhaven apprenticeship three decades earlier.

### `/work/studio-office-restoration/`

Project overview and photographs: The current barre studio and Repair Shop home, including the decision to retain and refinish an original solid-wood door.
