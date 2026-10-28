---
HEAD: b74056675b199b9db0c2d7b39207e3cf3c739935
kind: eng-mini
repo: skyview
date: 2026-10-21
---

# eng-mini: skyview — 2026-10-21 (REPORT MODE)

> 🧭 [[repos/skyview|skyview]] · ← [[reports/eng-mini-skyview-2026-10-02|2026-10-02]] <!-- nav -->
>
> Report only; no moves executed. Fresh `--depth 1` clone of `nitsuah/skyview`. Latest commit 2026-10-21 10:18 -0400. Previous report: 2026-10-02.

## Files Reviewed at Root

| File/Dir | Category | Action |
|---|---|---|
| `.github/`, `.gitignore`, `.env.example`, `.dockerignore`, `.claude/` | Required root | KEEP |
| `Dockerfile`, `package.json`, `package-lock.json`, `netlify.toml` | Build / manifest | KEEP |
| `LICENSE`, `README.md` | Root-only | KEEP |
| `index.html`, `robots.txt`, `sitemap.xml` | Site entry points / crawler files served from root | KEEP |
| `config.js` | Loaded by `index.html` via `<script src="config.js?v=…">` (runtime site config, not tooling config) | KEEP |
| `METRICS.md` | Root only, no `docs/METRICS.md` | KEEP (valid at root; vigil accepts either) |
| `Dockerfile.dev`, `docker-compose.dev.yml` | Dev containers; no references found in `package.json`, `scripts/`, `.github/`, `docs/`, README | CANDIDATE-MOVE (low risk, deferred: `docker-compose.yml` already lives in `config/`, so build context paths need review) |
| `assets/ db/ docs/ netlify/ pages/ platform/ promo/ scripts/ showcase/ styles/ tests/ config/` | Content dirs (`config/` already holds eslint, vitest, playwright, stylelint, pre-commit, nginx) | NO ACTION |

## Duplicate / Destination Checks

`docs/` holds ROADMAP, TASKS, FEATURES, CHANGELOG; root holds only METRICS. No root/`docs/` pairs. No CONTRIBUTING at either location. Moving the dev compose files to `config/` would not collide with `config/docker-compose.yml`: `docker-compose.dev.yml` is a different filename. Their relative paths still need review (see Known Risks).

## Files Moved

None (report mode).

## Validation

Read-only audit; no build/test run.

## Known Risks / Deferred

- `docker-compose.dev.yml` / `Dockerfile.dev` move requires fixing relative `build.context`/`dockerfile`/volume paths. Deferred.
- `docs/lighthouse-desktop.report.{html,json}` are generated artifacts inside `docs/` (not root; informational).

## Overseer Decisions Required

None.

## Suggested Follow-up

Optionally move `docker-compose.dev.yml` → `config/` with corrected paths.
