---
HEAD: 1a24bf98c6ac1018e23b5c3db4f63c3ea20c9d66
kind: eng-mini
repo: osrs
date: 2026-10-21
---

# eng-mini: osrs — 2026-10-21 (REPORT MODE / DRY RUN)

> 🧭 [[repos/osrs|osrs]] · ← [[reports/eng-mini-osrs-2026-10-02|2026-10-02]] <!-- nav -->

>
> Report only — no moves executed, no changes made to the target repo. Selected as the #3 most recently active tracked repo this run (`git log -1 --format=%ci` from a fresh `--depth 1` clone: 2026-10-21T01:52:33-04:00). Root audited from a throwaway clone at `/home/user/osrs`.

## Root Audit — osrs/

| File/Dir | Category | MINI Rule | Proposed Action |
|------|----------|-----------|-----------------|
| `.git/` | VCS internal | N/A | **N/A (not a content file)** |
| `.github/` | Community health / CI | Must stay root | **KEEP** |
| `.gitignore` | VCS | Must stay root | **KEEP** |
| `.env.example` | Config template | Root-required (`.env*` class) | **KEEP** |
| `Dockerfile` | Build | Root-required for default `docker build` context; `COPY requirements.txt .` / `COPY requirements-dev.txt .` in the same build context assume root placement | **KEEP** |
| `LICENSE` | Legal | **Decided 2026-09-24: stays at root in every repo** | **KEEP** |
| `README.md` | Documentation | root-only | **KEEP** |
| `CHANGELOG.md` | Documentation | Root copy, no `docs/CHANGELOG.md` counterpart — not a duplicate (see below); vigil's multi-location support covers it (root OR `docs/`), so leaving it at root is a no-op either way | **KEEP** |
| `Makefile` | Build/dev tooling | `make` resolves `Makefile` from cwd by convention; root-required | **KEEP** |
| `pyproject.toml` | Manifest | Python package manifest + `[tool.ruff]` config; root-required | **KEEP** |
| `requirements.txt` / `requirements-dev.txt` | Dependencies | Referenced by exact root-relative path in `Dockerfile` (`COPY requirements.txt .`); moving needs a `Dockerfile` path update, no current benefit | **KEEP** |
| `.pre-commit-config.yaml` | Config | Vigil accepts root OR `config/.pre-commit-config.yaml` (no detection downgrade either way), but `pre-commit` CLI defaults to reading it from repo root with no `--config` flag anywhere in this repo (`Makefile`, CI, hook install) — moving would require adding `--config config/.pre-commit-config.yaml` to every invocation | **CANDIDATE-MOVE (deferred)** |
| `pytest.ini` | Config | `testpaths = tests` resolves relative to the file's own location (pytest `rootdir`); `Makefile`'s `test:` target runs bare `pytest` with no `-c` flag, so moving requires updating the Makefile and re-verifying `rootdir` auto-detection doesn't fall back to `pyproject.toml` first | **CANDIDATE-MOVE (deferred)** |
| `bot/`, `config/`, `docs/`, `tests/` | Pre-existing top-level content directories | Already organized per the repo's own Folder Strategy (`.flake8` and `docker-compose.yml` already live under `config/`, wired via `make lint` → `flake8 --config config/.flake8 .`) | **NO ACTION — out of MINI's root-file-hygiene scope** |

This repo has a partial `config/` migration already in place (`.flake8`, `docker-compose.yml`), consistent with the Folder Strategy. `.pre-commit-config.yaml` and `pytest.ini` are the remaining root config files that *could* follow the same pattern, but both need a tool invocation update to avoid breaking default discovery — flagged as deferred, not moved.

## Duplicate / Destination Checks

Checked ROADMAP, TASKS, FEATURES, METRICS, CHANGELOG, CONTRIBUTING at both root and `docs/`. `docs/` holds `FEATURES.md`, `METRICS.md`, `ROADMAP.md`, `TASKS.md`, plus `archive/`; root holds only `CHANGELOG.md`. **No overlap** — `CHANGELOG.md` exists only at root, and `ROADMAP.md`/`TASKS.md`/`FEATURES.md`/`METRICS.md` exist only in `docs/`. No duplicate pair found. No `CONTRIBUTING.md` found at either location (absent, not a duplicate).

Checked config-file multi-location candidates (`.pre-commit-config.yaml`, `.pylintrc`): only one copy of each exists in the repo (`.pre-commit-config.yaml` at root; no `.pylintrc` present at all — this repo uses `pyproject.toml`'s `[tool.ruff]` instead). No destination conflicts for either deferred candidate above — `config/.pre-commit-config.yaml` does not currently exist, so a future move wouldn't collide with anything.

## Proposed Moves (Dry Run — Not Executed)

**None executed.** Two deferred candidates noted above (`.pre-commit-config.yaml`, `pytest.ini`) — both require a coordinated tool-invocation update (per MINI.md's tool-specific path table) that should land with its own validation pass (`pre-commit run --all-files`, `make test`), not bundled into this audit.

## Files Left Exempt (with rationale)

| File | Reason |
|------|--------|
| `README.md`, `LICENSE` | Root-only per MINI.md |
| `.gitignore`, `.env.example` | Standard root-required files |
| `Dockerfile` | Build entry point resolved from repo root by default |
| `requirements.txt`, `requirements-dev.txt` | Referenced by exact root-relative path in `Dockerfile` |
| `Makefile`, `pyproject.toml` | Build/dev tooling and package manifest, canonical root location |
| `CHANGELOG.md` | Root-only copy, no duplicate; vigil accepts root or `docs/` either way |

## Overseer Decisions Required

None — no duplicates found, and LICENSE's root placement is pre-decided (not listed here per the 2026-09-24 ruling).

## Out-of-Scope Observations

- `.pre-commit-config.yaml` and `pytest.ini` are the only two tool configs left at root while `.flake8` and `docker-compose.yml` already moved to `config/` with explicit `--config` wiring in the `Makefile`. Worth a dedicated follow-up to finish that migration, since the repo has already absorbed the convention for other tools.

## Errors Encountered

None — root read from a clean `--depth 1` clone at `/home/user/osrs`.

## Suggested Follow-up

1. Optional, low priority: move `.pre-commit-config.yaml` → `config/.pre-commit-config.yaml` and `pytest.ini` → `config/pytest.ini`, updating the `Makefile`'s `lint`/`test` targets (and any hook install command / CI step) to pass the explicit `--config`/`-c` flag, with its own validation run (`pre-commit run --all-files`, `make test`).

---

*Report generated by eng-mini (report mode / dry run) — no changes made to `nitsuah/osrs`.*
