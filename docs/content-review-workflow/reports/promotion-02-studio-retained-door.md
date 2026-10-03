# Content Promotion 1 - Task 02 Studio Retained Door

- Report: `TJ-CP-T02-R01`, revision 1; October 3, 2026.
- Child: `01a103d7-2126-7733-b898-99e97195de7b`.
- Hub: `01a062b2-cd26-7552-a5f9-3996acac6392`.
- Approval: Shawn's "yes" to starting this bounded task in hub turn
  `01a103d6-c391-71f3-97ea-8e3b79ddafca`.
- Branch and HEAD: `codex/concept-b-homepage`,
  `e6f3571a878fe250e1cb1a6409860671b5490169` throughout this task.

## Candidate Result

The existing Current Barre Studio page now gives the retained solid-wood door
its own short craft account. It explains the decision to preserve the original
door, stripping to bare wood, the documented charred appearance, and hand
application of finish. It preserves the source notes' water-based polyurethane
and custom Dutch-oil sequence without inventing product details or ratios.

All five established gallery photographs remain in their original order. Two
new details follow them:

1. [Flickr `52704581571`](https://www.flickr.com/photos/boocher/52704581571/in/set-72177720306207693/) — brush applying finish to the dark, textured surface. The image includes a gloved hand and clothed torso, but no visible face or identifying feature. It does not show the earlier torch pass.
2. [Flickr `52704058327`](https://www.flickr.com/photos/boocher/52704058327/in/set-72177720306207693/) — close checked-char texture beside a lighter wood edge, distinct from the active brush detail.

Both selected 1024-pixel-class Flickr images were inspected directly and saved
as local selected assets. The site records preserve their source URLs, album
identity, dimensions and descriptive alternatives. The person-visible torch
frame `52704581761` was neither downloaded nor included in the candidate.

The source journal's `2022` heading conflicts with mostly February 2023 Flickr
labels, so the site does not claim a dated sequence. The stripped door is shown
installed before treatment; no final installation of the charred door is
claimed. The current studio remains distinct from the future living-room
studio and the dedicated Office. The treatment is presented as an appearance
and material-reclamation choice, not traditional yakisugi or fire resistance.

## Changed Files And Ownership

Child-created or edited files:

- `website/content/projects/studio-office-restoration.json`
- `website/content/stories/studio-office-restoration.md`
- `website/content/media/flickr-52704581571.json`
- `website/content/media/flickr-52704058327.json`
- `site_example/assets/flickr/studio-office/06.jpg`
- `site_example/assets/flickr/studio-office/07.jpg`
- `website/README.md`
- `website/tests/build.test.mjs`
- `website/tests/studio-content.test.mjs`
- `website/tests/rendering.test.mjs`
- this report.

The shared checkout also contains the hub-owned modified
`docs/content-review-workflow/task-register.md` and untracked
`docs/content-review-workflow/promotion-02-studio-retained-door.md`; this child
did not edit them. No homepage, Office, other project, source journal,
inventory, dependency, reviewed release fingerprint or source-platform record
was changed by this child.

## Verification And Return

- Repository Python suite: 84 passed.
- Markdown lint: 136 files, zero issues before this report; final lint and
  whitespace recheck follow report creation.
- Site-evidence manifest current; site search tests: five Python and five
  JavaScript passed.
- Website suite: 121 Node and 37 Python source/HTML tests passed.
- Preview build and output checker: 18 pages, 55 files, 327 references;
  selected image assets present.
- Browser review: existing project and TradeJournal routes render the updated
  content. The two new images, captions and Flickr source links appear in the
  project gallery. Desktop pairing and 390-pixel single-column reading were
  inspected; the narrow journal had `scrollWidth` 390 at width 390.
- The gallery test initially failed because its caption comparison omitted
  apostrophe escaping. The test now distinguishes text escaping from
  double-quoted attribute escaping; the focused test and full suite passed.
- `git diff --check` passed. No stage, commit, fetch, push, release-snapshot
  update, deployment, or successor task was performed.

Candidate is ready for Shawn's content review. Report delivery to the hub,
content acceptance, Git closeout, release approval and publication are separate
later decisions. The current local preview remains a candidate with its review
notice and `noindex` metadata.
