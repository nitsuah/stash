# kryptos - K4 cryptanalysis research platform

**Last Validated:** 2026-03-27 | PMO audit - Docker-first validation
**Repo:** https://github.com/nitsuah/kryptos
**Branch convention:** pmo/kryptos/planning-alignment-YYYY-MM-DD

---

## Runtime Status

| Check | Status | Notes |
|---|---|---|
| Docker build | PASS | Image builds successfully |
| Container runtime | FAIL | Startup hits permission error creating artifacts under site-packages |
| Docs baseline | PASS | Rich docs set and governance files present |

---

## Stack

- Python package for multi-stage cryptanalysis workflows
- K4-focused pipeline modules (Hill, transposition, masking, scoring)
- Large pytest suite with fast/slow partitioning and CI segmentation

---

## PMO Findings

- P0 runtime blocker: default container command cannot persist artifacts due to write path permissions.
- Planning docs were updated to prioritize container reliability and phase-6.2 completion.
- Root roadmap and phase docs should remain linked to avoid planning drift.

---

## Priority Focus

1. Route artifacts/logs to writable app-owned path in container runtime.
2. Complete composite-chain validation thresholds and reporting.
3. Raise coverage gate after targeted test additions in critical modules.

---

## Key Commands

```bash
docker build -t pmo-kryptos-audit .
docker run --rm pmo-kryptos-audit
# currently fails with PermissionError on artifacts path
```

---

## Active PMO

See TASKS.md and ROADMAP.md for current priorities.

---

## Vault Index

*Copied from repo — do not edit these files, overwritten on sync. Edit only this `.md`.*

**Core:** [[repos/kryptos/ROADMAP|ROADMAP]] · [[repos/kryptos/TASKS|TASKS]] · [[repos/kryptos/FEATURES|FEATURES]] · [[repos/kryptos/METRICS|METRICS]] · [[repos/kryptos/CHANGELOG|CHANGELOG]] · [[repos/kryptos/README|README]]

**docs/:** [[repos/kryptos/docs/INDEX|INDEX]] · [[repos/kryptos/docs/governance|governance]]
