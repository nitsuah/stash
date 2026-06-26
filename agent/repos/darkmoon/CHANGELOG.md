# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Documentation compliance updates for Overseer integration
- Comprehensive FEATURES.md documenting all game features
- Structured TASKS.md with phased development plan
- METRICS.md with repository health tracking

### Changed

- Refactored ROADMAP.md to quarterly format with checkboxes
- Bumped vitest from 4.0.4 to 4.0.15
- Bumped @vitest/coverage-v8 from 4.0.4 to 4.0.15
- Synced react-dom to 19.2.3 to match react version

## [1.0.0] - 2025-11-23

### Added

- **Multiplayer 3D Tag Game**: Real-time multiplayer gameplay with Socket.io
- **Solo Mode with AI Bots**: Practice mode with intelligent bot opponents
- **React Three Fiber**: 3D scene rendering with Three.js
- **Desktop Controls**: WASD movement, mouse camera, jetpack mechanics
- **Mobile Controls**: Virtual joystick and touch buttons
- **Dark Mode**: System preference detection with manual toggle
- **CI/CD Pipeline**: GitHub Actions with automated testing and deployment
- **Test Suite**: Vitest + React Testing Library (41 test files, 302 test cases)
- **Code Quality Tools**: ESLint, Prettier, TypeScript strict mode
- **Pre-commit Hooks**: Husky + lint-staged for quality gates
- **WebSocket Server**: Express + Socket.io with health check endpoint
- **Netlify Deployment**: Automated deployment with CDN delivery

### Technical Details

- React 19.2.0 with TypeScript
- Vite 7.1.12 for fast builds and HMR
- Socket.io 4.8.1 for real-time communication
- Three.js 0.180.0 for 3D graphics
- Comprehensive test coverage with Vitest

## [0.1.0] - 2025-10-15

### Added

- Initial project setup
- Basic multiplayer lobby system
- 3D character models (astronaut theme)
- Collision detection system
- Tag game mechanics

---

**Note**: Dates are approximate based on commit history. For detailed commit history, see [GitHub commits](https://github.com/nitsuah/darkmoon/commits).
