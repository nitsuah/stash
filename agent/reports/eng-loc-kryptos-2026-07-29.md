# ENG LOC Report — kryptos (2026-07-29)

> 🧭 [[repos/kryptos|kryptos]] · ← [[reports/eng-loc-kryptos-2026-07-04|2026-07-04]] · [[reports/eng-loc-kryptos-2026-09-01|2026-09-01]] → <!-- nav -->

**Thresholds**: `max_lines=500`, `min_lines=30`
**Extensions**: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rs`, `.java`, `.cs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.vue`, `.svelte`
**Excluded**: `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `.claude/worktrees/`, `.playwright-mcp/`, `.venv/`, `venv/`, `env/`, `htmlcov/`

---

## 🔴 Too Large (> 500 lines) — Refactor Candidates

| Lines | File | Secondary Scan Notes |
|-------|------|---------------------|
| 903 | kryptos/src/kryptos/k4/transposition_analysis.py | Transposition analysis - extract algorithms |
| 897 | kryptos/src/kryptos/k4/hypotheses.py | Hypotheses - split by type |
| 756 | kryptos/src/kryptos/cli/main.py | CLI main - extract commands |
| 733 | kryptos/htmlcov/coverage_html_cb_497bf287.js | Generated coverage HTML |
| 658 | kryptos/src/kryptos/k4/scoring.py | Scoring - extract metrics |
| 650 | kryptos/src/kryptos/agents/ops_director.py | Ops director - extract operations |
| 610 | kryptos/src/kryptos/k4/vigenere_key_recovery.py | Vigenere recovery - extract methods |
| 606 | kryptos/src/kryptos/autonomous_coordinator.py | Coordinator - extract stages |
| 591 | kryptos/tests/functional/test_k4_hypotheses.py | Tests - split by hypothesis |
| 579 | kryptos/src/kryptos/pipeline/attack_generator.py | Attack generator - extract strategies |

---

## 🟢 Too Small (< 30 lines) — Merge Candidates

| Lines | File | Suggested Merge Target |
|-------|------|------------------------|
| 1 | kryptos/tests/__init__.py | Package init |
| 4 | kryptos/src/kryptos/stages/__init__.py | Package init |
| 5 | kryptos/src/kryptos/provenance/__init__.py | Package init |
| 5 | kryptos/src/kryptos/scoring/__init__.py | Package init |
| 5 | kryptos/src/kryptos/tuning/__init__.py | Package init |
| 5 | kryptos/src/kryptos/research/__init__.py | Package init |
| 5 | kryptos/src/kryptos/rag/__init__.py | Package init |
| 7 | kryptos/src/kryptos/api/__init__.py | Package init |
| 7 | kryptos/frontend/src/components/MetricCard.tsx | Merge with MetricCards |
| 8 | kryptos/frontend/src/main.tsx | Check if entry |
| 8 | kryptos/tests/smoke/test_cli.py | Merge with smoke tests |
| 8 | kryptos/src/kryptos/cli/__init__.py | Package init |
| 10 | kryptos/frontend/src/components/MetricCards.tsx | Merge with MetricCard |
| 10 | kryptos/frontend/src/components/KeyedAlphabetTable.tsx | Check if component |
| 10 | kryptos/src/kryptos/cli/__init__.py | Duplicate |
| 11 | kryptos/scripts/find_free_port.py | Check if utility |
| 13 | kryptos/src/kryptos/pipeline/__init__.py | Package init |
| 13 | kryptos/tests/functional/test_logging_setup.py | Merge with functional |
| 13 | kryptos/scripts/find_free_port.py | Duplicate |
| 13 | kryptos/tests/functional/test_public_api.py | Merge with functional |
| 13 | kryptos/tests/smoke/test_deprecation_warning.py | Merge with smoke |
| 14 | kryptos/frontend/src/components/FormField.tsx | Merge with forms |
| 14 | kryptos/tests/functional/test_ciphers_rotate_matrix_minimal.py | Merge with functional |
| 14 | kryptos/tests/e2e/test_k4_demo.py | Merge with e2e |
| 14 | kryptos/tests/functional/test_scoring_letter_coverage_empty.py | Merge with functional |
| 16 | kryptos/src/kryptos/agents/__init__.py | Package init |
| 16 | kryptos/frontend/src/components/StatusIndicator.tsx | Merge with indicators |
| 16 | kryptos/tests/functional/test_pipeline_parallel_hill_variants.py | Merge with functional |
| 16 | kryptos/frontend/src/components/CandidateRow.tsx | Merge with table |
| 16 | kryptos/frontend/vite.config.ts | Check if config |
| 17 | kryptos/tests/functional/test_analysis_edge_cases.py | Merge with functional |
| 17 | kryptos/frontend/src/components/KeyedAlphabetTable.tsx | Duplicate |
| 17 | kryptos/tests/functional/test_pipeline_noop_multi_crib.py | Merge with functional |
| 17 | kryptos/src/kryptos/stages/mock_stage.py | Check if mock |
| 17 | kryptos/tests/functional/test_pipeline_masking_null_chars.py | Merge with functional |
| 17 | kryptos/tests/functional/test_composite_report_no_weights.py | Merge with functional |
| 17 | kryptos/frontend/src/components/MetricCard.tsx | Duplicate |
| 18 | kryptos/tests/functional/test_scoring_cache_branch.py | Merge with functional |
| 18 | kryptos/tests/functional/test_multi_crib_attempt_log.py | Merge with functional |
| 18 | kryptos/tests/functional/test_pipeline_clock_attempt_log.py | Merge with functional |
| 18 | kryptos/tests/functional/test_scoring_positional_empty.py | Merge with functional |
| 18 | kryptos/tests/functional/test_transposition_constraints_bonus.py | Merge with functional |
| 18 | kryptos/tests/functional/test_k4_decrypt_best.py | Merge with functional |
| 18 | kryptos/tests/functional/test_docs_breadcrumbs.py | Merge with functional |
| 19 | kryptos/src/kryptos/k4/hill_search.py | Check if module |
| 19 | kryptos/frontend/src/components/KeyedAlphabetTable.tsx | Triplicate |
| 19 | kryptos/tests/functional/test_hill_cipher_edge.py | Merge with functional |
| 19 | kryptos/tests/e2e/test_k4_pipeline_stage.py | Merge with e2e |
| 20 | kryptos/tests/functional/test_pipeline_adaptive_transposition_stage.py | Merge with functional |
| 20 | kryptos/src/kryptos/deprecation.py | Check if module |
| 20 | kryptos/tests/functional/test_ciphers_polybius_expected.py | Merge with functional |
| 20 | kryptos/tests/functional/test_scoring_letter_freq_fallback.py | Merge with functional |
| 20 | kryptos/tests/functional/test_k4_entropy.py | Merge with functional |

---

*Generated: 2026-07-29*
