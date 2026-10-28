---
HEAD: 8a04e089fbbb42776b6a881de3cd88dd9c16cfcb
kind: eng-mini
repo: bb-mcp
date: 2026-10-28
---

# eng-mini: bb-mcp — 2026-10-28 (REPORT MODE)

> Report only; no moves executed. Fresh `--depth 1` clone of `nitsuah/bb-mcp`. Latest commit 2026-10-28 10:48 -0700.

## Files Reviewed at Root

| File/Dir | Category | Action |
|---|---|---|
| `.github/`, `.gitignore`, `.gitattributes`, `.env.example`, `Dockerfile`, `Makefile`, `package.json`, `package-lock.json`, `tsconfig.json` | Required root / build | KEEP |
| `.pre-commit-config.yaml` | Valid at root or `config/` per vigil | KEEP (moving needs `--config` + hook updates) |
| `LICENSE`, `README.md` | Root-only | KEEP |
| `brag-plan.md` | Planning/promo note; referenced by `promo/spots.json` | CANDIDATE-MOVE to `docs/brag/` (low-medium risk: update the reference in `promo/spots.json` first) |
| `src/ tests/ scripts/ config/ docs/ brand/ promo/` | Content dirs | NO ACTION |

## Duplicate / Destination Checks

ROADMAP, TASKS, FEATURES, METRICS, CHANGELOG live in `docs/` only. No root/`docs/` pairs, no CONTRIBUTING at either location. `docs/brag/` exists; no `brag-plan.md` there, so no conflict.

## Files Moved

None (report mode).

## Validation

Read-only audit; no build/test run.

## Known Risks / Deferred

- `brag-plan.md` move: update `promo/spots.json` reference and verify promo build (`promo/build.sh`).
- `.pre-commit-config.yaml` move deferred (hook path updates).

## Overseer Decisions Required

None.

## Suggested Follow-up

Optional PR moving `brag-plan.md` to `docs/brag/` with reference update.
