# farm-3j — Interactive Farm Website + Farm Tycoon Game

**Last Validated:** 2026-06-09 | Initial vault entry
**Repo:** https://github.com/nitsuah/farm-3j (auto-synced from v0.dev)
**Live:** https://vercel.com/austin-hardys-projects/v0-farm-contact-website
**Branch convention:** `pmo/farm-3j/planning-alignment-YYYY-MM-DD`

---

## Runtime Status

| Check | Status | Notes |
|---|---|---|
| Vercel deployment | PASS | Auto-deploys from v0.dev sync |
| Contact form | PASS | `POST /api/contact` with server-side validation |
| Docs baseline | PASS | README, ROADMAP, TASKS, FEATURES, METRICS + game manual |

---

## Stack

- **Framework:** Next.js 15 (App Router)
- **Language:** TypeScript (strict mode)
- **Styling:** Tailwind CSS v4
- **State:** React Context + useReducer
- **Animation:** CSS + requestAnimationFrame
- **Sync:** v0.dev auto-push → Vercel deploy

---

## PMO Findings

- Repo is auto-synced from v0.dev — direct commits may be overwritten by v0.dev deploys.
- Game docs are comprehensive: manual, north star, and TODO all present in docs/.
- Contact webhook (`FARM_CONTACT_WEBHOOK_URL`) is optional; fallback logs locally.

---

## Priority Focus

1. Clarify branch/commit ownership vs v0.dev auto-sync before adding manual features.
2. Complete Farm Tycoon Phase 2+ items documented in `docs/FARM-RTS-TODO.md`.
3. Wire contact webhook for production form delivery.

---

## Key Commands

```bash
# Dev (standard Next.js via npm or Docker)
npm run dev    # http://localhost:3000

# Build
npm run build
```

---

## Active PMO

See TASKS.md and ROADMAP.md for current priorities.

---

## Vault Index

*Copied from repo — do not edit these files, overwritten on sync. Edit only this `.md`.*

**Core:** [[repos/farm-3j/ROADMAP|ROADMAP]] · [[repos/farm-3j/TASKS|TASKS]] · [[repos/farm-3j/FEATURES|FEATURES]] · [[repos/farm-3j/METRICS|METRICS]] · [[repos/farm-3j/CHANGELOG|CHANGELOG]] · [[repos/farm-3j/README|README]]

**docs/:** [[repos/farm-3j/docs/Farm_RTS_Game_Manual|Farm RTS Game Manual]] · [[repos/farm-3j/docs/FARM-RTS-NORTH-STAR|North Star]] · [[repos/farm-3j/docs/FARM-RTS-TODO|TODO]] · [[repos/farm-3j/docs/INSTRUCTIONS|Instructions]]
