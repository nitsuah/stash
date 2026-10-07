---
kind: rsi-report
---

# RSI report — 2026-10

> 🧭 ← [[reports/rsi-report-2026-09|2026-09]] <!-- nav -->

This is a catch-up run of `monthly-self-improvement`. The 10-02 run was DEFERRED with the weekly window at 99%. `ops-catchup` scheduled this one for 2026-10-07 16:30 ET, after the reset. Usage at the start: weekly 6%, 5-hour 36%. Spec: [[RSI]]. Every prompt, wrapper and memory edit is logged first in `agent/logs/rsi-changes.log`, which is local-only.

## Inputs read
- [[usage-report-2026-09]] (written 10-01 and left uncommitted; it lands in this PR), [[pmo-audit-2026-10-01]], [[tire-kick-2026-09-30]] (stranded, also lands here), the findings ledger, `routine-run-findings-2026-09-24`, and sotu W39–W41.
- Live state:
  - `list_scheduled_tasks` shows 8 recurring local tasks, all enabled. `list_task_runs` was read for each.
  - `RemoteTrigger list_runs` was read for the 5 enabled cloud routines (IDs from the `reference-cloud-routine-ids` memory).
  - `daily-git-sync.log`, `stale-worktrees.log` and `ops-catchup.log` tails.
- scope.md against `gh repo list nitsuah` and `gh repo list Nitsuah-Labs`: **drift** (see Decisions).

## Headline: routine output that never reached GitHub

Routines that run on the local machine kept writing into the shared stash checkout and leaving the result there. RSI and every cloud routine read stash from GitHub, so they never saw it, and stash stayed `SKIPPED_DIRTY` in daily-git-sync on every logged run since 9/18. This cycle found four outputs stranded that way:

| Output | Why it stranded | Evidence |
|---|---|---|
| `usage-report-2026-09.md` (this cycle's RSI input 1) | USAGE.md step 3: "leave it uncommitted" | daily-git-sync 10-02 and 10-07 list it as dirty |
| `tire-kick-2026-09-30.md` + the ledger | The wrapper said a dirty stash means hand off to a human, so they sat in a scratchpad for 7 days | tire catch-up session's final message. Meanwhile `ops-catchup.log` 10-07 logged tire-kick as "ok" |
| `sotu-2026-W41.md` | SOTU step 8 skips the commit when stash is dirty | untracked in the main checkout |
| Vault-index output for 24 reports | It rode on daily-note stash#184, which was closed unmerged on 10-04. Later runs commit only files the generator *reports* changing, so these were never listed again | obn-import-2026-10-07: graph check went from 1 to 24 FAILs |

The original reason for "skip or hand off when dirty" was that stash's gitleaks hook failed from a worktree. stash#171 fixed that on 9/30, so every one of these can now ship from a worktree cut from `origin/main`.

## Changes made

### PRs (stash), none merged by RSI
| PR | Theme | Ledger |
|---|---|---|
| [stash#195](https://github.com/nitsuah/stash/pull/195) | Regenerated vault indexes (generator output only; `check-generated-diff` ok; unreachable notes 29 → 1, ghost links 4 → 0) | F-20260930-02 |
| [stash#196](https://github.com/nitsuah/stash/pull/196) | USAGE ships its own PR, SOTU commits from a worktree, DAILY picks up stranded generator output, CATCHUP checks that output landed | F-20261007-01 |
| [stash#197](https://github.com/nitsuah/stash/pull/197) | DAILY and METRICS read scope.md live, with no cached repo lists; RSI.md map refreshed (USAGE PR, `week-fin-sum` row) | scope drift |
| this PR | Lands the stranded usage report, the TIRE 9/30 report and the merged ledger, plus this report | — |

The ledger in this PR is TIRE's 9/30 version, which has 13 new rows and a `## Closed` section. On top of it:
- PMO #174's three `done` flips (F-20260916-04/-05/-06) are re-applied.
- nitsuah-io#540, which merged after TIRE ran, is marked done.
- The new RSI rows are F-20261007-01…05.

I verified that no row present on `main` was dropped.

### Local scheduled-task wrappers (logged first)
- `monthly-tire-kick`: when stash is dirty, land the ledger and report from a worktree instead of handing them to a human.
- `monthly-usage-report`: "never commits or opens PRs" became "opens exactly one report PR" (matches #196).
- `monthly-pmo-audit`: dropped the stale "As of 2026-09-16" repo list, which still said `auto-apply-plugin` and `overseer` (matches #197).

### Cloud routines
None changed. All 5 enabled routines ran on cadence and their report PRs merged:
- daily-brief: every weekday from 9/28 to 10/7.
- obn-import: 9/30 and 10/7.
- eng-mini: 9/30, 10/1 and 10/7.
- eng-loc: 10/1.
- week-vuln: 10/1.

## Ledger aging
No open item is older than 21 days or has Seen ≥ 3. The three items TIRE expected to cross 21 days on 10-07 (F-20260916-04/-05/-06) were closed by PMO on 10-01. The oldest open item is F-20260926-01 (`RemoteTrigger list` pagination, 11 days). I re-verified it today: `list` still returns 20 one-shot reminders. The loop is closing; the gap was output not landing, and that's fixed above.

## Considered but not done
- **Usage-report candidate 1, re-check reminders spawning new triggers:** already resolved. The newest reminder in `RemoteTrigger list` is 2026-09-30 23:04, and none since the desktop Auto-fix watcher took over.
- **Usage-report candidate 2, a usage preflight for daily-repo-sync:** declined. All 10 of its September failures were spend-limit errors at session start, about 6 s in, before any prompt runs, so a preflight inside the prompt can't intercept them. They cost nothing and the next morning's run covers the sync.
- **daily-brief frontmatter (the other half of F-20260930-02):** no cloud prompt change. `build-vault-indexes.py` adds the `kind`/`date` frontmatter and nav itself, so #196's stranded-output pickup covers it.
- **Recovering the 10-02 daily note (F-20261007-04):** you closed stash#184 by hand, so I left it closed.
- **SOTU routine candidates:** none appeared in 3 or more weekly reports. The vigil-key item appeared only in W39.
- **Map "Known gap"** (account-level skills that don't match their routines): no new evidence.

## Decisions for the user
1. **Merge stash#187** (agent-board → motor-pool in scope.md), or say the rename should wait. With #197, every routine reads scope.md live, so that one merge updates them all.
2. **`nitsuah/.github`**: track it in scope.md, or list it as Excluded (F-20261007-03)?
3. **Stash main checkout:**
   - After #195 merges, most of the dirty report files match `main`.
   - The `.obsidian/*` edits and the untracked `sotu-2026-W41.md` remain. `week-sotu` was still running at the time of writing, and with #196 merged future weeks will ship themselves.
   - Decide whether to discard or commit the leftovers so daily-repo-sync stops skipping stash (F-20261007-05).
4. **Still open from TIRE 9/30:**
   - 5 merged remote branches whose deletes the classifier blocked (F-20260930-07/-08).
   - 8 branches that need a keep/delete call.
   - vigil parked on a merged branch.
   - avatar's untracked `.claude/`.
   - Dependabot PRs in farm-3j, games and deployer.
   - The daily-brief vigil egress allowlist plus `VIGIL_MCP_KEY`.

## Next
Merge #195 → #196 → #197 → this PR. #195 is generated-only. #196 and #197 touch different lines of DAILY.md, so they should merge cleanly in either order. The next TIRE run (10-28) is the first test of the worktree landing path.
