# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
