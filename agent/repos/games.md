# Games Repository Runbook (PMO)

Last Validated: 2026-03-27

## Repository Type

Browser-based arcade collection built on Next.js with multiple game routes under a shared frontend application.

## Verified Product State

- Deployed site observed at `https://nitsuah-arcade.netlify.app/`.
- Homepage loads successfully and presents a game-selection carousel.
- Asteroid route observed at `/asteroid` with an in-game HUD and active gameplay screen.

## Runtime Validation Evidence

- Browser validation completed against deployed production.
  - Homepage loaded.
  - Game route navigation worked.
  - Asteroid route rendered game HUD.
- Live runtime issue observed on deployed route.
  - Repeated console errors: `Sound not found: bgm`
  - Request failures observed for audio assets during route load (`/sounds/hit.mp3`, prior `/sounds/arcade.mp3` request aborted)

## Build / Packaging Evidence

- Docker-first validation attempted with:
  - `docker build -t games-pmo-audit .`
- Docker build currently fails.
  - Dockerfile uses Node 20, while dependencies report Node 22+ engine expectations.
  - `npm ci --omit=dev` triggers `prepare`, which calls `husky` but `husky` is not installed in the production-only dependency set.
  - `.dockerignore` is missing.

## Documentation Mismatch Observed

- `README.md` describes static HTML export hosting.
- `netlify.toml` uses `@netlify/plugin-nextjs` and publishes `.next`.
- `app/package.json` uses `next start`.
- Dockerfile also assumes a Next.js server runtime.

These sources currently describe different deployment models and should be unified before more release-path work proceeds.

## Additional Documentation Gaps

- `API.md` missing
- `ARCHITECTURE.md` missing
- `METRICS.md` contains multiple unverified/self-reported values

## Environment Constraints Observed During Audit

- Docker is available.
- Node/npm are not available in the current shell.
- `scripts/setup-node-env.ps1` currently reports that Node.js is not found in PATH.

## Recommended PMO Focus Order

1. Fix Docker/build reliability.
2. Resolve the live audio initialization/runtime error.
3. Align deployment documentation with the actual production model.
4. Refresh metrics with measured values.
5. Re-sequence feature expansion behind release reliability.
