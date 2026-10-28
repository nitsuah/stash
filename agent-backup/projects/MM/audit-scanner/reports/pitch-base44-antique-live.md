# Accessibility & Performance Audit: https://heritage-finds-hub.base44.app

_Scanned 2026-10-22 · 5 page(s) · axe-core 4.10.2 · DRAFT, not reviewed by a human_

## Summary
- **Total violations:** 54 (0 critical, 42 serious, 12 moderate, 0 minor)
- **Score (100 − weighted violations, floor 0):** 0

## Page metrics
| Page | Load (ms) | Transfer (KB) |
|---|---|---|
| / | 1001 | 919.1 |
| /featured-finds | 548 | 1138.6 |
| /visit | 645 | 686.5 |
| /about | 429 | 827.4 |
| /sell-consign | 287 | 686.5 |

## Findings
### /
- **[serious] Elements must meet minimum color contrast ratio thresholds** (`color-contrast`, 4 elements) — https://dequeuniversity.com/rules/axe/4.10/color-contrast?application=axeAPI
  - `<dd class="tabular-nums text-ink/60">Closed</dd>`
  - `<dd class="tabular-nums text-ink/60">10am – 6pm</dd>`
- **[moderate] All page content should be contained by landmarks** (`region`, 2 elements) — https://dequeuniversity.com/rules/axe/4.10/region?application=axeAPI
  - `<img src="https://media.base44.com/images/public/builder-assets/symbol-orange.png" alt="base44" styl`
  - `<span style="white-space: nowrap; font-size: 12px;">`

### /featured-finds
- **[serious] Elements must meet minimum color contrast ratio thresholds** (`color-contrast`, 5 elements) — https://dequeuniversity.com/rules/axe/4.10/color-contrast?application=axeAPI
  - `<p class="max-w-md text-sm leading-relaxed text-ink/60">Inventory changes weekly and photographs are`
  - `<dd class="tabular-nums text-ink/60">Closed</dd>`
- **[moderate] Heading levels should only increase by one** (`heading-order`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/heading-order?application=axeAPI
  - `<h3 class="font-display text-lg leading-snug text-ink">Art Deco Brass Table Lamp</h3>`
- **[moderate] All page content should be contained by landmarks** (`region`, 2 elements) — https://dequeuniversity.com/rules/axe/4.10/region?application=axeAPI
  - `<img src="https://media.base44.com/images/public/builder-assets/symbol-orange.png" alt="base44" styl`
  - `<span style="white-space: nowrap; font-size: 12px;">`

### /visit
- **[serious] Elements must meet minimum color contrast ratio thresholds** (`color-contrast`, 10 elements) — https://dequeuniversity.com/rules/axe/4.10/color-contrast?application=axeAPI
  - `<p class="mt-6 inline-flex items-center gap-2 text-sm text-ink/60">`
  - `<label for="contact-name" class="flex items-baseline gap-1 text-[10px] uppercase tracking-[0.2em] te`
- **[moderate] All page content should be contained by landmarks** (`region`, 2 elements) — https://dequeuniversity.com/rules/axe/4.10/region?application=axeAPI
  - `<img src="https://media.base44.com/images/public/builder-assets/symbol-orange.png" alt="base44" styl`
  - `<span style="white-space: nowrap; font-size: 12px;">`

### /about
- **[serious] Elements must meet minimum color contrast ratio thresholds** (`color-contrast`, 7 elements) — https://dequeuniversity.com/rules/axe/4.10/color-contrast?application=axeAPI
  - `<p class="font-display text-sm text-gilt">01</p>`
  - `<p class="font-display text-sm text-gilt">02</p>`
- **[moderate] All page content should be contained by landmarks** (`region`, 2 elements) — https://dequeuniversity.com/rules/axe/4.10/region?application=axeAPI
  - `<img src="https://media.base44.com/images/public/builder-assets/symbol-orange.png" alt="base44" styl`
  - `<span style="white-space: nowrap; font-size: 12px;">`

### /sell-consign
- **[serious] Elements must meet minimum color contrast ratio thresholds** (`color-contrast`, 16 elements) — https://dequeuniversity.com/rules/axe/4.10/color-contrast?application=axeAPI
  - `<label for="consign-name" class="flex items-baseline gap-1 text-[10px] uppercase tracking-[0.2em] te`
  - `<label for="consign-email" class="flex items-baseline gap-1 text-[10px] uppercase tracking-[0.2em] t`
- **[moderate] Aside should not be contained in another landmark** (`landmark-complementary-is-top-level`, 1 element) — https://dequeuniversity.com/rules/axe/4.10/landmark-complementary-is-top-level?application=axeAPI
  - `<aside class="lg:col-span-4">`
- **[moderate] All page content should be contained by landmarks** (`region`, 2 elements) — https://dequeuniversity.com/rules/axe/4.10/region?application=axeAPI
  - `<img src="https://media.base44.com/images/public/builder-assets/symbol-orange.png" alt="base44" styl`
  - `<span style="white-space: nowrap; font-size: 12px;">`



---
Prepared by Nitsuah Labs. Automated scan; findings should be verified manually before remediation.
