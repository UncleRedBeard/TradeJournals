# Project Memory: TradeJournals Portfolio Direction

This repository is a craftsman-first trade journal and portfolio archive. The goal is to showcase physical restoration skill, preservation judgment, material knowledge, and process transparency rather than software-development ability.

## Core Vision

The project should become an interactive, evidence-backed portfolio for restoration and craft work. Technical tools such as Markdown, GitHub, Flickr, and possibly MCP servers are background infrastructure. The client-facing value is the craft story: what was restored, why it mattered, how the work was done, what tradeoffs were avoided, and what visible evidence supports the claim.

The portfolio should help historic homeowners, preservation-minded clients, or collaborators understand the author as a serious craftsperson who respects original fabric, understands old materials, and can solve messy real-world restoration problems.

## Portfolio Pillars

- `01_the_residence_1894`: restoration work on the 1894 house, especially office renovation, structural stabilization, framing, trim, windows, envelope, and historically sensitive repair decisions.
- `02_the_forge_and_shop`: workshop restoration/buildout using reclaimed timber where possible. This is the working environment and philosophical bridge between architectural craft and mechanical restoration.
- `03_the_machines`: vintage scooter and motorcycle restoration, including a 1964 Vespa. This complements the home work by showing preservation across metal, mechanics, bodywork, electrical systems, and original material stewardship.
- `04_materials_and_alchemy`: pottery, clay, glazes, kiln building, and firing.
- `05_the_lens`: film photography and visual documentation.

## Flickr And AI Portfolio Concept

The user has a public Flickr album for the 1894 office renovation:

[1894 office renovation Flickr album](https://www.flickr.com/photos/boocher/albums/72177720316928566/)

The album documents office renovation work in Smithville. It should be used as visual evidence for trade journals. Future photo work should add clear titles and short descriptions directly in Flickr, especially for key milestone images.

Important guidance from prior discussion:

- The album is strong because it shows exposed structural work, historic framing, rough-sawn true-dimensional lumber, and unfiltered renovation reality.
- It could be improved with more close-up photos of the actual interventions: joinery, sistering, bolt or screw patterns, sill repairs, shoring, leveling equipment, tool use, and clean before/during/after transitions.
- Flickr descriptions should explain the specific challenge, the method used, and why that method respected the historic structure.

## Markdown Trade Journals

Markdown files are the preferred content format because they are easy to write, easy to version, and easy for AI tools to read. Journals should be organized by trade, system, or skill rather than only by timeline.

Recommended journal pattern:

- The Challenge
- Historic Preservation Context
- My Craftsmanship Execution
- Materials And Tools
- Tradeoffs Avoided Or Accepted
- Visual Evidence / Flickr References

Example trade journal topics:

- structural framing and stabilization
- historic framing and lumber
- reclaimed timber joinery
- finish carpentry and millwork
- fenestration, sash, wavy glass, and glazing
- masonry and lime mortar
- exterior envelope and siding
- mechanical integration in historic structures
- Vespa chassis, metalwork, motor rebuild, and electrical systems

## Possible Technical Direction

A future interactive portfolio could use:

- GitHub as the durable home for Markdown trade journals and project structure.
- Flickr as the visual archive for high-resolution process photos.
- A custom Python/FastMCP Flickr server to fetch public album metadata, image URLs, titles, descriptions, tags, and photo IDs.
- A GitHub MCP server or similar integration to read and update trade journals.

The technical implementation should remain invisible to clients. The result should feel like a conversational craftsman portfolio or construction log, not a developer demo.

## Brand Narrative

The unifying idea is preservation across disciplines:

- The 1894 residence proves architectural preservation and structural restoration skill.
- The reclaimed-timber workshop proves commitment to material reuse, tooling, and the craft environment.
- The 1964 Vespa and other machines prove precision mechanical restoration and respect for original engineering.

The portfolio should present an ecosystem of preservation: living in, working in, documenting, and restoring historic materials and machines with care.

## Current Progress

The repository now has tracked pillar folders and `trade_journals` folders for each major portfolio area. Markdownlint is configured and should be run with `npm run lint:md` before commits.

The active first journal is `03_the_machines/trade_journals/1964_vespa_restoration.md`. It contains:

- A first journal entry based on scanned handwritten notes found in the Vespa side storage compartment.
- Initial repair observations around rear brake light switch location, rear brake pedal rubber, surface rust, paint chipping, Ford 76 / code 2R paint reference, and frame serial number `BA276439`.
- Additional scanned notes for model/year and replacement parts: 1964 Vespa 150, all cables, rear brake pedal, rear brake foot pedal rubber cover, side storage door keyed lock, cotter pin / 14 mm bolt and nut note for securing the rear brake cable, tail light assembly, and petcock lever gasket or rubber grommet.
- A public Flickr album reference for the Vespa: [1964 Vespa](https://www.flickr.com/photos/boocher/albums/72177720305371229/), owned by UncleRedBeard, with 427 public photos.
- A working `Visual Evidence` map that treats photo links as pre-work or baseline-condition evidence unless the user says otherwise.
- Mapped pre-work evidence for overall condition, frame/body provenance, engine condition, electrical condition, rear wheel/brake/control cable condition, cable routing, engine access, original markings, and stamped engine/case number.

Recent GitHub sync points:

- `fe856cd Add Vespa pre-work journal evidence`
- `8a4b3e2 Append Vespa scanned parts notes`
