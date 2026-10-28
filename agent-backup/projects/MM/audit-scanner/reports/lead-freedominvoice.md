# Accessibility & Performance Audit: https://www.freedominvoice.com

_Scanned 2026-10-22 · 1 page(s) · axe-core 4.10.2 · DRAFT, not reviewed by a human_

## Summary
- **Total violations:** 9 (0 critical, 7 serious, 1 moderate, 1 minor)
- **Score (100 − weighted violations, floor 0):** 62

## Page metrics
| Page | Load (ms) | Transfer (KB) |
|---|---|---|
| / | 1065 | 1045.5 |

## Findings
### /
- **[serious] Elements must meet minimum color contrast ratio thresholds** (`color-contrast`, 7 elements) — https://dequeuniversity.com/rules/axe/4.10/color-contrast?application=axeAPI
  - `<span>or</span>`
  - `<small>Example</small>`
- **[moderate] Heading levels should only increase by one** (`heading-order`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/heading-order?application=axeAPI
  - `<h3>Connect your AI</h3>`
- **[minor] Alternative text of images should not be repeated as text** (`image-redundant-alt`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/image-redundant-alt?application=axeAPI
  - `<img src="/assets/homepage/hvac.webp" alt="HVAC" width="900" height="1350" loading="lazy" decoding="`



---
Prepared by Nitsuah Labs. Automated scan; findings should be verified manually before remediation.
