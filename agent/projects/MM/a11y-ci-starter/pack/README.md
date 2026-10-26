# Accessibility CI Starter

Fails a pull request when the current scan exceeds the configured accessibility severity thresholds. Uses axe-core and Playwright (both free, open source).
No AI, no paid services, no accounts.

## Setup (10 minutes)
1. Copy the `.github/` and `a11y/` folders into your repo.
2. Edit `a11y/a11y.config.json`: your site URL, the pages to check, and how many problems you allow per level.
3. In `.github/workflows/a11y.yml`, change the "Start site" step to how your site starts (or scan a preview URL).
4. Open a pull request. The report is attached as a build artifact.

## What you get
- A markdown and JSON report per run (score, findings by severity, page weight).
- A pass/fail gate with limits you set (defaults: no critical or serious, up to 10 moderate).
- `ignoreRules` for findings you have decided to accept.

## Notes
- Automated checks find roughly a third of accessibility problems. Keep manual checks too.
- Platform-injected elements (some site builders add badges) can cause warnings you cannot fix; add their rule to `ignoreRules`.
- License: personal and commercial use, do not resell.
