---
kind: usage-report
---

# Usage report — 2026-09

Generated 2026-10-01 ~18:10 UTC by the first scheduled run of `monthly-usage-report` (spec: [[USAGE]]). Window: **full calendar month, 2026-09-01 → 2026-09-30**. This replaces the partial 9/24 preview of this file, which covered 8/24 → 9/24; that version is in git at `a885bb8`. The two are not directly comparable. Read-only: nothing was committed, no PR was opened, and no task config was changed.

## Claude usage trend

**Plan:** Pro. The preflight `get_usage` snapshot at the start of this run:

| Window | % used | Resets |
|---|---|---|
| 5-hour | 45% | 2026-10-01 20:00 UTC |
| Weekly (all models) | 72% | 2026-10-07 05:00 UTC (Wed) |
| Extra usage | 0% of $100 (disabled). The monthly counter reset on Oct 1. | monthly |

- **Quota samples this month.** `get_usage` has no history, so these come from three point readings plus run errors:
  - 9/24 07:05 UTC: weekly 50%, 5-hour 70%. This was the usage report preview.
  - 9/26 18:40 UTC: weekly 46%, 5-hour 38%, extra usage maxed at $101.06/$100. Source: routine-audit.
  - 9/30 ~11:50 UTC: weekly 10%, 5-hour 1%, just after the reset. Source: `ops-catchup.log`.
  - 10/01: weekly is already at **72% one day into the window**, the same fast burn seen after the 9/23 reset.
- **Limits hit in September** (from scheduled-task error strings):
  - Weekly limit: 9/05–9/07 and 9/12–9/13.
  - 5-hour limit: 9/16.
  - **Monthly spend limit: 9/19, 9/20, 9/24 and 9/28.** The spend cap is now the most frequent blocker. It stopped both `daily-repo-sync` and `monthly-tire-kick` on 9/28.
- **Sessions:** 93 local CCD sessions had their last activity in September, out of 174 on record (oldest 2026-06-08, so the list is complete). The count uses last activity because `list_sessions` gives no start time. This is up from 56 in the preview's window.
  - PR state of the 93: 55 merged, 6 closed, 3 open, 29 with no PR.
  - 71 of the 93 ran from `C:\Users\ajhar\code` itself.
  - Busiest days: 9/30 (13), 9/24 (10), 9/23, 9/25 and 9/26 (8 each). Activity bunched up after each weekly reset (Wed 05:00 UTC).

**Top work areas by session count**, from session titles. The working directory says little, since most sessions run from the root.

1. `daily-repo-sync` / "Daily repo sync": **26**. This counts scheduled runs plus manual re-runs.
2. Other routine and meta-routine work: **18**.
   - Scheduled runs: monthly-pmo-audit ×2, monthly-tire-kick ×2 plus one catch-up, monthly-routine-rsi, week-fin-sum ×4, week-sotu, ops-catchup.
   - Routine planning: ROUTINES, routine execution order, the routine audit, SOTU usage planning, State of the Union.
3. fire: **8**. Fire MCP, the eBay signature and deletion endpoint, the realtime dashboard, the Plaid/Netlify split, PR docs, the Brag video, categorizeItem.
4. Security and dependency hygiene: **7**. eslint/js-yaml bumps, dep consolidation, vuln cleanup, the bb-mcp `ip-address` audit, the gitleaks hook in worktrees, stripping credentials from enrich-mirror.
5. Coverage, METRICS and docs: **7**. vhs/farm coverage, the deploy badge, coverage improvement ×2, docs updates, `docs/` folder support.

Close behind: vigil/overseer (5: MCP connection, rollup, PMO UI) and 9router (3).

## Scheduled-task health

Local `mcp__scheduled-tasks`, runs **started 9/01–9/30**. The October 1 runs are excluded and go in next month's report.

- **Landed** = succeeded and its output exists.
- **Suspected no-op** = a daily-repo-sync run under 60 s, or with no dated `daily-git-sync.log` entry.
- **Hijacked** = `last_activity_at` more than 2 h after `started_at`.

| Task | Runs | Succeeded | Failed | Fail rate | Landed | Suspected no-op | Hijacked | Most common failure |
|---|---|---|---|---|---|---|---|---|
| daily-repo-sync | 27 | 17 | 10 | **37%** | 15 | 2 (9/03: 10 s; 9/29: no log entry, and the 9/30 log confirms none) | 3 (9/26: 8.5 h; 9/29: **43 h**; 9/30: 8.6 h) | Weekly limit (5/10), monthly spend (4/10), 5-hour (1/10). All failed at init in under 10 s. |
| monthly-pmo-audit | 2 (9/16, 9/24) | 2 | 0 | 0% | 2 | n/a | 1 (9/16: 10.4 h) | none |
| monthly-usage-report | 1 (9/24 preview) | 1 | 0 | 0% | 1 | n/a | 0 | none |
| monthly-self-improvement | 1 (9/25) | 1 | 0 | 0% | 1 | n/a | 0 | none |
| monthly-tire-kick | 2 (9/24, 9/28) | 1 | 1 | 50% | 1 (+1 via catch-up) | n/a | 1 (9/24: 4.2 h) | Monthly spend (9/28) |
| catchup-monthly-tire-kick-2026-09-30 | 1 | 1 | 0 | 0% | 1 | n/a | 0 | none (24 min) |
| week-fin-sum | 3 (9/24, 9/26, 9/28) | 3 | 0 | 0% | 3 | n/a | 2 (9/24: 3 h; 9/28: **49 h**) | none |
| week-sotu | 1 (9/28) | 1 | 0 | 0%* | ? | n/a | 1 (9/28: **50 h**) | *see note |
| ops-catchup | 1 (9/30) | 1 | 0 | 0% | 1 | n/a | 0 | none |

Compared with the preview: `daily-repo-sync` went from 8/19 failed (42%) to 10/27 (37%) for the full month. Every September failure was a quota or spend rejection, and none came from a bug. 9 of 17 runs hit some cap.

Notes on the table:

- **Hijacked runs distort status.** 8 of 39 September runs (21%) were reused as working sessions. `ops-catchup.log` on 9/30 records `week-sotu` 9/28 as "failed (monthly spend limit)", yet `list_task_runs` shows it as succeeded. Its session was resumed until 9/30 14:09, so the final status reflects the later work, not the scheduled run. Treat hijacked runs' status as unreliable.
- **DEFERRED runs:** none can be identified. `list_task_runs` returned no `summary` field for any run, and the preflight was only added on 9/26. See the spec fix below.
- **Window at run time:** not recoverable per run. The only evidence is the error strings above.
- **`daily-repo-sync` has no usage preflight.** It's the most-failed task, and the 9/26 RSI pass only added preflights to the monthly-* tasks (week-sotu has one; week-fin-sum doesn't).

**Cloud routines** (`RemoteTrigger list`). The first page holds 20 triggers, and `next_cursor` is present but `list` ignores it, so the recurring fleet can't be enumerated. The first page shows:

- **17 one-shot `reminder` check-ins** and 3 one-shot triage or review tasks (9/27). There are no recurring routines on page 1.
- **Duplicate check-ins got worse.**
  - **"Re-check PR #233" (kryptos): 7 triggers on 9/30 alone**, fired roughly hourly from 14:57 to 00:06 UTC.
  - "Re-check kryptos PR #228": 6 triggers (9/27–9/30).
  - "Re-check PR 535 CI" and "Re-check fire#134": 2 each.
  - That's 17 cloud runs spent on 4 PRs in 4 days. The prompt says "re-arm this check-in unless the PR is merged or closed", and each re-arm creates a new trigger.
- From the 9/26 routine-audit:
  - The recurring cloud fleet went from 15 to 5 daily runs/week (`daily-brief` replaced checkin/email/pr-review).
  - week-metrics, sun-stale-worktrees and week-vigil-check were disabled.
  - Connectors were cleared on the remaining clone-based routines.
  - Five routines from the 9/16 list (`outreach-writer`, `lead-finder`, `job-evaluator`, `application-tracker`, cloud `daily-git-sync`/`obn-repo`) are still unaccounted for (F-20260924-13).

**Output lost.** 12 `nitsuah/stash` PRs were closed without merging in September:

- 6 `obn: daily note` (#78, #82, #83, #86, #90, #98)
- 2 `metrics:` reports (#91, #99)
- 2 `eng-mini:` reports (#85, #87)
- `daily: run sync-repos.ps1 -Prune` (#132)
- the routine-audit report (#149; its content landed via a later PR, and the file is on disk)

Only #149 falls after the 9/24 close-the-loop auto-merge fix. Duplicate daily-note PRs (#82/#83 for the same 9/04 date) haven't recurred since the once-per-day guard.

Folded in from `routine-run-findings-2026-09-24.md` and `routine-audit-2026-09-26.md`:

- On 9/25 every cloud run was rejected at init (`seven_day` plus monthly spend) and re-run by a hand-typed "Try again".
- The cached stash clone in the cloud sandbox diverged after the 9/24 history rewrite, so routines improvise `git reset --hard`.
- Report-PR ceremony takes about 15 of 37 turns per cloud run.
- The local stash checkout keeps blocking `daily-repo-sync`:
  - 9/30: local `main` had diverged (`SKIPPED_DIVERGED`).
  - 10/01: a rebase was left in progress with conflicts in `docs/ROADMAP.md` and `docs/TASKS.md`.
  - The daily note is now built from a scratch worktree off `origin/main` to work around it.

## Shipped work

Commits per repo use `git log --all --since=2026-09-01 --until=2026-10-01`, so they count every local ref, feature branches included. Merged PRs use `gh pr list --state merged --search "merged:2026-09-01..2026-09-30"` against each repo's `origin`.

| Repo (local dir → origin) | Commits (all refs) | Merged PRs |
|---|---|---|
| fire | 342 | 56 |
| stash | 171 | **84** |
| vigil (was `overseer`) | 146 | 57 |
| ats-fill → `nitsuah/auto-apply-plugin` | 109 | **0** |
| kryptos | 103 | 38 |
| farm-3j | 95 | 59 |
| skyview | 87 | 45 |
| nitsuah-io (Nitsuah-Labs) | 61 | 26 |
| vhs | 56 | 13 |
| games | 52 | 30 |
| darkmoon | 51 | 32 |
| avatar | 47 | 15 |
| agent-board | 42 | 24 |
| bb-mcp | 37 | 14 |
| gcp | 34 | 15 |
| deployer (Nitsuah-Labs) | 33 | 17 |
| osrs | 29 | 12 |
| windirstat-mcp | 18 | 5 |
| **Total** | **1,513** | **542** |

Notes:

- `9router` is excluded. It's a fork (`isFork: true`), and its 267 September commits are almost all upstream authors, with 0 merged PRs.
- `auto-apply-plugin` was renamed locally to `ats-fill`. It had 109 commits (69 yours) and still **0 merged PRs**, making two months in a row. One PR is open, and the checkout is now on `main`.
- `stash`'s 84 merged PRs are mostly routine output: daily notes, reports, prompt changes. fire leads on product commits.

## Personal usage signal

**Unavailable.** ActivityWatch (`localhost:5600`) didn't respond within 3 s (curl exit 7, connection refused), so it isn't installed or isn't running. Per the spec, the Security 4800/4801 and System 7001/7002 proxies weren't retried: both are known not to produce hours on this machine. **Installing ActivityWatch** (free, local-only, https://activitywatch.net) would give a real per-app breakdown next month.

**Calendar** (Google Calendar): 5 events in September, none recurring, so there's nothing to template.

- 3 all-day travel blocks: 9/01–9/04, 9/08–9/11, 9/15–9/18.
- The hand-made **"Claude resets"** reminder on 9/09.
- One personal to-do on 9/28 (finance errands).

The quota-failure clusters (9/05–9/07, 9/12–9/13, 9/19–9/20) again fall on or right after travel days, when nobody was around to catch up. `ops-catchup` (created 9/26, first run 9/30) now covers that gap.

## Automation candidates (ranked)

1. **Check-in reminders create a new trigger on every re-arm.** This month 17 cloud runs went to 4 PRs, including kryptos #233 checked **7 times in ~10 h on 9/30**. Last month's candidate #2 wasn't fixed, and the problem grew. **Fix:** the drive-to-green check-in should `RemoteTrigger update` its own trigger's `run_once_at` instead of creating a new one. Cap it at about 3 re-arms per PR, then post a single "needs human" note. RSI should own this, since each fire also costs weekly quota.
2. **`daily-repo-sync` has no usage preflight and fails the most.** It failed 10 of 27 runs, all at init on caps, and the monthly spend cap alone blocked it 4 times. **Fix:** prepend the same USAGE PREFLIGHT block used by the monthly-* tasks, plus week-fin-sum. A clean `DEFERRED:` is cheap, it can't trip extra-usage spend, and ops-catchup already re-runs chain-critical routines after the reset.
3. **Routine sessions get reused as work sessions.** 8 of 39 runs (21%) were hijacked, including week-sotu at 50 h, week-fin-sum at 49 h and daily-repo-sync at 43 h. That corrupts run status (week-sotu shows succeeded while ops-catchup logged it failed) and carries a large context into the work. **Fix (you plus a small prompt tweak):** end each routine's SKILL.md with a one-line "start follow-up work in a new session" closer. ops-catchup should judge success by the run's first-hour outcome, not the final status.
4. **The weekly window burns out early.** It was 72% used about 1 day after the 9/30 reset, and 50% within a day of the 9/23 reset. Post-reset catch-up plus manual work front-loads the week, and the spend cap gets hit by the end. **Fix:** have ops-catchup re-run at most 1–2 chain-critical routines on reset day, and push the rest to day 2–3. Re-check the monthly extra-usage cap ($100, maxed in September) against the fleet's real cost.
5. **The local stash checkout is chronically dirty, diverged or mid-rebase.** That's 9/30 diverged and 10/01 with a rebase left in conflict, and it forces scratch worktrees every day. This is a human action, not automation: finish or abort the `ROADMAP.md`/`TASKS.md` rebase, and keep human edits off the checkout that routines commit to (see the one-worktree-per-task rule).
6. **`ats-fill` / `auto-apply-plugin` has been parked for 2 months** (109 commits, 0 merged PRs). It needs a decision: merge the open PR or archive the repo. It's listed so it doesn't slip a third month.
7. **Install ActivityWatch.** This is the third run without a personal usage signal.

## Spec fixes made this run (per USAGE.md "Continuous improvement")

The spec was edited directly and left uncommitted:

- **DEFERRED counting:** `list_task_runs` returned no `summary` on any run, so a `DEFERRED:` first line can't be seen from it. The spec now says to check a run's first assistant message with `mcp__ccd_session_mgmt__list_events` only when the run is short (under 2 min) and succeeded.
- **Hijacked runs:** the final status of a hijacked run reflects the later work, not the scheduled run, so the spec says not to trust its success/fail status.
- **Repo list:** local directory names now differ from origins (`vigil` was `overseer`, `ats-fill` is `auto-apply-plugin`), and `9router` is a fork whose `--all` commits are upstream noise. The spec now says to resolve each repo by `origin` and exclude forks.
