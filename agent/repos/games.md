# games

> Reviewed: 2026-09-23

## Overview

Browser arcade collection at nitsuah-arcade (Netlify) built with Next.js 16, Three.js, and React Three Fiber. Nine live games — the original seven (Asteroid Space Shooter, FPS Tank Commander, Breakout, Flappy Bird, Pong, Snake, Space Invaders) plus two standalone sandboxed-iframe HTML5 games (Memory Match, Dodge Blocks). 482 unit tests (95.41% statement coverage), Playwright E2E, deployed as a Next.js runtime build on Netlify. Current focus is release-path reliability and runtime cleanup rather than new games.

## Current Goals / Roadmap Focus

**2025 Q4 – 2026 Q1** ✅ Completed — live multi-game arcade, Docker release path, CI smoke validation, Netlify hosting model, audio init fixes, architecture docs.

**2026 Q2** ✅ Completed — per `docs/ROADMAP.md`/`docs/TASKS.md` (2026-08-28, the current versions; the repo-root `ROADMAP.md`/`TASKS.md` are stale duplicates still dated 2026-06-08 and still showing these as open). Performance/asset-loading audit, mobile responsiveness + touch input, accessibility audit, and UX verification pass all shipped.

**2026 Q3 (planned):** fix game-selection UI for keyboard/programmatic navigation; add unit/E2E test coverage for Memory Match and Dodge Blocks (iframe-hosted standalone games, not covered by the Jest suite); add high-score persistence to Memory Match (currently just a win alert); add mobile touch controls to Dodge Blocks (keyboard-only today); evaluate further game work only once these are closed.

**2026 Q4 (exploratory):** per-game achievement system (localStorage, no backend); federated leaderboard (Netlify Function/Cloudflare Worker, offline fallback); shared touch-control component (new idea, 2026-08-28) — a reusable on-screen d-pad/button component rather than a one-off for Dodge Blocks. Not started.

## Open P0/P1 Tasks

None open. The two former P1 items — performance/asset-optimization audit and mobile responsiveness/touch input — are complete per `docs/TASKS.md` (2026-08-28, current; supersedes the stale root-level `TASKS.md` dated 2026-06-08 which still shows them open), along with the P2 accessibility and UX verification passes. Remaining open items are P2/P3 or untagged: fix game-selection keyboard nav, add unit/E2E tests for Memory Match/Dodge Blocks (P2), add high-score persistence to Memory Match (P3), add mobile touch controls to Dodge Blocks (P3).

## Blockers

None. The previously-flagged **[BLOCKED]** global client-side `ReferenceError` preventing games from loading in Docker is confirmed **[RESOLVED]** in `docs/TASKS.md` (2026-08-28). Note the repo has two copies of TASKS.md/ROADMAP.md: the repo-root files are stale (last updated 2026-06-08, still show the blocker and Q2 items open) while `docs/TASKS.md`/`docs/ROADMAP.md` are current — treat the `docs/` versions as authoritative going forward.

## Recent Changes (Unreleased)

- **Two new games**: Memory Match (`/memory-match`) and Dodge Blocks (`/dodge-blocks`) — standalone HTML5 games embedded via sandboxed iframe, bringing the collection from 7 to 9 games; documented across README.md, FEATURES.md, ARCHITECTURE.md, API.md (which hadn't been updated when these originally shipped).
- Unit test suite grown to 482 passing tests (from 218 at the 1.0.0 tag).
- Arcade cabinet (`ArcadeLayout`) fixes: no longer clips its neon hood/title or joystick/buttons/coin-slot console on tablet/mobile portrait; non-fullscreen pages now scroll instead of clipping; fixed a mobile `width: 100vw` overflow bug, a mobile breakpoint that grew the title instead of shrinking it, and a missing sub-768px breakpoint on the 3x3 game grid; two-line game titles no longer get clipped.
- Press feedback (`:active` states) and a click sound added to the cabinet's decorative console buttons/joystick, plus a cosmetic wear/scuff overlay.
- Deduplicated a corrupted, triplicated `.github/dependabot.yml` and corrected its npm `directory` to `/app`.
- Documentation audit pass (2026-08-22): corrected game count (9, not 7), unit test count (482, not 218), coverage (95.41%), and dependency versions across README.md, FEATURES.md, ROADMAP.md, TASKS.md, METRICS.md, docs/API.md.

## Verified Runbook (PMO 2026-09-24)

> Commands verified during the 2026-09-24 PMO audit (`agent/reports/pmo-audit-2026-09-24.md` §7). **obn-review: keep this section when refreshing the summary.**

- `docker build --target test-unit -t games-test . && docker run --rm games-test npm run test:coverage`. Leave out `-it` for non-interactive runs.
- Right now a non-zero exit means the coverage threshold failed, not that a test failed. It's 61.09% against a 75% threshold, because `lib/tank/TankGame.jsx` (837 lines) is at 0%.
