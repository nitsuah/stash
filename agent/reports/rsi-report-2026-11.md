---
kind: rsi-report
---

# RSI report — 2026-11

> 🧭 ← [[reports/rsi-report-2026-10|2026-10]] <!-- nav -->
>
> Run 2026-11-24, off the quarterly cadence. Usage at start: weekly 34%, 5-hour 45%. Prior cycle: [[rsi-report-2026-10]].

## Inputs and what was missing

| Input | State |
|---|---|
| 1. usage-report-2026-11 | **Missing.** `monthly-usage-report` has been disabled since its 10-01 run, and install-tasks.ps1 gave it no Windows replacement. It wasn't in that script's list of tasks to disable. |
| 2. pmo-audit (Nov) | Missing, as expected. `routine-pmo` was registered after the Nov 4 reset, so its first run is 2026-12-01. |
| 3. Scheduled tasks | Desktop: only `pmo-loop` and this task are enabled. Windows: `routine-daily-run`, `-sotu`, `-tire`, `-pmo` and `-fin-checkin` all show Ready. |
| 4. Sync logs | `daily-run.log` and `routine-run.log` were read (see below). |
| 5. scope.md cross-check | Not re-run this cycle to save budget. Deferred to January. |
| 6. routine-run-findings | Nothing new since 2026-09-24. |
| 7. findings-ledger / TIRE | Latest is tire-kick-2026-10-28. The next `routine-tire` run is 11-28. |
| 8. SOTU | On main: W40–W43 and W46. **W44, W45 and W47 are missing**, and W48 failed to push (see finding 1). |
| 9. Journey metrics | Not run this cycle. |

## Findings and actions

1. **Routine PRs fail on the `no_push` pushurl.** Fixed in [stash#431](https://github.com/nitsuah/stash/pull/431).
   - What breaks: the PMO loop's push toggle (`~/.imps/pmo/bin/push.sh`, `mergemain.sh`) leaves `remote.origin.pushurl = no_push` in every clone. `daily-run.mjs` and `pipeline-run.mjs` push with `git push origin`, so the 2026-11-23 daily note and SOTU W48 both failed.
   - Evidence: `daily-run.log` and `pipeline-sotu.log` on 11-23 both show `'no_push' does not appear to be a git repository`.
   - Fix: push `HEAD:refs/heads/<branch>` to the fetch URL instead. Tests pass 23/23.
   - Follow-up: the W48 SOTU and the 11-23 daily note need a re-run once #431 merges.
2. **DAILY-MODEL keeps running out of budget.** Proposed only, not applied.
   - Evidence: `routine-run.log` shows `error_max_budget_usd` on 6 of 8 runs since 11-04 (11-04, 06, 07, 13, 21, 23). The other two were `skip-9router-down`.
   - The fix in stash#407 (11-05: $1 → $4, read at most 2 files per hub) didn't stop it. Runs still use about 220k tokens.
   - Options: cap the hubs per run in the handoff (for example 3, rotating), or lower the per-hub reads to 1. Picking one is a design choice, so I didn't make it unattended.
3. **Usage report is orphaned.** It needs your decision: re-enable `monthly-usage-report`, port it to `pipeline-run.mjs`, or retire it. If it's retired, RSI Input 1 and the TIRE/SOTU token columns need rewording.
4. **SOTU W44, W45 and W47 never ran.** `pipeline-sotu.log` has no entry for those Mondays.
   - W44 and W45 predate the Windows task. W47 (11-16) has no log line at all, which suggests the machine was off or asleep at 05:10.
   - Consider adding `/RI` or "run as soon as possible after a missed start" (`StartWhenAvailable`) to install-tasks.ps1. Not changed this run.
5. **Worktree sprawl.** About 90 sibling `~/code/*-imp_*`, `*-wt-*` and `*-qa` directories exist. On 11-23, `daily-run` reported "28 to remove, 25 flagged". Its push failure meant the cleanup summary never landed. Recheck after #431.
6. **Stale RSI references.** Fixed and logged in `rsi-changes.log`.
   - The RSI wrapper still pointed DEFERRED runs at the retired `ops-catchup`.
   - RSI.md's map still described the disabled desktop tasks as live. It now has a dated 2026-11 note at the top.

## Considered and declined

- **Re-enabling `daily-imps-triage` and the `ats-fill-*` tasks.** They're disabled, apparently on purpose: the PMO loop absorbed imps triage on 11-22. They're flagged only.
- **Editing the PMO loop's `no_push` convention.** It's a deliberate safety guard. The fix belongs in the routine scripts instead.

## PRs

- [stash#431](https://github.com/nitsuah/stash/pull/431): push fix.
- This report, the RSI.md map note and the log entry: PR `rsi/stash/cycle-report-2026-11`.

RSI merged neither PR.
