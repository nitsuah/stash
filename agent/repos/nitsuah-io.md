# nitsuah-io

> Reviewed: 2026-06-25

## Overview

Austin J. Hardy's personal portfolio site at nitsuah.io. Next.js 16 + TypeScript with Web3 integration (wagmi, viem, ConnectKit), Spline 3D hero, interactive Labs section (ENS, NFT minting, token staking, DAO governance), and Netlify SSR deployment. 213 unit tests, Playwright E2E.

## Current Goals / Roadmap Focus

**Q2 2026 (active):**
- Replace placeholder demo assets (restaurant, e-commerce, real-estate, CMS, NFT) — P1
- Replace duplicate project/crypto page assets — P1
- Migrate labs contracts from Mumbai to Amoy testnet — P1
- Add AI chat widget via bb-mcp (`/api/chat` proxy, streaming, server-side key) — P1
- Bento grid layout for Projects and Skills sections — P1
- Micro-interaction and animation pass (hover states, scroll reveals, page transitions) — P2
- Variable font + fluid typography scale — P2
- Live kryptos feed widget in Labs sidebar — P2
- Wire skyview analytics (privacy-first, no PII) — P2
- Add `docs/API.md` (wagmi hook surface, chain config, `/api/*` routes) — P2
- `docs/INTEGRATIONS.md` cross-repo connection map — P2
- Refresh `METRICS.md` with `last validated` marker — P2

**Q3 2026 (planned):**
- motor-pool showcase section (`/lab/agents` read-only activity feed)
- On-chain resume page (EAS attestations tied to wallet)
- AI-generated project summaries with human-editable overrides
- Playwright Nightly wallet-flow coverage expansion
- EIP-6963 multi-wallet discovery
- PWA manifest + service worker + offline fallback

**Q4 2026 (exploratory):**
- Commit activity heatmap (GitHub API, no redirect)
- Repo dependency graph (D3/Cytoscape from `docs/INTEGRATIONS.md`)
- Core Web Vitals audit (LCP < 1.5s, CLS=0, INP < 100ms)
- Turbopack migration; bundle below 150KB gzip
- Evaluate/reduce Spline 3D scene weight (hero-only, lazy or CSS replace others)
- Evaluate Material-UI → Tailwind migration

Sister-repo integration priority: bb-mcp → kryptos → skyview → motor-pool → farm → darkmoon

## Open P0/P1 Tasks

- [ ] **P1** Keep Playwright Docker + npm in lockstep (coordinated upgrades)
- [ ] **P1** Replace placeholder-heavy client demo assets
- [ ] **P1** Replace duplicate project and crypto page assets
- [ ] **P1** Migrate labs contracts Mumbai → Amoy (Mumbai deprecated)
- [ ] **P1** Add AI chat widget via bb-mcp
- [ ] **P1** Bento grid layout for Projects + Skills sections

## Blockers

- bb-mcp needs stable MCP provider contract before chat widget can be built
- Mumbai testnet deprecated; Amoy migration required for labs contract flows

## Recent Changes

**[Unreleased]:**
- Planned: AI chat widget, bento grid, kryptos feed, skyview analytics, `docs/API.md`, `docs/INTEGRATIONS.md`
- ROADMAP extended through Q4 2026; TASKS updated with Q2 P1/P2 items

**[0.3.0] - 2026-04-03:**
- Dark mode toggle with localStorage persistence and hydration-safe rendering
- Docker test infrastructure with production build strategy
- Split Playwright CI: required `CI Fast` + scheduled `Playwright Nightly`
- Playwright Docker image coordinated with `@playwright/test` npm version
- Config centralized under `config/`
