# ENG LOC Report: overseer
**Date:** 2026-07-03
**Repo:** overseer (overseer)
**Thresholds:** max_lines=500, min_lines=30

## Large Files (> {max_lines} lines) — Refactor Candidates

| Lines | Path | Secondary Findings |
|-------|------|---------------------|
| 853 | `lib/github.ts` | Unused function (heuristic): constructor |
| 754 | `app/api/enrich-template/route.ts` | Unused function (heuristic): switch |
| 750 | `components/GuidedTour.tsx` | Unused function (heuristic): switch; Repeated block (2 occurrences, 10+ lines):                   setTimeout(() => {
                    // Give DOM time to upd... |
| 670 | `lib/ai-prompt-chain.ts` | — |
| 643 | `lib/github.test.ts` | — |
| 639 | `hooks/useRepoActions.ts` | Repeated block (2 occurrences, 10+ lines):       });

      if (previewRes.ok) {
        const { previews } = await preview... |
| 627 | `lib/sync.ts` | Repeated block (2 occurrences, 10+ lines):         )
        ON CONFLICT (name) DO UPDATE SET
          description = EXCLU... |
| 548 | `components/dashboard/RepoTableRow.tsx` | — |
| 516 | `components/Header.tsx` | — |
| 508 | `components/repo-details/RoadmapSection.tsx` | Unused function (heuristic): switch |

## Small Files (<= 30 lines) — Merge Candidates

| Lines | Path | Suggested Merge Target |
|-------|------|------------------------|
| 2 | `app/api/auth/[...nextauth]/route.ts` | — |
| 2 | `lib/constants.ts` | lib/default-repos.ts |
| 6 | `next-env.d.ts` | next.config.ts |
| 9 | `scripts/check-last-sync.ts` | scripts/migrate.ts |
| 14 | `next.config.ts` | next-env.d.ts |
| 14 | `types/next-auth.d.ts` | — |
| 15 | `components/ScrollPane.tsx` | components/Toast.tsx |
| 15 | `lib/default-repos.ts` | lib/constants.ts |
| 17 | `components/Toast.tsx` | components/ScrollPane.tsx |
| 18 | `templates/testing/vitest.config.ts` | — |
| 19 | `components/dashboard/repo-row/repo-row-utils.ts` | — |
| 20 | `tests/auth.setup.ts` | tests/setup-env.ts |
| 20 | `tests/setup-env.ts` | tests/auth.setup.ts |
| 22 | `components/icons/GithubIcon.tsx` | — |
| 23 | `scripts/migrate.ts` | scripts/check-last-sync.ts |
| 24 | `lib/log.ts` | lib/constants.ts |
| 28 | `lib/markdown-utils.tsx` | lib/constants.ts |
| 29 | `scripts/test-parser.ts` | scripts/check-last-sync.ts |
| 30 | `app/layout.tsx` | — |
| 30 | `app/test-health/page.tsx` | — |
| 30 | `config/vitest.config.ts` | — |
| 30 | `lib/gemini-config.ts` | lib/constants.ts |
