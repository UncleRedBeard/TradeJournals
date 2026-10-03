# Website 2 - Task 14 Journals And Archive

Workflow status: COMPLETE — hub technical review passed; Shawn's acceptance received
Brief revision: 1
Approval: Shawn said `kick off task 14` in website updates on October 2, 2026.
Hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` / website updates
Child: `01a0ff4e-a59e-7b02-a44b-d36c0663db18`
Dispatch: `WK-WEB-T14-D01` — SENT once; active execution verified
Register: [task-register.md](task-register.md)

Exact idle child verified before dispatch. Fresh wait observed active turn
`01a0ff50-6839-7921-b6e9-6fff0dea4bd4` after the approved start.

Hub receipt `WK-WEB-T14-H01`, October 2, 2026: report `WK-WEB-T14-R01`,
revision 1 received. Hub inspected the five-file implementation/test/doc delta
and desktop/phone journal and actual-search screenshots; no blocking issues.
Independently reran 121 Node and 37 Python tests, Markdown lint (107 files,
zero errors) and whitespace checks. Both retained outputs independently validate
against matching models at 18 pages, 52 files, 318 references each; review is
current with zero changed keys. Content, search scripts, accepted earlier-stage
components and snapshot bytes are unchanged. Detailed live interactions and
fallback checks are child-reported in the report. Shawn's visual acceptance
is pending. Task 15 has not started; Task 14 changes remain uncommitted.

Preview: `http://127.0.0.1:8139/tradejournals/` and
`http://127.0.0.1:8139/tradejournals/entry-restoration/`.

Hub acceptance `WK-WEB-T14-H02`, October 3, 2026: after the review server was
restarted and its homepage/archive/journal responses verified against saved
preview bytes, Shawn said `looks good. approved` directly in the hub. Combined
with passed technical review H01, this completes Task 14's accepted scope.
Earlier pending-acceptance statements describe the initial report checkpoint.
Changes remain uncommitted; Task 15 and Git closeout await separate instructions.

## Assignment

Carry the approved Concept B Craftsman's Atelier style into TradeJournal
reading pages and archive/search presentation. Keep typography, line length,
headings and spacing comfortable to read. Give the archive and its search
controls/results a consistent, understated appearance. Preserve existing
content, navigation destinations and search behavior.

This is approved implementation, not another request for design permission.
Reuse the settled charcoal/brass/parchment palette and local Cormorant fonts.
Make routine presentation choices within that direction. Shawn wants simple,
maintainable work: more technically capable than the average tradesman, less
flashy than an influencer site. Historic-home restoration and woodwork lead;
other craft remains a supporting layer.

## Scope And Boundaries

- Journal template `website/src/pages/tradejournals/[id].astro`: readable story
  hierarchy, evidence details and navigation to its project and archive.
- Archive page `website/src/pages/tradejournals/index.astro` and
  `website/src/components/ArchiveSearch.astro`: heading, search controls,
  fallback entries, result presentation and readable status/empty/error states.
- Narrow component/style adaptations are permitted; inspect all consumers.
  Reuse the accepted frame and project styling without redesigning them.
- Search uses `website/src/scripts/archive-search.js`, generated `/search.json`
  and the existing journal search engine. Preserve query matching/ranking, link
  identities, text-safe rendering and the fallback when search is unavailable.
  Dynamically inserted results must receive the intended styling too; Astro's
  scoped CSS must not silently miss them. Avoid unnecessary JS or dependencies.
- Preserve approved story/copy, selected media/order/captions/alt text and source
  evidence. Do not add records or rewrite journals/inventories. Existing project
  routes and matching journal destinations remain intact.
- Current barre studio, future barre studio/former living room and Office are
  distinct. Moving is unconfirmed. Preserve approved window/Office wording.
- Keep Work & Craft navigation and disabled inquiries. No contact destination,
  CMS, backend, hosting integration or speculative framework work.
- Task 15 owns integrated release review. No Git commit/push, merge, deployment,
  archive, snapshot refresh or successor dispatch is authorized by this start.

## Starting State And References

Workspace: `/Users/shkelley/Documents/PERSONAL/Shawn/Nerds/TradeJournals`.
Same-directory fork on `codex/concept-b-homepage`; baseline
`6042f00416a2d04382dbc57f249bbd15c1d315b8` contains accepted Tasks 12 and 13,
pushed and verified at `0 0`. Website files were clean at Task 14 preparation.
Concurrent content-review work owns the Lomography overlap journal, its
register, and SXSW briefs/reports. Preserve that work; refresh status before
editing and before reporting, since shared HEAD can advance independently.

Read `website/README.md`, the Task 12/13 briefs and reports, current journal
templates/stories, `EvidenceDetails.astro`, `ArchiveSearch.astro`, search tests,
`atelier-frame.css` and `tokens.css`. The older Concept B homepage review gives
the visual direction; later hub records supersede its historical failure notes.
Use workflow-hub, frontend-design and senior-developer guidance as applicable.

Last preview: `http://127.0.0.1:8139/`, serving `.preview-dist`; verify it before
reuse and leave other tasks' servers alone. The baseline had 120 Node tests and
37 Python tests passing, and both outputs validated at 18 pages/52 files/302
references. Those are prior results, not a substitute for fresh verification.

## Deliverables And Acceptance

1. Journal and archive presentation matching the accepted direction, with small
   maintainable changes and existing content/search preserved.
2. Desktop and phone preview links/screenshots covering a long journal, a shorter
   or fallback entry where available, archive entries and actual search results.
3. Browser checks at narrow and desktop widths: no overflow, readable prose and
   evidence, correct heading hierarchy, keyboard focus, labelled controls,
   working project/archive/source links and disabled inquiry controls.
4. Exercise a matching query, no results, empty query and unavailable-search
   fallback. Confirm `original door` finds Entry and `office` keeps Office and
   current studio distinct. Check results after client-side insertion, not just
   static markup; retain graceful browsing when scripts/data are unavailable.
5. Run proportionate regression checks for changed behavior, the complete
   `npm run test:website`, `npm run check:website`, guarded release build,
   `npm run lint:md`, and whitespace checks using the scoped runtime documented
   in `website/README.md`. Preserve snapshot bytes. Validate both retained
   outputs against their matching prepared models. Report any source drift from
   concurrent work; never refresh fingerprints just to make a build pass.
6. Inspect the accepted homepage, shared frame and project page for unintended
   changes. Record limitations and actual checks without claiming deployment.

## Return To Hub

Read this brief before executing; the active hub turn is not in forked history.
Apply dispatch `WK-WEB-T14-D01` once. Update the child to
`Website 2 - Task 14 Journals - IN PROGRESS` and continue to a reviewable result.
Do not edit the hub register or brief.

Save report `WK-WEB-T14-R01`, revision 1, to
`docs/website-workflow/reports/task-14-journals-archive.md`. Include implementation,
verification, screenshot paths, preview, preserved concurrent work and remaining
issues. Rename to `Website 2 - Task 14 Journals - READY FOR REVIEW`, then send
the report to the exact hub for reconciliation and Shawn's visual acceptance.
No automatic next stage. Keep all project material in this authorized workspace.
