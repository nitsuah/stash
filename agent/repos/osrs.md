# osrs - Automation bot for game interaction

**Last Validated:** 2026-09-24 | PMO audit - doc-sync validation (no live Docker run this pass)
**Repo:** https://github.com/nitsuah/osrs
**Branch convention:** pmo/osrs/planning-alignment-YYYY-MM-DD

---

## Runtime Status

| Check | Status | Notes |
| --- | --- | --- |
| Docker build | PASS | Multi-stage image builds successfully |
| Container runtime | PASS (per source docs) | `Dockerfile` CMD fixed to `python -m bot.core` 2026-04-03 (see HANDOFF below); TASKS.md/CHANGELOG confirm delivery. Not re-verified with a live `docker run` this pass. |
| Docs baseline | PASS | README, ROADMAP, TASKS, FEATURES, METRICS and governance docs present |

---

## Stack

- Python automation toolkit (vision + OCR + action modules)
- Tesseract OCR integration for chat parsing
- Test suite for camera/compass/utils/smoke paths

---

## PMO Findings

- Prior audit pass flagged both a container-entrypoint mismatch and Python-version drift; both are now recorded as delivered in the source docs — entrypoint fixed 2026-04-03 (`Dockerfile` CMD → `python -m bot.core`, see `docs/HANDOFF-docker-entrypoint-20260403.md`), Python version unified 2026-09-02 (Dockerfile pinned to `python:3.10-slim-bookworm`, matching CI/pyproject). Table above updated accordingly; still worth a live `docker run` to fully re-confirm.
- Health/recovery work landed this cycle: `bot/health.py` `StuckStateMonitor` (stale OCR frames, capture failures, idle time) and `bot/checkpoint.py` `CheckpointLogger` (periodic structured state log + failure-summary dump), both fully tested.
- A real correctness gap was found and fixed in review (2026-09-09): OCR failures and legitimately-empty chat were both collapsing to the same `record_frame("")` call, which reset the stuck-state counter on every call — a persistent Tesseract failure could never trip recovery. Now routed through an explicit `ocr_ok` flag.

---

## Open P0/P1 Tasks

None open at P0/P1 — both open TASKS.md items are P2: (1) give `StuckStateMonitor.recover()` a real corrective action and stop `record_activity()` from resetting stale-frame state on unverified progress (needs live-game verification, deliberately not rushed), and (2) expand skill modules behind stable shared automation primitives.

## Priority Focus

1. Give `StuckStateMonitor.recover()` an actual corrective action (camera re-center/pan) instead of only logging + resetting counters — needs live-game verification.
2. Expand skill coverage (woodcutting/mining) on top of stable shared primitives, per ROADMAP Q3.
3. Do a live `docker build && docker run` pass to fully re-confirm the entrypoint/Python-version fixes recorded in TASKS.md (doc-only confirmation so far this cycle).

---

## Key Commands

```bash
docker build -t pmo-osrs-audit .
docker run --rm pmo-osrs-audit
# entrypoint fixed 2026-04-03 (python -m bot.core); not re-run live this pass
```

---

## Active PMO

See TASKS.md and ROADMAP.md for current priorities. Recent (Unreleased): `bot/checkpoint.py` `CheckpointLogger` added (delivered 2026-09-10); `record_capture_failure`/`ocr_ok` fix for the stuck-counter reset bug (2026-09-09); `actions.py` fix removing a redundant `time.sleep(60)` that had doubled fishing-loop wait time to ~120s; `question_handler.py` hardened against malformed `questions.json` and OCR line-break splits via a new `squash_for_match` fallback.

---

## Vault Index

*Copied from repo — do not edit these files, overwritten on sync. Edit only this `.md`.*

**Core:** [[repos/osrs/ROADMAP|ROADMAP]] · [[repos/osrs/TASKS|TASKS]] · [[repos/osrs/FEATURES|FEATURES]] · [[repos/osrs/METRICS|METRICS]] · [[repos/osrs/CHANGELOG|CHANGELOG]] · [[repos/osrs/README|README]]

**docs/:** [[repos/osrs/docs/HANDOFF-docker-entrypoint-20260403|HANDOFF: docker entrypoint (2026-04-03)]]
