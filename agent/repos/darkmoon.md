# darkmoon

> Reviewed: 2026-06-25

## Overview

Solo-live 3D browser tag game at darkmoon.dev built with React 19, Three Fiber, Socket.io, and Vite. Solo mode with AI bots is the live experience; multiplayer foundations exist but are not yet deployed. Recently expanded into a full shooter with Deathmatch and Capture the Flag modes.

## Current Goals / Roadmap Focus

**Q2 2026 (active):**
- 21st.dev component integration (lobby, scoreboard, game-over screens) — P1
- UI/UX interactivity improvements (micro-interactions, card layouts) — P1
- Open-source safety scrub (remove sensitive/employer-identifying content) — P1
- Fix Docker production build path — P0
- Align product messaging (docs still overstate live multiplayer) — P0
- Mobile controls + responsive layout validation on real devices — P0

**Q3 2026 (planned):**
- Ship first validated multiplayer-capable experience after readiness gate

**Q4 2026 (exploratory):**
- Identity, progression, social systems
- Native mobile packaging

## Open P0/P1 Tasks

- [ ] **P0** Fix Docker production build path (currently broken)
- [ ] **P0** Align product messaging — README/FEATURES still overstate live multiplayer
- [ ] **P0** Stabilize mobile input and mobile layout on physical devices (iOS Safari + Android Chrome)
- [ ] **P1** 21st.dev component integration — lobby, scoreboard, game-over, nav
- [ ] **P1** UI/UX interactivity improvements (hover states, transitions, Lighthouse no-regress)
- [ ] **P1** Open-source safety scrub — remove/anonymize sensitive examples
- [ ] **P1** Architecture and deployment contract docs (`ARCHITECTURE.md`, `API.md`)
- [ ] **P1** Refresh `METRICS.md` with measured values
- [ ] **P1** Server production-hardening (structured logging, graceful shutdown, operational visibility)
- [ ] **P1** Fix server-side multiplayer tag parity before Multiplayer Tag ships (no cooldown/freeze enforcement, trusts client IDs)
- [ ] **P2** Grenade hold-to-throw + trajectory arc [Phase BM]
- [ ] **P2** Multiplayer shooter polish [Phase E] — aim camera + combat music

Completed: pluggable game modes, combat primitives (Phases B–BL), Deathmatch mode, CTF mode, tag logic edge case tests, bot tag parity fix.

## Blockers

- Docker production build path broken — blocks Docker-first validation
- Server-side multiplayer tag parity must be fixed before Multiplayer Tag exits `[planned]`

## Recent Changes (Unreleased)

- Documentation compliance updates for Overseer integration
- FEATURES.md, TASKS.md, METRICS.md structured
- Vitest bumped 4.0.4 → 4.0.15; react-dom synced to 19.2.3
- Roadmap refactored to quarterly format

Latest gameplay work (from TASKS Done):
- Tag cooldown/freeze edge cases: 8 new tests in `gameManager.edgeCases.test.ts`; `lastTaggedById`-based tag-back cooldown; 200ms `TAG_RETRY_INTERVAL_MS` bot retry
- Full test suite: 378 passed / 5 skipped, lint clean, `tsc --noEmit` clean
