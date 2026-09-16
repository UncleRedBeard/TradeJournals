# Task 03 — Astro Pages

**Status:** COMPLETE — hub direct recovery
**Branch:** `codex/website-updates`
**Scope:** Astro pilot pages only; no editorial approval, publication, commit, or push

## Delivered

- A static Astro build with four pilot routes: home, Office project, TradeJournals
  index, and Office journal record; `/search.json` supplies the optional archive
  search.
- One shared site layout and reusable hero, service, project-card, gallery,
  evidence, archive-search, and contact-invitation components.
- A staged public build that copies only selected media and generated candidate
  records. It preserves each original Flickr source link and does not expose a
  local archive path.
- A Markdown tree policy that rejects raw HTML, images, and unsafe links before
  story rendering.
- A server-rendered archive index whose JavaScript search enhances the page and
  leaves the project list available if search data cannot load.
- Preview-only candidate labeling. The release command refuses unreviewed
  candidate content.

## Verification

- `npm --prefix website test` — 50 passing tests.
- `npm run check:site-evidence` — manifest current.
- `npm run test:site` — 10 passing existing site-evidence/search tests.
- `npm --prefix website run build` — intentionally rejected with
  `Release requires current reviewed content; state is candidate`.
- Browser review at `http://127.0.0.1:8126/` confirmed the home page, Office
  gallery with its ten selected images and original source links, archive search
  for `door`, and a one-column mobile project view. No browser console warnings
  or errors were observed.

## Boundary and follow-up

The Office record and photographs remain candidate review material. No contact
form, live analytics, deployment configuration, editorial promotion, commit, or
push was performed. Task 04 remains separate and has not started.
