# Accessibility & Performance Audit: https://awidercircle.org

_Scanned 2026-10-22 · 1 page(s) · axe-core 4.10.2 · DRAFT, not reviewed by a human_

## Summary
- **Total violations:** 6 (0 critical, 3 serious, 3 moderate, 0 minor)
- **Score (100 − weighted violations, floor 0):** 79

## Page metrics
| Page | Load (ms) | Transfer (KB) |
|---|---|---|
| / | 439 | 3057.6 |

## Findings
### /
- **[moderate] Document should have one main landmark** (`landmark-one-main`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/landmark-one-main?application=axeAPI
  - `<html dir="ltr" lang="en-US" prefix="og: https://ogp.me/ns#">`
- **[serious] Links must have discernible text** (`link-name`, 3 elements) — https://dequeuniversity.com/rules/axe/4.10/link-name?application=axeAPI
  - `<a rel="home" href="https://awidercircle.org/" h-use-smooth-scroll="true" class="d-flex align-items-`
  - `<a href="https://www.guidestar.org/profile/52-2345144" target="_blank" h-use-smooth-scroll="true" cl`
- **[moderate] All page content should be contained by landmarks** (`region`, 2 elements) — https://dequeuniversity.com/rules/axe/4.10/region?application=axeAPI
  - `<div data-colibri-id="11-h33" class="h-row-container gutters-row-lg-2 gutters-row-md-2 gutters-row-0`
  - `<div class="h-column h-column-container d-flex h-col-lg-auto h-col-md-auto h-col-auto style-8617-out`



---
Prepared by Nitsuah Labs. Automated scan; findings should be verified manually before remediation.
