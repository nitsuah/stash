---
HEAD: 129df8db091521126ddc5175897900ae0f548ae3
kind: eng-mini
repo: vigil
date: 2026-10-28
---

# eng-mini: vigil — 2026-10-28 (REPORT MODE)

> 🧭 [[repos/vigil|vigil]] · ← [[reports/eng-mini-vigil-2026-10-21|2026-10-21]] <!-- nav -->

> Report only; no moves executed. Fresh `--depth 1` clone of `nitsuah/vigil`. Latest commit 2026-10-28 10:48 -0700.

## Files Reviewed at Root

| File/Dir | Category | Action |
|---|---|---|
| `.github/`, `.gitignore`, `.env.example`, `.husky/`, `.nvmrc`, `.dockerignore`, `Dockerfile`, `package.json`, `package-lock.json`, `next.config.ts`, `tsconfig.json`, `postcss.config.mjs`, `netlify.toml`, `proxy.ts`, `auth.ts` | Required root / build / runtime | KEEP |
| `LICENSE`, `README.md` | Root-only | KEEP |
| `ROADMAP.md`, `TASKS.md`, `FEATURES.md`, `METRICS.md`, `CHANGELOG.md` | Planning docs; vigil reads root first; no `docs/` copies | KEEP (valid at root) |
| `AGENTS.md`, `CLAUDE.md` | Tool-discovered at root | KEEP |
| `.prettierrc.json`, `.prettierignore` | Editors walk upward | KEEP |
| `.vscode/`, `.claude/` | Editor/tool config | KEEP |
| `playwright.ci.config.ts`, `playwright.config.ts`, `playwright.journeys.config.ts`, `playwright.smoke.config.ts`, `playwright.visual-docs.config.ts` | Referenced from `package.json` and workflows | CANDIDATE-MOVE (deferred; medium risk; `testDir`/`globalSetup` shift to `../`) |
| `app/ components/ hooks/ lib/ types/ database/ e2e/ tests/ scripts/ public/ site/ promo/ skills/ templates/ config/ docs/` | Content dirs | NO ACTION |

## Duplicate / Destination Checks

Planning docs exist at root only; `docs/` holds none of them. No pairs, no CONTRIBUTING at either location. The previously reported tracked artifacts (`build.log`, `build-out.log`, `build2.log`, `.coverage`) are no longer present at root, so that earlier decision is resolved.

## Files Moved

None (report mode).

## Validation

Read-only audit; no build/test run.

## Known Risks / Deferred

- Moving five Playwright configs to `config/` needs updates to `package.json`, workflows, and path settings. Medium risk, deferred.

## Overseer Decisions Required

None.

## Suggested Follow-up

Optionally consolidate Playwright configs under `config/` in a dedicated PR.
