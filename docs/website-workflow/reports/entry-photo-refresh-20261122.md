# Entry and Stair Photo Refresh

November 22, 2026. Direct follow-up in the website updates hub; no new child
chat. Shawn authorized the reviewed recommendation with “cool...make it
happen cap'n”. Status: COMPLETE — accepted November 22, 2026.

Shawn accepted the exact preview with “looks great...reviewed and approved.
git er done”. This authorizes the release snapshot refresh and scoped Git
closeout to established `origin/main`, alongside the visual acceptance.

## Selection

- Lead: [front door and staircase](https://www.flickr.com/photos/boocher/55667855085/in/album-72177720334259189/).
- Second: [floor toward the studio](https://www.flickr.com/photos/boocher/55667552918/in/album-72177720334259189/).
- Retain the existing condition and process photographs, in that order.

Flickr displayed November 16, 2026 as the capture date for both images and
November 22 as the upload date. Both local JPEGs are the Flickr-served
1536 × 2048 versions, exported through the authenticated browser without
image editing. Stable media records retain the individual source URLs and
the established Home Reno - Entry album key. The source album currently shows
96 items; its older inventory count remains a dated source checkpoint.

The gallery and search selection now contain four photographs. The homepage
Entry card follows the new lead automatically and preserves its full portrait
composition. The home record's legacy hero selection also follows the new
lead; the current homepage template uses a text hero, not that photograph.

Captions and Entry stage labels identify the new images as November 2026
finished-room views. The 2024–25 restoration timeline is unchanged. The old
lead asset/record is retained, and the journal and source inventory are
unchanged. There are no new layout, viewer, route or dependency changes.

## Review boundary

The reviewed snapshot is refreshed for the accepted four-photo gallery and
new lead. No public deployment or inquiry activation is included.

## Verification

- 125 Node tests and 37 Python source/HTML tests pass. Existing assertions were
  updated for the new four-photo selection and home media identity.
- Preview build and independent output checks pass: 20 pages, 64 files,
  378 references. Markdown lint and `git diff --check` pass.
- Desktop browser: all four gallery images load with their recorded dimensions;
  both new photographs open with matching captions and close successfully.
- Mobile at 390 × 844: document width remains 390 pixels, with no horizontal
  overflow. The homepage card uses the new lead with `object-fit: contain` on
  desktop and mobile. The temporary viewport override was reset.
- Reviewed image bytes are preserved in the local assets. No runtime Flickr
  request is needed to display the new photographs.

[Review the Entry gallery](http://127.0.0.1:8145/work/entry-restoration/#project-photographs).
Loopback preview serves `website/.preview-dist`, exec session `48886`; left
running for Shawn's review. Screenshot: `/tmp/entry-refresh-lead.jpg`.

## Accepted release and Git closeout

November 22 validation under pinned Node 24.21.0 passes: 125 Node tests,
37 Python source/HTML tests, repository Markdown lint and whitespace checks.
Preview and guarded release each validate 20 pages, 64 files and 378 references.
Both outputs preserve the approved four-photo order, homepage lead, exact new
image bytes and expected robots state. The nine project galleries now contain
41 photographs in total.

The reviewed snapshot is current with zero changed keys, covering 64 records
and 59 sources. Changed fingerprints are confined to the Entry project, home
media selection and the replaced/added image selections. Snapshot SHA-256:
`d379fc062d03ca4b476f9ce296b008590deb0b32c68de32aa9ad138cd9f9876c`.

Closeout destination is established `origin/main` at
`git@github.com:UncleRedBeard/TradeJournals.git`, starting from synchronized
`92f57e9`. Final commit identity and post-push synchronization are verified in
the hub response. Public deployment remains separate.
