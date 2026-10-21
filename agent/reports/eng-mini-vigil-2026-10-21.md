---
HEAD: 2fb956b0a386c6186f209232a8629f3f187a8cec
kind: eng-mini
repo: vigil
date: 2026-10-21
---

# eng-mini: vigil — 2026-10-21 (REPORT MODE)

> Report only; no moves executed. Fresh `--depth 1` clone of `nitsuah/vigil`. Latest commit 2026-10-21 10:18 -0400. Previous report: 2026-10-14.

## Files Reviewed at Root

| File/Dir | Category | Action |
|---|---|---|
| `.github/`, `.gitignore`, `.env.example`, `.husky/`, `.nvmrc`, `.dockerignore` | Required root | KEEP |
| `Dockerfile`, `package.json`, `package-lock.json`, `next.config.ts`, `tsconfig.json`, `postcss.config.mjs`, `netlify.toml`, `proxy.ts`, `auth.ts` | Build / manifest / runtime | KEEP |
| `LICENSE`, `README.md` | Root-only | KEEP |
| `ROADMAP.md`, `TASKS.md`, `FEATURES.md`, `METRICS.md`, `CHANGELOG.md` | Planning docs; vigil reads root first, no `docs/` copies exist | KEEP (valid at root) |
| `AGENTS.md`, `CLAUDE.md` | Agent instruction files, tool-discovered at root | KEEP |
| `.prettierrc.json`, `.prettierignore` | Editors walk upward | KEEP |
| `.vscode/`, `.claude/` | Editor/tool config | KEEP |
| `playwright.ci.config.ts`, `playwright.config.ts`, `playwright.journeys.config.ts`, `playwright.smoke.config.ts`, `playwright.visual-docs.config.ts` | Referenced via `-c <root path>` in `package.json` and `.github/workflows/{e2e,smoke,visual-docs}.yml` | CANDIDATE-MOVE (deferred; Playwright `testDir`/`globalSetup` also shift to `../`) |
| `build.log`, `build-out.log`, `build2.log`, `.coverage` | **Tracked** build artifacts (verified via `git ls-files`); no references found | CANDIDATE: removal, see Overseer Decisions |
| `app/ components/ hooks/ lib/ types/ database/ e2e/ tests/ scripts/ public/ site/ promo/ skills/ templates/ config/ docs/` | Content dirs (`config/` already holds eslint, vitest, docker test files) | NO ACTION |

## Duplicate / Destination Checks

Planning docs: ROADMAP, TASKS, FEATURES, METRICS, CHANGELOG exist at root only (last commit 2026-10-21 each); `docs/` holds none of them. No root/`docs/` pairs. No CONTRIBUTING at either location. No destination conflicts for any proposed move.

## Files Moved
None (report mode).

## Validation
Read-only audit; no build/test run.

## Known Risks / Deferred
- Moving the five `playwright.*.config.ts` files to `config/` requires updating `package.json` (`test:journeys`, others), three workflows, comments in `smoke.yml`/`e2e.yml`, and `testDir`/`globalSetup` paths. Medium risk, deferred.

## Overseer Decisions Required
1. Tracked `build.log`, `build-out.log`, `build2.log` (212/212/834 bytes) and `.coverage` (53 KB): look like accidental commits. Removal is a deletion (out of scope for the non-destructive pass). Propose: `git rm` them and add to `.gitignore`. Needs approval.

## Suggested Follow-up
Approve the artifact removal; optionally consolidate Playwright configs under `config/` in a dedicated PR.
