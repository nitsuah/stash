# Accessibility & Performance Audit: https://www.thehoneycombproject.org

_Scanned 2026-10-22 · 1 page(s) · axe-core 4.10.2 · DRAFT, not reviewed by a human_

## Summary
- **Total violations:** 9 (3 critical, 3 serious, 3 moderate, 0 minor)
- **Score (100 − weighted violations, floor 0):** 49

## Page metrics
| Page | Load (ms) | Transfer (KB) |
|---|---|---|
| / | 2016 | 23037.5 |

## Findings
### /
- **[serious] Elements must meet minimum color contrast ratio thresholds** (`color-contrast`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/color-contrast?application=axeAPI
  - `<code>make a difference</code>`
- **[moderate] Heading levels should only increase by one** (`heading-order`, 2 elements) — https://dequeuniversity.com/rules/axe/4.10/heading-order?application=axeAPI
  - `<h5 class="preFade" style="transition-timing-function: ease; transition-duration: 0.8s; transition-d`
  - `<h4 style="text-align: center; white-space: pre-wrap; transition-timing-function: ease; transition-d`
- **[critical] Images must have alternative text** (`image-alt`, 3 elements) — https://dequeuniversity.com/rules/axe/4.10/image-alt?application=axeAPI
  - `<img data-load="false" data-mode="cover" data-src="https://images.squarespace-cdn.com/content/v1/5ed`
  - `<img data-load="false" data-mode="cover" data-src="https://images.squarespace-cdn.com/content/v1/5ed`
- **[moderate] Landmarks should have a unique role or role/label/title (i.e. accessible name) combination** (`landmark-unique`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/landmark-unique?application=axeAPI
  - `<nav class="header-nav-list">`
- **[serious] Links must have discernible text** (`link-name`, 2 elements) — https://dequeuniversity.com/rules/axe/4.10/link-name?application=axeAPI
  - `<a class="sqs-block-image-link js-content-mode-element content-fit" data-sqsp-image-block-link="" hr`
  - `<a href="http://www.constantcontact.com/index.jsp?cc=forms_inline" rel="nofollow" target="_blank" no`



---
Prepared by Nitsuah Labs. Automated scan; findings should be verified manually before remediation.
