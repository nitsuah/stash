# Products

Small, self-contained things we ship to marketplaces: browser extensions, Apify Actors and similar. One folder per product, each with a `release.json` that says where it publishes and which files go in the package.

| Package | Target | State |
|---|---|---|
| `a11y-check-extension` | Chrome Web Store | built and tested; not published (needs the one-time manual store upload and CWS secrets) |
| `a11y-audit-actor` | Apify Store | built and tested in the Apify account; Actor is private, monetization needs billing details |
| `broken-link-actor` | Apify Store | built and tested locally against a test site (3 of 3 known broken links found); not uploaded yet |
| `seo-health-actor` | Apify Store | built and tested locally against a site with planted SEO problems (all found); not uploaded yet |

## Adding a product
1. Create `projects/products/<name>/` with its sources and a `release.json` (`targets`, `versionFile`, `packageFiles`, `storeId`).
2. Run `node projects/products/scripts/validate.mjs` (CI runs it on every change to this folder).
3. Publishing is per package and per target, triggered by a tag named `<name>@vX.Y.Z` once the release workflow exists. Shared store credentials live in repository secrets; only the store id is per package.

## Testing
The extension test loads it in headless Chromium against a deliberately inaccessible page: from `a11y-check-extension`, run `npm i playwright && node test.mjs` inside the Playwright Docker image (`mcr.microsoft.com/playwright:v1.64.0-noble`). The Actor runs locally with `docker build` and a mounted `storage/` folder; see its `PUBLISH.md`.
