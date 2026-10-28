---
up: "[[repos/stash]]"
title: "stash · README"
source: https://github.com/nitsuah/stash/blob/main/projects/products/sitemap-checker-actor/README.md
kind: repo-doc
repo: stash
---

# Sitemap URL Checker (robots.txt, 404s, redirects)

A sitemap should list only live, canonical, indexable pages. This Actor finds a site's sitemaps, reads every URL in them, tests each URL and reports the ones that hurt your SEO. Run it after a migration, a redesign or on a monthly schedule.

## How it works
1. It reads `robots.txt` and uses the `Sitemap:` lines. If there are none it tries `/sitemap.xml`.
2. It follows sitemap index files (up to three levels) and reads `.xml.gz` files.
3. It tests every unique URL with a HEAD request, falling back to GET when a server rejects HEAD. Redirects are not followed, so you see them.

## What it reports
- URLs that return an error status (404, 410, 5xx) or cannot be reached.
- URLs that redirect (the sitemap should list the final URL).
- URLs on a different host than the site.
- Duplicate URLs listed more than once.
- URLs that send an `X-Robots-Tag: noindex` header while sitting in the sitemap.
- Invalid `lastmod` dates, sitemaps that cannot be fetched, and files that are not valid sitemaps.

## Output
One summary row per site (`type: site`) with robots.txt status, the sitemaps checked, URL counts and a plain message such as "All 120 sitemap URLs look healthy". Then one row per problem URL (`type: url`) with the issue, status, redirect target and the sitemap it came from. A site with no usable sitemap still gets a summary row.

## Limits
A `noindex` set only in the page HTML (meta tag) is not seen, because the Actor does not download page bodies. Up to 5000 URLs are tested per site (default 200). Sites that block automated requests may report errors that a browser does not see. Only test sites you are allowed to test.

Pricing is per tested URL (pay per event).
