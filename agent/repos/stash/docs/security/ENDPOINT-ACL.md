---
up: "[[repos/stash]]"
title: "stash · ENDPOINT-ACL"
source: https://github.com/nitsuah/stash/blob/main/docs/security/ENDPOINT-ACL.md
kind: repo-doc
repo: stash
---

# API / MCP endpoint authorization matrix

No keys, tokens, or secrets in this file. Tracking: nitsuah/stash#302.
The AuthZ column records the principal and any tenant or object-ownership check (per user, per account, per object); it stays unverified until the per-repo review completes. Routes detected are auto-counted from tracked source (a lead, not proof). Values marked "prior lead" come from earlier docs and stay unverified until the per-repo review completes. Findings from this review are tracked privately, not here.

| Repo | Surface | Routes detected | AuthN | AuthZ / principal / tenant checks | Rate limit | Deny behaviour | Tracking | Status |
|---|---|---|---|---|---|---|---|---|
| ats-fill | browser extension (message router) | 0 | TBD | TBD | TBD | TBD | nitsuah/ats-fill#176 | unverified |
| gcp | dashboard (apps/server.js) | 9 | TBD | TBD | TBD | TBD | nitsuah/gcp#78 | unverified |
| vigil | HTTP API + MCP server | 46 | shared admin key (prior lead, unverified) | TBD | 60 req/min (docs/MCP.md; prior lead, unverified) | TBD | nitsuah/vigil#345 | unverified |
| vhs | HTTP API | 37 | TBD | TBD | TBD | TBD | nitsuah/vhs#102 | unverified |
| fire | Express API + MCP + Netlify functions | 72 | TBD | TBD | TBD | TBD | nitsuah/fire#279 | unverified |
| skyview | Netlify functions API | 12 | TBD | TBD | TBD | TBD | nitsuah/skyview#213 | unverified |
| bb-mcp | MCP server | 0 | OIDC (prior lead, unverified) | TBD | TBD | TBD | TBD | unverified |
| stash | sso/ SAML example; demo backends | 2 | TBD | TBD | TBD | TBD | nitsuah/stash#303 | unverified |
| imps-runner | CLI + workflows (nitsuah/.github) | 0 | TBD | TBD | TBD | TBD | TBD | unverified |
| deployer | deploy CLI + contracts (private repo) | 0 | TBD | TBD | TBD | TBD | TBD | unverified |
| nitsuah-io | static site + /sw.js | 0 | TBD | TBD | TBD | TBD | TBD | unverified |
| kryptos | HTTP API | 20 | TBD | TBD | TBD | TBD | TBD | unverified |
| darkmoon | game server | 4 | TBD | TBD | TBD | TBD | TBD | unverified |
| gods-eye-view | dev server (upstream fork; not scanned in this pass) | n/a | TBD | TBD | TBD | TBD | TBD | unverified |
