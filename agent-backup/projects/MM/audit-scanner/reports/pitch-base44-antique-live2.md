# Accessibility & Performance Audit: https://heritage-finds-hub.base44.app

_Scanned 2026-10-22 · 5 page(s) · axe-core 4.10.2 · DRAFT, not reviewed by a human_

## Summary
- **Total violations:** 11 (0 critical, 0 serious, 11 moderate, 0 minor)
- **Score (100 − weighted violations, floor 0):** 78

## Page metrics
| Page | Load (ms) | Transfer (KB) |
|---|---|---|
| / | 1308 | 919.4 |
| /featured-finds | 348 | 1139.0 |
| /visit | 299 | 686.8 |
| /about | 292 | 827.8 |
| /sell-consign | 321 | 686.8 |

## Findings
### /
- **[moderate] All page content should be contained by landmarks** (`region`, 2 elements) — https://dequeuniversity.com/rules/axe/4.10/region?application=axeAPI
  - `<img src="https://media.base44.com/images/public/builder-assets/symbol-orange.png" alt="base44" styl`
  - `<span style="white-space: nowrap; font-size: 12px;">`

### /featured-finds
- **[moderate] All page content should be contained by landmarks** (`region`, 2 elements) — https://dequeuniversity.com/rules/axe/4.10/region?application=axeAPI
  - `<img src="https://media.base44.com/images/public/builder-assets/symbol-orange.png" alt="base44" styl`
  - `<span style="white-space: nowrap; font-size: 12px;">`

### /visit
- **[moderate] All page content should be contained by landmarks** (`region`, 2 elements) — https://dequeuniversity.com/rules/axe/4.10/region?application=axeAPI
  - `<img src="https://media.base44.com/images/public/builder-assets/symbol-orange.png" alt="base44" styl`
  - `<span style="white-space: nowrap; font-size: 12px;">`

### /about
- **[moderate] All page content should be contained by landmarks** (`region`, 2 elements) — https://dequeuniversity.com/rules/axe/4.10/region?application=axeAPI
  - `<img src="https://media.base44.com/images/public/builder-assets/symbol-orange.png" alt="base44" styl`
  - `<span style="white-space: nowrap; font-size: 12px;">`

### /sell-consign
- **[moderate] Aside should not be contained in another landmark** (`landmark-complementary-is-top-level`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/landmark-complementary-is-top-level?application=axeAPI
  - `<aside class="lg:col-span-4">`
- **[moderate] All page content should be contained by landmarks** (`region`, 2 elements) — https://dequeuniversity.com/rules/axe/4.10/region?application=axeAPI
  - `<img src="https://media.base44.com/images/public/builder-assets/symbol-orange.png" alt="base44" styl`
  - `<span style="white-space: nowrap; font-size: 12px;">`



---
Prepared by Nitsuah Labs. Automated scan; findings should be verified manually before remediation.
