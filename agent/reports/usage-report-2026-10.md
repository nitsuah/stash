---
kind: usage-report
---

# Usage report — 2026-10

Generated 2026-10-28 ~18:00 UTC by the catch-up run `catchup-monthly-usage-report-2026-10-28` (spec: [[USAGE]]). Window: **2026-10-01 → 2026-10-28**, so a partial month, written three days early. The 10/01 scheduled run produced the September report, which landed on main via stash#198 on 10/07. No October report existed on `origin/main` before this one. Read-only apart from this PR; no task config was changed.

## Claude usage trend

**Plan:** Pro. Preflight `get_usage` at the start of this run:

| Window | % used | Resets |
|---|---|---|
| 5-hour | 22% | 2026-10-28 20:40 UTC |
| Weekly (all models) | 5% | 2026-11-04 05:00 UTC (just reset Wed 10/28 05:00 UTC) |
| Extra usage | 0% of $100 (disabled) | monthly |

- **Quota history:** `get_usage` is a snapshot, so the trend comes from failed-run error strings.
  - **Weekly limit exhausted three times in October:** 10/11 → reset 10/14, 10/17 → reset 10/21, and 10/22 → reset 10/28 (the last was a 6-day lockout; failures on 10/24, 10/25 and 10/28 03:20 UTC).
  - 5-hour/session limit: once (10/14, `daily-repo-sync`).
  - **Monthly spend limit: no hits in October.** September had four days of them.
  - So the blocker moved from the spend cap to the weekly cap, which now runs out well before its reset.
- **Sessions:** 132 local sessions had last activity in October (of 200 returned; the oldest is 9/16, so October is fully covered).
  - 70 were scheduled-routine sessions, 62 manual or delegated.
  - PR state: 82 merged, 4 open, 3 closed, 43 with no PR.
  - 77 ran from `C:\Users\ajhar\code` itself, so cwd says little.
  - Busiest days (by last activity): 10/14 (17), 10/15 (16), 10/08 (14), 10/01 and 10/22 (13 each), 10/28 (12).

**Top work areas by session count** (titles; some overlap):

1. `daily-repo-sync`: about 21 scheduled runs plus manual re-runs, the largest single line item again.
2. Other routine sessions: week-sotu 7, ops-catchup 6, daily-imps-triage 7, week-fin-sum 5, ats-fill inbox/review 19.
3. vigil (6), fire (5), darkmoon, vhs and Netlify (4 each).
4. Auth/secret-template cleanup across repos: a batch of one-session-per-repo PRs (vigil, vhs, avatar, kryptos, fire, gcp, motor-pool, skyview).
5. imps/9router/motor-pool (about 8): the imps loop, a 9router PR audit, and the Rust rewrite assessment.

## Scheduled-task health

Local `mcp__scheduled-tasks`, runs **started 10/01–10/28**. `list_task_runs` returns only 10 by default; `limit` accepts up to 50, which this run used for the two tasks with more.

- **Landed** = succeeded and its output exists.
- **Hijacked** = `last_activity_at` more than 2 h after `started_at`, so the final status is unreliable.

| Task | Runs | Succeeded | Failed | Fail rate | Hijacked | Most common failure |
|---|---|---|---|---|---|---|
| daily-repo-sync | 21 | 16 | 5 | **24%** | 6 (10/07 26 h, 10/08 6 h, 10/09 6 h, 10/14 2.1 h, 10/15 10 h, 10/22 6 h) | Weekly limit (4/5), session limit (1/5) |
| daily-imps-triage | 7 | 3 | 4 | **57%** | 3 (10/22 11.8 h, 10/22 PM 33 h, 10/23 11 h) | Weekly limit (4/4) |
| ats-fill-daily-inbox-sync | 16 | 12 | 4 | 25% | 3 (10/15 30 h, 10/15 3.7 h, 10/21 9 h) | Weekly limit (4/4) |
| ats-fill-weekly-review | 3 | 2 | 1 | 33% | 2 (10/15 17 h, 10/21 52 h) | Weekly limit |
| week-sotu | 7 | 6 | 1 | 14% | 5 (10/01 7 d, 10/07 3 h, 10/08 32 h, 10/16 5 h, 10/21 16 h) | Process crash, exit code 3221225794 (10/14) |
| week-fin-sum | 5 | 5 | 0 | 0% | 1 (10/21 23.5 h) | none |
| ops-catchup | 6 | 6 | 0 | 0% | 1 (10/14: 7 d) | none |
| monthly-pmo-audit | 1 (10/01) | 1 | 0 | 0% | 1 (6.1 h) | none |
| monthly-usage-report | 1 (10/01) | 1 | 0 | 0% | 0 | none (4.4 min) |
| monthly-self-improvement | 1 (10/02) | 1 | 0 | 0% | 0 | none, but the run lasted 13 s: **suspected no-op**. The 2026-10 RSI report landed via stash#198 from another session. |
| monthly-tire-kick | 1 (10/28) | 1 | 0 | 0% | 0 | none; partial pass (3 vuln bumps, ledger and report, stash#333 merged) |

Notes:

- **Weekly-limit failures cluster on the weekend before each reset** and hit every daily task at once, in under 10 s each. 17 of 18 October failures were quota rejections.
- **Missed Mondays:** week-sotu and week-fin-sum have no run for Monday 10/26 (weekly lockout); `catchup-week-sotu-2026-10-28` is queued for tonight.
- **Hijacking is routine, not exceptional:** 22 of 69 October runs (32%, up from 21% in September) were resumed for other work. Statuses for those are unreliable.
- **Output verification not done for every run.** `daily-git-sync.log` headings did not parse reliably, so no-op counts for `daily-repo-sync` are not reported. The only sub-60 s run was 10/28 16:06 (46 s), which correctly detected that the day's run had already completed.
- **DEFERRED runs:** none identifiable; `list_task_runs` summaries are mostly absent.
- **Window at run time:** not recoverable per run.

**Cloud routines** (`RemoteTrigger list`): page 1 has 20 triggers, `has_more` is true, and cursor paging is ignored, so the recurring fleet cannot be enumerated. All 20 are disabled one-shot reminders: "Re-check PR #233" ×6, "Re-check kryptos PR #228" ×5, "Check PR #164" ×2, "Re-check PR 535 CI" ×2, plus singles. The duplicate re-arm pattern from September remains visible on page 1.

**Output lost:** one `nitsuah/stash` PR closed unmerged since 10/01: #226 `obn: daily note 2026-10-10`. September had 12, so the close-the-loop fix is working.

## Shipped work

Commits on each repo's default branch since 2026-10-01 (origin ref, no feature branches, so lower than September's all-refs counts), and merged PRs via `gh pr list --search "merged:>=2026-10-01"`. Repos resolved by origin URL; forks (`9router`, `windirstat-mcp`) and `latent-spaces/brag` excluded.

| Repo | Commits | Merged PRs |
|---|---|---|
| stash | 152 | 143 |
| fire | 106 | 101 |
| nitsuah/.github (imps-runner) | 88 | 63 |
| vigil | 57 | 60 |
| nitsuah-io (Nitsuah-Labs) | 60 | 51 |
| ats-fill | 59 | 57 |
| skyview | 46 | 46 |
| kryptos | 45 | 46 |
| farm-3j | 39 | 40 |
| vhs | 26 | 26 |
| motor-pool | 25 | 26 |
| darkmoon | 22 | 22 |
| bb-mcp | 19 | 20 |
| games | 16 | 16 |
| deployer (Nitsuah-Labs) | 14 | 14 |
| avatar | 7 | 7 |
| osrs | 7 | 7 |
| gcp | 4 | 4 |
| **Total** | **792** | **755** |

Notes:

- Merged PRs are 755 in 28 days, against 542 for all of September. Much of the rise is routine and imps output (stash 143, `.github` 63).
- ats-fill now merges PRs (57), where September had 0.
- `motor-pool` is the renamed `agent-board` repo.

## Personal usage signal

Unavailable. ActivityWatch (`localhost:5600`) did not respond, and the lock/unlock events (Security 4800/4801) are not logged on this machine. Installing ActivityWatch (https://activitywatch.net, free, local-only) would enable a per-app breakdown.

## Automation candidates

Ranked by evidence:

1. **Weekly-limit collisions.** Four daily tasks (`daily-repo-sync`, `daily-imps-triage`, both ats-fill syncs) all fire in the same 5-hour window and all fail together when the cap is gone. 17 failures this month. Fix: give each a usage preflight like `monthly-usage-report`'s, and skip or stagger them once weekly use passes about 85% rather than failing at init.
2. **Run hijacking (32% of runs).** Scheduled sessions are reused for follow-up work, which corrupts status and duration. Fix: have routines end with an instruction to start a fresh session for follow-up, or record completion in a log that does not depend on session status.
3. **Missed Monday runs are caught up by hand.** Weekly tasks (week-sotu, week-fin-sum) miss when the weekend lockout runs past Monday. `ops-catchup` handles it on Wednesday; fixing item 1 reduces the need.
4. **Catch-up duplicates the schedule.** The `catchup-monthly-usage-report-2026-10-28` task existed because no 2026-10 file was on main. The 10/01 run wrote the September report, so the monthly task will fire again 11/01 and produce a 2026-11 report. Fix: decide whether the report covers the previous or the current month and name the file accordingly (see the spec fix below).
5. **Cloud reminder churn.** 20 disabled one-shot reminders crowd page 1 of `RemoteTrigger list`, hiding any recurring fleet. A cleanup session already exists ("RemoteTrigger pagination and reminder cleanup"); deleting finished reminders would make the list usable.

## Spec fixes made in this run

`agent/prompts/USAGE.md`: noted that `list_task_runs` takes `limit` up to 50 (default 10 silently truncates counts), and that the report's month is the one being run in or just ended, with its filename stating the window.
