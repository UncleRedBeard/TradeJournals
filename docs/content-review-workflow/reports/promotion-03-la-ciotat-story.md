# Content Promotion 1 - Task 03 La Ciotat Story

- Report: `TJ-CP-T03-R01`, revision 1; October 3, 2026.
- Child: `01a10405-54e9-7452-95ac-e4df7f49da44`.
- Hub: `01a062b2-cd26-7552-a5f9-3996acac6392`.
- Dispatch: `TJ-CP-T03-D01`.
- Branch and HEAD: `codex/concept-b-homepage`,
  `849fbce4f33ecd6c0ac6b2a284dd44ab89885e53` throughout this task.

## Candidate Result

La Ciotat now has a compact Lens project at `/work/la-ciotat/` and a
source-cited story at `/tradejournals/la-ciotat/`. The existing archive lists
the project, and searching for `La Ciotat` returns its entry. The homepage's
featured and workshop selections are unchanged. The story is place-centered,
moving from harbor to street and back to the harbor as an editorial sequence,
not a claimed route or capture chronology.

Exactly three accepted photographs from recorded 118-photo Flickr album
`72157626174678654` were inspected visually and saved as selected local assets:

1. [Harbor `5489412430`](https://www.flickr.com/photos/boocher/5489412430/in/album-72157626174678654/) — boat bows, moored boats, reflections, and waterfront buildings; 1024 × 768 pixels.
2. [Street `5488818887`](https://www.flickr.com/photos/boocher/5488818887/in/album-72157626174678654/) — shuttered shopfronts, signs, paving, and three receding pedestrians; 1024 × 768 pixels.
3. [Film scan `52834975513`](https://www.flickr.com/photos/boocher/52834975513/in/album-72157626174678654/) — overlapping boats, waterfront, reflections, and a broad dark band at left; 1024 × 691 pixels.

Media records preserve the source URLs, album key, actual dimensions, and
descriptive alternatives. The two digital photo pages have February 6, 2011
taken labels in the accepted review. The `R1-08767-0000` title identifies a
35mm film scan, but its camera, film stock, exposure date, and the technical
cause of its visible bands and softness are not established. The site does
not apply one camera, process, or date to all three images.

## Changed Files And Ownership

Child-created or edited files:

- `website/content/projects/la-ciotat.json`
- `website/content/stories/la-ciotat.md`
- `website/content/media/flickr-5489412430.json`
- `website/content/media/flickr-5488818887.json`
- `website/content/media/flickr-52834975513.json`
- `site_example/assets/flickr/la-ciotat/01.jpg`
- `site_example/assets/flickr/la-ciotat/02.jpg`
- `site_example/assets/flickr/la-ciotat/03.jpg`
- `website/tests/build.test.mjs`
- `website/README.md`
- this report.

The shared checkout already had parent-owned changes to
`website/content/reviews/pilot.json`,
`website/docs/pilot-editorial-review.md`, and
`docs/content-review-workflow/task-register.md`, plus the untracked
`docs/content-review-workflow/promotion-03-la-ciotat-story.md` brief. This
child preserved them. It made no source journal, album inventory, homepage,
other project, dependency, review-fingerprint, or release-approval edits.

## Verification And Return

- Repository Python suite: 84 passed.
- Markdown lint: 140 files, zero issues after this report.
- Site-evidence manifest current; site search suite: five Python and five
  JavaScript tests passed (count label corrected during hub closeout).
- Website suite: 121 Node and 37 Python tests passed.
- Preview build and output checker: 20 pages, 60 files, 363 references; all
  three selected image assets and both new routes present.
- Browser review: project and TradeJournal routes rendered with captions,
  evidence boundary, and Flickr source links. All three images loaded at their
  recorded dimensions. The archive listed La Ciotat, and `La Ciotat` search
  returned one result. Desktop and 390-pixel mobile layouts were inspected;
  no horizontal overflow occurred. The film scan and its caption were
  inspected on mobile.
- `git diff --check` passed after this report.
- No stage, commit, fetch, push, reviewed-snapshot refresh, release build,
  deployment, or successor task was performed.

The candidate is ready for Shawn's content review. The local preview retains
its review notice and `noindex` metadata. Sending this report to the hub,
accepting the content, Git closeout, release approval, and publication remain
separate decisions.
