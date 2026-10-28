# Accessibility & Performance Audit: https://preview-sandbox--6ad9c0537875bacef6cdde69.base44.app

_Scanned 2026-10-22 · 1 page(s) · axe-core 4.10.2 · DRAFT, not reviewed by a human_

## Summary
- **Total violations:** 4 (0 critical, 1 serious, 3 moderate, 0 minor)
- **Score (100 − weighted violations, floor 0):** 89

## Page metrics
| Page | Load (ms) | Transfer (KB) |
|---|---|---|
| / | 3892 | 11782.9 |

## Findings
### /
- **[serious] Elements must meet minimum color contrast ratio thresholds** (`color-contrast`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/color-contrast?application=axeAPI
  - `<h1 data-source-location="src/lib/PageNotFound.jsx:28:24" data-dynamic-content="false" class="text-7`
- **[moderate] Document should have one main landmark** (`landmark-one-main`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/landmark-one-main?application=axeAPI
  - `<html lang="en">`
- **[moderate] All page content should be contained by landmarks** (`region`, 2 elements) — https://dequeuniversity.com/rules/axe/4.10/region?application=axeAPI
  - `<div data-source-location="src/lib/PageNotFound.jsx:27:20" data-dynamic-content="false" class="space`
  - `<div data-source-location="src/lib/PageNotFound.jsx:33:20" data-dynamic-content="true" class="space-`



---
Prepared by Nitsuah Labs. Automated scan; findings should be verified manually before remediation.
