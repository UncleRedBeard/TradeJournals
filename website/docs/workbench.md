# Website Editing With TradeJournals Workbench

TradeJournals Workbench is a private editor for the structured records that feed
the Astro website. It supports several projects in one change set, explicit room
occupancy, album reassignment, story editing, photo ordering, and isolated
preview. The archive repository remains the authority for validation and public
content.

## Everyday Flow

1. Start the local Workbench with its private configuration and open
   **Website**.
2. Choose a canonical project. Add related projects to the same draft when one
   correction must update shared references.
3. Edit the project fields, story, occupancy, albums, and selected photos.
   Project ID replacement and album movement are explicit operations.
4. **Save draft**. This creates an immutable private revision in the Workbench
   store. It does not change the archive repository.
5. **Build preview**. Open and inspect the private preview for that exact saved
   revision and digest.
6. Use **Publish update** only after the exact preview has separate content
   approval. The operation applies that revision to local canonical source files
   and rebuilds the local candidate preview.

The browser remembers only the active draft identifier. The saved change set
reopens from private storage after a browser or Workbench restart. Unsaved edits
remain browser state; use **Discard changes** or **Reopen saved revision** only
when replacing them is intentional.

## Occupancy Is An Editorial Fact

Every room whose use can change carries an explicit occupancy state and label.
Choose `current`, `future`, or `former` only from Shawn's confirmation. Renovation
progress, album names, photo dates, and a finished-looking room do not establish
occupancy. Keep a current room current and a future room future until Shawn
explicitly confirms the move.

Album ownership is exclusive across projects. Reassigning an album moves its
selected evidence; it does not automatically move historical claims, dates, or
room narratives. Review those claims separately.

## What Each Stage Means

| Stage | Location | Effect |
| --- | --- | --- |
| Browser edits | Browser memory | No durable or public change |
| Private draft | Owner-only Workbench store | Immutable saved revision and proposal |
| Private preview | Owner-only isolated build | Inspectable output for one revision and digest |
| Canonical source | `website/content/` and approved assets | Local public-content candidate after **Publish update** |
| Reviewed snapshot | `website/content/reviews/pilot.json` | Separate editorial release decision |
| Local candidate preview | Canonical Astro build output | Release candidate built from canonical source |
| Hosted output | Future hosting provider | Separate deployment decision |

Saving or previewing never changes canonical source, review state, Git, or a
hosted site. **Publish update** does not deploy, approve a release, edit journals
or inventories, commit, or push. It applies only the exact previewed revision to
the local website source and then attempts the ordinary candidate build.

## Conflicts And Recovery

Each draft records fingerprints for the canonical files it touches. An external
edit to an unrelated record does not invalidate the draft. An external edit to a
touched project, story, home record, service record, navigation record, or media
record makes the draft stale. Workbench keeps the saved revision and refuses to
preview or publish it until the change is reconciled and saved against current
source.

The website lifecycle uses these visible states:

- `draft`: a saved private revision that can be edited;
- `previewed`: the current revision and digest have a successful private preview;
- `publishing`: a durable publication manifest exists and application is in
  progress;
- `recovery`: the source result is uncertain and requires inspection; and
- `published`: the exact source application was verified. The local candidate
  preview may still need a separate rebuild if that build failed.

Mutation requests have durable receipts. If the browser loses a response, check
the receipt before retrying. A retry with the same request identifier and payload
returns the recorded result. A publication in `recovery` is never blindly
replayed. Restart inspection marks it published only when every expected after
digest is already present; otherwise use the explicit recovery path.

## Offline Website-Store Upgrade

Normal startup never upgrades an older private store. Stop every Companion
server that could own the store, retain the generated verified backup, and run:

```sh
node dashboard/start.mjs --upgrade-website --server-stopped \
  --config /absolute/private/companion-config.json
```

Restart normally after the command reports schema version 3. Unknown, damaged,
live-owned, or ambiguously owned stores are refused without replacement.

## Structured-File Editing Remains Available

The browser editor and direct file editing use the same archive-owned schemas.
Maintainers may continue to edit:

- `website/content/projects/*.json` and matching
  `website/content/stories/*.md`;
- `website/content/home.json`, `website/content/services/*.json`, and
  `website/content/site.json` for references and navigation; and
- `website/content/media/*.json` for public media metadata.

Run the website tests and candidate build after structured-file changes. Do not
edit the same records in files while a Workbench draft based on them is active;
the safe stale check will require the private draft to be reconciled.

## Photos And Source Evidence

Photos Inbox remains the private intake boundary. Only ready photos with a
complete public media record can enter a website change set. Public promotion is
additive and content-addressed; originals remain untouched. Captions,
alternative text, role, focal point, source URL, album key, and photo order stay
explicit.

Google Photos is not an account integration. Download only selected evidence and
retain individual source URLs. If a downloaded JPEG contains an MPF auxiliary
layer, export an ordinary JPEG copy before intake and keep the original. Failed
intake outcomes remain private and never become website assets.

## Verification

The public Astro build does not read the private store or managed media. Use the
commands in `website/README.md` for tests, candidate builds, and output checks.
Before Git closeout, inspect the actual source diff, verify that private
configuration and storage did not enter either repository, and confirm the
review record still reflects the intended editorial state.
