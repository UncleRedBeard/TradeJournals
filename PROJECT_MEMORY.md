# Project Memory: TradeJournals Portfolio Direction

Last refreshed: 2026-09-03

TradeJournals is a craftsman-first trade journal, evidence archive, and portfolio
source. Its purpose is to make physical restoration skill, preservation judgment,
material knowledge, and process transparency visible. Markdown, Git, import
scripts, and the website are supporting infrastructure; they should not become
the client-facing story.

## Purpose And Boundaries

The portfolio should help historic homeowners, preservation-minded clients, and
collaborators understand the author as a serious craftsperson who can diagnose
messy conditions, respect original fabric, choose compatible materials, explain
tradeoffs, and show evidence for the result.

TradeJournals owns craft history, process decisions, source references, and
public-facing portfolio material. Private business strategy, finances, legal and
administrative planning, lead development, and career-transition decisions belong
in the separate private `restoration-business-operations` repository.

Real credentials, private media, local databases, machine-specific paths, and
other sensitive working data do not belong in this repository.

## Portfolio Pillars And Current Maturity

- `01_the_residence_1894`: seven journals covering historic-home restoration.
  This is the broadest portfolio area. The ballet studio is near completion, but
  its durable representative-image identifiers and final room-ready evidence are
  still pending.
- `02_the_forge_and_shop`: one journal documenting the working shop, material
  reuse, tool systems, utilities, and project staging. The evidence base is
  strong, but the narrative breadth remains comparatively narrow.
- `03_the_machines`: five journals covering vintage scooters, motorcycles, and
  mechanical restoration. The 1964 Vespa is the most developed case study and
  includes notebook, condition, repair, electrical, and Flickr evidence.
- `04_materials_and_alchemy`: one deep, active pottery journal centered on the
  return to clay, material tests, firing, formal critique, and a deliberate
  apprenticeship practice.
- `05_the_lens`: thirteen journals spanning film photography, camera-specific
  archives, and visual documentation. Coverage is broad, but several entries are
  source catalogs rather than complete craft narratives.

The strongest journals explain why a choice was made and what the evidence
proves. Album coverage alone does not make a journal portfolio-ready.

## Evidence Sources And Rules

Markdown journals are the durable source of truth. Organize them by project,
trade, system, or skill rather than treating the archive as a bare chronology.

Keep Flickr, Google Photos, Lomography, and scanned source material distinct:

- Flickr is the primary public, high-resolution evidence archive. The tracked
  inventory records 39 public albums, with 32 mapped into TradeJournals and seven
  intentionally excluded. Its recorded check date is 2026-08-07, so those counts
  are a repository checkpoint rather than proof of current external state.
- Google Photos shared URLs preserve album provenance, but durable image-level
  evidence should come from a project manifest or local export. Two albums are
  tracked, and neither yet has a complete durable representative-image set. The
  studio is the priority; pottery uses Flickr as its primary public evidence.
- Lomography records remain separate from related Flickr albums even when the
  photographs overlap.
- Scanned sketchbooks and handwritten notes provide provenance and decision
  context. They should support the journal narrative rather than be presented as
  unexplained artifacts.

Do not infer a restoration stage, material, date, or outcome from an image alone.
Preserve uncertainty when the surrounding record does not establish the fact.

## Implemented Functionality

### Media Maintenance

- `scripts/import_flickr_album.py` supports public album import, directory
  discovery, inventory generation, known-album count reconciliation, bounded
  metadata preview, and journal merging.
- `scripts/import_google_photos_album.py` records shared-album sources and builds
  image-level evidence from manifests or local exports.
- Importers deduplicate stable media identities, redact Flickr credentials from
  failures, keep public-read behavior separate from private access, and fail
  closed when a proposed change could overwrite curated Markdown.
- Dry-run and metadata-preview modes are the normal first step. Inventory or
  journal writes require review of the proposed result.

### Website Prototype

`site_example/` is a working local static portfolio prototype, not merely a
future concept. It includes:

- a five-pillar preservation narrative
- representative local images linked to original sources
- project evidence cards with stage, date, album, and source information
- an offline generated evidence manifest
- an "Ask the journals" keyword-ranking search across thirteen indexed entries

The search is deterministic local retrieval, not a semantic or conversational AI
assistant. The site has no repository-managed hosting or deployment workflow yet.

`scripts/build_site_evidence.py` builds the checked-in browser manifest from
`site_example/evidence-source.json` and the tracked media inventories. It
validates journal paths, representative-image paths, page anchors, album
identities, counts, and human-readable fallback text without credentials or live
network calls.

## Journal Standard

Each substantive journal should make the hidden work legible:

- the original challenge or constraint
- historic, mechanical, or material context
- craftsmanship execution and tools
- tradeoffs avoided or accepted
- dated work entries
- representative visual evidence
- what each selected image proves
- current stage, unresolved questions, and evidence still needed

Prefer three to five strong representative images for a project presentation.
Select before, difficult-middle, intervention-detail, and finished-state evidence
where the record supports those stages.

## Recommended Journal-To-Site Workflow

1. Capture photographs and brief field notes while the work is happening. Record
   the constraint, action, material, reason, result, and remaining uncertainty.
2. Classify the source platform and target pillar. Keep different media platforms
   and unrelated projects separate.
3. Run the relevant importer in `--dry-run` or bounded metadata-preview mode.
   Review the proposed output before permitting a journal or inventory write.
4. Curate one journal at a time. Add interpretation, material judgment, tradeoffs,
   and precise evidence labels rather than bulk album links alone.
5. Select representative images and update `site_example/evidence-source.json`
   when the journal is ready for the portfolio surface.
6. Run `npm run build:site-evidence`, inspect the relevant site section and search
   result, and verify the complete scoped change.
7. Before committing, run:

   ```sh
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
   npm run lint:md
   npm run check:site-evidence
   npm run test:site
   git diff --check
   ```

8. Review the exact diff for accidental private data, stale counts, unsupported
   claims, and loss of curated prose. `git er done` means commit the approved
   project changes and synchronize them with the configured GitHub remote.

## Near-Term Priorities

1. Finish the ballet studio evidence set with durable image identifiers, final
   trim-out details, and an explicit room-ready status.
2. Deepen the shed into focused craft stories around shop infrastructure,
   material reuse, and restoration workflow.
3. Develop one secondary machine journal into a complete case study instead of
   spreading shallow additions across every motorcycle entry.
4. Keep the root README and this document aligned with implemented behavior.
5. Add a single full-verification command and continuous integration before
   treating the website as a deployable public product.
6. If substantial Flickr functionality is added, split the large importer into
   smaller discovery, metadata, inventory, rendering, and CLI units while
   preserving its tested contracts.
