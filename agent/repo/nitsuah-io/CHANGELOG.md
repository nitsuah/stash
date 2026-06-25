# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Planned: AI chat widget via bb-mcp (`/api/chat` proxy).
- Planned: Bento grid layout for Projects and Skills sections.
- Planned: Live kryptos cipher-challenge stats in Labs sidebar.
- Planned: skyview privacy-first analytics event sink.
- Planned: `docs/API.md` wagmi hook and chain surface documentation.
- Planned: `docs/INTEGRATIONS.md` cross-repo connection map.

### Changed
- ROADMAP.md expanded through Q4 2026 with AI, PWA, cross-repo, and on-chain resume milestones.
- TASKS.md updated with Q2 P1/P2 tasks for bento grid, AI chat, analytics, and design refresh.
- FEATURES.md extended with Planned Capabilities section (AI, analytics, PWA, cross-repo integrations, on-chain resume).

## [0.3.0] - 2026-04-03

### Added
- Dark mode toggle UI in header with localStorage persistence and hydration-safe rendering.
- Docker test infrastructure with production build strategy for CI/local parity.
- Split Playwright CI strategy: required `CI Fast` and scheduled `Playwright Nightly`.

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