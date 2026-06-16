# TradeJournals

A craftsman-first portfolio and trade journal archive.

This repository is intended to document restoration work, material knowledge, process decisions, and visual evidence across several related craft disciplines. The goal is not to present a developer portfolio, but to create a durable source of truth for a future interactive portfolio centered on preservation, hands-on skill, and thoughtful material stewardship.

## Portfolio Pillars

```text
TradeJournals/
├── 01_the_residence_1894/       # Historic home restoration
├── 02_the_forge_and_shop/       # Reclaimed timber workshop buildout
├── 03_the_machines/             # Vintage scooters, motorcycles, and mechanical restoration
├── 04_materials_and_alchemy/    # Pottery, clay, glazes, kiln building, and firing
└── 05_the_lens/                 # Film photography and visual documentation
```

## Journal Philosophy

Each journal should explain more than what happened. It should capture:

- the original problem or constraint
- the historical or material context
- the tools, methods, and decisions used
- the tradeoffs avoided or accepted
- the visible evidence, such as Flickr photo references
- the value delivered through preservation-minded craftsmanship

The writing should make the hidden work legible: the structural stabilization, material matching, repair logic, tool choices, and craft judgment that separate preservation work from generic replacement work.

## Markdown Standards

All `.md` files should follow Markdown best practices and pass Markdownlint before changes are committed.

Run:

```sh
npm run lint:md
```

The lint rule is intentionally prose-friendly: line length is not enforced, but structure, spacing, headings, lists, fenced code blocks, and link formatting are checked.

### Flickr Evidence Links

When adding or embedding a Flickr URL, use the Flickr image title as the source label. If the title is a timestamp such as `YYYYMMdd_HHMMss`, translate it to `YYYY-MM-DD HH:MM`, drop the seconds, and ignore export or duplicate suffixes such as `(1)` or `-01`. If the image title has extra leading alphabetic characters before the timestamp, disregard those characters and use the photo EXIF capture date/time for the label instead.
