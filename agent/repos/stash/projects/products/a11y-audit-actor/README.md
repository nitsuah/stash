---
up: "[[repos/stash]]"
title: "stash · README"
source: https://github.com/nitsuah/stash/blob/main/projects/products/a11y-audit-actor/README.md
kind: repo-doc
repo: stash
---

# Website Accessibility Audit (WCAG, axe-core)

Give this Actor a list of page URLs and it returns, for each page, a 0 to 100 accessibility score and every WCAG violation found, with the failing elements and a link explaining the fix.

It loads each page in a real Chrome browser (so JavaScript-rendered pages work) and runs [axe-core](https://github.com/dequelabs/axe-core), the engine most accessibility tools use.

## What you get per page
- `score`: 100 minus weighted penalties per violated rule (critical 10, serious 5, moderate 2, minor 1), never below 0.
- `violationCount` and `byImpact` counts.
- `violations[]`: rule id, impact, plain-language help text, a help URL, number of affected elements and example selectors with HTML snippets.
- `passedRules`, the axe-core version and a timestamp.

## Input
| Field | Meaning |
|---|---|
| `startUrls` | Pages to audit, up to 200 per run. |
| `standards` | axe-core tags. Default: WCAG 2.0 to 2.2 A and AA. |
| `maxNodesPerViolation` | Examples to include per rule (1 to 20, default 3). |

## Example output (shortened)
```json
{
  "url": "https://example.com/",
  "score": 83,
  "violationCount": 3,
  "byImpact": { "critical": 0, "serious": 1, "moderate": 2, "minor": 0 },
  "violations": [{ "rule": "color-contrast", "impact": "serious", "affectedElements": 4 }]
}
```

## Use cases
Agency client reports, monitoring a site after each release (schedule the Actor), checking a list of landing pages before a launch, and building an accessibility statement.

## Limits and honesty
Automated checks find roughly a third to half of accessibility problems. A passing score does not prove WCAG conformance, and manual testing with a screen reader and keyboard is still needed. Pages behind a login are not supported. This is not legal advice.

Pricing is per audited page (pay-per-event), so you only pay for pages that were actually checked.
