# osrs - Automation bot for game interaction

**Last Validated:** 2026-03-27 | PMO audit - Docker-first validation
**Repo:** https://github.com/nitsuah/osrs
**Branch convention:** pmo/osrs/planning-alignment-YYYY-MM-DD

---

## Runtime Status

| Check | Status | Notes |
|---|---|---|
| Docker build | PASS | Multi-stage image builds successfully |
| Container runtime | FAIL | Startup command is `python main.py` but `main.py` is missing at repo root |
| Docs baseline | PASS | README, ROADMAP, TASKS, FEATURES, METRICS and governance docs present |

---

## Stack

- Python automation toolkit (vision + OCR + action modules)
- Tesseract OCR integration for chat parsing
- Test suite for camera/compass/utils/smoke paths

---

## PMO Findings

- P0 runtime blocker: container entrypoint mismatch prevents operational Docker use.
- Runtime version policy drift: README cites Python 3.13 while Docker stages use 3.10 and 3.11.
- TASKS and ROADMAP were updated to prioritize runtime and reliability before feature expansion.

---

## Priority Focus

1. Fix Docker entrypoint to a valid executable module/script.
2. Standardize version policy across README, Dockerfile, and CI.
3. Improve OCR robustness and health/recovery signals before adding new skill modules.

---

## Key Commands

```bash
docker build -t pmo-osrs-audit .
docker run --rm pmo-osrs-audit
# currently errors: python: can't open file '/app/main.py'
```

---

## Active PMO

See TASKS.md and ROADMAP.md for current priorities.

