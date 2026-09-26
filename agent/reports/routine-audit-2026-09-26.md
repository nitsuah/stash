---
kind: routine-audit
date: 2026-09-26
---

# Routine audit — 2026-09-26 (chain, toil, token spend)

This is the input for [[RSI]] on Oct 2 and for [[USAGE]] on Oct 1. It covers only runs **after** the 9/24–9/25 fixes (see [[routine-run-findings-2026-09-24]] and [[rsi-report-2026-09]]); it doesn't re-report what those fixed. Every claim cites a run ID or file.

**Goal set by the user:** less toil and less need for them to be present, product and feature kickoff stays theirs, every token earns its keep, failures get corrected before the next run, and costly jobs aren't re-run by accident.

## 0. Quota posture (get_usage, 2026-09-26 ~18:40 UTC)
| Window | Used | Resets |
|---|---|---|
| 5-hour | 38% | 21:50 UTC |
| Weekly (all models) | 46% | **Wed 2026-09-30 05:00 UTC** |
| Extra usage | $101.06 / $100 (maxed, disabled) | monthly, Oct 1 |

**Correction:** the weekly window resets **Wednesday 05:00 UTC (Wed 1am ET)**, not Tuesday. That makes Sun/Mon days 5–6 of the window. The error came from addendum 2 of the 9/24 findings.

## 1. Current fleet and chain (verified)

Local means `mcp__scheduled-tasks` and needs this PC on. Cloud means RemoteTrigger. All times are UTC.

| Stage | Routine | Where | When | Reads | Writes |
|---|---|---|---|---|---|
| sync | daily-repo-sync ([[DAILY]]) | local | daily 11:07 | scope.md, every repo | notes, agent/repos, logs, obn PR (merges yesterday's) |
| brief | daily-checkin | cloud sonnet | wkdy 13:00 | calendar etc. | reports/cloud/daily-checkin (PR) |
| brief | daily-pr-review | cloud default | wkdy 14:00 | GitHub search | reports/cloud/daily-pr-review (PR) |
| brief | daily-email | cloud default | wkdy 15:00 | Gmail | reports/cloud/daily-email (PR) |
| weekly | week-obn-import | cloud | Mon 10:00 | stash | reports/cloud/obn-import (PR) |
| weekly | week-fin-sum | local | Mon 12:30 | fire MCP | report |
| weekly | week-vigil-check | cloud sonnet | Mon 15:00 | GitHub search | reports/cloud/week-vigil-check (PR) |
| weekly | week-eng-loc ([[LOC]]) | cloud | Mon 17:00 | clones | eng-loc reports (PR) |
| weekly | week-eng-mini ([[MINI]]) | cloud | Wed 18:00 | clones | eng-mini reports (PR) |
| weekly | week-metrics (METRICS.md) | cloud sonnet | Fri 13:00 | api.github.com (stale) | target-repo PRs + metrics report |
| weekly | sun-stale-worktrees | cloud | Sun 14:00 | remote branches | report (PR) |
| weekly | sun-vuln-patcher | cloud sonnet | Sun 15:00 | clones + WebSearch | advisory report (PR) |
| monthly | monthly-tire-kick ([[TIRE]]) | local | 28th 12:00 | all reports | ledger, ≤5 fix PRs |
| monthly | monthly-pmo-audit ([[PMO]]) | local | 1st 12:00 | repo docs | doc PRs, pmo-audit |
| monthly | monthly-usage-rpt ([[USAGE]]) | local | 1st 13:12 | sessions, git | usage-report |
| monthly | monthly-routine-rsi ([[RSI]]) | local | 2nd 12:10 | all of the above | prompt/memory fixes, PRs |
| — | State of the Union / Portfolio Checklist | **manual** | ad hoc | hand-verified TASKS/ROADMAP | 62.8 KB HTML artifact |

That's about 30 runs a week. 15 of them are the three daily cloud briefs, and each of those does its own clone, report, PR, CI wait and merge.

**Unaccounted for.** No trigger ID is recorded for `outreach-writer`, `lead-finder`, `job-evaluator`, `application-tracker`, or the cloud `daily-git-sync` / `obn-repo` from the 9/16 list. Nobody currently knows whether they're enabled, and `RemoteTrigger list` can't show them (F-20260924-13).

## 2. What went wrong since the 9/24–25 fixes

1. **Quota outage, then manual retries.** All 9/25 cloud runs were rejected at init with `seven_day` plus monthly spend: week-metrics `cse_018ggSSC…`, daily-pr-review `cse_01FJCpkd…`, and likewise checkin and email. At 16:05 each was re-run by a hand-typed "Try again". That's the toil the fleet is supposed to remove, and there's still no automated, serialized catch-up (USAGE candidate #3 is still open).
2. **Routine sessions turn into work sessions.** Today's `daily-repo-sync` run (`local_cddfa61b…`) has **568 messages over 7.5 h and is still "running"**. It became the working session for vigil docs, the MCP bearer walkthrough and Autofix CI events on vigil#246. The week-metrics cloud session got a later "Clone ats-fill" plus "stop" as well. Costs:
   - every turn re-sends the whole routine context;
   - run history reports a 7.5 h daily sync;
   - Autofix events get routed into a routine session.
3. **Stale stash clone in the cloud sandbox.** After the 9/24 history rewrite, the cached clone's `main` diverged from origin (50 behind / 64 ahead, `cse_01FJCpkd…`). Each routine's `git checkout main && git pull --ff-only` fails, and the model improvises `git reset --hard`. The recovery costs turns on every run, and improvised hard resets are a risk.
4. **Every cloud routine carries 5 connectors it doesn't use.** Figma, Google Calendar, Gmail, Google Drive and Claude_Code_Remote are attached to week-metrics, sun-vuln-patcher and week-vigil-check (checked with `get`). Their tool schemas load on every run. They also give a web-reading routine (vuln-patcher's WebSearch) Gmail and Drive access, which is prompt-injection exposure with no benefit.
5. **week-metrics was never rewritten.** It still calls `api.github.com/users/nitsuah/repos`, which returns 403, and pushes to target repos that aren't attached. It spawned a sub-agent just to run `list_repos`. 9/18 output was lost (stash#99 closed) and 9/25 failed. It also can't run most suites without Docker (F-20260904-02).
6. **daily-pr-review can find PRs but can't inspect them.** `pull_request_read` returns `Access denied … not configured for this session` for every non-stash repo, so its detail rows are guesses from search results. It also tried `sleep 45` and a polling loop to wait for its own report's CI.
7. **Report-PR ceremony is the biggest recurring cost.** About 15 of the 37 turns in a typical cloud run go to branch, commit, push, PR, poll CI, merge and delete. That's repeated 15+ times a week for single-file markdown reports.
8. **Overlap:**
   - `sun-stale-worktrees` (cloud) can't see local worktrees, which is the only place they exist, while DAILY already does local stale-worktree cleanup (`logs/stale-worktrees.log`).
   - `week-vigil-check` re-derives CI, PRs and health that vigil already computes (`get_portfolio_overview`, `get_repo_health`).
9. **Chain timing:**
   - The heavy weeklies (vigil-check, eng-loc, stale, vuln, obn-import) sit on Sun/Mon, days 5–6 of the weekly window.
   - PMO (1st 12:00) and USAGE (1st 13:12) can overlap if PMO takes more than 72 min.
   - On the 1st, three monthlies plus the daily land in the same 5-hour window.
10. **vuln-patcher only advises.** It reads manifests and WebSearches, then writes a report. It never patches, and dependabot breakages still get fixed by hand (darkmoon#450 and farm-3j#338 per rsi-changes.log). Open dependabot PRs today: 3, all in vigil (#238–#240).
11. **State of the Union is hand-built.** Last updated Sep 16, so it's stale. It's 62.8 KB, and roughly half of that is the same two inline SVG icons repeated for 59 items. Regenerating it means rewriting the whole page. vigil's `get_open_tasks` now returns exactly this data (vigil#241), but vigil MCP isn't connected: there's no `vigil` entry in `~/.claude.json` and no `VIGIL_MCP_KEY`. The endpoint is up (307 without a bearer token, as MCP.md documents).

## 3. Recommendations

### 3a. New routines
| New | Replaces | Where / when | What it does | Why |
|---|---|---|---|---|
| **ops-catchup** (failover) | manual "Try again" retries, the hand-made "Claude resets" calendar event | local, daily 10:30 UTC (before daily-repo-sync). Also **Wed 05:30 UTC**, right after the reset | 1. `get_usage`: exit if weekly >80% or 5h >50%. 2. For each known routine (the IDs memory), check the latest run. If it failed on `rate_limit` since the last successful fire, re-run it. 3. **One at a time**, oldest-first in chain order (daily → weekly → monthly), re-checking usage between runs. 4. Write one line per action to `logs/ops-catchup.log`, and send a push notification only if something is still failing after a retry. | Removes the biggest remaining manual chore. Serialization is enforced by code, not memory. |
| **week-sotu** (State of the Union) | week-vigil-check (cloud) + the manual Portfolio Checklist regen | local, **Mon 12:00 UTC** (start of your week; cheap, no clones) | Reads vigil MCP (`get_open_tasks`, `get_portfolio_overview`, `get_security_summary`), `findings-ledger.md` (open `human`/`pmo`), the latest `reports/cloud/*`, and each routine's last-run status. It writes rows into the Portfolio Checklist artifact's data store. The page itself stays fixed, so this is a data write, not a regenerated page. | One place to look each week. It also closes the loop from routines to the ledger to you. |
| **daily-brief** | daily-checkin + daily-email + daily-pr-review | cloud, weekdays 13:00, **one** run, sonnet | Same three sections, one report file, one PR, one push notification. Exits early on the PR section if the open-PR set and head SHAs match yesterday's. | Cuts 10 runs/week and two-thirds of the PR ceremony. |

### 3b. Existing routines to change
- **sun-vuln-patcher → week-vuln (Thu 15:00):**
  - Add the lockfile-changed gate (F-20260924-31).
  - Add a *patch lane*: for HIGH/CRITICAL findings with a clean fix, or a dependabot PR that fails CI on a peer-dep split (the darkmoon#450/farm-3j#338 pattern), open a `tire/`-style fix PR, capped at 3 per run. Cloud can't run Docker, so the patch lane fits **monthly-tire-kick** better (local, Docker). Vuln files ledger items as `quick`, and TIRE fixes them. That's the "does what I'd do" behavior without giving cloud push rights.
- **week-eng-loc → Thu 17:00, week-obn-import → Wed 10:00:** moves them from the end of the weekly window to the start.
- **week-metrics:** retire the cloud version. Run METRICS locally inside **monthly-tire-kick** (Docker available, same PR governance). PMO already audits metrics integrity.
- **sun-stale-worktrees:** retire. Local worktrees are covered by DAILY. Remote stale-branch pruning becomes a monthly TIRE line item.
- **Every cloud routine:**
  1. **Detach unused connectors.** Keep Gmail only on daily-brief, and Calendar only if checkin uses it. Drop Figma, Drive and Claude_Code_Remote everywhere.
  2. **Replace the stash sync line** with `git fetch origin main && git checkout -B main origin/main` (never `pull --ff-only` or an improvised `reset --hard`).
  3. **Wait for CI** with `gh pr checks --watch` (or one re-check), never sleep loops.
- **Local monthlies:**
  - **Usage preflight:** first step is `get_usage`. If weekly >75% or 5h >50%, write `DEFERRED: <reason>` and exit. ops-catchup picks it up after the reset.
  - **Stagger the 1st:** move USAGE to the 1st 18:00 UTC so it can't overlap PMO.

### 3c. "Are you sure?" guard on costly manual runs
- Add `ask` permission rules for `RemoteTrigger` (action run) and `mcp__scheduled-tasks__run_scheduled_task` in `~/.claude/settings.json`, so every manual fire needs a click.
- Add a PreToolUse hook on the same matchers that prints a cost tier and the last-run time. Tiers:
  - **heavy:** PMO, RSI, tire-kick, eng-loc, eng-mini
  - **medium:** vuln, sotu
  - **light:** everything else
- The hook should refuse a re-run of anything that already succeeded today unless you confirm.

### 3d. Session hygiene (you, not a routine)
- Treat routine runs as read-only reports: start a **new** session for follow-up work instead of continuing the routine's session.
- Also: DAILY's last step prints `DONE — start a new session for follow-ups`, and ops-catchup counts routine sessions >2 h as `hijacked` in its log so USAGE can report it.

### 3e. Portfolio Checklist / State of the Union rebuild
- **Page:** a fixed HTML shell (one SVG `<symbol>` and `<use>` references, so no 59× duplication), backed by the artifact data store:
  - `items`: repo, tier, priority, title, ref, owner, needs_you, source (vigil / ledger / report), first_seen
  - `routine_health`: routine, last_run, status, next_run
  - `meta`: quota snapshot, generated_at
- **Weekly update:** week-sotu only writes rows, so a refresh costs a few KB of JSON, not a 60 KB rewrite.
- **Sections, top to bottom:**
  1. **Needs you** (owner = you, `human` ledger items, blocked PRs)
  2. **Kickoff queue:** the top P0/P1 product items. Their copy buttons copy a ready-to-paste kickoff prompt (repo, item, TASKS ref, acceptance criteria from TASKS), not just the title.
  3. **Open work by repo** (current list)
  4. **Routine health strip** (green, amber, red per routine; quota bar)
  5. **Findings aging** (ledger items older than 21 days or seen 3+ times)
- **Blocker:** vigil MCP bearer setup (the `MCP_API_KEY` in Netlify plus `VIGIL_MCP_KEY` locally, per vigil `docs/MCP.md`). You're doing this in the daily-repo-sync session now. Once `claude mcp get vigil` reports Connected, week-sotu can run.

## 4. Target weekly shape (UTC; window starts Wed 05:00)
| Day | Runs |
|---|---|
| Wed | ops-catchup 05:30 · obn-import 10:00 · eng-mini 18:00 |
| Thu | vuln 15:00 · eng-loc 17:00 |
| Mon | week-sotu 12:00 · fin-sum 12:30 |
| Daily | ops-catchup 10:30 (no-op unless something failed) · daily-repo-sync 11:07 |
| Weekdays | daily-brief 13:00 |

That comes to about 20 real runs a week, down from about 30. The 10 runs cut are cloud report-PR cycles, which are the most turn-heavy kind.

## 5. Decisions for the user (not taken)
1. Consolidate checkin + email + pr-review into **daily-brief**?
2. Retire **week-metrics** (cloud; move into TIRE) and **sun-stale-worktrees**?
3. Replace **week-vigil-check** with local **week-sotu**, with the Portfolio Checklist artifact moving to data-backed rows?
4. Create **ops-catchup** with the thresholds above (80% weekly / 50% 5h)?
5. Add the "are you sure" `ask` rules and hook on manual routine runs?
6. At claude.ai/code/routines: say which of outreach-writer, lead-finder, job-evaluator, application-tracker and cloud daily-git-sync/obn-repo still exist, and delete the ~20 disabled "Re-check PR" reminders (F-13). That unblocks `RemoteTrigger list` for every future audit.
