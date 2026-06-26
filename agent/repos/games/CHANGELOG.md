# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Documentation updates for Overseer compliance (FEATURES.md, CHANGELOG.md)

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
