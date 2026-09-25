---
kind: eng-loc
repo: gcp
date: 2026-07-29
---

# ENG LOC Report — gcp (2026-07-29)

> 🧭 [[repos/gcp|gcp]] <!-- nav -->

**Thresholds**: `max_lines=500`, `min_lines=30`
**Extensions**: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rs`, `.java`, `.cs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.vue`, `.svelte`
**Excluded**: `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `.claude/worktrees/`, `.playwright-mcp/`, `.venv/`, `venv/`, `env/`

---

## 🔴 Too Large (> 500 lines) — Refactor Candidates

| Lines | File | Secondary Scan Notes |
|-------|------|---------------------|
| 778 | gcp/gcp/copy_folder.py | Copy folder script - extract operations |
| 635 | gcp/apps/server.js | Server entry - extract routes |
| 633 | gcp/tests/test_q3_features.py | Tests - split by feature |
| 377 | gcp/tests/test_main.py | Tests - split by module |
| 369 | gcp/tests/test_copy_folder_extended.py | Tests - split by case |
| 334 | gcp/gcp/gcp_setup.py | GCP setup - extract configs |
| 324 | gcp/apps/public/app.js | Public app - extract components |

---

## 🟢 Too Small (< 30 lines) — Merge Candidates

| Lines | File | Suggested Merge Target |
|-------|------|------------------------|
| 3 | gcp/gcp/__init__.py | Package init |

---

*Generated: 2026-07-29*
