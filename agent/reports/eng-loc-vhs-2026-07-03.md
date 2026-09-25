# ENG LOC Report: vhs

> 🧭 [[repos/vhs|vhs]] · ← [[reports/eng-loc-vhs-2026-06-25|2026-06-25]] · [[reports/eng-loc-vhs-2026-07-04|2026-07-04]] → <!-- nav -->

**Date:** 2026-07-03
**Repo:** vhs (vhs)
**Thresholds:** max_lines=500, min_lines=30

## Large Files (> {max_lines} lines) — Refactor Candidates

| Lines | Path | Secondary Findings |
|-------|------|---------------------|
| 1165 | `.claude/worktrees/fix-env-path/public/js/inventory.js` | Unused function (heuristic): openNewTapeModal; Unused function (heuristic): _fetchPosterImage; Unused function (heuristic): _fillLookup |
| 1165 | `.claude/worktrees/vhs-omdb-fixes/public/js/inventory.js` | Unused function (heuristic): openNewTapeModal; Unused function (heuristic): _fetchPosterImage; Unused function (heuristic): _fillLookup |
| 1165 | `public/js/inventory.js` | Unused function (heuristic): openNewTapeModal; Unused function (heuristic): _fetchPosterImage; Unused function (heuristic): _fillLookup |
| 1002 | `.claude/worktrees/vhs-omdb-fixes/src/server.js` | Unused function (heuristic): cleanupOldLookups |
| 1002 | `src/server.js` | Unused function (heuristic): cleanupOldLookups |
| 754 | `.claude/worktrees/fix-env-path/server.js` | — |
| 571 | `.claude/worktrees/fix-env-path/tests/coverage-boost.test.js` | Unused function (heuristic): beforeEach |
| 571 | `.claude/worktrees/vhs-omdb-fixes/tests/coverage-boost.test.js` | Unused function (heuristic): beforeEach |
| 571 | `.claude/worktrees/vhs-refactor-modules/tests/coverage-boost.test.js` | Unused function (heuristic): beforeEach |
| 571 | `tests/coverage-boost.test.js` | Unused function (heuristic): beforeEach |
| 514 | `.claude/worktrees/vhs-omdb-fixes/tests/test-omdb-enhancements.spec.js` | Unused function (heuristic): beforeEach; Unused function (heuristic): afterEach; Repeated block (4 occurrences, 10+ lines): 
      mockQuery.mockImplementation((query, ...params) => {
        if (query.in... |
| 514 | `tests/test-omdb-enhancements.spec.js` | Unused function (heuristic): beforeEach; Unused function (heuristic): afterEach; Repeated block (4 occurrences, 10+ lines): 
      mockQuery.mockImplementation((query, ...params) => {
        if (query.in... |
| 508 | `.claude/worktrees/fix-env-path/tests/server.test.js` | Unused function (heuristic): beforeEach |
| 508 | `.claude/worktrees/vhs-omdb-fixes/tests/server.test.js` | Unused function (heuristic): beforeEach |
| 508 | `.claude/worktrees/vhs-refactor-modules/tests/server.test.js` | Unused function (heuristic): beforeEach |
| 508 | `tests/server.test.js` | Unused function (heuristic): beforeEach |

## Small Files (<= 30 lines) — Merge Candidates

| Lines | Path | Suggested Merge Target |
|-------|------|------------------------|
| 11 | `playwright.config.js` | jest.config.js |
| 11 | `.claude/worktrees/fix-env-path/playwright.config.js` | .claude/worktrees/fix-env-path/jest.config.js |
| 11 | `.claude/worktrees/fix-env-path/tests/basic.test.js` | — |
| 11 | `.claude/worktrees/vhs-omdb-fixes/playwright.config.js` | .claude/worktrees/vhs-omdb-fixes/jest.config.js |
| 11 | `.claude/worktrees/vhs-omdb-fixes/tests/basic.test.js` | — |
| 11 | `.claude/worktrees/vhs-refactor-modules/playwright.config.js` | .claude/worktrees/vhs-refactor-modules/jest.config.js |
| 11 | `.claude/worktrees/vhs-refactor-modules/tests/basic.test.js` | — |
| 11 | `tests/basic.test.js` | — |
| 14 | `.claude/worktrees/vhs-refactor-modules/src/modules/ids.js` | .claude/worktrees/vhs-refactor-modules/src/modules/json-parser.js |
| 14 | `.claude/worktrees/vhs-refactor-modules/src/modules/json-parser.js` | .claude/worktrees/vhs-refactor-modules/src/modules/ids.js |
| 14 | `.claude/worktrees/vhs-refactor-modules/src/modules/retry.js` | .claude/worktrees/vhs-refactor-modules/src/modules/ids.js |
| 16 | `jest.config.js` | playwright.config.js |
| 16 | `.claude/worktrees/fix-env-path/jest.config.js` | .claude/worktrees/fix-env-path/playwright.config.js |
| 16 | `.claude/worktrees/vhs-omdb-fixes/jest.config.js` | .claude/worktrees/vhs-omdb-fixes/playwright.config.js |
| 16 | `.claude/worktrees/vhs-refactor-modules/jest.config.js` | .claude/worktrees/vhs-refactor-modules/playwright.config.js |
| 16 | `.claude/worktrees/vhs-refactor-modules/test-debug.js` | .claude/worktrees/vhs-refactor-modules/playwright.config.js |
| 16 | `.claude/worktrees/vhs-refactor-modules/src/modules/analytics.js` | .claude/worktrees/vhs-refactor-modules/src/modules/ids.js |
| 25 | `.claude/worktrees/fix-env-path/public/js/init.js` | — |
| 25 | `.claude/worktrees/vhs-omdb-fixes/public/js/init.js` | — |
| 25 | `public/js/init.js` | — |
| 26 | `.claude/worktrees/vhs-refactor-modules/src/modules/ollama.js` | .claude/worktrees/vhs-refactor-modules/src/modules/ids.js |
| 28 | `.claude/worktrees/vhs-refactor-modules/public/js/modules/inventory-state.js` | — |
