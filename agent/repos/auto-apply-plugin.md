# auto-apply-plugin — AI Job Application Chrome Extension

**Last Validated:** 2026-06-10 | Initial vault entry
**Repo:** https://github.com/nitsuah/auto-apply-plugin
**Branch convention:** `pmo/auto-apply-plugin/planning-alignment-YYYY-MM-DD`

---

## Runtime Status

| Check | Status | Notes |
|---|---|---|
| Docker build | N/A | Chrome extension — no Docker runtime path |
| Test suite | PASS | 63 unit tests pass (Vitest via Docker Compose) |
| E2E | Available | Playwright via Docker Compose |
| Docs baseline | PASS | README, ROADMAP, TASKS, FEATURES, METRICS, PRIVACY present |

---

## Stack

- **Type:** Chrome MV3 extension (zero build step, load unpacked)
- **AI:** Gemini 2.5 (REST API, auto-model selection via `models.list`)
- **Storage:** `chrome.storage.local` — local-first, no external servers
- **Testing:** Vitest (63 tests) + Playwright E2E (Docker Compose)
- **CI:** GitHub Actions (lint, type check, test)
- **ATS support:** Greenhouse, Ashby, Lever, LinkedIn Easy Apply (Phase 1); Workday, Jobvite, iCIMS (Phase 2)

---

## PMO Findings

- Privacy-first design: no external calls except Gemini API (user's own key) and opt-in job search sources.
- Job search panel aggregates 14 sources (9 keyless, 1 session-based, 4 keyed).
- CSV import for tracker history is fully specified; test coverage should be validated against import edge cases.

---

## Priority Focus

1. Validate Phase 2 ATS platforms (Workday, Jobvite, iCIMS, Circle/Phenom).
2. Maintain screenshot gallery currency (last refreshed 2026-05-21).
3. Extend E2E coverage for job search panel filter combinations.

---

## Key Commands

```bash
# Unit tests (63, Docker-based)
docker compose -f config/docker-compose.yml run --rm test

# Lint
docker compose -f config/docker-compose.yml run --rm lint

# E2E
docker compose -f config/docker-compose.yml run --rm e2e
```

---

## Active PMO

See TASKS.md and ROADMAP.md for current priorities.

---

## Vault Index

*Copied from repo — do not edit these files, overwritten on sync. Edit only this `.md`.*

**Core:** [[repos/auto-apply-plugin/ROADMAP|ROADMAP]] · [[repos/auto-apply-plugin/TASKS|TASKS]] · [[repos/auto-apply-plugin/FEATURES|FEATURES]] · [[repos/auto-apply-plugin/METRICS|METRICS]] · [[repos/auto-apply-plugin/CHANGELOG|CHANGELOG]] · [[repos/auto-apply-plugin/README|README]] · [[repos/auto-apply-plugin/PRIVACY|PRIVACY]]
