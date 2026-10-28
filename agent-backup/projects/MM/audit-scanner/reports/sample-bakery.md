# Accessibility & Performance Audit: http://localhost:8080

_Scanned 2026-10-22 · 2 page(s) · axe-core 4.10.2 · DRAFT, not reviewed by a human_

## Summary
- **Total violations:** 13 (2 critical, 4 serious, 7 moderate, 0 minor)
- **Score (100 − weighted violations, floor 0):** 46

## Page metrics
| Page | Load (ms) | Transfer (KB) |
|---|---|---|
| / | 41 | 0.3 |
| /menu.html | 23 | 0.2 |

## Findings
### /
- **[critical] Buttons must have discernible text** (`button-name`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/button-name?application=axeAPI
  - `<button></button>`
- **[serious] Elements must meet minimum color contrast ratio thresholds** (`color-contrast`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/color-contrast?application=axeAPI
  - `<div class="muted">Fresh bread daily</div>`
- **[serious] <html> element must have a lang attribute** (`html-has-lang`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/html-has-lang?application=axeAPI
  - `<html>`
- **[critical] Images must have alternative text** (`image-alt`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/image-alt?application=axeAPI
  - `<img src="logo.png">`
- **[moderate] Document should have one main landmark** (`landmark-one-main`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/landmark-one-main?application=axeAPI
  - `<html>`
- **[serious] Links must have discernible text** (`link-name`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/link-name?application=axeAPI
  - `<a href="/menu.html"></a>`
- **[moderate] All page content should be contained by landmarks** (`region`, 6 elements) — https://dequeuniversity.com/rules/axe/4.10/region?application=axeAPI
  - `<div class="muted">Fresh bread daily</div>`
  - `<img src="logo.png">`

### /menu.html
- **[serious] Elements must meet minimum color contrast ratio thresholds** (`color-contrast`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/color-contrast?application=axeAPI
  - `<p style="color:#ccc;background:#fff">Sourdough $6</p>`



---
Prepared by Nitsuah Labs. Automated scan; findings should be verified manually before remediation.
