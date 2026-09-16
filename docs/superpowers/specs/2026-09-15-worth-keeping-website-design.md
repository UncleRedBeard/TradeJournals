# Worth Keeping Website Architecture

- Date: 2026-09-15
- Status: Written design approved by Shawn on 2026-09-15
- Development branch: `codex/website-updates`
- Source handoff: `WK-TJ-20260914-H01`

## Purpose And Decisions

Build a maintainable public website for Worth Keeping, with TradeJournals as
its deeper craft archive. Routine changes should have a clear home: updating a
project record, selecting photographs, changing service copy, or adjusting a
shared component should not require editing repeated page markup.

Shawn accepted the content and component boundaries, the visitor relationship,
and Astro as the website foundation in the website updates discussion. This
document consolidates that direction and its implementation boundaries. Shawn
then explicitly said "reviewed and approved" to this written design, authorizing
preparation of the implementation plan. It does not record implementation or
launch approval.

The website will use Astro to generate static files. It will build independently
of the private Companion Dashboard. Hosting remains undecided; the core output
must work on a conventional static web host with custom-file upload support.
Provider-specific services must remain optional integrations.

## Public Identity And Visitor Structure

Use this working identity:

> Worth Keeping
>
> Time & Timber Restoration
>
> Historic floors, interior woodwork, and architectural restoration.

The service line is exact, including its punctuation. In running text, use
**Worth Keeping — Time & Timber Restoration**. This is a working public identity;
the discussion did not establish business-name clearance or a domain.

Worth Keeping is the public front door:

- Home: the preservation focus, selected work, approach, and an invitation.
- Work: curated project presentations supported by actual evidence.
- Approach and About: preservation judgment and the person behind the work.
- TradeJournals: deeper exploration across the existing five craft pillars.
- Contact: a deliberately configured invitation, once the channel is agreed.

Ceramics and vintage two-wheelers belong in the broader personal craft story.
Archive categories do not establish commercial services. Historic-home
restoration remains the primary business focus.

The accepted visual concept establishes deep green, warm limestone, natural
wood, restrained pale sage, characterful serif display type, and readable
sans-serif supporting text. Its photographs are generated illustrations and
must not become project evidence. Exact fonts and final public copy beyond the
service line will be reviewed with the rendered design. The Horizon Astro demo
was a technology example, not a replacement visual direction.

## Content Ownership

These are logical boundaries within TradeJournals, not separate repositories or
databases. Existing ownership is documented in the
[module map](../../../MODULE_MAP.md#record-ownership).

| Content | Owns | Must Reference |
| --- | --- | --- |
| Source journals and evidence | Project facts, craft decisions, uncertainty, original source identities | Existing journals, inventories, and scans |
| Project presentations | Reviewed public summaries, selected evidence, dated stage, and source references | One or more source journals and selected media |
| Selected media | Stable image identity, original source link, and approved public asset | Source platform identity or durable source record |
| Business and editorial copy | Identity, service descriptions, approach, about text, and invitation | Approved public wording and supported project claims |
| Page selections | Featured project IDs, service IDs, ordering, and page-specific copy | Existing content records |

### Project Presentations

Each selected project has a stable ID independent of its title, source filename,
or destination URL. A route map determines where the project is displayed.
The public catalog is an explicit selection; discovering another journal does
not automatically add it to the website.

Use one small record per project with:

- Identity, title, craft area, and relevant tags.
- Source-journal references and fingerprints of the source material reviewed.
- A concise summary, with an optional longer project introduction and an
  optional search summary. Search falls back to the concise summary.
- A dated, source-backed craft stage and any material evidence limitation.
- Ordered media selections and their roles in the project story.

Craft stage, editorial review, and actual deployment are distinct. A source
change flags dependent presentations for review; it does not automatically
rewrite their public interpretation. A changed source revision blocks release
validation until the presentation is reviewed against the new source. Preview
can remain available with an explicit local review notice.

Source revisions mean fingerprints of explicitly referenced journal files,
relevant inventory records, and selected local media. They do not mean the
repository-wide commit. Unrelated journal or album edits, and the act of
committing a review, must not invalidate that presentation. These checks detect
local source changes; they do not verify current remote album contents.

Publication records belong to the website's reviewed source. Deployment success
is established by checking the actual hosted result, not by editing a
`published` field. The author's residence must retain that context rather than
being described as a client commission.

### Selected Media And Placement

Keep the media record small: stable ID, source identity, original source URL
where available, approved website asset, and a descriptive text alternative.
Album identities and recorded counts continue to come from the inventories.
Avoid collecting every archive photograph into a new media-management system.

A placement references that media ID and may specify a crop/focal point and a
contextual caption explaining what the image proves. An accessibility-text
override is allowed when the placement changes the image's purpose. Original
media is preserved. Gallery counts are derived from actual selections.

Only reviewed public assets can enter the build. Private Dashboard attachment
identifiers, local absolute paths, or unresolved photo links are not public
asset references. Generated concept imagery has a separate illustration role
and cannot satisfy a project-evidence selection.

### Editorial Copy And Page Selections

Store the working identity and exact service line once. Service records are
separate from archive categories and can reference selected projects as
supporting evidence. Homepage selections hold ordered project IDs rather than
copies of their records.

Use documented fields and a small set of supported content types. Plain text
and deliberately supported Markdown are sufficient initially. Page composition
stays in Astro templates; this design does not introduce an arbitrary HTML
editor or a drag-and-drop page builder.

Use JSON for structured records, with an explicit schema version and files
named by stable IDs. Optional longer narrative lives in a referenced Markdown
file. Content must not execute JavaScript or component code. The concrete field
schemas and validation messages belong in the implementation plan.

## Components And Dependencies

| Component | Responsibility | Receives |
| --- | --- | --- |
| Page shell | Header, navigation, footer, metadata, shared structure | Site identity and page metadata |
| Hero | Opening headline, introduction, image, and action | Reviewed page copy and resolved media |
| Service section | Explain an offering and its supporting work | Service record and selected project summaries |
| Project card | Consistent compact project presentation | Resolved project summary, destination, and image |
| Project story and gallery | Narrative, ordered images, captions, evidence details | Reviewed project presentation and resolved media |
| Archive search | Query selected records and link to current destinations | Generated public search data |
| Contact invitation | Display the configured invitation and destination | Approved copy and a validated action |

Components receive validated data. They do not fetch source albums, interpret
journals, determine publication approval, or reach into private Dashboard data.
Search ranking remains separate from its browser controls and activates only
on pages that include those controls.

Shared visual settings own colors, typography, spacing, and common layout
widths. Components own their responsive rules. Media roles and placement data
control cropping rather than positional selectors such as the second child.

## Build And Public Output

The planned flow is:

```text
Journals + inventories + approved assets
                  |
       Reviewed publication records
                  |
    Source resolution and validation
                  |
      Astro templates and components
                  |
      Static pages + assets + search data
```

The build reads local reviewed inputs without credentials, a running Dashboard,
or live Flickr/Google Photos calls. Astro may use validated content collections
internally; the editable record format remains documented independently.

Reuse the useful inventory parsing and source validation in the existing
evidence builder through a narrow boundary. Do not duplicate inventory parsing
inside individual components. The implementation plan must settle the order
of evidence preparation, Astro rendering, and generated-output validation so
that source validation does not require HTML that has yet to be built.

Use a dedicated `website/` source directory alongside `site_example/` during
migration. Keep pages, components, content records, styles, and source-resolution
helpers distinct inside it. Pin supported Astro and Node versions and retain
a dependency lockfile when implementation is authorized. Generated output and
temporary build data are not additional hand-maintained sources.

Only explicitly selected public records and assets are emitted. The repository
root, private configuration, raw internal records, and unrelated source files
must never be copied wholesale into the public output. Archive links must
resolve to reviewed public destinations; local Markdown paths alone do not
constitute a working public reading experience.

For static deployment, the generated output is uploaded to the chosen host's
document root. Node and Astro run in the build environment, not as requirements
for serving the finished files. Core pages require no provider-specific adapter.
Contact-form processing and other server features remain separate integrations.

## Companion Dashboard Boundary

The first website version uses structured files maintained through the existing
review workflow. A future Dashboard section could prepare changes to the same
records, validate them, and show a preview. That is a separately scoped
Companion feature, not part of this website implementation.

Private drafts and photo intake remain private. Promotion to a public asset and
selection for a public project presentation are deliberate steps. The website
build never reads the Dashboard's private database or managed media store.
Existing Companion authority to apply reviewed local journal additions does
not establish authority to edit website records, commit, push, or deploy them.

## Migration And First Implementation Boundary

The first implementation should prove one representative project end to end:
its reviewed record feeds a project page, a featured card, a gallery, and a
search result. Office Restoration is the proposed pilot because the current
site already presents its floor work and two related source albums. Its
specific public wording and image selections still require source review.

Retain the existing prototype as the comparison baseline while the pilot is
reviewed. Do not move journals, bulk rewrite the archive, or remove the
prototype during this first implementation.

The current builder assumes targets inside one `index.html`, fragment-only
destinations, exact fallback count markup, and unique album assignment across
catalog entries. Keep its existing checks working during the pilot. Translate
legacy inputs explicitly; any replacement of these assumptions needs focused
tests rather than being an incidental consequence of changing page layouts.

During the pilot, newly extracted project records are review candidates. The
existing catalog and page retain their documented ownership for the existing
prototype: the catalog owns search selection, while the page owns its narrative,
full galleries, original image links, and fallback text. Extraction must
reconcile both against the source journal and evidence before establishing a
new project record. Preserve intentional differences between page and search
copy, and account for every selected image and original link.

Before broader migration, choose one reviewed record as the ongoing editorial
source for each migrated project. Any retained legacy catalog and project-page
presentation become generated compatibility output for those projects. Do not
maintain two independently editable copies of the same published facts and
selections.

Before replacing the prototype, inventory its existing project anchors and
source links and verify a compatibility path for each. Retain a legacy landing
page with the old anchors and links to new destinations if fragment URLs need
to survive; server redirects alone cannot map browser fragments.

## Validation And Acceptance

The first implementation must demonstrate:

1. A project-copy change updates its intended presentations from one record.
2. A card-style change applies consistently without altering content records.
3. Changing featured-project order changes only the selected page composition.
4. Missing or duplicate IDs, missing sources/assets, invalid destinations,
   and unsupported evidence selections produce precise validation failures.
5. Changed source revisions are identified for editorial review; automated
   checks do not claim to validate craft interpretation or image authenticity.
6. Public output includes only reviewed content/assets, and core pages remain
   readable without browser JavaScript. Search enhancement fails gracefully.
7. Search links reach the correct project and existing source links survive.
8. Desktop and mobile review confirms legible type, image treatment, keyboard
   access, visible focus, and no unintended horizontal overflow.
9. The output can be served as ordinary static files with no Dashboard or
   application server running.

Use the existing checks where applicable:

```sh
npm run lint:md
npm run check:site-evidence
npm run test:site
git diff --check
```

Add focused record-validation, rendering, link, and browser checks with the
implementation. Run the full documented pre-commit checks if Git closeout is
later authorized. Documentation review does not establish application behavior,
live source availability, or deployment success.

## Explicit Follow-Up Decisions

These are outside the first architectural proof and must be settled before
their dependent work:

- Review real images, placement captions, and exact typography before approving
  the finished Worth Keeping visual presentation.
- Choose the contact destination and any form processor before enabling a
  public contact action; local prototypes must not imply a working submission.
- Review the public archive selection and route compatibility before migrating
  the full five-pillar presentation.
- Select the hosting plan, domain, and deployment procedure before publication.
- Define and authorize Dashboard website editing in the Companion workstream.

Commit, push, deployment, external contact, and additional task dispatch remain
separate from approval of this design. No such action is recorded here.

## References

- [TradeJournals purpose](../../../README.md)
- [Module map and ownership](../../../MODULE_MAP.md)
- [Portfolio direction](../../../PROJECT_MEMORY.md)
- [Existing website guide](../../../site_example/README.md)
- [Astro components](https://docs.astro.build/en/basics/astro-components/)
- [Astro content collections](https://docs.astro.build/en/guides/content-collections/)
- [Astro deployment](https://docs.astro.build/en/guides/deploy/)
- [Astro rendering modes](https://docs.astro.build/en/guides/on-demand-rendering/)
