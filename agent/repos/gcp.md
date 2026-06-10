# gcp - Google Drive automation toolkit

**Last Validated:** 2026-06-10 | PMO audit - Docker-first validation
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

- P0 blocker: Containerized path is broken due to Dockerfile copy path mismatch.
- TASKS previously listed several already-shipped items as open; PMO reset to actionable backlog.
- ROADMAP used stale sequencing and has now been reset to 2026 execution windows.

---

## Priority Focus

1. Fix Dockerfile build/runtime path to align with package layout.
2. Add Docker smoke validation in CI.
3. Keep README command examples aligned to shipped entrypoints.

---

## Key Commands

```bash
docker build -t pmo-gcp-audit .
# currently fails at COPY copy_folder.py
```

---

## Active PMO

See TASKS.md and ROADMAP.md for current priorities.

---

## Vault Index

*Copied from repo — do not edit these files, overwritten on sync. Edit only this `.md`.*

**Core:** [[repos/gcp/ROADMAP|ROADMAP]] · [[repos/gcp/TASKS|TASKS]] · [[repos/gcp/FEATURES|FEATURES]] · [[repos/gcp/METRICS|METRICS]] · [[repos/gcp/CHANGELOG|CHANGELOG]] · [[repos/gcp/README|README]]

**docs/:** [[repos/gcp/docs/HANDOFF-progress-telemetry-20260403|HANDOFF: progress telemetry (2026-04-03)]]
