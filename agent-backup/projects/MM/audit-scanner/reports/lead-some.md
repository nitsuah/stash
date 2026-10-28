# Accessibility & Performance Audit: https://some.org

_Scanned 2026-10-22 · 1 page(s) · axe-core 4.10.2 · DRAFT, not reviewed by a human_

## Summary
- **Total violations:** 26 (7 critical, 11 serious, 7 moderate, 1 minor)
- **Score (100 − weighted violations, floor 0):** 0

## Page metrics
| Page | Load (ms) | Transfer (KB) |
|---|---|---|
| / | 1139 | 7013.9 |

## Findings
### /
- **[critical] Elements must only use supported ARIA attributes** (`aria-allowed-attr`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/aria-allowed-attr?application=axeAPI
  - `<li class="slick-active" aria-hidden="false" role="presentation" aria-selected="true" aria-controls=`
- **[serious] ARIA hidden element must not be focusable or contain focusable elements** (`aria-hidden-focus`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/aria-hidden-focus?application=axeAPI
  - `<li aria-hidden="true" role="presentation" aria-selected="false" aria-controls="navigation01" id="sl`
- **[serious] ARIA input fields must have an accessible name** (`aria-input-field-name`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/aria-input-field-name?application=axeAPI
  - `<div class="slick-track" style="opacity: 1; width: 2556px;" role="listbox">`
- **[critical] Certain ARIA roles must contain particular children** (`aria-required-children`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/aria-required-children?application=axeAPI
  - `<ul class="slick-dots slick-nav" style="" role="tablist">`
- **[critical] ARIA attributes must conform to valid values** (`aria-valid-attr-value`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/aria-valid-attr-value?application=axeAPI
  - `<li class="slick-active" aria-hidden="false" role="presentation" aria-selected="true" aria-controls=`
- **[critical] Buttons must have discernible text** (`button-name`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/button-name?application=axeAPI
  - `<button aria-controls="mega-menu-main-nav" aria-expanded="false" aria-haspopup="true" aria-label="" `
- **[serious] Elements must meet minimum color contrast ratio thresholds** (`color-contrast`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/color-contrast?application=axeAPI
  - `<a class="mega-menu-link" href="https://some.org/get-help/" tabindex="0">Get Help</a>`
- **[critical] Images must have alternative text** (`image-alt`, 2 elements) — https://dequeuniversity.com/rules/axe/4.10/image-alt?application=axeAPI
  - `<img class="mega-menu-logo" src="https://some.org/wp-content/uploads/2022/07/SOME_logo.png">`
  - `<img class="footer-logo" src="https://some.org/wp-content/uploads/2022/07/some-footer-logo.png">`
- **[serious] Links must have discernible text** (`link-name`, 6 elements) — https://dequeuniversity.com/rules/axe/4.10/link-name?application=axeAPI
  - `<a class="mega-menu-logo" href="https://some.org" target="_self"><img class="mega-menu-logo" src="ht`
  - `<a href="https://www.linkedin.com/company/soothersmighteat/" target="_blank"><i class="fa fa-linkedi`
- **[serious] <ul> and <ol> must only directly contain <li>, <script> or <template> elements** (`list`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/list?application=axeAPI
  - `<ul>`
- **[serious] Interactive controls must not be nested** (`nested-interactive`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/nested-interactive?application=axeAPI
  - `<div class="carousel-slide slick-slide slick-current slick-active" data-slick-index="0" aria-hidden=`
- **[minor] Ensure elements marked as presentational are consistently ignored** (`presentation-role-conflict`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/presentation-role-conflict?application=axeAPI
  - `<li class="slick-active" aria-hidden="false" role="presentation" aria-selected="true" aria-controls=`
- **[moderate] All page content should be contained by landmarks** (`region`, 7 elements) — https://dequeuniversity.com/rules/axe/4.10/region?application=axeAPI
  - `<div class="row">
      <div class="col-md-8 offset-md-2 text-center">
        <h2 class="big-headin`
  - `<div class="sponsor-item slick-slide slick-current slick-active" data-slick-index="0" aria-hidden="f`
- **[critical] Select element must have an accessible name** (`select-name`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/select-name?application=axeAPI
  - `<select id="fieldtysitu" name="cm-fo-tysitu" value="">`



---
Prepared by Nitsuah Labs. Automated scan; findings should be verified manually before remediation.
