# ENG LOC Report — kryptos (2026-10-15)
HEAD: 7b1abd4ac9e4119072029c578b448827a2440009

Mode: `--report` (dry run, no changes made)
Date: 2026-10-15
Source: shallow clone (`--depth 1`) of `nitsuah/kryptos` @ `7b1abd4ac9e4119072029c578b448827a2440009`
Method: `git ls-files` (Phase 0 spec exclusions applied) + `wc -l` per file — actual line counts, not estimated.
Note: shallow clone — churn/author history is **not available**; marked "assumed: not confirmed" where used.
Changed-since gate: prior report `eng-loc-kryptos-2026-09-01.md` recorded `a7b6927f89c3d0cfaa512044c0e12c445b91b813`; current HEAD differs, so this repo was reanalyzed.

## Inventory Summary
- Tracked source files (post-exclusion, code extensions only): 428 (down from 452 noted 2026-09-01 — likely exclusion-rule differences rather than file deletion; not confirmed)
- Total LOC counted: 63,424 (up from 62,122 on 2026-09-01)

## Top 10 LOC Files

Code files only — test files excluded per `LOC.md` Phase 1. One test file in this repo is close to the ~1,500-line standalone-callout bar; see note below the table.

| # | File | LOC | Lang | Role | vs 2026-09-01 |
|---|------|-----|------|------|----------------|
| 1 | `src/kryptos/k4/frontier_checks.py` | 1,131 | Python | New K4 cipher-family checks (negative-space gap closers) | New entrant — not in prior top 10 |
| 2 | `src/kryptos/k4/transposition_analysis.py` | 903 | Python | K4 transposition-cipher solver algorithms | Unchanged (was #1 @ 903) |
| 3 | `src/kryptos/k4/hypotheses.py` | 898 | Python | K4 hypothesis definitions/data model | ~Unchanged (was #2 @ 897) |
| 4 | `src/kryptos/k4/crib_constraints.py` | 877 | Python | Crib-constraint solving engine | New entrant |
| 5 | `src/kryptos/k4/scoring.py` | 707 | Python | Plaintext scoring/fitness functions | Grew from 658 (was #6) |
| 6 | `src/kryptos/cli/main.py` | 705 | Python | CLI command dispatch | Shrunk from 756 (was #4) |
| 7 | `src/kryptos/agents/ops_director.py` | 650 | Python | Agent/ops orchestration | New entrant |
| 8 | `src/kryptos/k4/vigenere_key_recovery.py` | 610 | Python | Vigenère key-recovery solver | New entrant |
| 9 | `src/kryptos/autonomous_coordinator.py` | 606 | Python | Autonomous run coordinator | New entrant |
| 10 | `src/kryptos/pipeline/attack_generator.py` | 579 | Python | Attack-pipeline generation | New entrant |

Test file: `tests/functional/test_k4_hypotheses.py` (591 lines) would have ranked #10 above but is a test suite, under the ~1,500-line bar for a standalone callout.

Note: `src/kryptos/api/k4_attack_routes.py` (801 LOC, #3 on 2026-09-01) and `frontend/src/theme.css` (683 LOC, #5 on 2026-09-01, CSS — out of scope per guardrails) have dropped out of the top 10; not confirmed whether reduced or just outpaced by growth elsewhere.

## Risk Rank and Rationale

| File | Risk | Rationale |
|------|------|-----------|
| `src/kryptos/k4/frontier_checks.py` | **High** | 38 function definitions across 1,131 lines (~30 lines/def average is reasonable, but max indentation depth hits 32 spaces / 8 levels — deep nesting signal). Docstring describes 7+ distinct cipher-family check strategies bundled in one module — each is a plausible extraction boundary (`running_key_english`, `recurrence_key`, `dial_key_scan`, `hill_exhaustive`, etc.). |
| `src/kryptos/k4/transposition_analysis.py` | Medium | Flagged in the prior report too; single clear domain (transposition solving) — size reflects algorithmic breadth more than mixed concerns. Carried forward without re-justifying structure (not re-inspected this run beyond LOC count). |
| `src/kryptos/k4/hypotheses.py` | Medium | Data-model file per its role in the prior report; large but single concern (hypothesis definitions) — size alone insufficient to flag High per guardrails. |
| `src/kryptos/k4/crib_constraints.py` | Medium-High | Companion engine to `frontier_checks.py` (same docstring cross-references it); likely multiple constraint-family implementations bundled together, same extraction pattern as `frontier_checks.py`. Assumed: not confirmed by direct read this run. |
| `src/kryptos/cli/main.py` | Medium | 27 function definitions — CLI dispatch commonly mixes argument parsing with command logic. Carried forward as a known concern; size dropped since 2026-09-01. |
| `src/kryptos/agents/ops_director.py`, `autonomous_coordinator.py` | Medium | New entrants this run — orchestration/coordination code, plausible mixed concerns (state + dispatch + logging) typical of "director"/"coordinator" naming. Assumed: not confirmed without a full read. |

Test coverage: repo has `tests/` and `scripts/testing/` directories; `test_k4_hypotheses.py` present for the hypotheses module specifically. Coverage for `frontier_checks.py` and `crib_constraints.py` specifically is **assumed: not confirmed** — no `test_frontier_checks.py` or `test_crib_constraints.py` found in this scan.

Churn: **assumed: not confirmed** (shallow clone, no history available).

Canaries: N/A (canary list only applies to the `stash` repo; not scanned this run).

## Refactor Opportunities by Phase (handoff notes, not yet actioned)

- **`src/kryptos/k4/frontier_checks.py`**: the module's own docstring already enumerates independent check families (`running_key_english`, `transposition_running_key_english`, `recurrence_key`, `general_alphabet_periodic`, `dial_key_scan`, `bearing_route_scan`, `hill_exhaustive`, `reconstruction_suite`). Smallest safe extraction: pull `hill_exhaustive` (likely self-contained matrix math) into `src/kryptos/k4/hill_checks.py` first, leaving the rest as a barrel import.
- **`src/kryptos/k4/crib_constraints.py`**: same pattern as above — needs a direct read to confirm which constraint families are independent before proposing a specific cut; flagged for next-cycle inspection rather than a concrete phase plan this run.

## Validation Plan (for a future `--refactor` pass)
- Run `tests/functional/test_k4_hypotheses.py` and the broader `tests/` suite after each extraction.
- For `frontier_checks.py`/`crib_constraints.py` extractions, add a planted-solution regression test per extracted check family before merging (the module's own docstring convention — "has a planted-solution test" — should carry over to any split).

## Repo Summary

| Repo | Top Concern | Priority | Notes |
|------|-------------|----------|-------|
| kryptos | `src/kryptos/k4/frontier_checks.py` — 8 cipher-family checks bundled in one new 1,131-line module | High | New since 2026-09-01; docstring already documents independent check families, making extraction low-ambiguity |

## Ordered Next-Cycle Targets (cross-repo, tier-weighted)

Shared across this run's three reports (vigil, vhs, kryptos) — see each report's own Repo Summary for per-repo context. Tier from `agent/projects/scope.md`: vigil = T1, vhs = T2, kryptos = untiered (not yet registered in vigil; ranks alongside T2/T3 per `LOC.md`).

1. `app/api/mcp/route.ts` (vigil, T1, 893 LOC) — High, extract tool handlers
2. `lib/sync.ts` (vigil, T1, 707 LOC) — High, extract fallback cache
3. `components/dashboard/RepoTableRow.tsx` (vigil, T1, 699 LOC) — High, extract derived-data hook, needs manual QC
4. `src/kryptos/k4/frontier_checks.py` (kryptos, untiered, 1,131 LOC) — High, extract `hill_exhaustive` first
5. `public/js/ui.js` (vhs, T2, 896 LOC) — High, extract CSV/bulk-action helpers
6. `src/server.js` (vhs, T2, 761 LOC) — High, extract route groups into `./modules/routes/*`
7. `src/kryptos/k4/crib_constraints.py` (kryptos, untiered, 877 LOC) — Medium-High, needs direct read before a phase plan

Tier reordered what raw LOC would have suggested: `frontier_checks.py` (1,131 LOC, the largest file in this run) would rank #1 by size alone, but vigil's three T1 findings are weighted ahead of it despite being smaller, since vigil is a T1 (Critical/production) repo and kryptos isn't yet tiered.
