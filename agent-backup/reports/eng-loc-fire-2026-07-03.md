---
kind: eng-loc
repo: fire
date: 2026-07-03
---

# ENG LOC Report: fire

> 🧭 [[repos/fire|fire]] · ← [[reports/eng-loc-fire-2026-06-25|2026-06-25]] · [[reports/eng-loc-fire-2026-07-04|2026-07-04]] → <!-- nav -->

**Date:** 2026-07-03
**Repo:** fire (fire)
**Thresholds:** max_lines=500, min_lines=30

## Large Files (> {max_lines} lines) — Refactor Candidates

| Lines | Path | Secondary Findings |
|-------|------|---------------------|
| 1352 | `tests/unit/finance-core.test.js` | Repeated block (4 occurrences, 10+ lines):         const rows = [
            [
                'Transaction Date',
       ... |
| 822 | `app/server.js` | Unused function (heuristic): switch |
| 680 | `app/lib/charts.js` | Unused function (heuristic): renderProjectionsChart; Unused function (heuristic): renderDashboardProjectionsChart; Repeated block (2 occurrences, 10+ lines):                         callback: (v) =>
                            '$' +
     ... |
| 622 | `app/lib/tables-assets.js` | Unused function (heuristic): renderRealEstateTable; Unused function (heuristic): renderVehiclesTable; Unused function (heuristic): renderScenarioComparison; Unused function (heuristic): renderMilestones; Unused function (heuristic): renderAllocMiniBarsBanner; Unused function (heuristic): renderDiversificationSuggestions; Unused function (heuristic): renderQuickStatsList; Unused function (heuristic): renderMonthlyCashFlow |
| 515 | `app/lib/tables-positions.js` | Unused function (heuristic): renderDashboardTopPositionsTable; Unused function (heuristic): renderDashboardLiquidPanel; Unused function (heuristic): renderImportedFilesTable; Unused function (heuristic): renderCustomAccountsTable; Unused function (heuristic): renderCDTable; Unused function (heuristic): renderUnifiedHoldingsTable; Unused function (heuristic): renderSideGigLedgerTable |

## Small Files (<= 30 lines) — Merge Candidates

_None_
