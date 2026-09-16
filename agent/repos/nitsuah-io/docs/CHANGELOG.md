# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Home page redesigned as a focused landing page (`LandingHero` + `FeaturedProjects`) surfacing top projects (agent-board, overseer, bb-mcp, darkmoon) above the fold.
- Dedicated `/3d` route for the Spline experience, moved off the home page to cut critical-path bundle weight and improve LCP.
- Planned: AI chat widget via bb-mcp (`/api/chat` proxy).
- Planned: Bento grid layout for Projects and Skills sections.
- Planned: Live kryptos cipher-challenge stats in Labs sidebar.
- Planned: skyview privacy-first analytics event sink.
- Planned: `docs/API.md` wagmi hook and chain surface documentation.

### Changed
- ROADMAP.md expanded through Q4 2026 with AI, PWA, cross-repo, and on-chain resume milestones.
- TASKS.md updated with Q2 P1/P2 tasks for bento grid, AI chat, analytics, and design refresh.
- FEATURES.md extended with Planned Capabilities section (AI, analytics, PWA, cross-repo integrations, on-chain resume).
- Top-level docs consolidated under `docs/`, with completed handoffs and resolved trackers moved to `docs/archive/`.

### Fixed
- `npm run test:e2e:docker` (`config/docker-compose.test.yml`) was missing `--config config/playwright.config.ts` on its `playwright test` command, so it silently fell back to zero-config test discovery and crashed on the Jest files under `src/**/__tests__/` (`ReferenceError: describe is not defined`). Found while refreshing `docs/METRICS.md`.

### Verified (2026-09-01)
- Audited Q2 roadmap items against the codebase: none have shipped yet (AI chat, bento grid, Mumbai→Amoy migration, kryptos/skyview widgets, `docs/API.md`). They remain open in `docs/TASKS.md`.
- `docs/INTEGRATIONS.md` was already complete (shipped alongside 0.3.0) but still listed as an open task — removed the stale duplicate.
- Playwright Docker image and `@playwright/test` remain in lockstep (`v1.62.1`).
- Re-ran the full test suite in Docker: Jest 214/214 passing (97.21% stmt coverage, up from 213/98%); Playwright 11/20 passing with 9 intentionally skipped (wallet-connection tests, gated pending a local wallet mock). `docs/METRICS.md`'s previously published "Resume Tests" and "Visual Tests" rows no longer correspond to any spec file in the repo and were removed.

## [0.3.0] - 2026-04-03

### Added
- Dark mode toggle UI in header with localStorage persistence and hydration-safe rendering.
- Docker test infrastructure with production build strategy for CI/local parity.
- Split Playwright CI strategy: required `CI Fast` and scheduled `Playwright Nightly`.
- Cross-repo integration map (`docs/INTEGRATIONS.md`) documenting planned connections to bb-mcp, kryptos, skyview, motor-pool, farm, and darkmoon.

### Changed
- Playwright Docker image coordinated with npm `@playwright/test` version.
- Centralized configuration under `config/` directory.
- Comprehensive `.dockerignore` for optimized Docker context.

### Fixed
- Hydration mismatch in theme toggle prevented by mounted-state guard.
- Visual regression baselines regenerated to match production build output.

## [0.2.0] - 2025-12-15

### Added
- Web3 integration: wagmi v2, viem v2, ConnectKit wallet connector.
- Multi-chain support: Ethereum mainnet, Polygon, Sepolia.
- Labs section: ENS domain registration, NFT minting, token staking, DAO governance, AI oracle.
- Accessibility: WCAG 2.1 AA compliance with axe-core automated checks.
- Playwright E2E and visual regression test suite (59 tests).
- Resume PDF mode with print-optimized layout.

### Changed
- CSS architecture migrated to CSS custom properties design token system.
- Dark mode theme system with full token coverage.

## [0.1.0] - 2025-09-01

### Added
- Project initialization with Next.js 16 App Router and TypeScript.
- Initial portfolio structure: home, projects, crypto, resume, about pages.
- Spline 3D hero scene integration.
- Jest unit test suite (213 tests, 98% coverage).
- GitHub Actions CI pipeline (build, lint, typecheck, tests).
- Netlify deployment with deploy previews.

[Unreleased]: https://github.com/Nitsuah-Labs/nitsuah-io/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/Nitsuah-Labs/nitsuah-io/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/Nitsuah-Labs/nitsuah-io/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Nitsuah-Labs/nitsuah-io/releases/tag/v0.1.0