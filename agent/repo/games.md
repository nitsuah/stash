# games

> Reviewed: 2026-06-25

## Overview

Browser arcade collection at nitsuah-arcade (Netlify) built with Next.js 16, Three.js, and React Three Fiber. Seven complete games: Asteroid Space Shooter, FPS Tank Commander, Breakout, Flappy Bird, Pong, Snake, Space Invaders. 218 unit tests, Playwright E2E, deployed as Next.js runtime on Netlify.

## Current Goals / Roadmap Focus

**Q2 2026 (active):**
- Performance audit and asset optimization (lazy-load audio/sprites; target 3s load on mobile) — P1
- Mobile responsiveness and touch input verification (iOS Safari + Android Chrome) — P1
- Accessibility pass (ARIA labels, keyboard nav, WCAG AA color contrast) — P2
- UX verification pass (first-run walkthrough of all live routes) — P2

**Q3 2026 (planned):**
- Prioritize progression and platform features only after release reliability is stable
- Evaluate additional game work based on evidence

**Q4 2026 (exploratory):**
- Per-game achievement system (localStorage, no backend)
- Federated leaderboard (Netlify Function or Cloudflare Worker, graceful offline fallback)

## Open P0/P1 Tasks

- [ ] **BLOCKED** Global client-side exception debugging — all games fail to load in Docker due to ReferenceError; need browser console logs from Dockerized app
- [ ] **P1** Performance audit and asset optimization — each route within 3s on mobile; large assets lazy-loaded
- [ ] **P1** Mobile responsiveness — Asteroid + ≥2 other games fully playable on iOS Safari + Android Chrome
- [ ] **P2** Accessibility pass — no critical/serious axe-core violations; WCAG AA contrast
- [ ] **P2** UX verification pass — all live routes exercised end-to-end
- [ ] **P2** Re-scope expansion work after platform issues fixed
- [ ] Fix game selection UI for keyboard navigation and automated testing

## Blockers

- **Docker client-side ReferenceError** blocks all game load in Docker — diagnosis step is capturing browser console logs from Dockerized app (last logged step in docs/INSTRUCTIONS.md)

## Recent Changes

- Documentation updates for Overseer compliance
- Asteroid audio startup race fixed (`bgm` readiness-gated on route init)
- Docker-first validation now succeeds locally; CI has dedicated Docker smoke workflow
- Deployment model documented as Next.js runtime on Netlify (not static export)
- Architecture docs (`ARCHITECTURE.md`, `API.md`) added
