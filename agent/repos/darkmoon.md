---
kind: repo-hub
repo: darkmoon
---

# darkmoon

> Reviewed: 2026-09-23

## Overview

Solo-live 3D browser combat game at darkmoon.dev built with React 19, Three Fiber, Socket.io, and Vite. Solo mode with AI bots (Deathmatch, CTF, Tag) is the live experience; multiplayer foundations and a readiness gate exist but the deployed experience is still solo-first.

## Current Goals / Roadmap Focus

**2025 Q4 + "Beyond scope" combat phases (BC–BM): Complete.** Browser-game foundation, Deathmatch/CTF modes, weapon reload system, bot LOS/angular-spread AI, mouse-aimed firing, grenade hold-to-throw, GameUI/Solo.tsx componentization.

**2026 Q1: Complete.** Docker production build fixed; README/FEATURES messaging aligned with solo-first reality.

**2026 Q2: Mostly complete.**
- [x] Multiplayer readiness gate (deployment, CORS, logging, observability — all 4 criteria pass, PR #418)
- [x] `ARCHITECTURE.md` + `API.md` added
- [x] `METRICS.md` refreshed with measured values (71.18% stmts / 659 test cases, 2026-08-28)
- [ ] 21st.dev component integration (lobby, scoreboard, game-over) — CEO priority, not started, carried to 2027
- [ ] UI/UX interactivity pass — CEO priority, not started, carried to 2027
- [ ] Open-source safety scrub — CEO priority, not started, carried to 2027
- [ ] Re-scope remaining refactor backlog against current codebase

**2026 Q3 (in progress):** Ship first validated multiplayer-capable experience — readiness gate and server-side tag parity are both done (2026-09-11); no known blocker left on this goal. New: CORS wildcard/allowlist operator doc (not started).

**2026 Q4 (exploratory):** Identity/progression/social systems; native mobile packaging.

**2027 (scoped, not started):** 21st.dev + UI/UX pass, open-source safety scrub, aim camera + combat music (Phase E remaining), crosshair-vs-aim-point-under-pointer-lock fix (needs a design decision). (`docker-compose` `test`-service stale-image issue — fixed 2026-09-11, see Recent Changes.)

## Open P0/P1 Tasks

No open P0 items — Docker build, product messaging, and mobile-input stabilization all shipped.

- [ ] **P1** 21st.dev component integration — lobby, scoreboard, game-over, nav
- [ ] **P1** UI/UX interactivity improvements (hover states, transitions, Lighthouse no-regress)
- [ ] **P1** Open-source safety scrub — remove/anonymize sensitive examples

**Shipped since last review:** server-side multiplayer tag parity (2026-09-11) — cooldown/freeze enforcement (`TAG_BACK_COOLDOWN_MS`/`TAG_FREEZE_MS` ported into `server/tagAuthorization.js`) and IT-disconnect handoff (new `resolveItHandoff` in `server/itHandoff.js`, reassigns or ends the round) are both in; TASKS.md now marks this P1 done. This was the last blocker for Multiplayer Tag to exit `[planned]` in FEATURES.md — worth checking whether that flip has happened.

## Blockers

None currently tracked — the multiplayer tag-parity blocker cleared 2026-09-11 (see Recent Changes).

## Recent Changes (Unreleased)

- Shipped (2026-09-11): server-side multiplayer tag parity — see Open P0/P1 Tasks note above; new tests in `src/__tests__/server.tagAuthorization.test.ts` and `src/__tests__/server.itHandoff.test.ts`, full Docker suite green
- Fixed (2026-09-11): `.husky/pre-push` was silently validating a stale Docker test image — `config/docker-compose.yml`'s `test` service has no bind mount (unlike `solo`), so `docker compose run` without `--build` reused whatever `darkmoon-test:latest` image already existed locally; caught when a 41-hour-stale image reported different vitest/test-count output than a freshly built one for the same commit. Fixed by adding `--build` to both the real and Docker-missing-fallback command paths in `.husky/pre-push`.
- Multiplayer readiness gate (PR #418): structured JSON logging (`server/logger.js`), shared HTTP/WebSocket CORS allowlist (`server/cors.js`), `/health` and `PORT` validation modules, `player-tagged` authorization binding to the authenticated socket, SIGTERM graceful shutdown, 96 new server tests
- Mobile controls overhaul (PR #417): reworked touch joystick, aim assist, responsive HUD
- Fixed: CORS wildcard matcher escaping + single-DNS-label scoping; bare `ALLOWED_ORIGINS=*` no longer combines with `credentials: true`
- Fixed: downed player could still move (movement/jump/jetpack now frozen during respawn wait)
- Fixed: grenade charge (was bound to right-click) and throw (left-click) now consolidated onto left-click
- Fixed: rocket/grenade splash damage missing in Tag mode, including when the IT player lands the direct hit
- Fixed: mobile joystick camera vertical-axis inversion relative to desktop mouse-look
- Fixed: desktop jetpack double-jump (second SPACE press while airborne) now mirrors the mobile double-tap flow
- Fixed: home page bottom cards clipped on desktop (`.App { overflow: hidden }` outranked the mobile-only scroll fix)
- Docs: METRICS.md refreshed with measured values, README test-count staleness corrected, `docs/ROADMAP_DETAILED.md` archived, `docs/TECH_DEBT.md` updated

<!-- vault-links:start -->
## Vault links

_Generated by `scripts/build-vault-indexes.py`; edits inside this block are overwritten._

- Docs: [[repos/darkmoon/README|README]] (every doc hangs off its Docs Index)
- Overview: [[projects/KB/darkmoon-overview|KB overview]]
- Latest LOC report: [[reports/eng-loc-darkmoon-2026-09-16|2026-09-16]] (older ones chain from it)
- Latest MINI report: [[reports/eng-mini-darkmoon-2026-09-16|2026-09-16]] (older ones chain from it)
<!-- vault-links:end -->
