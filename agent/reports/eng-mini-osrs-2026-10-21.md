---
HEAD: 68395790e9514de497ccb6e76647fd0050d60cb3
kind: eng-mini
repo: osrs
date: 2026-10-21
---

# eng-mini: osrs — 2026-10-21 (REPORT MODE, second pass)

> 🧭 [[repos/osrs|osrs]] · ← [[reports/eng-mini-osrs-2026-10-02|2026-10-02]] <!-- nav -->
>
> Report only; no moves executed. Fresh `--depth 1` clone of `nitsuah/osrs`. Latest commit 2026-10-21 10:20 -0400. This supersedes the earlier same-day report (HEAD `1a24bf9…`); the repo moved since.

## Files Reviewed at Root

| File/Dir | Category | Action |
|---|---|---|
| `.github/`, `.gitignore`, `.env.example` | Required root | KEEP |
| `Dockerfile`, `requirements.txt`, `requirements-dev.txt` | Build (Dockerfile COPYs requirements by root path) | KEEP |
| `LICENSE` | Decided 2026-09-24: root in every repo | KEEP |
| `README.md` | Root-only | KEEP |
| `CHANGELOG.md` | Root only, no `docs/` counterpart | KEEP |
| `Makefile`, `pyproject.toml` | Tooling / manifest | KEEP |
| `.pre-commit-config.yaml` | pre-commit reads root by default; move needs `--config` everywhere | CANDIDATE-MOVE (deferred) |
| `pytest.ini` | rootdir/testpaths resolution; `make test` runs bare `pytest` | CANDIDATE-MOVE (deferred) |
| `bot/`, `config/`, `docs/`, `tests/` | Content dirs (`config/` holds `.flake8`, `docker-compose.yml`) | NO ACTION |

## Duplicate / Destination Checks

`docs/` has FEATURES, METRICS, ROADMAP, TASKS (+ `archive/`); root has only CHANGELOG. No root/`docs/` pairs. No CONTRIBUTING at either location. `config/.pre-commit-config.yaml` and `config/pytest.ini` do not exist, so no destination conflicts.

## Files Moved

None (report mode).

## Validation

Read-only audit; no build/test run.

## Known Risks / Deferred

Two deferred config moves above need tool-invocation updates (`pre-commit --config`, `pytest -c`) and their own validation (`pre-commit run --config config/.pre-commit-config.yaml --all-files`, `make test`).

## Overseer Decisions Required

None.

## Suggested Follow-up

Optionally finish the `config/` migration for `.pre-commit-config.yaml` and `pytest.ini` in a dedicated PR.
