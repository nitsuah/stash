# LOC Report — kryptos

Mode: `--report` (dry run, no changes made)
Date: 2026-09-01
Source: shallow clone (`--depth 1`) of `nitsuah/kryptos` @ `a7b6927f89c3d0cfaa512044c0e12c445b91b813`
Method: `git ls-files` (Phase 0 spec exclusions applied) + `wc -l` per file — actual line counts, not estimated.
Note: shallow clone — churn/author history (many-authors, frequent-edits signal) is **not available** for this repo; that structural signal is marked "assumed: not confirmed" throughout.

## Inventory Summary
- Tracked source files (post-exclusion): 452
- Total LOC counted: 62,122

## Top 10 LOC Files

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `src/kryptos/k4/transposition_analysis.py` | 903 | Python | K4 transposition-cipher solver algorithms |
| 2 | `src/kryptos/k4/hypotheses.py` | 897 | Python | K4 hypothesis definitions/data model |
| 3 | `src/kryptos/api/k4_attack_routes.py` | 801 | Python | FastAPI routes for launching/tracking K4 attacks |
| 4 | `src/kryptos/cli/main.py` | 756 | Python | CLI command dispatch |
| 5 | `frontend/src/theme.css` | 683 | CSS | Frontend theming |
| 6 | `src/kryptos/k4/scoring.py` | 658 | Python | Plaintext scoring/fitness functions |
| 7 | `src/kryptos/agents/ops_director.py` | 650 | Python | Agent orchestration |
| 8 | `src/kryptos/k4/vigenere_key_recovery.py` | 610 | Python | Key recovery algorithms |
| 9 | `src/kryptos/autonomous_coordinator.py` | 606 | Python | Autonomous run coordinator |
| 10 | `tests/functional/test_k4_hypotheses.py` | 591 | Python | Test file (large but expected — excluded from risk ranking) |

## Risk Rank & Rationale

1. **`src/kryptos/api/k4_attack_routes.py` — Critical**
   Structural evidence: contains `_run_attack_worker`, a single function spanning **343 lines** — far past the ~80-line guideline — that mixes background-thread orchestration, job-state mutation, and attack-stage dispatch in one body. This is a genuine mixed-concerns hotspot, not a size-only flag. Has partial test coverage (`tests/functional/test_k4_frontier_p15_p20.py` references it), but the giant worker function itself is not unit-isolated. High refactor ROI.

2. **`src/kryptos/k4/hypotheses.py` — Medium**
   903 lines but spread across 64 defs, mostly short `__init__`/data-class-style methods (max ~30 lines). This reads as a large *data catalog* of hypotheses rather than deep logic — closer to a config file with methods. Well covered by tests (`test_k4_hypotheses.py`, `test_scoring_fallback.py`, etc.). Low structural risk despite size; flag for a data/logic split only if it keeps growing.

3. **`src/kryptos/k4/transposition_analysis.py` — Medium-High**
   903 lines, 22 defs, with several 60–100+ line functions (`solve_columnar_permutation_simulated_annealing_multi_start` at 106 lines, `..._simulated_annealing` at 92 lines). Multiple related-but-distinct solver strategies live in one module. Extensively tested (13+ dedicated test files touch transposition logic), so extraction is lower-risk than usual. Medium-high priority.

4. **`src/kryptos/cli/main.py` — Low-Medium**
   756 lines but 24 defs, each a small `cmd_*` handler (7–12 lines) — this is a flat command-dispatch table, a single clear concern (CLI routing). Per Evidence Rules, a large-but-single-concern file is low structural risk. Not a refactor priority.

5. **`src/kryptos/k4/scoring.py` — Low-Medium**
   658 lines, 34 defs, mostly small scoring functions (20–45 lines), one larger composite function (45 lines). Cohesive single concern (fitness scoring). Low-medium risk.

6. **`frontend/src/theme.css` — Low (excluded per guardrail)**
   CSS-only large file — per LOC.md guardrails this is a style/maintainability item, not a complexity risk. Route to a design-system pass, not this cycle.

## Refactor Opportunities by Phase

**`k4_attack_routes.py`** (Critical):
- Phase 1: Extract `_run_attack_worker`'s job-state bookkeeping (`_update_job` calls, progress tracking) into a small `AttackJobState` helper — smallest safe cut, no behavior change, worker still calls into it.
- Phase 2: Extract the attack-stage dispatch logic (which stage runs which solver) into `k4/attack_dispatch.py`, leaving `k4_attack_routes.py` as the FastAPI route layer + thin re-export.
- Phase 3 (optional): If the worker is still large after 1–2, split per-stage execution into named functions colocated with their stage's solver module.

**`transposition_analysis.py`** (Medium-High):
- Phase 1: Extract the `*_multi_start` variants (thin wrappers that loop and call the single-start solver) into a shared `multi_start.py` helper, since they're structurally repetitive around the core solver.
- Phase 2: Leave core annealing solver in place; re-evaluate size after Phase 1.

## Validation Plan (for eventual `--refactor`)
- Run `pytest tests/functional -k "transposition or hypotheses or attack_routes"` before and after each extraction; line counts should be identical pre/post for un-touched behavior.
- For `k4_attack_routes.py`, smoke-test the FastAPI app boot and one attack-launch round-trip locally (no Docker config detected in repo root — flag for `--refactor` phase to confirm before assuming host-run is safe).

## Repo Summary Table

| Repo | Top Concern | Priority | Notes |
|------|-------------|----------|-------|
| kryptos | `k4_attack_routes.py`: 343-line `_run_attack_worker` mixing job-state + dispatch | High | Best next-cycle target; test coverage exists but not isolated to the worker function |

## Ordered Next-Cycle Targets (this repo)
1. `src/kryptos/api/k4_attack_routes.py` — extract `_run_attack_worker` job-state + dispatch (Critical, high ROI)
2. `src/kryptos/k4/transposition_analysis.py` — extract multi-start wrapper pattern (Medium-High)
3. `src/kryptos/k4/hypotheses.py` — monitor only, no action this cycle (Low, data-catalog shape)

## Deferred / Not Flagged
- `frontend/src/theme.css` (683 lines) — CSS-only, deferred to design-system pass per guardrail.
- `src/kryptos/cli/main.py` (756 lines) — single clear concern (flat CLI dispatch), deferred.
- Test files in top-10 by size (e.g. `test_k4_hypotheses.py`) — excluded from refactor ranking; large test files are expected.

## Assumptions / Unconfirmed
- Churn/author-frequency signal: **assumed unavailable** — shallow clone has no history beyond HEAD. A full-history run is needed to confirm/deny high-churn hotspots.
- Docker/devcontainer presence for local validation: not confirmed in this pass (report mode only; no filesystem walk beyond `git ls-files`).
