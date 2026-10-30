---
up: "[[repos/stash]]"
title: "stash · README"
source: https://github.com/nitsuah/stash/blob/main/projects/products/broken-link-actor/README.md
kind: repo-doc
repo: stash
---

# Broken Link Checker (internal and external)

Crawl a website and get a list of every broken link, with the pages it appears on. Useful after a redesign or migration, before a launch, and as a scheduled monthly check.

## How it works
1. It starts from your URLs and follows links on the same site, up to the page limit.
2. It collects every link found (pages, images are not included, only anchors).
3. It tests each unique link with a HEAD request, falling back to GET when a server rejects HEAD, and follows redirects.
4. It reports links that return an error status (400 and above), time out, or fail to resolve.

## Output
One row per broken link: `brokenLink`, `status` (the HTTP status, or `null` when the request failed before a response), `error` (the failure code such as `ENOTFOUND` or a timeout, otherwise `null`), `internal` (whether it is on the crawled site), `foundOnCount` (how many pages contain it) and `foundOn` (up to five of those pages). A clean site gets a single row with `brokenLink: null`, empty `foundOn`, and a `message` such as "No broken links found (N links checked on M pages)". A SUMMARY record in the key-value store has the counts: pages crawled, links checked, broken links.

## Input
- startUrls: where to begin (up to 20).
- maxPages: crawl limit, 1 to 1000, default 50.
- checkExternal: also test links to other websites, default on.
- timeoutSecs: per-link timeout, default 15.

## Limits
Links created by JavaScript after the page loads are not seen, because pages are fetched as plain HTML. Some sites block automated requests and may be reported as broken when they work in a browser. Pages behind a login are not supported. Up to 3000 links are checked per run.

Pricing is per crawled page (pay per event).
