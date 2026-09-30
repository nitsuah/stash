---
up: "[[repos/nitsuah-io]]"
title: "nitsuah-io · CHANGELOG"
source: https://github.com/Nitsuah-Labs/nitsuah-io/blob/main/docs/CHANGELOG.md
kind: repo-doc
repo: nitsuah-io
---

# Changelog

> 🧭 [nitsuah-io](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · **Changelog** · [Metrics](./METRICS.md) <!-- nav -->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `docs/API.md`: server routes (`/sw.js`, robots, sitemap, proxy middleware), page metadata via `pageMetadata()`, the wagmi config (chains, connectors, test-mode mock), generated contract hooks, Labs contract addresses and app hooks (TASKS P2).
- Per-page metadata: every route has its own title, description, canonical URL and Open Graph/Twitter card (`src/lib/seo.ts` plus a server `layout.tsx` per route); `/profile`, `/logout` and the WIP Labs pages are `noindex`. `src/__tests__/seo.test.ts` enforces it, and `tests/runtime.spec.ts` checks the rendered canonical and `og:image` against `next start`.
- `public/og-image.jpg` (1200×630) social card and a 180×180 `apple-icon.png`.
- Sitemap lists all 11 published blog posts.
- Home page redesigned as a focused landing page (`LandingHero` + `FeaturedProjects`) surfacing top projects (agent-board, overseer, bb-mcp, darkmoon) above the fold.
- Dedicated `/3d` route for the Spline experience, moved off the home page to cut critical-path bundle weight and improve LCP.
- `scripts/check-playwright-lockstep.js`, wired into `precheck:docker` and CI, fails the build if `config/Dockerfile.test`'s Playwright image tag drifts from the installed `@playwright/test` version, so Docker smoke runs can't silently break again.
- `scripts/check-node-lockstep.js` (`npm run check:node-lockstep`, CI, and a Jest test so the husky hooks catch it too) fails if any Node pin — `config/Dockerfile.unit`, the Node stage in `config/Dockerfile.test`, `config/docker-compose.yml`, the husky hooks, `netlify.toml`'s `NODE_VERSION`, or a workflow `node-version` — drifts from `.nvmrc`.
- Node runtime regression tests: `scripts/__tests__/node-runtime.test.js` (real-Node child processes: server Web Storage semantics, zustand `persist` for every installed copy, wagmi SSR config, sharp AVIF/WebP, native ws addons, esbuild, @parcel/watcher, unrs-resolver, wagmi codegen config), `src/__tests__/server-runtime.test.ts` (proxy middleware, `/sw.js` route handler, robots, sitemap under Jest's node environment), `src/contexts/__tests__/ThemeContext.test.tsx` (storage unavailable/throwing), and `tests/runtime.spec.ts` (security headers, `/sw.js`, robots/sitemap, prerendered blog posts, 404 handling and immutable static caching against `next start`).
- `Docker Images` workflow builds `config/Dockerfile.unit` and `config/Dockerfile.test` and runs Jest / Playwright inside them whenever `.nvmrc`, a Dockerfile or a compose file changes. CI Fast uses setup-node and never exercised these images.

### Fixed
- Every page declared `<link rel="canonical" href="https://nitsuah.io">` (a root-layout `alternates.canonical` inherited by all routes), telling search engines each page, including every blog post, was a duplicate of the homepage.
- Site-wide `og:image`/`twitter:image` pointed at `/social-preview.svg`, which doesn't exist (404), so shared links had no preview image.
- Netlify CSP blocked Reown/WalletConnect AppKit's `api.web3modal.org` on every page; `connect-src` now allows `https://*.web3modal.org`.
- All 19 non-blog pages shared one title and description; nested pages (Labs, blog posts) dropped the site-name suffix.
- `robots.txt` advertised a nonexistent `/sitemap-index.xml`; the sitemap listed `noindex` WIP Labs pages; `/blogs` and `/clients` redirected with 307 instead of a permanent 308.
- Accessibility (axe WCAG 2.1 A/AA + best-practice, every page): resume dates/durations (2.3–2.5:1), blog and client category pills and the blog CTA button now meet 4.5:1; skip-link and main navs have distinct labels; the resume header no longer declares a second `banner`; `/about` has an `<h1>`; project/client card titles no longer skip a heading level; code blocks are keyboard-focusable; WIP Labs nav items are plain text instead of focusable `href="#"` links.
- Blog posts: about 50 relative "Code References" links (e.g. `../Dockerfile`) resolved to `https://nitsuah.io/...` 404s; they now link only files verified to exist in the real repos. Removed unfilled template text ("Summarize the main points of the article", stub "Conclusion" sections), an orphan link list, off-topic boilerplate "Further Reading" links, missing images (`monorepo.png`, `nextjs.png`) and screenshots reused from other projects. Fixed dead links to `nitsuah/ecs-patterns`, `nitsuah/motor-pool` (now `agent-board`) and `nitsuah/nitsuah-io` (now `Nitsuah-Labs/nitsuah-io`).
- zustand `persist` stores threw on the server under Node 25+ (zustand <5.0.14, pulled in by `@wagmi/core` and `@base-org/account`); a `zustand: 5.0.15` override dedupes every copy to a fixed release, which also removes the `localStorage` ExperimentalWarning from builds.
- `lighthouse-check` never audited anything: `lhci autorun` couldn't find `config/lighthouserc.json` and exited before collecting (hidden by `continue-on-error`), and lhci 0.12's Lighthouse 10 scored accessibility as null because its axe-core can't parse CSS `color(srgb …)`. The step now passes `--config` and uses lhci 0.15 (Lighthouse 12.6); a local run on Node 26 scored performance 0.75 (warn threshold 0.85), and accessibility, best-practices and SEO 1.0.
- CI's `build-files` artifact never uploaded (`upload-artifact@v4` skips the `.next` dot-directory by default), so `lighthouse-check` always rebuilt instead of auditing the tested build; `include-hidden-files: true` fixes it.
- Playwright Docker image (`config/Dockerfile.test`, `mcr.microsoft.com/playwright`) was pinned to `v1.62.1-noble` while `@playwright/test` had moved to `1.63.0`; realigned both to `1.63.0` and added Dependabot grouping (npm `@playwright/*` bumps together; Docker image auto-updates ignored) so future upgrades land in lockstep by construction, not convention.

### Changed
- `package.json` `engines.node` drops end-of-life Node 20 (`^22.13.0 || >=24`); `check:node-lockstep` now also fails if `.nvmrc` falls outside it.
- Whole stack moved from Node 22 to Node 26.10.0 in one step, with `.nvmrc` as the single source of truth: unit and E2E Docker images, dev compose, husky hooks, Netlify, and CI (setup-node now reads `.nvmrc`). `config/Dockerfile.test` overlays Node 26 onto the Playwright image, which otherwise ships its own Node 24. CI keeps a temporary `22.x` comparison leg while 26 soaks.
- Labs contracts' chain config migrated from the shut-down Mumbai testnet to Amoy (`polygonAmoy`, chain id 80002, explorer/OpenSea links, copy) (#519). The contracts themselves still need redeploying to Amoy — tracked in TASKS.md.
- In-app "New Blog Post" form and localStorage drafts removed; posts are file-sourced from `src/data/blogs.json` (#526).
- `@splinetool/runtime` 2.0.56 with the Dependabot ignore removed (#524, #530); dotenv 18 (#528); grouped minor/patch bumps (#512, #518, #520, #525, #529).
- Planning docs reset for 2027 (`pmo-ff`): all open 2026 Q2–Q4 items (none shipped) carried into a 2027 Q1 triage pool, `motor-pool` renamed to `agent-board`, "Planned:" placeholders removed from this changelog, breadcrumb navigation + README docs index added.
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

### Security
- Patched high-severity `sharp` and `js-yaml` CVEs (#522).


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