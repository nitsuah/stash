# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **PG Farms branding** — site renamed from "Farm 3J RTS Prototype" to "PG Farms"; desktop/mobile header updated; hero button renamed "Play RTS"
- **RTS feature landing page** (`/rtsfarm`) — mechanics grid, unit roster (6 units), enemy roster (11 types), buildings grouped by Economy/Military/Defense; actual game moved to `/rtsfarm/play`
- **Privacy & Security page** (`/privacy`) — data policy covering localStorage, cloud saves, device ID, and contact; linked from desktop and mobile nav
- **Cloud save system** — anonymous device UUID (localStorage) identifies saves; Neon Postgres backend via `@neondatabase/serverless`; hybrid persistence: synchronous localStorage for game loop + fire-and-forget cloud writes; `/api/saves` (GET/POST/DELETE) and `/api/highscores` (GET/POST) edge routes; `scripts/db-init.sql` schema with migration block; `lib/db.ts` Neon client; `lib/api-types.ts` shared payload interfaces (`HighScorePostBody`, `HighScoreRow`, `isValidSaveSlot`)
- **Garrison barn HP regen** — each garrisoned unit heals barn 4 HP/tick; `GARRISON_BARN_HEAL_PER_UNIT` constant; floating `+N❤️` text

### Fixed

- **Grunt far-attack barn bug** — grunts stuck in `attacking` state after destroying a building could damage the barn from any distance; now checks `tileDist ≤ GRUNT_BARN_MELEE_RANGE` (2.0 tiles) before scheduling damage, re-paths if too far
- **Garrison regen rate** — `GARRISON_HEAL_AMOUNT` raised from 5 → 8 HP/tick
- **API slot validation** — GET and DELETE `/api/saves` handlers now reject slot values outside 0–2 (including partial-parse strings like `"1abc"`) via `Number()` + `isValidSaveSlot`; POST `/api/saves` gains try/catch for malformed JSON
- **High-score field alignment** — `HighScoreEntry` type (`result`, `gold`, `time`, `date`) now matches DB schema and API response; removed stale `player_name`/`difficulty_id` columns from `high_scores` table
- **GameOverOverlay async scores** — high scores now loaded via `useState`/`useEffect` + `loadHighScores()` with synchronous localStorage fallback; cloud scores appear after resolve
- **Privacy page accuracy** — removed "preserved across devices and browser resets" claim; clarified cloud saves require the browser-local UUID to be present

### Changed

- **Feature cards** (homepage) — `<div onClick>` replaced with `<button aria-expanded aria-controls>`; content div always mounted (hidden when collapsed) so `aria-controls` target is always present; animated children still unmount inside to stop timers
- **`GRUNT_BARN_MELEE_RANGE`** extracted from inline constant to `constants.ts`; `HeroPanel` magic `3` replaced with `HERO_MAX_ITEMS`; `tome_xp` Use button disabled (no handler); `WaveTimer` prop typed as `RefObject` not `MutableRefObject`
- **Dark-mode footer** — green → black in `SiteLayout`

### Refactored

- **RTS code modularization** — broke down the largest files into focused modules:
  - `RTSUI` (2110 lines) fully decomposed into `ui/BuildMenu`, `ui/WaveTimer`, `ui/HeroPanel`, `ui/BaseTab`, `ui/BuildTab`, `ui/TrainTab`, `ui/TechTab`, `ui/buildMenuHelpers` sub-components and helpers; all type/constant re-exports preserved for backward compat
  - `HeaderCropRow` background animation extracted to `animations/AnimatedBackground.tsx`
  - Pure combat/spawn helpers extracted to `spawnHelpers.ts` and `towerHelpers.ts`; map-state queries extracted to `game/mapSelectors.ts` — all immediately unit-tested
  - Domain-specific hook shells scaffolded (`useEnemyAI`, `useResourceTick`, `useCombatResolution`, `usePathfinding`) and `MapRenderer` shell created as migration targets for `useGameLoop` and `RTSMap` in follow-on PRs
- **Unit test coverage expanded** — +55 tests (264 total, up from 209) covering all newly extracted pure functions: spawn calculations, tower damage math, range queries, map selectors; silent-failure fixes in `WaveTimer` and `BuildMenu`

### Added

- **Farm Tycoon Phase 1 MVP**: Complete interactive farm simulation game
  - State management with React Context and useReducer
  - 60 FPS game loop with requestAnimationFrame
  - 4 animal types (cow, chicken, pig, sheep) with movement AI
  - Resource production system (milk, eggs, meat, wool)
  - Economic system (buy animals, sell resources)
  - Day/night cycle with dynamic sky gradients
  - Maintenance system (fence repair, animal healing)
  - Toast notification system
  - Tutorial overlay with 5-step onboarding
  - Keyboard shortcuts (Space/P, R, H, ?)
  - Bulk selling with "Sell All" buttons
  - Performance optimizations (React.memo, useMemo, useCallback)
- **Farm Tycoon Phase 2a-f**: Isometric grid foundation
  - Isometric coordinate transformation utilities
  - Grid-based terrain system with 4 tile types (grass, pasture, dirt, pond)
  - Visible fence entities with health indicators and perimeter
  - Editor sidebar with 3 modes (Build, Animals, Select)
  - Build panel for placing structures (fences, troughs)
  - Animal panel for grid-based spawning
  - Click-to-place interaction system with snap-to-grid
  - Hover indicator for placement preview
  - Grid overlay toggle
  - Escape key to cancel placement
- Implemented basic contact form structure
- Added initial styling for a clean and responsive layout

### Changed

- Refactored form submission logic for improved reliability
- Migrated to Tailwind CSS v4 with new @import syntax
- Updated ground rendering from solid background to isometric tiles
- Replaced duplicate animal spawning buttons with unified panel system

### Fixed

- Resolved minor styling issues on mobile devices
- Fixed TypeScript strict mode errors (generic types for Partial, Array)
- Fixed useState import positioning in notifications.ts
- Fixed pre-commit hook formatting issues

### Deprecated

### Removed

### Security

## [0.1.0] - YYYY-MM-DD

### Added

- Project initialization

[Unreleased]: https://github.com/nitsuah/farm-3j/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/nitsuah/farm-3j/releases/tag/v0.1.0
