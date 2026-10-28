---
HEAD: ebbb3051487367588a1b46f10df4b1c4063cc278
kind: eng-loc
repo: osrs
date: 2026-10-01
---

# ENG LOC Report — osrs (2026-10-01)

> 🧭 [[repos/osrs|osrs]] <!-- nav -->

**Mode**: `--report` (dry run, no refactoring performed)
**Thresholds**: `max_lines=500`, `min_lines=30`
**Extensions**: `.ts`, `.tsx`, `.js`, `.jsx`, `.mjs`, `.py`, `.go`, `.rs`, `.java`, `.cs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.vue`, `.svelte`
**Excluded**: `*.lock`, `*-lock.json`, `*.min.*`, `dist/`, `build/`, `vendor/`, `node_modules/`, `__pycache__/`, `*.pyc`, `*.map`, `*.d.ts`, binary assets

Source scanned: 22 files, 1,914 LOC. Analyzed from a `--depth 1` clone (single commit) — git history/churn signals are **not available** this run.

---

## Top LOC Files

| File | LOC | Lang | Role |
|---|---|---|---|
| `tests/test_question_handler.py` | 199 | Py | Test suite |
| `tests/test_health.py` | 160 | Py | Test suite |
| `tests/test_utils.py` | 152 | Py | Test suite |
| `tests/test_checkpoint.py` | 142 | Py | Test suite |
| `bot/skills/thieving.py` | 142 | Py | Thieving skill automation |
| `bot/skills/question_handler.py` | 137 | Py | Random-event / question handling |
| `bot/health.py` | 135 | Py | HP monitoring |
| `bot/checkpoint.py` | 125 | Py | Progress checkpointing |
| `tests/test_camera.py` | 124 | Py | Test suite |
| `bot/skills/fishing.py` | 114 | Py | Fishing skill automation |

No file exceeds `max_lines=500` — the largest source file (`bot/skills/thieving.py`, 142 LOC) is well under threshold. **No Critical/High/Medium refactor targets this run.**

---

## Risk Rank & Rationale

No file in this repo warrants a refactor flag by LOC.md's rules (require ≥1 structural rationale, never size alone — and no file is even large enough to raise the question). This is a small, flat automation-script codebase organized by skill (`bot/skills/*.py`), each file single-purpose.

### Merge candidates (`min_lines=30`) — **Low priority, informational only**
5 files are ≤30 lines:

| File | LOC | Note |
|---|---|---|
| `bot/camera.py` | 22 | Two tightly-scoped camera/zoom helpers |
| `bot/compass.py` | 10 | Single compass-click helper |
| `bot/config.py` | 13 | INI config loader |
| `tests/conftest.py` | 7 | Pytest fixtures |
| `tests/test_smoke.py` | 4 | Smoke test |

Each represents a distinct hardware-interaction or test-infra concern rather than accidental fragmentation — per LOC.md, small size alone isn't a merge mandate without a concrete reason (e.g. always imported together, near-identical surface area). `camera.py` and `compass.py` both wrap simple `pyautogui` calls for viewport control and could reasonably live in one `bot/viewport.py`, but this is a cosmetic consolidation, not a complexity fix — not worth a PR on its own.

---

## Refactor Opportunities by Phase

None proposed this cycle — no file meets the bar for a refactor target.

## Validation Plan

N/A — no changes proposed.

---

## Summary

| Repo | Top concern | Priority | Notes |
|---|---|---|---|
| osrs | None — all files well under threshold | None | Healthy, flat `bot/skills/*.py` structure; largest file is 142 LOC |

**Churn/history**: not assessable — analysis ran against a `--depth 1` clone (single commit visible).
**Canaries**: n/a — `stash` (the only tracked canary file's repo) was not in this run's target set.

---

## Ordered Next-Cycle Targets (across all 3 repos analyzed this run)

1. `games: app/lib/tank/TankGame.jsx` (698 LOC) — thin test coverage, ~470-line component mixing state/input/loop/render. Highest ROI.
2. `bb-mcp: src/index.ts` (1072 LOC) — `startHttpServer()` mixes HTTP transport, OAuth, and health/metrics in one ~382-line function.
3. `games: app/lib/asteroid/_comp/Game/Game.jsx` (721 LOC) — lower urgency than Tank; logic already extracted to tested handler files, this is composition/wiring.
4. `bb-mcp: src/tools/admin.ts` (728 LOC) — largest tool module, but single-concern and test-covered.
5. `bb-mcp: src/tools/{grade-writeback,parent,instructor,student,webhook-tools}.ts` (505–613 LOC each) — same low-risk pattern, split only if they keep growing.
6. `games: app/utils/audio/SoundManager.js` (820 LOC) — single concern (audio synthesis), low priority.
7. `games: app/_components/home/ArcadeLayout.tsx` (661 LOC) — CSS-heavy, defer to a design-system pass, not an LOC cycle.
8. `osrs` — nothing queued; repo is clean this run.
