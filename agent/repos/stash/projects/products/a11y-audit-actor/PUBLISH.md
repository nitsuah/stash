---
up: "[[repos/stash]]"
title: "stash · PUBLISH"
source: https://github.com/nitsuah/stash/blob/main/projects/products/a11y-audit-actor/PUBLISH.md
kind: repo-doc
repo: stash
---

# Publishing the Actor (needs the user's Apify account)

Tested locally in Docker on 2026-10-23: example.com scores 100, nitsuah.io/tools scores 100, Deque's deliberately inaccessible demo scores 40 with 9 violations. Sites that return 403 to bots (for example w3.org) produce an `error` record instead of a score.

1. Create a free account at apify.com and an API token (Settings, Integrations).
2. From this folder (CLI needs Node, so run it in Docker or install it):
   `npx apify-cli login` then `npx apify-cli push`
3. In the Apify Console open the Actor, then Publication, then Monetization: choose pay per event, add the event named exactly `page-audited` (the code charges this once per audited page). Suggested start: $0.02 per page. Apify keeps 20 percent.
4. Fill the Store listing (title, description and README are already written), set the categories to Developer tools and SEO tools, then publish.
5. Schedule a weekly run of the Actor on nitsuah.io/tools as a free regression check of our own site.

`storage/` holds local test runs only and should not be committed.
