---
kind: eng-loc
repo: kryptos
date: 2026-07-03
---

# ENG LOC Report: kryptos

> 🧭 [[repos/kryptos|kryptos]] · ← [[reports/eng-loc-kryptos-2026-06-25|2026-06-25]] · [[reports/eng-loc-kryptos-2026-07-04|2026-07-04]] → <!-- nav -->

**Date:** 2026-07-03
**Repo:** kryptos (kryptos)
**Thresholds:** max_lines=500, min_lines=30

## Large Files (> {max_lines} lines) — Refactor Candidates

| Lines | Path | Secondary Findings |
|-------|------|---------------------|
| 903 | `src/kryptos/k4/transposition_analysis.py` | Unused function (heuristic): score_combined_with_words; Unused function (heuristic): apply_columnar_permutation_encrypt; Unused function (heuristic): test_all_rotations; Unused function (heuristic): detect_period_by_brute_force; Unused function (heuristic): solve_columnar_permutation_simulated_annealing_multi_start; Unused function (heuristic): solve_columnar_permutation_exhaustive |
| 897 | `src/kryptos/k4/hypotheses.py` | Repeated block (2 occurrences, 10+ lines): 
    def _build_grid(self, keyword: str) -> list[list[str]]:
        alphabet = ... |
| 756 | `src/kryptos/cli/main.py` | Repeated block (2 occurrences, 10+ lines):     sp_tuning_holdout.set_defaults(func=cmd_tuning_holdout_score)

    sp_spy_ev... |
| 733 | `htmlcov/coverage_html_cb_497bf287.js` | — |
| 658 | `src/kryptos/k4/scoring.py` | — |
| 650 | `src/kryptos/agents/ops_director.py` | Unused function (heuristic): __init__; Unused function (heuristic): synthesize_agent_insights |
| 610 | `src/kryptos/k4/vigenere_key_recovery.py` | Unused function (heuristic): check_keyed_alphabet_realignment; Unused function (heuristic): recover_key_with_crib |
| 606 | `src/kryptos/autonomous_coordinator.py` | Unused function (heuristic): __init__; Unused function (heuristic): load_tested_keys; Unused function (heuristic): get_latest_checkpoint |
| 591 | `tests/functional/test_k4_hypotheses.py` | Unused function (heuristic): test_hill_cipher_exhaustive_search; Unused function (heuristic): test_hill_3x3_genetic_algorithm; Unused function (heuristic): test_transposition_berlin_clock_constraints; Unused function (heuristic): test_vigenere_hypothesis; Unused function (heuristic): test_playfair_hypothesis; Unused function (heuristic): test_berlin_clock_vigenere_candidate; Unused function (heuristic): test_simple_substitution_hypothesis; Unused function (heuristic): test_autokey_hypothesis; Unused function (heuristic): test_four_square_hypothesis; Unused function (heuristic): test_bifid_hypothesis; Unused function (heuristic): test_composite_hypothesis_chaining; Unused function (heuristic): test_composite_transformation_chain_metadata; Unused function (heuristic): test_composite_score_propagation; Unused function (heuristic): test_transposition_then_hill_basic; Unused function (heuristic): test_vigenere_then_transposition_basic; Unused function (heuristic): test_substitution_then_transposition_basic; Unused function (heuristic): test_composite_stage1_candidate_limit; Unused function (heuristic): test_hill_then_transposition_basic; Unused function (heuristic): test_autokey_then_transposition_basic; Unused function (heuristic): test_playfair_then_transposition_basic; Unused function (heuristic): test_double_transposition_basic; Unused function (heuristic): test_vigenere_then_hill_basic; Repeated block (4 occurrences, 10+ lines):         ciphertext = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIA... |
| 579 | `src/kryptos/pipeline/attack_generator.py` | Unused function (heuristic): __init__; Unused function (heuristic): generate_from_literature; Unused function (heuristic): generate_comprehensive_queue; Unused function (heuristic): export_queue |

## Small Files (<= 30 lines) — Merge Candidates

| Lines | Path | Suggested Merge Target |
|-------|------|------------------------|
| 1 | `tests/__init__.py` | — |
| 4 | `src/kryptos/stages/__init__.py` | src/kryptos/stages/mock_stage.py |
| 5 | `src/kryptos/provenance/__init__.py` | — |
| 5 | `src/kryptos/scoring/__init__.py` | — |
| 5 | `src/kryptos/tuning/__init__.py` | — |
| 7 | `src/kryptos/research/__init__.py` | — |
| 8 | `frontend/src/components/MetricCard.tsx` | frontend/src/components/MetricCards.tsx |
| 8 | `src/kryptos/api/__init__.py` | — |
| 8 | `tests/smoke/test_cli.py` | tests/smoke/test_deprecation_warning.py |
| 10 | `frontend/src/main.tsx` | — |
| 10 | `src/kryptos/cli/__init__.py` | — |
| 10 | `src/kryptos/rag/__init__.py` | src/kryptos/rag/embeddings.py |
| 11 | `tests/e2e/test_k4_demo.py` | tests/e2e/test_autopilot_demo.py |
| 12 | `tests/e2e/test_autopilot_demo.py` | tests/e2e/test_k4_demo.py |
| 13 | `scripts/find_free_port.py` | — |
| 13 | `src/kryptos/pipeline/__init__.py` | — |
| 13 | `tests/functional/test_logging_setup.py` | tests/functional/test_ciphers_rotate_matrix_minimal.py |
| 13 | `tests/smoke/test_deprecation_warning.py` | tests/smoke/test_cli.py |
| 14 | `frontend/src/components/MetricCards.tsx` | frontend/src/components/MetricCard.tsx |
| 14 | `tests/functional/test_ciphers_rotate_matrix_minimal.py` | tests/functional/test_logging_setup.py |
| 14 | `tests/functional/test_scoring_letter_coverage_empty.py` | tests/functional/test_logging_setup.py |
| 15 | `tests/functional/test_transposition_constraints_empty.py` | tests/functional/test_logging_setup.py |
| 16 | `frontend/src/components/FormField.tsx` | frontend/src/components/MetricCard.tsx |
| 16 | `src/kryptos/agents/__init__.py` | — |
| 16 | `tests/functional/test_public_api.py` | tests/functional/test_logging_setup.py |
| 17 | `frontend/vite.config.ts` | — |
| 17 | `frontend/src/components/CandidateRow.tsx` | frontend/src/components/MetricCard.tsx |
| 17 | `frontend/src/components/StatusIndicator.tsx` | frontend/src/components/MetricCard.tsx |
| 17 | `tests/functional/test_analysis_edge_cases.py` | tests/functional/test_logging_setup.py |
| 17 | `tests/functional/test_pipeline_parallel_hill_variants.py` | tests/functional/test_logging_setup.py |
| 18 | `tests/functional/test_multi_crib_attempt_log.py` | tests/functional/test_logging_setup.py |
| 18 | `tests/functional/test_scoring_cache_branch.py` | tests/functional/test_logging_setup.py |
| 19 | `frontend/src/components/KeyedAlphabetTable.tsx` | frontend/src/components/MetricCard.tsx |
| 19 | `src/kryptos/k4/hill_search.py` | — |
| 19 | `src/kryptos/stages/mock_stage.py` | src/kryptos/stages/__init__.py |
| 19 | `tests/functional/test_docs_breadcrumbs.py` | tests/functional/test_logging_setup.py |
| 19 | `tests/functional/test_k4_decrypt_best.py` | tests/functional/test_logging_setup.py |
| 19 | `tests/functional/test_scoring_positional_empty.py` | tests/functional/test_logging_setup.py |
| 20 | `src/kryptos/deprecation.py` | src/kryptos/analysis.py |
| 20 | `tests/functional/test_hill_cipher_edge.py` | tests/functional/test_logging_setup.py |
| 20 | `tests/functional/test_pipeline_adaptive_transposition_stage.py` | tests/functional/test_logging_setup.py |
| 20 | `tests/functional/test_pipeline_masking_null_chars.py` | tests/functional/test_logging_setup.py |
| 20 | `tests/functional/test_pipeline_noop_multi_crib.py` | tests/functional/test_logging_setup.py |
| 20 | `tests/functional/test_pipeline_route_stage.py` | tests/functional/test_logging_setup.py |
| 21 | `src/kryptos/k2/__init__.py` | — |
| 21 | `tests/functional/test_pipeline_clock_attempt_log.py` | tests/functional/test_logging_setup.py |
| 22 | `tests/e2e/test_k4_pipeline_stage.py` | tests/e2e/test_k4_demo.py |
| 22 | `tests/functional/test_ciphers_polybius_expected.py` | tests/functional/test_logging_setup.py |
| 22 | `tests/functional/test_k4_scoring.py` | tests/functional/test_logging_setup.py |
| 22 | `tests/functional/test_pipeline_dynamic_adaptive.py` | tests/functional/test_logging_setup.py |
| 22 | `tests/functional/test_pipeline_pruning.py` | tests/functional/test_logging_setup.py |
| 22 | `tests/functional/test_scoring_letter_freq_fallback.py` | tests/functional/test_logging_setup.py |
| 23 | `src/kryptos/analysis.py` | src/kryptos/deprecation.py |
| 23 | `tests/functional/test_hill_search_module.py` | tests/functional/test_logging_setup.py |
| 23 | `tests/functional/test_k4_entropy.py` | tests/functional/test_logging_setup.py |
| 23 | `tests/functional/test_transposition.py` | tests/functional/test_logging_setup.py |
| 23 | `tests/functional/test_transposition_constraints_bonus.py` | tests/functional/test_logging_setup.py |
| 24 | `frontend/src/components/AttackVectorVisualizer.tsx` | frontend/src/components/MetricCard.tsx |
| 24 | `tests/functional/test_rarity_weighted_crib_bonus.py` | tests/functional/test_logging_setup.py |
| 24 | `tests/functional/test_scoring_error_paths.py` | tests/functional/test_logging_setup.py |
| 24 | `tests/functional/test_transposition_constraints_early_continue.py` | tests/functional/test_logging_setup.py |
| 25 | `frontend/src/components/RunRow.tsx` | frontend/src/components/MetricCard.tsx |
| 25 | `src/kryptos/k3/__init__.py` | — |
| 25 | `src/kryptos/k4/tuning/__init__.py` | — |
| 25 | `tests/functional/test_ciphers_polybius_abc.py` | tests/functional/test_logging_setup.py |
| 25 | `tests/functional/test_cribs_functions.py` | tests/functional/test_logging_setup.py |
| 26 | `frontend/src/components/CandidatesTable.tsx` | frontend/src/components/MetricCard.tsx |
| 26 | `src/kryptos/rag/embeddings.py` | src/kryptos/rag/__init__.py |
| 26 | `tests/e2e/test_k4_fusion.py` | tests/e2e/test_k4_demo.py |
| 26 | `tests/functional/test_ciphers_edge_cases.py` | tests/functional/test_logging_setup.py |
| 26 | `tests/functional/test_multiproc_helpers.py` | tests/functional/test_logging_setup.py |
| 26 | `tests/functional/test_spy_extractor_threshold.py` | tests/functional/test_logging_setup.py |
| 27 | `src/kryptos/k1/__init__.py` | — |
| 27 | `src/kryptos/spy/__init__.py` | — |
| 27 | `tests/functional/test_spy_extractor.py` | tests/functional/test_logging_setup.py |
| 28 | `tests/functional/test_k4_transposition_adaptive.py` | tests/functional/test_logging_setup.py |
| 28 | `tests/functional/test_scoring_additional_branches.py` | tests/functional/test_logging_setup.py |
| 29 | `tests/functional/test_composite_report_no_weights.py` | tests/functional/test_logging_setup.py |
| 29 | `tests/functional/test_positional_letter_deviation.py` | tests/functional/test_logging_setup.py |
