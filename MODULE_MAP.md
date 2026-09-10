# Module Map And Working Guides

Use this map to choose a focused part of TradeJournals, find its authoritative
records, and identify the shared material an update may affect. The modules are
working boundaries within the existing repository. Craft history, material
judgment, and visual evidence remain the purpose of the archive.

## Choose A Work Area

| Work Area | Owns | Useful Unit Of Work | Working Guide |
| --- | --- | --- | --- |
| Residence | Historic-home restoration journals | One room, system, or intervention | [Residence](01_the_residence_1894/README.md#working-guide) |
| Forge and shop | Workshop, tool-system, and material-reuse journals | One shop project or focused part of its record | [Forge and shop](02_the_forge_and_shop/README.md#working-guide) |
| Machines | Mechanical restoration and machine-shop journals | One machine, system, or shop-context record | [Machines](03_the_machines/README.md#working-guide) |
| Materials and alchemy | Pottery, firing, and material-study journals | One study, batch, or bounded journal section | [Materials and alchemy](04_materials_and_alchemy/README.md#working-guide) |
| The lens | Photography narratives and source catalogs | One camera, collection, or platform record | [The lens](05_the_lens/README.md#working-guide) |
| Evidence maintenance | Media importers, album inventories, and source provenance | One source review or importer behavior | [Media maintenance](scripts/README.md#working-guide) |
| Portfolio publishing | Curated site catalog and offline evidence builder | One journal's portfolio selection | [Publishing](site_example/README.md#portfolio-publishing) |
| Website and search | Page layout, styles, browser behavior, and retrieval | One presentation or search behavior | [Website and search](site_example/README.md#website-and-search) |

The pillar READMEs explain how to work in an area. Their `trade_journals/README.md`
files index the journals. Start with an existing journal or section before
creating another record for the same project.

## Record Ownership

| Information | Authoritative Record | How Other Areas Use It |
| --- | --- | --- |
| Project facts, craft decisions, interpretation, current stage, and unresolved evidence | The relevant Markdown journal | Link to the journal; base portfolio claims on its supported record |
| Album identities, journal routing, source counts, and verification dates | [Flickr inventory](FLICKR_PUBLIC_ALBUMS.md) or [Google Photos inventory](GOOGLE_PHOTOS_ALBUMS.md) | Reference the exact album block; retain its recorded date and source limitations |
| Notebook provenance and page assignments | [Scanned sketchbook guide](source_materials/scanned_sketchbooks/README.md) and its source scans | Link to the relevant pages from each journal |
| Area navigation and working procedure | Pillar, journal-index, and shared-area READMEs | Direct readers to the authoritative record instead of repeating its changing status |
| Portfolio-wide direction, maturity overview, and priorities | [Project memory](PROJECT_MEMORY.md) | Treat summaries as dated checkpoints; consult the journal for current project detail |
| Published selection, search summary, tags, evidence labels, and representative search images | [Site evidence source](site_example/evidence-source.json) | Curate from the journal and inventories; this is a selected presentation of the archive |
| Page narrative, gallery links, section anchors, and fallback counts | [Site page](site_example/index.html) | Keep the relevant section consistent with the curated selection and inventory |
| Browser evidence data | [Generated manifest](site_example/evidence-manifest.js) | Rebuild from its inputs; do not maintain a separate hand-edited copy |

Existing inventories and overview documents may contain project summaries. Read
those against the journal before reusing a claim. Keep new detailed status and
next-action notes in the journal; use the overview for cross-project priorities.

## Shared Dependencies

The five craft areas share sources and publication infrastructure:

- Album inventories route evidence to journals across the pillars. An album's
  platform identity remains distinct even when another platform holds the same
  photographs.
- The intact house sketchbook supports several residence journals and the
  Vespa. Each journal references its pages rather than copying the master scan.
- Shop practice and photography can support another craft journal without
  becoming the owner of that project's conclusions.
- The website presents selected journals. A journal can be maintained without
  being added to that selection.

The publication path includes human curation:

```text
Journal + source evidence -> reviewed portfolio selection
Selection + inventories + page anchors/fallback counts -> evidence builder
Evidence builder -> generated manifest -> website and search
```

The builder checks journal paths and other structural relationships. It does not
read journal prose to refresh a summary, judge a craft claim, or confirm that a
project is finished. Those comparisons require editorial review.

## Scope An Update

1. Name one work area and the journal, section, album, or behavior being changed.
   Read its working guide and the [journal standards](README.md#journal-philosophy).
2. Identify the files to edit and the records to consult. Resolve the exact
   source album and any shared scan pages before changing evidence references.
3. Keep facts and interpretation in their owning record. For media intake, use
   the relevant preview or dry-run workflow and review the proposed result
   before authorizing an inventory or journal write.
4. Check downstream impact. A navigation change may affect a journal index; a
   revised published claim, image selection, or album count may affect the site.
   Follow the [publishing guide](site_example/README.md#portfolio-publishing)
   when that presentation is part of the approved scope.
5. Run the checks below and inspect the exact diff. Confirm that curated prose,
   source identities, uncertainty, and unrelated projects were preserved.

For example, a pottery practice note can be a journal-only edit. A new portfolio
checkpoint based on that note also needs a reviewed site summary and page
section. A Flickr count reconciliation needs review of the album's journal
references and any published fallback count.

## Existing Validation

Run commands from the repository root. These are the existing checks; the map
does not add a new verification command or change their behavior.

| Change | Checks And Review |
| --- | --- |
| Working guides, indexes, or journal prose | `npm run lint:md`; `git diff --check`; follow changed local links and anchors; review claims against their source |
| An indexed journal's facts or evidence | The prose checks, plus compare the matching catalog entry and page section with the journal; automated checks cannot detect stale interpretation |
| Importer code or importer tests | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`; review documented commands and preservation behavior |
| Inventory counts, site selection, page anchors, or representative assets | `npm run check:site-evidence`; `npm run test:site`; inspect the affected page section, source links, and search result |
| Website layout, styling, or search behavior | `npm run test:site`; `npm run check:site-evidence`; inspect the changed behavior in the browser at relevant screen sizes |

Use all applicable rows for a change that crosses boundaries. The full existing
pre-commit sequence is in the [journal-to-site workflow](PROJECT_MEMORY.md#recommended-journal-to-site-workflow).
`npm run test:site` covers the evidence builder and search tests; importer tests
remain part of the separate Python command. These checks use repository data
and do not verify current external album visibility or counts.

## Repository Boundaries

TradeJournals owns the craft archive and portfolio source. Private business
strategy, finances, client operations, and transition planning belong in the
separate `restoration-business-operations` repository. Capture-product planning
and Companion experiments belong in `tradejournals-companion`.

Keep shared archive sources here and reference them from the appropriate
journals. Working on a module does not authorize moving content between
repositories, publishing private material, or committing and pushing changes.
