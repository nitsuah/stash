# ROADMAP

> 🧭 [nitsuah-io](../README.md) · [Features](./FEATURES.md) · **Roadmap** · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

**Last Updated:** 2026-09-24
Next Review: 2026-10-24

> 2027 planning reset (2026-09-24): 2026 Q1 shipped (Playwright/npm lockstep, dark mode, INTEGRATIONS.md) and is in
> [FEATURES](./FEATURES.md). **None of the 2026 Q2–Q4 items shipped** — engineering time went to dependency maintenance,
> CVE fixes, CI/Playwright stabilization and the Mumbai→Amoy chain-config migration (see [CHANGELOG](./CHANGELOG.md)).
> All of them were carried into 2027 Q1 below as the triage pool for planning; sequencing within Q1 is still to be
> decided. `motor-pool` references were renamed to its current name, `agent-board`.

## 2027 Q1 - Triage Pool (Planned — carried from 2026)

### Committed candidates *(carried from 2026 Q2 — "0% shipped")*

#### Carry-overs
- [ ] Replace placeholder-heavy client demo assets (restaurant, e-commerce, real-estate, CMS, NFT).
- [ ] Replace duplicate project and crypto page assets with distinct representative media.

#### Web3 Maintenance
- [ ] Redeploy the Register and Domains labs contracts to Amoy and update `CONTRACT_ADDRESS` (chain-config/UI migrated in #519; contracts were only ever on the now-shut-down Mumbai — see TASKS.md).
- [ ] Add a local wallet testing path (mock provider, no live wallet required).
- [ ] Upgrade to wagmi v4 / viem v3 when stable; update generated hooks.

#### AI Integration (bb-mcp)
- [ ] Add AI chat widget powered by bb-mcp for portfolio visitor Q&A.
- [ ] Expose `/api/chat` route proxying bb-mcp; keep API key server-side only.
- [ ] Add streaming response support and typing indicator.

#### Design Refresh
- [ ] Bento grid layout for Projects and Skills sections.
- [ ] Micro-interaction pass: hover states, scroll-triggered reveals, smooth page transitions.
- [ ] Variable font + fluid typography scale for all headings.
- [ ] Glassmorphism card polish on Labs and Crypto pages.

#### Cross-Repo Data
- [ ] Live kryptos feed widget: pull real-time cipher challenge stats into Labs sidebar.
- [ ] Wire skyview event sink to capture page-view telemetry (privacy-first, no PII).

#### Docs & Quality
- [ ] Add `docs/API.md` covering wagmi hook surface, chain config, and `/api/*` routes.
- [ ] Refresh `METRICS.md` with a `last validated` marker and re-run coverage.

### Next candidates *(carried from 2026 Q3)*

#### Portfolio Intelligence
- [ ] agent-board (formerly motor-pool) showcase section: visualize autonomous agents building / maintaining the site.
- [ ] On-chain resume page: verifiable credentials tied to wallet address (EAS attestations).
- [ ] AI-generated project summaries with human-editable overrides.

#### Web3 Depth
- [ ] Expand wallet-flow coverage in Playwright Nightly (connection, signing, disconnect).
- [ ] Add EIP-6963 multi-wallet discovery support.
- [ ] Hardware wallet path (Ledger/Trezor) for Labs contract interactions.
- [ ] Farm staking demo: embed live staking flow pulling from farm repo contracts.

#### PWA & Offline
- [ ] Add `manifest.json` and service worker for installable PWA on mobile.
- [ ] Offline fallback page with cached project data.
- [ ] Push notification opt-in for new project announcements (vapid, server-side).

### Exploratory *(carried from 2026 Q4)*

#### Scale & Performance
- [ ] **Commit activity heatmap** — embed a GitHub-style contribution heatmap on the portfolio landing page, pulling live data from the public GitHub API; shows recent coding velocity across all repos without requiring a GitHub redirect.
- [ ] **Repo dependency graph** — D3 or Cytoscape visualization auto-generated from `docs/INTEGRATIONS.md` showing how sister repos (bb-mcp, kryptos, skyview, agent-board, farm, darkmoon) interconnect at the API/data level; gives portfolio visitors a map of the full ecosystem in one glance.
- [ ] Full Core Web Vitals audit targeting LCP < 1.5s, CLS = 0, INP < 100ms.
- [ ] Migrate to Turbopack for dev and production (drop webpack config).
- [ ] Bundle splitting review: reduce initial JS payload below 150 KB (gzip).

#### Ecosystem Expansion
- [ ] Internationalization (i18n) foundation via `next-intl`.
- [ ] Social graph page: aggregate on-chain activity, GitHub contributions, and project signals.
- [ ] skyview dashboard embed: public analytics card showing visitor trends.
- [ ] darkmoon theming engine: pull design tokens from darkmoon for consistent cross-repo branding.

#### Deprecation / De-prioritization Signals
- [ ] Evaluate Spline 3D scenes: keep hero only, lazy-load or replace others with CSS animations to improve LCP.
- [ ] Assess Material-UI dependency: plan incremental migration to pure Tailwind if bundle cost outweighs benefit.

## Notes

- The product is intentionally Netlify SSR, not a static export.
- `docs/ARCH.md` and `docs/TESTING.md` remain the supporting reference docs; `docs/PLAYWRIGHT_FIXES.md` and `docs/SCREENSHOTS.md` moved to `docs/archive/` in the July 2026 docs reorg (paths below are updated accordingly — `docs/SCREENSHOTS.md`'s asset backlog is still open, tracked under the "Carry-overs" task above).
- Sister-repo integration priority: bb-mcp (AI chat) → kryptos (data) → skyview (analytics) → agent-board (showcase) → farm (staking) → darkmoon (theming).
- Deprioritized repos (no active integration planned for 2027 Q1): gcp, stash, osrs — set to low-friction contribution mode. See `docs/INTEGRATIONS.md`.
