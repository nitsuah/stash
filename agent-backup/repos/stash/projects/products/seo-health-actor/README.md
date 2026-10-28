---
up: "[[repos/stash]]"
title: "stash · README"
source: https://github.com/nitsuah/stash/blob/main/projects/products/seo-health-actor/README.md
kind: repo-doc
repo: stash
---

# SEO Health Check (titles, descriptions, sitemap, noindex)

Crawl a website and get one row per page with an SEO score and the exact problems found. Run it before a launch, after a redesign or on a schedule to catch regressions.

## What it checks
- Page: HTTP errors, missing, short or long title, missing or badly sized meta description, missing or multiple h1, noindex robots tag, missing canonical, missing html lang, images with no alt attribute, missing Open Graph title.
- Across the crawl: duplicate titles and duplicate descriptions.
- Site: whether robots.txt exists, whether it blocks everything, whether it lists a sitemap, whether sitemap.xml exists and how many URLs it lists.

## Output
One dataset row per page: url, status, score (0 to 100), issueCount, title and an issues list with rule, severity (high, medium, low) and a plain-language detail. A SUMMARY record has the totals and the site-level checks.

## Input
- startUrls: where to begin (up to 20).
- maxPages: crawl limit, 1 to 1000, default 50.

## Limits
Pages are fetched as plain HTML, so tags added by JavaScript after load are not seen. The score is a simple weighted count of issues, not a ranking prediction. Length guidance (titles 15-60, descriptions 70-160 characters) follows common practice, not a search engine rule. Pages behind a login are not supported.

Pricing is per checked page (pay per event).
