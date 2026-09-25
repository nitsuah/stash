# ENG LOC Report — overseer (2026-07-29)

> 🧭 [[repos/vigil|overseer]] · ← [[reports/eng-loc-overseer-2026-07-04|2026-07-04]] <!-- nav -->

**Thresholds**: `max_lines=500`, `min_lines=30`
**Extensions**: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rs`, `.java`, `.cs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.vue`, `.svelte`
**Excluded**: `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `.claude/worktrees/`, `.playwright-mcp/`, `.venv/`, `venv/`, `env/`

---

## 🔴 Too Large (> 500 lines) — Refactor Candidates

| Lines | File | Secondary Scan Notes |
|-------|------|---------------------|
| 853 | overseer/lib/github.ts | GitHub API - extract endpoints |
| 754 | overseer/app/api/enrich-template/route.ts | Enrich template route - extract logic |
| 750 | overseer/components/GuidedTour.tsx | Guided tour - extract steps |
| 670 | overseer/lib/ai-prompt-chain.ts | AI prompt chain - extract chains |
| 643 | overseer/lib/github.test.ts | GitHub tests - split by endpoint |
| 639 | overseer/hooks/useRepoActions.ts | Repo actions hook - extract actions |
| 631 | overseer/lib/sync.ts | Sync logic - extract operations |
| 548 | overseer/components/dashboard/RepoTableRow.tsx | Table row - extract cells |
| 516 | overseer/components/Header.tsx | Header - extract nav, user menu |
| 508 | overseer/components/repo-details/RoadmapSection.tsx | Roadmap section - extract items |

---

## 🟢 Too Small (< 30 lines) — Merge Candidates

| Lines | File | Suggested Merge Target |
|-------|------|------------------------|
| 2 | overseer/lib/constants.ts | Merge with lib barrel |
| 9 | overseer/scripts/check-last-sync.ts | Check if script |
| 9 | overseer/components/ScrollPane.tsx | Merge with UI components |
| 14 | overseer/next.config.ts | Check if config |
| 14 | overseer/types/next-auth.d.ts | Merge with types |
| 15 | overseer/components/Toast.tsx | Merge with UI components |
| 15 | overseer/lib/default-repos.ts | Merge with lib |
| 15 | overseer/components/dashboard/repo-row/repo-row-utils.ts | Merge with repo-row |
| 17 | overseer/templates/testing/vitest.config.ts | Check if test config |
| 18 | overseer/scripts/migrate.ts | Check if migration |
| 18 | overseer/scripts/test-parser.ts | Check if script |
| 22 | overseer/components/icons/GithubIcon.tsx | Merge with icons |
| 24 | overseer/lib/log.ts | Merge with lib |
| 24 | overseer/lib/markdown-utils.tsx | Merge with lib |
| 28 | overseer/lib/log.ts | Duplicate |

---

*Generated: 2026-07-29*
