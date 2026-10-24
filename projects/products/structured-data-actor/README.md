# Structured Data Validator (JSON-LD, schema.org)

Crawl a site and get one row per page showing which schema.org types it declares and which properties are missing. Use it before a launch, after a template change, or monthly to catch broken markup that quietly removes rich results from search.

## What it checks
- Every `script type="application/ld+json"` block is parsed. Invalid JSON is reported.
- Entities are found at the top level, inside `@graph`, and nested (offers, questions, list items).
- Required and recommended properties are checked for: Product and Offer, Article (also NewsArticle, BlogPosting), LocalBusiness (and common subtypes such as Restaurant), Organization, FAQPage and Question, BreadcrumbList and ListItem, Event, Recipe, WebSite, Person, JobPosting.
- Pages with no JSON-LD are flagged, and the number of microdata items is reported.
- Pages that return an HTTP error or cannot be fetched are flagged.

## Scoring
Each issue takes points off 100: required missing 12, recommended missing 2, no JSON-LD 8. A page with no structured data at all is not an error for every site, so treat the score as a review aid.

## Output
One row per page: url, status, score, types found, number of JSON-LD blocks, microdata items and an issues list (type, rule, property, severity, detail).

## Limits
The property lists are a practical subset of Google's guidance, not the full schema.org vocabulary and not a replacement for Google's Rich Results Test. Markup added by JavaScript after page load is not seen because pages are fetched as plain HTML. Pages behind a login are not supported.

Pricing is per validated page (pay per event).
