# Routine run findings — 2026-09-23/24 (manual catch-up session)

Written by a manual catch-up session that re-ran failed routines in pipeline order (daily → weekly → Sunday → monthly). The input for [[USAGE]] and [[RSI]] this cycle. Every item below cites the run or file it came from.

## 1. Failures were quota, not bugs (confirmed again)
- Every failed cloud/local run 9/18–9/22 was an instant `rate_limit: rejected (seven_day)` at session init (0–1s, no work done). Weekly cap reset 2026-09-23 05:00 UTC.
- **New:** firing 6 cloud routines within ~5 min (manual catch-up, 2026-09-24 02:08–02:13 UTC) hit the **five_hour** session cap at 02:17 UTC. It killed `week-eng-loc` mid-analysis and a follow-up check-in scheduled by `week-obn-notes`. Sunday runs (`sun-stale-worktrees`, `sun-vuln-patcher`) started at 02:13 and are presumed killed too (not verified).
- Takeaway for RSI: catch-up or backfill runs must be **serialized**, and cloud routines that spawn sub-agents (`week-vigil-check` did) multiply the burn.

## 2. Read-only cloud routines escalate to push access
- `week-eng-loc` (cse_018qmLZjHhYAFseeJ2AejqMu) and `week-vigil-check` (cse_01DVUr8cKuK3e8NqR5UcMBg7) both called `add_repo {access:"push"}` although their prompts say read-only. Cause: the cloud GitHub REST API returns 403 for any repo that isn't attached with credentials, so a "read" attach isn't enough for `api.github.com` calls.
- `week-eng-loc` then had 7 Bash actions denied by the auto-mode classifier (`[Permission Grant]`) and stalled on `requires_action` for a human.
- Likely fix: attach tracked repos as `sources` on these routines, **or** rewrite the prompts to use only `git clone --depth 1` + Grep/Read (these worked) and never the REST API. Same risk applies to `sun-stale-worktrees` and `sun-vuln-patcher`, which have the same add_repo pattern.

## 3. Weekly obn pair is disconnected
- `week-obn-review` collects `- [x]`/`- [ ]` checkboxes from `Daily Notes/`, but daily notes written per [[DAILY]] have **zero checkboxes** (four prose sections: Repo Activity / Tasks / Notes / Reflections). Friday's review has nothing to collect.
- `week-obn-notes` writes Goals as 3 blank checkboxes that nothing ever fills (W38 and W39 are both blank).
- Proposed fix (user has not yet approved the prompt edits): the review summarizes daily-note sections, with Wins taken from merged PRs and carry-overs being Tasks items that appear on 2+ days, and it names the missing days. `obn-notes` seeds Goals from last week's carry-overs.

## 4. `daily-repo-sync` never commits its own writes to stash
- The 2026-09-24 run logged `stash | SKIPPED_DIRTY`: 72→88 uncommitted paths on `main`, 4 commits behind, all from the obn-repo/obn-review writes (`agent/repos/**`) on 9/23 and 9/24.
- The routine writes into stash, doesn't commit, then skips syncing stash because it's dirty. That compounds daily.
- User-approved direction: fix in [[DAILY]]. Either commit the obn-repo/obn-review writes on the same branch as the daily-note PR, or stage them somewhere that isn't the checked-out `main`.

## 5. Other items
- `week-fin-sum`: `lifefire.netlify.app` is egress-blocked from cloud, and no `fire` connector exists, so it falls back to web search every time. Either drop the "use the fire mcp" line or make it a local routine.
- `week-obn-notes` produced PR #105 (merged 2026-09-24). Daily note PR #107 is open.
- Local cleanup done this session: agent-board back on `master` (+ PR agent-board#79 gitignores `tools/opencut*` clones); avatar/bb-mcp/deployer/skyview/fire/vhs switched from merged `fix/nits` to `main` (local `fix/nits` branches kept); overseer `navbar-v2` + 2 worktrees removed after recovering one uncommitted change into PR vigil#230.
- Still parked, needs a human: `auto-apply-plugin` is on the merged `chore/chrome-web-store-cicd` with an uncommitted `.env.example` + icons + screenshots. Its `icons/icon32.png` is 768×768 / 750 KB and should be 32×32.
- GitHub repo `nitsuah/overseer` now resolves to `nitsuah/vigil`. Check whether scope.md needs the new name.

## 6. Addendum: post-PMO audit (same day, ~07:40 UTC)
- **Results nobody reads:** 8 of the 13 active cloud routines (`obn-import`, `daily-checkin`, `daily-pr-review`, `daily-email`, `week-fin-sum`, `week-vigil-check`, `sun-stale-worktrees`, `sun-vuln-patcher`) write their results only into their session transcript. There's no stash file, email or notification (`week-fin-sum` has `notifications` explicitly all-false). They go green and nobody reads them. **User decision pending** on where these should report. Don't pick a channel unilaterally.
- **Duplicate one-shot check-in triggers:** 5× "Re-check PR #78" and 4× "Re-check PR #83". The drive-to-green check-ins re-arm instead of replacing. They're disabled after firing, but they fill the first page of `RemoteTrigger list`, whose pagination is broken, and that hides the recurring routines. Deleting them is irreversible, so it needs user approval.
- **`week-metrics` 9/18** was marked "succeeded", but its stash PR #99 was closed without merging on 9/19 (superseded by #101?). Its data never landed.
- **`daily-repo-sync` 9/03** "succeeded" in 10 s, which is almost certainly a no-op counted as a pass. Worth a success check that verifies the log entry was written.
- **PMO follow-through:** all 11 PMO PRs merged. The osrs P0 got a fix in osrs#44 (Python 3.12 alignment plus a CI docker-build job; 87 tests pass, 98% coverage). Still open as code work: deployer Slither no-op, games coverage 61% (Tank Battle), fire branch coverage plus Dockerfile `chown`. PMO's portfolio rule is "CI must run whatever METRICS.md cites."
- **Cleanup done:** darkmoon and farm-3j merged agent worktrees removed; `darkmoon-solo` container (started by a pre-commit hook during PMO) stopped. **Kept:** `darkmoon/.claude/worktrees/docs-update-retry` has 2 never-PR'd commits ("chargeable weapon config", "weapon charge state", about 3 months old). Needs a human decision.
- **ats-fill:** 12 screenshot-pipeline PRs merged overnight, then #92 "refresh UI screenshots" opened at 06:18, *after* #91 "prevent screenshot refresh merge loop". The loop may still be live.
- **Merge gate:** the auto-mode classifier blocks `gh pr merge` from this session ("Merge Without Review"). Daily-note PRs (e.g. stash#107) need a human merge, or the next daily-repo-sync run's close-the-loop step.

## Addendum 2: quota gating and schedule (evening, 2026-09-24)

Context: weekly plan usage was at 72% with 5 days to reset, and extra usage was maxed ($101 of $100). This is for RSI to act on (Oct 2).

- **Done:** `week-eng-mini` was set to run every weekday (`0 18 * * 1-5`) despite its name. It now runs weekly: `0 18 * * 3`, Wed 2pm ET.
- **Gate every recurring routine on "has anything changed since my last report?"** Start each run with a cheap check and exit early with a one-line report if nothing changed:
  - `eng-mini` / `eng-loc`: record each repo's HEAD SHA in the report and skip repos whose HEAD matches the previous report.
  - `sun-vuln-patcher`: skip repos whose dependency manifests and lockfiles haven't changed since the last report. Re-check advisories for known versions only.
  - `sun-stale-worktrees` / `week-vigil-check`: skip if `git ls-remote --heads` output (or open PR/issue counts) matches the previous report.
  - `daily-pr-review`: exit early if the set of open PRs and their head SHAs is unchanged from yesterday's report.
  - `monthly-tire-kick` already does this (14-day sweep skip, #120).
- **`week-eng-mini` prompt is stale:** it still fetches `api.github.com/.../contents`, which returns 403 in the cloud sandbox and is why it misses `.gitignore`. Switch it to `git clone --depth 1` like the other rewritten routines, and read the repo list from scope.md.
- **Model choice:** `daily-email` and `daily-pr-review` run on the default model. The summary-only routines (`daily-checkin`, `daily-email`) are candidates for a smaller model.
- **Weekly-window timing:** the weekly limit resets Tue ~1am ET, so the Sun/Mon cluster (stale-worktrees, vuln-patcher, obn-import, vigil-check, eng-loc) runs at the end of the window, when it's most likely to be starved. Consider moving the heavier ones to Tue/Wed.
- **Cleanup:** ~20 fired one-shot "Re-check PR #…" reminders (`created_kind: reminder`, `ended_reason: run_once_fired`) still come back from the routines API. They're disabled and don't run, and the API has no delete.
