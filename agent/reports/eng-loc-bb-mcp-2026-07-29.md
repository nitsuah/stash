# ENG LOC Report — bb-mcp (2026-07-29)

**Thresholds**: `max_lines=500`, `min_lines=30`
**Extensions**: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rs`, `.java`, `.cs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.vue`, `.svelte`
**Excluded**: `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `.claude/worktrees/`, `.playwright-mcp/`, `.venv/`, `venv/`, `env/`

---

## 🔴 Too Large (> 500 lines) — Refactor Candidates

| Lines | File | Secondary Scan Notes |
|-------|------|---------------------|
| 697 | bb-mcp/src/index.ts | Main entry - extract routes, handlers |
| 589 | bb-mcp/src/tools/instructor.ts | Instructor tools - extract methods |
| 515 | bb-mcp/src/tools/student.ts | Student tools - extract methods |

---

## 🟢 Too Small (< 30 lines) — Merge Candidates

| Lines | File | Suggested Merge Target |
|-------|------|------------------------|
| 7 | bb-mcp/src/constants.ts | Merge with lib barrel |
| 22 | bb-mcp/src/privacy.ts | Merge with src |
| 25 | bb-mcp/config/vitest.config.ts | Check if test config |

---

*Generated: 2026-07-29*