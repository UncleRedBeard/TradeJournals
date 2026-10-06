# SEO Meta Descriptions — Start Request

Request ID: `WK-WEB-SEO-META-20261006-01`
Requesting chat: `01a1118b-5382-7490-a139-217004cba7fc`
Receiving hub: `01a0a263-8d09-7ff2-8144-a71eb6ec16f6` — website updates
Date: October 6, 2026, America/Chicago
Coordination delivery: RECEIVED; Task 21 execution observed ACTIVE
Receiving turn: `01a11243-b25a-7fe0-8e8b-633a44768daa`
Child: `01a11244-b428-73c2-a870-621a495540b8`
Child execution turn: `01a11245-8afe-74c2-b2bd-b4ad93085148`
Hub dispatch: `WK-WEB-T21-D01`

The hub created the child and dispatched once. The requesting chat independently
observed an active execution turn and the child's acknowledgement that it will
add descriptions through the shared layout and verify all 20 generated pages.
Further implementation review and acceptance belong to the established hub.

Shawn instructed the requesting chat to use workflow-hub to "kick off the
medium priority task" after addressing both high-priority items. The requesting
chat stated that this means page-specific meta descriptions, the next item in
the audit. This is approval to prepare and start that bounded task now.

## Scope and acceptance

Continue the established hub sequence as Task 21 Page Meta Descriptions after
checking for any newer reservation or dispatch. Keep the work lean: reuse the
shared layout and existing content where sound, with no new dependency or page.

- Add exactly one useful, non-empty meta description to each HTML route.
- Cover the homepage, archive index, project overviews, and TradeJournal pages.
  Distinguish an overview from its corresponding journal; avoid one generic
  site-wide description or a mechanically imposed character count.
- Describe actual visible content and approved practice facts. Preserve
  own-home context and uncertainty; avoid unsupported services, client claims,
  availability promises, town stuffing, and ranking/snippet guarantees.
- Verify generated descriptions across all current pages, including escaping,
  unintended duplication, and consistency with visible content. Run relevant
  existing website tests, preview/output checks, and `git diff --check`.
- Preserve titles, visible design, navigation, preview noindex, contact state,
  and content validation. Record the review-snapshot state without changing
  reviewed fingerprints or promoting a release.

Task 19 and Task 20 are recorded COMPLETE, approved, and closed out at `cedebf8`.
The current shared checkout is `main`; preserve the unrelated local
`PROJECT_MEMORY.md` edit. Current `SiteLayout.astro` still has no description
prop or tag. All four page templates use that layout.

The hub owns its brief, child fork, approval/dispatch record, acceptance, and
register. The child owns implementation and its completion report. This request
is a coordination record, not a second register. Verify the actual child title
and execution state before reporting that the task has started.

Out of scope: the separate direct-landing attribution finding, canonical URLs,
sitemap, crawler policy, images, new routes, redesign, contact activation,
hosting/deployment, snapshot refresh, Git commit/push, private business edits,
or resuming paused WS08/A-06. Prior Tasks 19–20 closeout approval is specific to
those tasks and is not a new Git authorization.
