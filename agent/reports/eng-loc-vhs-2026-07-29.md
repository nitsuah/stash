# ENG LOC Report — vhs (2026-07-29)

> 🧭 [[repos/vhs|vhs]] · ← [[reports/eng-loc-vhs-2026-07-04|2026-07-04]] <!-- nav -->

**Thresholds**: `max_lines=500`, `min_lines=30`
**Extensions**: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rs`, `.java`, `.cs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.vue`, `.svelte`
**Excluded**: `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `.claude/worktrees/`, `.playwright-mcp/`, `.venv/`, `venv/`, `env/`

---

## 🔴 Too Large (> 500 lines) — Refactor Candidates

| Lines | File | Secondary Scan Notes |
|-------|------|---------------------|
| 579 | vhs/tests/coverage-boost.test.js | Test file - split by coverage area |
| 561 | vhs/src/server.js | Server entry - extract routes, modules |
| 509 | vhs/tests/server.test.js | Server tests - split by module |

---

## 🟢 Too Small (< 30 lines) — Merge Candidates

| Lines | File | Suggested Merge Target |
|-------|------|------------------------|
| 11 | vhs/playwright.config.js | Check if config |
| 11 | vhs/tests/basic.test.js | Merge with tests |
| 14 | vhs/src/modules/ids.js | Merge with modules |
| 14 | vhs/src/modules/retry.js | Merge with modules |
| 15 | vhs/test-current.js | Check if test script |
| 15 | vhs/test-debug.js | Check if debug script |
| 16 | vhs/jest.config.js | Check if config |
| 16 | vhs/src/modules/analytics.js | Merge with modules |
| 16 | vhs/src/modules/ollama.js | Merge with modules |

---

*Generated: 2026-07-29*
