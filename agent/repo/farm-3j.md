# farm-3j

> Reviewed: 2026-06-25

## Overview

Interactive farm website (v0.dev / Vercel) built with Next.js 15, TypeScript, and Tailwind CSS v4. Features an animated homepage with weather effects/day-night cycle and a Farm Tycoon isometric simulation game. Currently pivoting focus to a Farm RTS MVP.

## Current Goals / Roadmap Focus

**Q2–Q3 2026 (active):** Farm RTS MVP
- Complete all MVP milestones from `docs/Farm_RTS_Game_Manual.md` and `docs/FARM-RTS-TODO.md`
- Core systems: map, camera, resource, worker, building, win/lose
- Stretch: combat, AI, upgrades, polish
- Progress: Milestone 1 (map/camera) complete; Milestone 3 (resource node depletion/feedback) complete

**Q4 2026 (planned):** Product and Content Surface
- Product gallery and catalog improvements
- Blog/news publishing path
- Ecommerce phase 1
- Accessibility and SEO hardening
- Fog of war (tile visibility by unit/building vision radius)
- Unit formation commands (line, wedge, box)

**Legacy Tycoon Tasks (on hold):**
- Animal needs loop, feeding mechanics, fence placement, save/load

## Open P0/P1 Tasks

- [ ] **P0** Complete Farm RTS MVP — all core gameplay systems playable and validated in Docker
  - Remaining unfinished todos:
    - [ ] Add stone resource nodes
    - [ ] Add animal units (chickens, cows, pigs) with grazing AI
    - [ ] Implement grazing logic and food meter
    - [ ] Enable building placement on valid tiles
    - [ ] Ensure farmers render in front of barn and are always selectable
    - [ ] Add box selection for multiple units
    - [ ] Lay groundwork for control groups
    - [ ] Add buttons to train animal units

## Blockers

None documented. Farm RTS is the single active focus; Tycoon work deferred.

## Recent Changes (Unreleased)

- Farm Tycoon Phase 1 MVP: 60 FPS game loop, 4 animal types, resource production, economic system, day/night cycle, tutorial overlay, keyboard shortcuts
- Farm Tycoon Phase 2a–f: isometric grid foundation, grid-based terrain (4 tile types), visible fence entities, editor sidebar with Build/Animals/Select modes, click-to-place, hover indicator
- Tailwind CSS v4 migration with new `@import` syntax
- Contact form: `POST /api/contact`, optional `FARM_CONTACT_WEBHOOK_URL`
