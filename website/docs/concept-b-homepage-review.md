# Concept B Homepage Candidate

Parent closeout update, October 2, 2026: the three stale-review test
assumptions were corrected, and the complete website suite passed 118 Node and
37 Python tests. Shawn approved the homepage order and two changed journal
sources for the exact reviewed snapshot. The guarded release build now passes;
the [release review](pilot-editorial-review.md) records the scope and checks.
The site-wide visual update remains pending. The status below records the
earlier child handoff before this closeout.

## Scope And Status

Shawn approved starting the homepage-first implementation on October 2, 2026.
This candidate adapts the Stitch Craftsman's Atelier direction into Astro.
Shawn accepted the implemented Concept B homepage on October 2, 2026 and
explicitly approved extending the style across the entire site. The homepage
child task is complete; the remaining site update returns to the parent.

- Charcoal hero, Cormorant Garamond headings, parchment project cards, alternating
  desktop photographs, and a dark workshop section.
- Documented Projects: Living Room Restoration — Future Barre Studio, Entry and
  Stair Restoration, Guest Bath and Dresser Vanity, Master Bedroom Restoration.
- Existing selected photographs, approved project summaries, and working links
  to the existing project and TradeJournal pages.
- Full portrait photographs in matte frames on desktop; the lead room receives
  a taller frame on mobile so its floor and ceiling remain visible.
- Responsive navigation, keyboard focus indicators, image alternative text,
  and disabled `Email us — coming soon` controls.

Current and future barre rooms remain distinct. The project records, source
journals, galleries, and release review fingerprints have not been changed.
The shared layout gained optional header/footer slots; other pages retain their
existing appearance. No additional runtime JavaScript or npm dependency was
introduced.

## Verification

- Candidate build and independent output check: 18 pages, 52 files, 236 checked
  references.
- Python website checks: 37 passed.
- Complete Node suite: 115 passed, three pre-existing review-state failures.
- Markdown lint: 91 files, zero errors. `git diff --check` passed.
- Four focused rendering and synthetic-maintenance tests passed, covering card
  links and order, disabled inquiries, editable presentation, and room identity.
- Browser review: 320, 390, 768, 1024, and 1280-pixel widths fit without horizontal
  document overflow. Desktop and phone layouts, all six loaded photographs,
  section navigation, and the Living Room project destination were inspected.
- The complete Node suite retains three failures found before implementation:
  tests in `build.test.mjs`, `office-content.test.mjs`, and `rendering.test.mjs`
  assume the earlier release snapshot is current. The baseline was already stale
  after changes to the current Studio and Office source journals. This candidate
  also changes the homepage record. The release fingerprints remain untouched.

## Font Provenance

Cormorant Garamond normal and italic Latin WOFF2 files come from Google Fonts.
They are embedded locally through Vite's inline asset support. The full SIL Open
Font License is retained in `src/styles/fonts/OFL.txt` and in the homepage's inert
`font-license` template, so it accompanies the built font data.

- [Google Fonts family source](https://github.com/google/fonts/tree/main/ofl/cormorantgaramond)
- [Cormorant upstream](https://github.com/CatharsisFonts/Cormorant)

## Parent Handoff

Report ID: `concept-b-homepage-20261002-r1`.

- Child: `01a0fdbf-9367-7c03-aaca-2636ec924012`.
- Parent: `01a0fce4-a907-7981-a469-b3b101199a36`.
- Workspace: `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/TradeJournals`.
- Branch: `codex/concept-b-homepage`; implementation is uncommitted. No push,
  release snapshot refresh, or deployment was performed.
- Local candidate: `http://127.0.0.1:8134/`, served from `.preview-dist`.
  Verify the listener before assuming it remains available.

Exact approval in the child task:

> concept b approved. and an entire site update is approved as well. handoff
> back to the parent then update the title to completed

The parent should record the accepted homepage and carry forward the approved
site-wide scope: shared header/footer, project pages and galleries, TradeJournal
reading pages, and archive/search cards and controls. Preserve existing content,
source links, room identities, search behavior, and disabled contact behavior.
Apply the established typography, charcoal/brass/parchment palette, spacing, and
card treatments with suitable long-form reading layouts. Verify desktop/mobile,
keyboard use, links, search, and candidate output. No repeat design approval is
needed to begin that scope.

Refresh repository and concurrent-task state before further edits because the
child and parent share the same checkout. Homepage styling currently lives in
`src/styles/atelier.css`, `src/components/AtelierProjectCard.astro`, and
`src/components/AtelierContact.astro`; `SiteLayout.astro` offers header/footer
slots. Broader adoption will require deliberate reuse beyond the current
homepage body class. Retain the bundled font license when moving font imports.

Release snapshot approval and deployment remain separate steps. The three
pre-existing snapshot test failures above are explicitly handed back for
reconciliation; the suite must not be reported as fully green.
