# farm-3j

> Reviewed: 2026-09-23 (no material change since 2026-09-16 PMO audit — see [[pmo-audit-2026-09-16]])

## Overview

"PG Farms" (site rebranded from "Farm 3J RTS Prototype") — an interactive farm website (v0.dev / Vercel) built with Next.js 16, TypeScript, Tailwind CSS v4, and pnpm 9. Centerpiece is a full-featured isometric Farm RTS game (`/rtsfarm/play`, SVG-rendered, Warcraft II/AoE II-inspired) with workers, combat units, buildings, enemy waves, a hero unit, fog of war, and tech upgrades; also has an animated homepage and a legacy Farm Tycoon simulation (`/farm`, on hold). Cloud saves/high scores are backed by Neon Postgres with localStorage fallback. 440 Vitest tests across `lib/`, `components/`, and RTS domain hooks.

## Current Goals / Roadmap Focus

**2026 Q1** ✅ Completed — core Next.js architecture, Farm Tycoon Phase 1 MVP, Phase 2a–2f isometric grid.

**2026 Q2–Q3: Farm RTS MVP** ✅ Feature-complete — 25×25 map, 10+ enemy unit types, full economy/combat/building loop, fog of war, day/night cycle, hero unit, 20+ buildings, unit veterancy, tech research, save/load, procedural audio, high-score leaderboard. Modularization Phases 1, 2a, and 2b all complete (`RTSUI`, `useGameLoop`, and `RTSMap`'s SVG render tree all decomposed into focused modules/hooks).

**2026 Q3: Farm RTS — Round 2** (active)
- Technical health: [x] blacksmith upgrade costs extracted to shared constants; [ ] continued SVG component extraction (worker/enemy/building shapes); [ ] render-loop profiling at 30+ units; [ ] unit tests for `tileDist`/`tileToSvg`/A* pathfinding
- Gameplay: [x] cloud save slots (Neon-backed, 3 slots); [ ] named unit formations; [ ] enemy hero (Warlord); [ ] dropped hero items; [ ] achievement/challenge system; [ ] campaign mode Phase 1
- Content & polish: [ ] ambient audio loop; [ ] more voice lines/audio cues; [ ] minimap shows dropped items/loot crates; [ ] farmers always render in front of barn and stay selectable

**2026 Q4 (planned): Product and Content Surface**
- Product gallery/catalog, blog/news path, ecommerce phase 1, subscription evaluation, accessibility/SEO hardening — none started

**Legacy Tycoon Tasks (on hold):** animal needs loop, feeding mechanics, fence placement/terrain editing, save/load, full Docker gameplay validation

## Open P0/P1 Tasks

None open (updated 2026-09-25). The old P0 "Complete all Farm RTS MVP milestones" is gone from `docs/TASKS.md` after the 2027 Q1 planning reset. Its unfinished sub-todos now sit, untagged, under "Farm RTS — Round 2 (2027 Q1)": for example "Add buttons to train animal units from Barn", core-helper unit tests (`tileDist`, `tileToSvg`, A* pathfinding) and campaign mode Phase 1.

## Blockers

None documented. Coverage % is currently untrustworthy rather than blocking: METRICS.md notes the 2026-09-02 Docker/bind-mount coverage run produced an empty `coverage-final.json` (v8 provider attribution failure) and needs a clean re-run. **Re-confirmed still broken on 2026-09-16** (PMO audit re-ran `test:docker`/`test:coverage`): same 0%-across-the-board report despite 440/440 tests passing. Two audits in a row now without a fix attempt — worth a dedicated ticket if a real coverage number becomes a reporting requirement.

## 2026-09-16 PMO Audit

Docs (README/ROADMAP/TASKS/FEATURES/METRICS) were current and accurate — no contradictions found, nothing needed beyond a metrics refresh. `scripts/run-in-docker.js test:coverage` re-run: 440/440 tests passed in ~14s (was ~35s on 2026-09-02 — same test count, faster this run). Filled in previously-`TBD` Open Issues (0, via `gh issue list`) and reconfirmed the coverage bug above. PR: [nitsuah/farm-3j#340](https://github.com/nitsuah/farm-3j/pull/340) (initial push failed CI on `prettier --check`; fixed with a follow-up `pnpm run format` commit, all checks green after).

## Recent Changes (Unreleased)

- **PG Farms rebrand** — site renamed from "Farm 3J RTS Prototype"; new `/rtsfarm` feature landing page (mechanics/unit/enemy/building rosters); actual game moved to `/rtsfarm/play`
- **Cloud save system** — anonymous device UUID + Neon Postgres backend (`@neondatabase/serverless`); hybrid persistence (sync localStorage + fire-and-forget cloud writes); `/api/saves` and `/api/highscores` edge routes
- **Privacy & Security page** (`/privacy`) documenting the data policy
- **Garrison barn HP regen** — garrisoned units heal the barn 4 HP/tick
- Fixed: grunts could damage the barn from any distance after a far attack (now range-checked); save-slot API validation hardened; high-score field alignment with DB schema; async high-score loading with localStorage fallback; inaccurate privacy-page cross-device claim removed
- Accessibility: homepage feature cards switched from `<div onClick>` to proper `<button aria-expanded aria-controls>`
- **RTS code modularization** — `RTSUI` (2110 lines) decomposed into `BuildMenu`/`WaveTimer`/`HeroPanel`/`BaseTab`/`BuildTab`/`TrainTab`/`TechTab`; background animation extracted; combat/spawn/map-selector helpers extracted and unit-tested; +55 tests (264 → up further to 440 total with later RTS coverage expansion)
