---
up: "[[repos/stash]]"
title: "stash · NOTICE"
source: https://github.com/nitsuah/stash/blob/main/projects/products/NOTICE.md
kind: repo-doc
repo: stash
---

# Third-party notices

- axe-core (Deque Systems), MPL-2.0: bundled unmodified as `a11y-check-extension/axe.min.js` and installed from npm by `a11y-audit-actor`. The license header stays in the file. Source: https://github.com/dequelabs/axe-core
- Crawlee and the Apify SDK (Apify), Apache-2.0: dependencies of the Actors, installed from npm.
- Playwright (Microsoft), Apache-2.0: used by `a11y-audit-actor` and the extension test, installed from npm.

Our own code in this folder is what we sell: the packaging, scoring, defaults, tests and release setup. Shared patterns (release.json, validate.mjs, CI) are reused across packages. Each Actor stays self-contained on purpose, because Apify builds it from its own folder.
