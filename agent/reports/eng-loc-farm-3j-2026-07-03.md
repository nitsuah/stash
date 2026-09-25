# ENG LOC Report: farm-3j

> 🧭 [[repos/farm-3j|farm-3j]] · ← [[reports/eng-loc-farm-3j-2026-06-25|2026-06-25]] · [[reports/eng-loc-farm-3j-2026-07-04|2026-07-04]] → <!-- nav -->

**Date:** 2026-07-03
**Repo:** farm-3j (farm-3j)
**Thresholds:** max_lines=500, min_lines=30

## Large Files (> {max_lines} lines) — Refactor Candidates

| Lines | Path | Secondary Findings |
|-------|------|---------------------|
| 6120 | `components/rts/RTSMap.tsx` | Unused function (heuristic): makeSwordsman; Repeated block (6 occurrences, 10+ lines):                       if (xpGain === 0) return u;
                      const ne... |
| 993 | `components/rts/RTSUI.tsx` | — |
| 937 | `components/animations/HeaderCropRow.tsx` | Repeated block (2 occurrences, 10+ lines):         >
          ⛰️
        </div>
        <div
          className="text-6xl... |
| 813 | `lib/farm/__tests__/farmReducer.test.ts` | Repeated block (2 occurrences, 10+ lines):       };

      const action: FarmAction = {
        type: 'SPAWN_ANIMAL',
     ... |
| 728 | `lib/farm/__tests__/gameLogic.test.ts` | Repeated block (2 occurrences, 10+ lines):           type: 'fence',
          x: 52,
          y: 52,
          gridX: 10,
... |

## Small Files (<= 30 lines) — Merge Candidates

| Lines | Path | Suggested Merge Target |
|-------|------|------------------------|
| 2 | `global.d.ts` | next-env.d.ts |
| 5 | `app/farm/page.tsx` | app/farm/layout.tsx |
| 5 | `app/rtsfarm/layout.tsx` | app/rtsfarm/page.tsx |
| 6 | `next-env.d.ts` | global.d.ts |
| 6 | `lib/utils.ts` | lib/utils.test.ts |
| 7 | `app/rtsfarm/page.tsx` | app/rtsfarm/layout.tsx |
| 8 | `app/not-found.tsx` | app/global-error.tsx |
| 8 | `components/animations/index.ts` | — |
| 8 | `config/vitest.setup.ts` | — |
| 9 | `app/farm/layout.tsx` | app/farm/page.tsx |
| 21 | `app/global-error.tsx` | app/not-found.tsx |
| 25 | `components/rts/CommandCard.tsx` | — |
| 29 | `scripts/print-docker-port.js` | — |
| 30 | `lib/utils.test.ts` | lib/utils.ts |
| 30 | `lib/farm/FarmContext.tsx` | — |
