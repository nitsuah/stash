# ENG LOC Report — fire (2026-07-29)

> 🧭 [[repos/fire|fire]] · ← [[reports/eng-loc-fire-2026-07-04|2026-07-04]] · [[reports/eng-loc-fire-2026-09-16|2026-09-16]] → <!-- nav -->

**Thresholds**: `max_lines=500`, `min_lines=30`
**Extensions**: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rs`, `.java`, `.cs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.vue`, `.svelte`
**Excluded**: `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `.claude/worktrees/`, `.playwright-mcp/`, `.venv/`, `venv/`, `env/`

---

## 🔴 Too Large (> 500 lines) — Refactor Candidates

| Lines | File | Secondary Scan Notes |
|-------|------|---------------------|
| 822 | fire/app/server.js | Server entry - extract routes, middleware |
| 680 | fire/app/lib/charts.js | Charts library - extract chart types |
| 622 | fire/app/lib/tables-assets.js | Assets tables - extract by type |
| 515 | fire/app/lib/tables-positions.js | Positions tables - extract by type |

---

## 🟢 Too Small (< 30 lines) — Merge Candidates

| Lines | File | Suggested Merge Target |
|-------|------|------------------------|
| 1 | fire/coverage/prettify.js | Generated coverage file |
| 2 | fire/app/lib/finance-parsing.js | Merge with finance-core |
| 2 | fire/app/lib/managers.js | Merge with finance-core |
| 2 | fire/app/lib/finance-core.js | Merge with finance-core |
| 2 | fire/tests/e2e/app-flow.test.js | Merge with e2e tests |
| 2 | fire/app/app.js | Check if app entry |
| 2 | fire/app/lib/projections.js | Merge with finance-core |
| 2 | fire/app/lib/side-gig.js | Merge with finance-core |
| 2 | fire/app/lib/finance-calcs.js | Merge with finance-core |
| 2 | fire/coverage/sorter.js | Check if needed |

---

*Generated: 2026-07-29*
