# nitsuah-io — Portfolio Site

**Last Validated:** 2026-03-27 | PMO audit — Docker build + live site + docs/ review  
**Repo:** [Nitsuah-Labs/nitsuah-io](https://github.com/Nitsuah-Labs/nitsuah-io)  
**Live:** https://nitsuah.io  
**Branch convention:** `pmo/nitsuah-io/planning-alignment-YYYY-MM-DD`

---

## Runtime Status

| Check | Status | Notes |
|---|---|---|
| Live site | ✅ Working | Homepage loads, hero + Spline 3D scene render |
| `/projects` route | ✅ Working | Navigable from homepage, filtering UI renders |
| Docker image build | ✅ Passing | `docker build -f Dockerfile.test -t nitsuah-io-pmo-audit .` ~3min |
| Docker smoke tests | ❌ Failing | Playwright image version drift — see Blockers below |
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

### P0 — Playwright Docker Image Version Drift

`Dockerfile.test` pins `mcr.microsoft.com/playwright:v1.56.1-noble` but `package.json` has `@playwright/test@1.57.0`.  
`docker run --rm nitsuah-io-pmo-audit npx playwright test tests/smoke.spec.ts --project=chromium-desktop` fails with:  
`Executable doesn't exist at /ms-playwright/chromium_headless_shell-1200/chrome-headless-shell-linux64/chrome-headless-shell`  
The WebServer starts fine (`✓ Ready in 150ms`) — only the browser binary is missing.  
**Fix:** `Dockerfile.test` line 1 → `mcr.microsoft.com/playwright:v1.57.0-noble`  
**Impact:** Blocks `npm run precheck:docker` — the prescribed pre-push validation workflow.

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

---