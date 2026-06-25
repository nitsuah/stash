# kryptos

> Reviewed: 2026-06-25

## Overview

Python cryptanalysis research toolkit for solving the Kryptos CIA sculpture puzzle. K1, K2, K3 are solved; K4 remains unsolved. Implements Vigenère, Hill cipher, transposition, masking, Berlin Clock, Quagmire I–IV, Beaufort, and composite pipeline attacks with autonomous Q/OPS/SPY agent system, FastAPI dashboard, React SPA, Neon PostgreSQL persistence, and turbovec RAG semantic search.

## Current Goals / Roadmap Focus

**Q1 2027 (active — post-untested-vector phase):**

Phase 1 — K4 Attack completion: ✅ All five untested attack vectors completed (Clock→Hill, Clock→Vigenère, Berlin Clock sub-rows, Clock transposition, Beaufort sweep) — all null results, documented in `docs/analysis/K4_ACTIVE_RESEARCH.md`

Phase 2 — Dashboard & UI: ✅ FastAPI + React SPA shipped (Ops Center, K1–K3 animated decoder, Database admin, Vault, SSE live-log tail)
- [ ] K4 Attack Dashboard — dedicated attack-vector fingerprint view (remaining; Ops Center covers most)

Phase 3 — API: ✅ REST dashboard API, strategy_kb write path, candidate + run storage in Neon

Phase 4 — Validation: ✅ K3 double-transposition Monte Carlo, K1/K2 Vigenère stress tests, SA transposition seeding + crib locking

Phase 5 — Post-solution:
- [ ] Solution documentation (after K4 is solved)
- [ ] README and docs update reflecting solution

**Misc/Supporting:**
- [ ] Update `docs/analysis/K4-FRONTEND.md` for frontend/dashboard integration
- [ ] Ensure all new features have test coverage and artifact logging

## Open P0/P1 Tasks

All major Q1 2027 Phase 1–4 items are done. Remaining open items:

- [ ] **K4 Attack Dashboard** — standalone attack-vector fingerprint/progress view (low priority; Ops Center + RAG covers it)
- [ ] **Post-solution documentation** — blocked until K4 is solved
- [ ] **`docs/analysis/K4-FRONTEND.md` update**

No P0 blockers. K4 itself is unsolved (research problem, not a project blocker).

## Blockers

- K4 is unsolved — all systematic attack vectors tried have returned null results
- 5 untested vectors from prior roadmap all confirmed null (PR #83)
- Physical grid keystream attack: null result (108 geometric routes, 216 candidates)
- Quagmire I–IV sweep: null result (6,240 combinations)
- Remaining search space: substitution+transposition composite model remains most plausible

## Recent Changes (Unreleased)

- `kryptos serve` command — FastAPI app with `/health`, `/api/rag/*` endpoints
- turbovec-backed `ArtifactIndex` — sentence-transformers embeddings, 4-bit quantized index over `artifacts/`

Recent completed work (TASKS Done, 2026):
- 5 untested K4 attack vectors (all null): Clock→Hill 2×2, Clock→Vigenère 4-char, Berlin Clock sub-rows, Clock transposition column widths, Beaufort sweep
- K3 double-transposition Monte Carlo (75% best-of-top-10 success; brute-force ranks true plaintext #1)
- K1/K2 Vigenère stress tests (noise injection, wrong key length, partial ciphertext)
- SA columnar solver seedable; early-crib locking verified (>90% pruning at depth 1)
- `kryptos.benchmarks` CLI + CI job
- Physical grid attack (`run_physical_grid_attack`): null
- Quagmire I–IV solver + K4 sweep: null
- Agent module review: 5 bugs fixed in `AutonomousCoordinator` (crash-on-startup, crash-on-cycle-1, API drift, infinite loop on `max_hours=0.0`)
- `LinguistAgent` wired into `PlaintextValidator` as opt-in stage 3 (`enable_linguist=False` default)
- `strategy_kb` write path: OpsStrategicDirector persists BOOST/PIVOT/STOP/START_NEW to Neon with JSONL fallback
