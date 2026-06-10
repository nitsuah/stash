# nitsuah-io — Portfolio Site

**Last Validated:** 2026-06-10 | PMO audit — Docker build + live site + docs/ review  
**Repo:** [Nitsuah-Labs/nitsuah-io](https://github.com/Nitsuah-Labs/nitsuah-io)  
**Live:** https://nitsuah.io  
**Branch convention:** `pmo/nitsuah-io/planning-alignment-YYYY-MM-DD`

---

## Runtime Status

| Check | Status | Notes |
|---|---|---|
| Live site | ✅ Working | Homepage loads, LandingHero + FeaturedProjects (agent-board, overseer, bb-mcp, darkmoon) |
| `/projects` route | ✅ Working | Navigable from homepage, filtering UI renders |
| Docker image build | ✅ Passing | `config/Dockerfile.test` pins `playwright:v1.60.0-noble`, matches `@playwright/test@^1.60.0` |
| Docker smoke tests | ✅ Re-aligned | Version drift from prior audit resolved during 2026-06-03 `config/` reorg (verify with `npm run precheck:docker`) |
| Netlify deployment | ✅ Working | Node 22, `@netlify/plugin-nextjs` SSR mode |

---

## Stack

- **Framework:** Next.js 16 (App Router, SSR — no static export)
- **Language:** TypeScript
- **Web3:** wagmi v2 + viem v2, custom Connect UI (wallet logos, install prompts)
- **UI:** Material-UI + Emotion + CSS Modules + CSS custom properties
- **3D:** `@splinetool/react-spline` (lazy-loaded, idle callback)
- **Testing:** Jest (213 tests, 98% stmt coverage) + Playwright (smoke, a11y, E2E, visual regression)
- **CI:** GitHub Actions — CI Fast (required: lint/typecheck/unit/build/Lighthouse) + Playwright Nightly
- **Deployment:** Netlify, `netlify.toml` aligned with `next.config.js`

---

## Blockers

_None open._ Prior P0 (Playwright Docker image version drift) was resolved during the 2026-06-03 `config/` reorg — `config/Dockerfile.test` and `package.json` are both pinned to `1.60.0`.

---

## Key Gaps

- **Dark Mode Toggle UI** — `ThemeContext` wired, toggle component not shipped (P1)
- **Visual assets** — `docs/SCREENSHOTS.md` tracks 🔴 missing images for Restaurant, E-Commerce, Real Estate client demos; 🟡 duplicate images on crypto/projects pages
- **Mumbai → Amoy testnet migration** — Polygon deprecated Mumbai; `/labs` pages affected (P1)
- **`docs/API.md`** — not present; `src/generated.ts` wagmi hooks undocumented (P2)
- **METRICS.md currency** — values accurate but ~3 months stale; no "last validated" date (P2)

---

## Docs Inventory (`docs/`)

| File | Status | Notes |
|---|---|---|
| `ARCH.md` | ✅ Comprehensive | Theme system, Web3 integration, CSS Modules strategy, CI/CD, testing strategy |
| `TESTING.md` | ✅ Complete | Docker-first workflow, CI split, all test commands |
| `PLAYWRIGHT_FIXES.md` | ✅ Current | CI Fast vs Playwright Nightly rationale, test entry points |
| `SCREENSHOTS.md` | ✅ Tracked | Priority legend per page; 3 🔴 client demo gaps, 4 🟡 crypto page gaps |
| `DEMO_REF.md` | ✅ Current | DemoCard, DemoButton, DemoTable quick reference (last updated Dec 4 2025) |
| `API.md` | ❌ Missing | No wagmi hook or server endpoint docs |

---

## Key Commands

```powershell
# Docker-first validation (prescribed pre-push workflow)
npm run precheck:docker     # Build image + run full Playwright suite

# Individual
npm test                    # Unit tests (213 tests)
npm run test:smoke          # Playwright smoke only
npm run test:a11y           # Accessibility only
npm run test:e2e            # Full E2E browser suite
npm run test:e2e:docker:build  # Rebuild Docker image
npm run test:e2e:docker        # Run Playwright in Docker

# Web3
npm run wagmi               # Regenerate wagmi hooks from ABIs
npm run build:skip-wagmi    # Build without wagmi regen (faster)
```

---

## Active PMO PR

See TASKS.md and ROADMAP.md for current priorities. Last PR: `pmo/nitsuah-io/planning-alignment-2026-03-27`

Home-landing-redesign HANDOFF (2026-04-11) is complete and merged (PR #266, follow-up cleanup PR #348) — `LandingHero` + `FeaturedProjects` are live on `main`. Next roadmap item per that HANDOFF: Lighthouse audit on the new home page, confirm LCP improvement ≥15 points vs. the old scroll-based hero.

---

## Vault Index

*Copied from repo — do not edit these files, overwritten on sync. Edit only this `.md`.*

**Core:** [[repos/nitsuah-io/ROADMAP|ROADMAP]] · [[repos/nitsuah-io/TASKS|TASKS]] · [[repos/nitsuah-io/FEATURES|FEATURES]] · [[repos/nitsuah-io/METRICS|METRICS]] · [[repos/nitsuah-io/CHANGELOG|CHANGELOG]] · [[repos/nitsuah-io/README|README]]

**docs/:** [[repos/nitsuah-io/docs/ARCH|Architecture]] · [[repos/nitsuah-io/docs/TESTING|Testing]] · [[repos/nitsuah-io/docs/PLAYWRIGHT_FIXES|Playwright Fixes]] · [[repos/nitsuah-io/docs/SCREENSHOTS|Screenshots]] · [[repos/nitsuah-io/docs/DEMO_REF|Demo Ref]] · [[repos/nitsuah-io/docs/INTEGRATIONS|Integrations]] · [[repos/nitsuah-io/docs/HANDOFF-home-landing-redesign-20260411|HANDOFF: home-landing-redesign (2026-04-11)]] · [[repos/nitsuah-io/docs/HANDOFF-spline-move-3d-20260403|HANDOFF: spline-move-3d (2026-04-03)]]

## Related
- [[repos/nitsuah|nitsuah (v1)]] — legacy predecessor portfolio (React + Vite, archived)