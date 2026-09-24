# Usage report — 2026-09

Generated 2026-09-24 by the `monthly-usage-report` scheduled task (spec: [[USAGE]]). This was a manually triggered run, 7 days before the first scheduled fire on 2026-10-01. Window: **2026-08-24 → 2026-09-24** (the last ~30 days). Read-only: nothing was committed, no PR was opened, and no task config was changed.

## Claude usage trend

**Plan:** Pro. Snapshot from `get_usage` at 2026-09-24 ~07:05 UTC:

| Window | % used | Resets |
|---|---|---|
| 5-hour | 70% | 2026-09-24 11:10 UTC |
| Weekly (all models) | 50% | 2026-09-30 05:00 UTC, 5d 21h away |
| Extra usage | **100%**: $101.06 spent against a $100.00 monthly limit (extra usage is disabled) | n/a |

- Only one sample exists this month. `get_usage` returns the current value, not a history, so the trend is only the failure pattern below. Half the weekly budget was gone about 1 day after the 9/23 reset. That fits the catch-up burst described in `routine-run-findings-2026-09-24.md`.
- Hit the cap in 3 distinct ways this month, per the `daily-repo-sync` run errors: **weekly limit** (9/5–9/7 and 9/12–9/13), **5-hour session limit** (9/16), and **monthly spend limit** (9/19–9/20). The monthly extra-usage cap is new since the 9/16 audit.
- **Sessions:** 56 local CCD sessions had their last activity in the window (52 in September). `list_sessions` returned 123 sessions in total, oldest 2026-06-08, so the list is complete. It only reports *last activity*, not a start date, so "started this month" is approximated by last activity.
- PR state of those 56: 25 merged, 5 open, 5 closed, 21 with no PR.
- Days with the most activity: 9/23 (8), 9/16 (6), 9/24 (6), 9/02 (5).

**Top work areas by session count.** Almost every session (41/56) runs from `C:\Users\ajhar\code` itself, so the working directory says little. These counts come from the session titles:

1. `daily-repo-sync` / "Daily repo sync": **19** (scheduled plus manual re-runs)
2. Code coverage and METRICS work (farm, vhs, coverage improvement, deploy badge): 4
3. 9router (security reconciliation, Watchtower/upgrade, 9router-v2): 3
4. MCP maintenance (windirstat-mcp fixes, MCP instance reuse, MCP fixes, Fire MCP usage): 4
5. Routine or PMO meta-work (ROUTINES, Routines execution order, monthly-pmo-audit ×2, State of the union): 5

Skill usage per session isn't exposed by `list_sessions` (see the spec fix at the end).

## Scheduled-task health

Local `mcp__scheduled-tasks`, all runs on record:

| Task | Runs | Succeeded | Failed | Fail rate | Most common failure |
|---|---|---|---|---|---|
| daily-repo-sync | 19 (9/03–9/24) | 11 | 8 | **42%** | Weekly limit (5/8). The others were monthly spend limit (2/8) and 5-hour limit (1/8). All failed at init in under 10 s, before doing any work. |
| monthly-pmo-audit | 2 (9/16 manual, 9/24) | 2 | 0 | 0% | none |
| monthly-usage-report | 1 (this run) | n/a | n/a | n/a | first run |
| monthly-self-improvement | 0 | n/a | n/a | n/a | first fire 2026-10-02 |

Compared with the 9/16 audit: `daily-repo-sync` was 5/11 failed (45%) then and is 8/19 (42%) now. Quota is still the only failure cause, and no run has failed because of a bug.

**Caveat:** the 9/03 "succeeded" run lasted 10 s (11:04:55 → 11:05:05). That is too short to have synced 17 repos, so it may have been a silent no-op counted as a success.

**Cloud routines** (`RemoteTrigger list`): the API returned the first 20 triggers plus a `next_cursor`, but `list` ignores the cursor, so the recurring cloud fleet (~20 routines, per the 9/16 audit) couldn't be enumerated. Unavailable: the list endpoint doesn't paginate. What the first page did show:

- All 20 are **one-shot `reminder` triggers** that the "drive-to-green" PR check-ins create, then disable after firing.
- Duplicates: **5 separate "Re-check PR #78 status"** triggers, **4 "Re-check PR #83 (daily note)"**, and 2 each of "Re-check 6 metrics PRs".

From `routine-run-findings-2026-09-24.md`, folded in:

- Every cloud and local failure from 9/18 to 9/22 was a `seven_day` rate-limit rejection at init.
- Firing 6 cloud routines in about 5 minutes (9/24 02:08–02:13 UTC) tripped the **five_hour** cap. It killed `week-eng-loc`, and probably the Sunday runs too.
- `week-eng-loc` and `week-vigil-check` escalate to `add_repo {access:"push"}` even though they're read-only. `week-eng-loc` then stalled on 7 denied Bash actions.
- `daily-repo-sync` writes into `stash` without committing, then skips `stash` as `SKIPPED_DIRTY`. That was 72 → 88 uncommitted paths as of 9/24.

## Shipped work

Commits per repo use `git log --all --since=2026-08-24`, so they include every local ref (feature branches too), not just the default branch. Merged PRs use `gh pr list --state merged --search "merged:>=2026-08-24"` against the owner taken from each repo's `origin`.

| Repo | Commits (all refs) | Merged PRs |
|---|---|---|
| kryptos | 128 | 35 |
| fire | 99 | 31 |
| skyview | 85 | 33 |
| overseer (→ `nitsuah/vigil`) | 82 | 37 |
| nitsuah-io (Nitsuah-Labs) | 79 | 34 |
| games | 71 | 25 |
| farm-3j | 70 | 45 |
| auto-apply-plugin | 66 | **0** |
| darkmoon | 65 | 34 |
| stash | 62 | 22 |
| vhs | 53 | 13 |
| agent-board | 47 | 19 |
| bb-mcp | 47 | 17 |
| deployer (Nitsuah-Labs) | 24 | 13 |
| gcp | 22 | 8 |
| avatar | 17 | 7 |
| osrs | 17 | 5 |
| **Total** | **1,034** | **378** |

Two notes on the table:

- `auto-apply-plugin` has 66 commits and 0 merged PRs. That matches the findings report: it's parked on the merged `chore/chrome-web-store-cicd` branch with uncommitted work.
- `overseer`'s origin now resolves to `nitsuah/vigil`, but `scope.md` still lists `nitsuah/overseer`.

## Personal usage signal

Unavailable for real active-hours numbers:

- **ActivityWatch** (`localhost:5600`): no response within 3 s. It isn't installed or isn't running.
- **System log 7001/7002:** 23 events over 31 days, spread across 13 days. These are **Winlogon logon/logoff** notifications, not lock/unlock, so they can't be turned into active hours, and no hours figure is given here.
- **Security log 4800/4801 (lock/unlock):** no events. The "Audit Other Logon/Logoff Events" policy is off, so Windows never records them.

To get a real per-app breakdown next month, install ActivityWatch (free, local-only, https://activitywatch.net). Turning on the audit policy would also work, but that's a security-settings change, so it's left to you.

**Calendar** (Google Calendar, connected): 4 events in the window, and no recurring meetings to template.

- 3 are all-day travel blocks: 9/01–9/04, 9/08–9/11, 9/15–9/18.
- 1 is a manually created **"Claude resets"** event on 9/09 00:30 ET. You're tracking the quota reset by hand; see candidate #3.

The travel blocks line up with the failure clusters. 9/05–9/07 and 9/19–9/20 both came right after travel days, when nobody was around to re-run the failed tasks.

## Automation candidates (ranked)

1. **Quota exhaustion is still the #1 failure cause.** `daily-repo-sync` failed 8/19 times, all on quota (weekly, 5-hour, and now monthly spend). The cloud fleet fails the same way. **Fix:** cut the cloud fleet's cadence, or gate each routine on a `get_usage` check at startup that exits cleanly when the weekly limit is over ~85%, so the daily sync keeps its budget. RSI should own this.
2. **Duplicate PR check-in reminders.** Nine one-shot triggers were spent re-checking just two PRs (#78 ×5, #83 ×4). **Fix:** make the drive-to-green check-in *update* one existing reminder for each PR instead of creating a new one every time. Each fire costs quota, which makes #1 worse.
3. **Manually tracking the quota reset.** There's a hand-made "Claude resets" calendar event, and 19 daily-sync sessions include manual catch-up re-runs (9/16 ×3, 9/23). **Fix:** have a small scheduled task run the day's failed routines once, serialized, just after the weekly reset. The 9/24 findings show that an unserialized catch-up trips the 5-hour cap.
4. **`daily-repo-sync` leaves uncommitted writes in `stash` (DAILY finding #4).** The uncommitted paths grow every day and stop `stash` from ever syncing. **Fix:** the approved DAILY.md change to commit obn-repo/obn-review writes on the daily-note branch.
5. **Read-only cloud routines escalate to push access** (`week-eng-loc`, `week-vigil-check`, and the same pattern in `sun-stale-worktrees` / `sun-vuln-patcher`). **Fix:** attach the repos as `sources`, or rewrite the prompts to use only `git clone --depth 1` plus Read/Grep.
6. **`scope.md` drift.** `overseer` is now `nitsuah/vigil`. **Fix:** update `scope.md` and DAILY's cached repo list together.
7. **`auto-apply-plugin` has been parked all month** (66 commits, 0 merged PRs). This needs a human decision, not automation. It's listed so it doesn't slip another month.

## Spec fixes made this run (per USAGE.md "Continuous improvement")

The spec was edited directly (uncommitted), so the same "unavailable" lines won't come back next month:

- **Source 3:** Event IDs 7001/7002 are logon/logoff, not lock/unlock, and 4800/4801 need an audit policy that is off on this machine. The spec now says so and no longer treats 7001/7002 as an hours proxy.
- **Source 1:** `list_sessions` gives only last-activity time and no skill data. `RemoteTrigger list` doesn't paginate, so cloud routines have to be fetched some other way. Both are now noted in the spec.
