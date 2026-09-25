# Changelog

> 🧭 [games](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · **Changelog** · [Metrics](./METRICS.md) <!-- nav -->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Maintenance (2026-09)

- Tank Battle logic extracted to tested `lib/tank/tankLogic.js`; coverage restored above the 75% threshold and `test:ci` now runs `--coverage` so CI enforces it (#341, #342).
- Coverage now counts TypeScript, audio and asteroid UI: 1017 tests / 98.58% statements, CI threshold raised to 85%; 5 edge-case bugs fixed along the way (#343).
- Removed the dead React Three Fiber Breakout implementation (#344).
- Security: patched `sharp` and `js-yaml` (#335). React / React DOM 19.3.0 and `@react-three/fiber` 9.8.0 (#340); Lighthouse CI action 12.6.2 (#329); grouped minor/patch bumps (#330, #334, #337).
- Planning docs reset for 2027 (`pmo-ff`): completed roadmap/TASKS items condensed into FEATURES/CHANGELOG, open 2026 Q3/Q4 items carried into 2027 Q1, breadcrumb navigation + README docs index added.

### Added

- Documentation updates for Overseer compliance (FEATURES.md, CHANGELOG.md)
- **Memory Match** (`/memory-match`) and **Dodge Blocks** (`/dodge-blocks`): two
  standalone HTML5 games embedded via sandboxed iframe, bringing the collection
  to 9 games. Documented in README.md, FEATURES.md, ARCHITECTURE.md, and API.md,
  which had not been updated when these shipped.
- Unit test suite grown to 482 passing tests (previously 218 at the 1.0.0 tag);
  README.md and FEATURES.md corrected to match.
- Press feedback (button/joystick `:active` states) and a quiet click sound on
  the arcade cabinet's decorative console buttons and joystick, plus a subtle
  cosmetic wear/scuff overlay on the cabinet frame.
- Unit coverage now counts `.ts/.tsx` files and `contexts/` (previously only
  `.js/.jsx`). 507 new tests cover the TS game components (Breakout, Flappy,
  Space Invaders), shared physics/progression/scoring/combat, the audio layer,
  asteroid weapons/collisions/power-ups/UI, shared controls and contexts:
  1017 tests, 98.58% statements / 92.2% branches. CI threshold raised to 85%.

### Fixed

- Asteroid laser hits now spawn their impact effect at the target; the hit
  test mutated the target position into a unit direction vector first.
- `ProximityWarning` no longer re-renders endlessly when rendered without
  `playerPosition`, and no longer recomputes on every parent render.
- `SettingsMenu` merges saved settings over defaults, so older partial saves
  no longer show `NaN` and a stored `"null"` no longer crashes the menu.
- `LivesManager`/`WaveManager` honour explicit `0` config values instead of
  silently replacing them with defaults.

- Arcade cabinet (`ArcadeLayout`) no longer clips its neon hood/title or its
  joystick/buttons/coin-slot console when the cabinet is taller than the
  viewport — routine on tablet and mobile portrait widths. Non-fullscreen
  pages (home, snake, flappy, memory-match, dodge-blocks) now scroll instead
  of clipping; fullscreen game pages keep their original fixed layout.
- Cabinet frame, marquee title, and the 3x3 game grid no longer overflow the
  viewport edges on tablet/mobile widths (several independent CSS bugs: a
  mobile `width: 100vw` override wider than its parent, a mobile breakpoint
  that grew the title instead of shrinking it, and a game grid with no
  breakpoint below 768px).
- Two-line game titles (e.g. "Tank Battle") no longer get clipped by a
  fixed-height card and read as overlapping the row below.
- Deduplicated a corrupted, triplicated `.github/dependabot.yml` and corrected
  its npm `directory` to `/app` (the repo has no root `package.json`).

### Changed

- Documentation audit pass (2026-08-22): corrected game count (9, not 7), unit test count (482, not 218), coverage (95.41%), and dependency versions across README.md, FEATURES.md, ROADMAP.md, TASKS.md, METRICS.md, docs/API.md
- **Memory Match**: documented existing vanilla JS card-matching game served via iframe at `/memory-match` (existing route, not a new addition)
- **Dodge Blocks**: documented existing vanilla JS canvas dodge game served via iframe at `/dodge-blocks` (existing route, not a new addition)

## [1.0.0] - 2025-11-25

### Added

- **7 Complete Arcade Games**: Asteroid Space Shooter, FPS Tank Commander, Breakout Classic, Flappy Bird, Pong, Snake, and Space Invaders
- **Comprehensive Testing**: 218 unit tests with ~85% code coverage
- **E2E Testing**: 8 Playwright test scenarios covering complete game flows
- **CI/CD Pipeline**: GitHub Actions workflow with linting, testing, and E2E checks
- **Netlify Deployment**: Automated production deployments with preview branches
- **Lighthouse Audits**: Automated performance and accessibility monitoring
- **Shared Physics System**: Collision detection, spatial partitioning, and elastic collision calculations
- **Arcade UI Components**: Reusable ArcadeButton, ArcadeCard, ArcadeHeader, and ArcadeMenu components
- **High Score Tracking**: LocalStorage-based score persistence across all games
- **Sound System**: Comprehensive sound effects and music for all games
- **Accessibility Features**: Keyboard navigation, ARIA labels, 100/100 Lighthouse A11y score
- **Pre-commit Hooks**: Husky integration for automated linting and formatting

### Changed

- Migrated several components to TypeScript for better type safety
- Improved game loop performance across all games
- Enhanced visual feedback for power-ups and game events
- Consolidated documentation (removed outdated planning docs)

### Fixed

- TypeScript type issues in GameCarousel component
- Enhanced useEffect documentation in game components
- Extracted magic numbers to named constants for better maintainability

## [0.3.0] - 2025-11 (Phase 9-10)

### Added

- **Breakout Classic**: Complete brick-breaking game with power-ups and wave progression
- **Flappy Bird**: Procedural pipe generation with physics-based flight
- **Pong**: AI opponent with adjustable difficulty
- **Snake**: Classic snake mechanics with progressive difficulty
- **Space Invaders**: Formation enemies with wave progression and defensive shields
- Test coverage for new games
- Shared UI component library

### Changed

- Refactored shared systems for reusability across games
- Improved collision detection performance with spatial grid
- Enhanced arcade aesthetic consistency across all games

### Fixed

- Target velocity refactoring in Asteroid game
- Collision physics improvements across all games

## [0.2.0] - 2025-10 (Phase 6-8)

### Added

- **FPS Tank Commander**: First-person tank game with Tokyo drift physics
- Power-up system for FPS game (health, shield, weapon upgrades)
- Dynamic terrain and destructible targets
- E2E testing framework setup

### Changed

- Improved physics engine for more realistic behavior
- Enhanced visual effects for explosions and particle systems

### Fixed

- Performance optimizations for particle rendering
- Memory leak fixes in game cleanup

## [0.1.0] - 2025-09 (Phase 1-5)

### Added

- **Asteroid Space Shooter**: 6DOF space shooter with physics-based combat
- Multiple weapon types (Spread, Laser, Explosive)
- Six power-up types (Health, Shield, Invincibility, Rapid Fire, Slow Motion, Speed Boost)
- Wave management system with progressive difficulty
- Basic collision detection and physics
- Initial sound effects and music
- Next.js 15 project setup with Three.js and React Three Fiber
- Basic arcade UI styling with neon aesthetic

### Changed

- Initial project architecture and structure

### Fixed

- Initial bug fixes and performance improvements

---

**Legend**:

- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements
