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
