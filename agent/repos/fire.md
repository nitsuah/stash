# fire — FIRE Calculator & Tracker

**Last Validated:** 2026-06-10 | Initial vault entry
**Repo:** https://github.com/nitsuah/fire
**Branch convention:** `pmo/fire/planning-alignment-YYYY-MM-DD`

---

## Runtime Status

| Check | Status | Notes |
|---|---|---|
| Docker build | PASS | Nginx Alpine static container |
| App runtime | PASS | `http://localhost:8080` via `docker run -p 8080:80` |
| Docs baseline | PASS | README, ROADMAP, TASKS, FEATURES, METRICS present |

---

## Stack

- **Type:** 100% client-side static web app (HTML5 + Vanilla JS + CSS3)
- **Charts:** Chart.js (CDN)
- **Container:** Docker + Nginx Alpine
- **Storage:** Browser `localStorage` — no external server, no accounts

---

## Key Features

- Net worth projections with togglable SWR (3%, 3.5%, 4%) and inflation adjustment
- Safe read-only CSV import: Fidelity portfolio, Chase/CapOne statements
- CD & Fixed Income tracker with ladder visualizer
- Side gig / eBay profit calculator
- One-click JSON backup + restore

---

## PMO Findings

- Fully client-side — no backend risk surface; privacy-preserving by design.
- ROADMAP references `file:///c:/Users/ajhar/code/fire/` absolute paths — needs cleanup to relative links.
- Sample Fidelity CSV (`Portfolio_Positions_Jun-02-2026.csv`) is committed — verify it contains no real financial data.

---

## Priority Focus

1. Fix absolute `file:///` links in ROADMAP.md to relative links.
2. Audit committed CSV for PII before making repo public.
3. Add E2E test coverage for CSV import paths.

---

## Key Commands

```bash
docker build -t fire-calculator .
docker run -d -p 8080:80 -v ${PWD}:/usr/share/nginx/html --name fire-app fire-calculator
# → http://localhost:8080

docker stop fire-app && docker rm fire-app
```

---

## Active PMO

See TASKS.md and ROADMAP.md for current priorities.

---

## Vault Index

*Copied from repo — do not edit these files, overwritten on sync. Edit only this `.md`.*

**Core:** [[repos/fire/ROADMAP|ROADMAP]] · [[repos/fire/TASKS|TASKS]] · [[repos/fire/FEATURES|FEATURES]] · [[repos/fire/METRICS|METRICS]] · [[repos/fire/CHANGELOG|CHANGELOG]] · [[repos/fire/README|README]]

**docs/:** [[repos/fire/docs/fire-plan|fire-plan]] · [[repos/fire/docs/fire-feedback|fire-feedback]]
