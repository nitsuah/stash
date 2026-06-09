# skyview - Static marketing site and client portal

**Last Validated:** 2026-03-27 | PMO audit - Docker-first validation
**Repo:** https://github.com/nitsuah/skyview
**Branch convention:** pmo/skyview/planning-alignment-YYYY-MM-DD

---

## Runtime Status

| Check | Status | Notes |
|---|---|---|
| Docker build | PASS | Nginx static image builds successfully |
| Container runtime | PASS | HTTP 200 observed from container on localhost |
| Docs baseline | PASS | Core planning and governance docs are present |

---

## Stack

- Static HTML/CSS/JavaScript site with modular scripts
- Netlify deployment model + Decap CMS admin flow
- Playwright E2E and Vitest unit test setup

---

## PMO Findings

- Product appears launch-ready from infrastructure perspective.
- Planning docs were overly narrative and not parser-safe; roadmap/tasks are now aligned to execution format.
- METRICS currently contains conflicting coverage values in separate sections and needs one authoritative source.

---

## Priority Focus

1. Complete production launch identity tasks (domain/business metadata/search console).
2. Reconcile coverage and performance metrics into a single dated source of truth.
3. Implement optional portal enhancements only after launch checklist closure.

---

## Key Commands

```bash
docker build -t pmo-skyview-audit .
docker run -d -p 18080:80 pmo-skyview-audit
# Validate with HTTP GET to http://localhost:18080
```

---

## Active PMO

See TASKS.md and ROADMAP.md for current priorities.

---

## Vault Index

*Copied from repo — do not edit these files, overwritten on sync. Edit only this `.md`.*

**Core:** [[repos/skyview/ROADMAP|ROADMAP]] · [[repos/skyview/TASKS|TASKS]] · [[repos/skyview/FEATURES|FEATURES]] · [[repos/skyview/METRICS|METRICS]] · [[repos/skyview/CHANGELOG|CHANGELOG]] · [[repos/skyview/README|README]]

**docs/:** [[repos/skyview/docs/DEPLOYMENT_GUIDE|Deployment Guide]] · [[repos/skyview/docs/GETTING_STARTED|Getting Started]] · [[repos/skyview/docs/QUICK_REFERENCE|Quick Reference]] · [[repos/skyview/docs/OWNER_GUIDE|Owner Guide]] · [[repos/skyview/docs/SEO_GUIDE|SEO Guide]] · [[repos/skyview/docs/ANALYTICS_SETUP|Analytics Setup]] · [[repos/skyview/docs/CLIENT_PORTAL|Client Portal]] · [[repos/skyview/docs/PERFORMANCE_CHECKLIST|Performance Checklist]] · [[repos/skyview/docs/ASSET_MANAGEMENT|Asset Management]]
