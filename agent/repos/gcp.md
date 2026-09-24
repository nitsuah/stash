# gcp - Google Drive automation toolkit

**Last Validated:** 2026-09-24 | PMO audit - Docker-first validation
**Repo:** https://github.com/nitsuah/gcp
**Branch convention:** pmo/gcp/planning-alignment-YYYY-MM-DD

---

## Runtime Status

| Check | Status | Notes |
|---|---|---|
| Docker build | FAIL | `Dockerfile` references `COPY copy_folder.py .` at repo root, but source file lives under `gcp/copy_folder.py` |
| Python tests | Not run in this pass | Container build blocked runtime validation path |
| Docs baseline | PASS | README, ROADMAP, TASKS, FEATURES, METRICS present |

---

## Stack

- Python package with Google Drive API integration
- CLI entrypoint: `drive-report`
- Quality tooling: pylint, bandit, codeql, dependency review
- Packaging: `pyproject.toml` + pytest suite

---

## PMO Findings

- Docker build status above (`COPY copy_folder.py .` path mismatch) is from a prior audit pass and was not re-validated this cycle — flag for a fresh Docker smoke test rather than trusting as current.
- `drive-copy` CLI is now explicitly in **maintenance mode** per ROADMAP.md: the Q1–Q3 2026 core feature set and both Q4 exploratory items (duplicate-detection report, permission mirroring) have all shipped.
- Only remaining open idea is a 2027 web-UI evaluation, which was itself evaluated and deferred this cycle — scoped as a standalone FastAPI/Flask app if ever revisited, explicitly not a thin wrapper (no persistent server/session model exists to attach one to).

---

## Open P0/P1 Tasks

None open at P0/P1 — TASKS.md's only Todo item is the 2027 web-UI evaluation (deferred, not actionable now). Future work here is expected to be bugfixes/dependency upkeep, not new CLI surface area.

## Priority Focus

1. Re-validate the Docker build path mismatch noted above — confirm whether it's still current before treating it as a live blocker.
2. Add Docker smoke validation in CI (still relevant regardless of current build status).
3. No feature work planned; treat as maintenance-mode.

---

## Key Commands

```bash
docker build -t pmo-gcp-audit .
# currently fails at COPY copy_folder.py
```

---

## Active PMO

See TASKS.md and ROADMAP.md for current priorities. Recent (Unreleased): duplicate-detection report (`--duplicate-report`, CSV of same-name/same-size files across source+destination, Google-native files excluded); permission mirroring (`--mirror-permissions`, ACL copy onto new destination objects, ownership never mirrored, failures logged not fatal); new tests for both in `tests/test_roadmap_2026.py`; web-UI evaluation deferred to 2027.

---

## Vault Index

*Copied from repo — do not edit these files, overwritten on sync. Edit only this `.md`.*

**Core:** [[repos/gcp/ROADMAP|ROADMAP]] · [[repos/gcp/TASKS|TASKS]] · [[repos/gcp/FEATURES|FEATURES]] · [[repos/gcp/METRICS|METRICS]] · [[repos/gcp/CHANGELOG|CHANGELOG]] · [[repos/gcp/README|README]]

**docs/:** [[repos/gcp/docs/HANDOFF-progress-telemetry-20260403|HANDOFF: progress telemetry (2026-04-03)]]

## Verified Runbook (PMO 2026-09-24)

> Commands verified during the 2026-09-24 PMO audit (`agent/reports/pmo-audit-2026-09-24.md` §7). **obn-review: keep this section when refreshing the summary.**

- Coverage needs an editable install: `pip install -r requirements-dev.txt -e .`. A plain `pip install .` reports 0%.
- The Dockerfile has no test stage. Working command: `docker run --rm -v <repo>:/src:ro python:3.12-slim sh -c "cp -r /src /app && cd /app && pip install -q -r requirements-dev.txt -e . && pytest tests/ --cov=gcp --cov-report=term-missing"`
