# nitsuah-io

> Reviewed: 2026-09-23

## Overview

Austin J. Hardy's personal portfolio site at nitsuah.io. Next.js 16 + TypeScript with Web3 integration (wagmi, viem, ConnectKit), Spline 3D hero (now split onto a dedicated `/3d` route), interactive Labs section (ENS, NFT minting, token staking, DAO governance), and Netlify SSR deployment. 214 Jest unit tests (97.21% stmt coverage) + 20 Playwright specs (11 running, 9 intentionally skipped pending a wallet mock).

## Current Goals / Roadmap Focus

**Status check (per `docs/ROADMAP.md`, 2026-09-01): none of the Q2 2026 backlog items shipped during Q2** — engineering time instead went to dependency maintenance and CI/Playwright stabilization. The full Q2 list below carries forward unchanged as active backlog, re-verified against the codebase on 2026-09-01.

**Shipped since last review (not on the roadmap as a line item, done ad hoc):**
- Home page redesigned as a focused landing page (`LandingHero` + `FeaturedProjects`), surfacing agent-board, overseer, bb-mcp, darkmoon above the fold
- Spline 3D experience moved off the home page to a dedicated `/3d` route to cut critical-path bundle weight / improve LCP
- `docs/METRICS.md` refreshed with a validation marker (this was itself a Q2 P2 backlog item — now done)

**Q2 2026 (carried over, mostly unshipped):**
- Replace placeholder demo assets (restaurant, e-commerce, real-estate, CMS, NFT) — P1
- Replace duplicate project/crypto page assets — P1
- Migrate labs contracts from Mumbai to Amoy testnet — P1 — **partially shipped**: `src/wagmi.ts`/UI/chain-id checks/explorer links all moved to Amoy (zero Mumbai references remain in `src/`), but the two labs contracts (Register, Domains) were only ever deployed to Mumbai and still have no Amoy counterpart — needs a funded Amoy wallet to redeploy and update `CONTRACT_ADDRESS` before those labs pages work on-chain
- Add AI chat widget via bb-mcp (`/api/chat` proxy, streaming, server-side key) — P1
- Bento grid layout for Projects and Skills sections — P1
- Micro-interaction and animation pass, variable font/typography, glassmorphism polish — P2
- Live kryptos feed widget in Labs sidebar — P2
- Wire skyview analytics (privacy-first, no PII) — P2
- Add `docs/API.md` (wagmi hook surface, chain config, `/api/*` routes) — P2

**Q3 2026 (planned):** motor-pool showcase, on-chain resume (EAS attestations), AI-generated project summaries, Playwright Nightly wallet-flow expansion, EIP-6963 multi-wallet discovery, PWA manifest/offline fallback.

**Q4 2026 (exploratory):** commit activity heatmap, repo dependency graph, Core Web Vitals audit, Turbopack migration, Spline/Material-UI weight reduction.

Sister-repo integration priority: bb-mcp → kryptos → skyview → motor-pool → farm → darkmoon. Deprioritized (low-friction contribution mode only): gcp, stash, osrs.

## Open P0/P1 Tasks

Re-verified against the codebase 2026-09-01 (`docs/TASKS.md`) — none have shipped:

- [ ] **P1** Keep Playwright Docker + npm in lockstep (coordinated upgrades)
- [ ] **P1** Replace placeholder-heavy client demo assets
- [ ] **P1** Replace duplicate project and crypto page assets
- [ ] **P1** Migrate labs contracts Mumbai → Amoy — chain-config/UI side done 2026-09-01; the Register and Domains labs contracts themselves still need redeployment to Amoy by someone with a funded testnet wallet
- [ ] **P1** Add AI chat widget via bb-mcp
- [ ] **P1** Bento grid layout for Projects + Skills sections

## Blockers

- bb-mcp needs a stable MCP provider contract before the chat widget can be built
- Mumbai testnet deprecated; chain-config/UI now points at Amoy, but the Register/Domains labs contracts still need manual redeployment to Amoy (funded wallet required) before those flows work on-chain

## Recent Changes (Unreleased)

- Home page redesigned as a landing page (`LandingHero` + `FeaturedProjects`) surfacing top projects (agent-board, overseer, bb-mcp, darkmoon) above the fold
- Dedicated `/3d` route added for the Spline experience, split off the home page for LCP
- Top-level docs consolidated under `docs/`; completed handoffs and resolved trackers moved to `docs/archive/`
- **Bug found and fixed**: `npm run test:e2e:docker` was missing `--config config/playwright.config.ts`, so Playwright silently fell back to zero-config discovery and crashed on Jest test files (`ReferenceError: describe is not defined`) — found while refreshing `docs/METRICS.md`
- Full Docker test re-run (2026-09-01): Jest 214/214 passing (97.21% stmt coverage, up from 213/98%); Playwright 11/20 passing, 9 intentionally skipped wallet-connection tests (gated pending a local wallet mock); Playwright Docker image bumped to v1.62.1, still in lockstep with `@playwright/test`
- `docs/METRICS.md`'s stale "Resume Tests"/"Visual Tests" rows removed — no longer correspond to any spec file in the repo
- Audit confirmed `docs/INTEGRATIONS.md` was already complete (shipped alongside 0.3.0) but was still listed as an open task — stale duplicate removed from TASKS.md

**[0.3.0] - 2026-04-03:** dark mode toggle, Docker test infra, split Playwright CI (`CI Fast` + `Playwright Nightly`), config centralized under `config/`, `docs/INTEGRATIONS.md` cross-repo map.
