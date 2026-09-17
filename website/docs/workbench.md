# Website Editing With TradeJournals Workbench

The private Workbench edits the same public JSON records used by Astro and by
file editing. This first version supports the Studio gallery only. Project prose
and other projects remain editable in their existing structured files.

## Everyday Use

1. Run **Open TradeJournals Workbench.command** from
   `~/Library/Application Support/TradeJournals Dashboard/`.
2. In **Photos Inbox**, choose local photographs, inspect the previews, and use
   **Review selected photos → Stage selected photos**. Nothing is public yet.
3. Open **Website**. Studio opens directly. Select staged or previously saved
   photographs. Keep an individual Studio Google Photos source link for each
   newly selected photo.
4. Write the caption and alternative text, choose its role, and move the lead
   photo to the top. Removing a selection retains its saved asset.
5. Confirm copying new selections into the website candidate, then **Save
   candidate**. This copies prepared JPEGs into `website/assets/workbench/`, adds
   media records, and updates Studio's gallery and search image order.
6. **Build preview → Open website preview**. Check the project, homepage card,
   and archive. Saving and previewing do not approve, publish, commit, or deploy.

A newly saved candidate survives a browser or Workbench restart. Use **Reopen
saved candidate** for changes made in files. If a save reports changed records,
keep any text you need, reload the browser to discard its stale copy, and reopen.
Do not edit the same candidate simultaneously in the browser and files.

## Google Photos Intake

There is no Google Photos account integration. Download only the chosen photos
from the shared Studio album and retain their individual photo URLs. The three
Task 06 images are inspected Google display renditions, 1012–1080 pixels wide,
not original camera files. Public copies are normalized JPEG previews; original
source images are untouched. Higher-resolution replacements can be selected later.

Some Google JPEG downloads include an MPF auxiliary image layer. The existing
private importer deliberately refuses these multi-image files. Export an ordinary
JPEG copy with Preview, or use `sips -s format jpeg input.jpg --out copy.jpg`,
then import the copy. Keep the original download. Failed intake outcomes remain
visible; they do not become public website assets.

## Implementation And Configuration

- Companion checkout: `../tradejournals-companion`, branch
  `codex/website-workbench`; Website HTTP adapter and small standalone editor.
- Archive branch: `codex/website-updates`; `website/lib/workbench.mjs` validates
  and writes public records. Astro does not import this authoring module.
- Private launcher config: `allowWebsiteWrites: true`; `allowJournalWrites`
  remains false. Website editing defaults off in other configurations.
- Workbench listens only on `127.0.0.1:8125`; preview uses
  `127.0.0.1:8126` after building. Optional `websitePreviewPort` changes the latter.
- An occupied preview port produces an error; the Workbench does not stop another
  process. Its preview listener stops when the Workbench shuts down.
- The old **Start TradeJournals Dashboard.command** forwards to the new launcher.
  The private storage folder retains its old name for compatibility.

Only ready photos can be promoted. A same-origin request token, candidate-only
state, revision check, and schema validation protect each save. Content-addressed
assets are additive; the project record is replaced atomically. An interrupted
save can leave an unselected public asset; inspect the diff before closeout.
Automatic cleanup is intentionally absent.

The public build works without a running Workbench and never reads its private
SQLite store or managed media. Run the existing commands in `website/README.md`
for file-based preview, tests, and output validation. Review state remains
`candidate` until Shawn explicitly approves a complete reviewed snapshot.
