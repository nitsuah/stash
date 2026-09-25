---
kind: rsi-report
---

# RSI report — 2026-09

This is the first run of the `monthly-self-improvement` scheduled task. It was kicked off manually on 2026-09-24 (ET), ahead of the 2026-10-02 fire, with the user's kickoff context in `routine-run-findings-2026-09-24.md` addendum 3. Spec: [[RSI]]. Every prompt, routine and memory edit is logged in `agent/logs/rsi-changes.log`, which is local-only because `*.log` is gitignored.

Quota posture: the weekly window was about 72% used and extra usage was maxed, so this cycle did prompt and config fixes only. It did no product-repo work.

## Inputs read
- `usage-report-2026-09.md`, `pmo-audit-2026-09-24.md`, `routine-run-findings-2026-09-24.md` (addenda 1–3), `findings-ledger.md`, `tire-kick-2026-09-24.md`, `rsi-changes.log`.
- Live state from `list_scheduled_tasks`, with 6 local tasks all enabled. Cloud routines were read with `RemoteTrigger get` on the 3 recurring routines whose IDs could be recovered.
- scope.md against `gh repo list nitsuah` / `Nitsuah-Labs`: **no drift**. 17 tracked repos, all present, visibility matches. The cached lists in DAILY.md, METRICS.md and the `monthly-pmo-audit` wrapper (16 repos; stash is skipped by design) all match scope.md.

## Changes made

### PRs (stash)
| PR | Theme | Ledger |
|---|---|---|
| [stash#126](https://github.com/nitsuah/stash/pull/126) | Move `Daily Notes/` + `Weekly Notes/` to flat `agent/notes/`. Every reader and writer moves in the same change: DAILY guard, **merge-gate filename regex**, commit scope, TIRE, RSI map, pii-scan, pre-commit. **Merge before the next daily-repo-sync run (07:07 ET).** | user decision 6 |
| [stash#127](https://github.com/nitsuah/stash/pull/127) | TIRE: re-verify `routine` items against the current prompt; branch in the main checkout instead of a worktree; don't `docker stop` containers that hooks started | addendum 3 |
| [stash#128](https://github.com/nitsuah/stash/pull/128) | Make "succeeded" prove output landed: DAILY runs an end-of-run evidence check and reports `INCOMPLETE:` when output is missing; USAGE counts no-ops and lost output separately | F-20260924-22 |
| this PR | Ledger status updates + 6 new rows, RSI.md map drift fix, this report | — |

### Cloud routines (RemoteTrigger update, logged first)
- **week-eng-mini** (`trig_01N2Uyn…`): rewritten to match week-eng-loc. It now reads the scope.md Tracked list, uses `git clone --depth 1` plus Read/Glob only (no `api.github.com`, no push escalation) and `git add -f`. It honors MINI.md's LICENSE = KEEP rule and has a HEAD-SHA changed-since gate. Tools: added Grep, dropped WebFetch/WebSearch. Evidence: the 9/24 run used a `search_code` workaround, excluded vigil and ats-fill, and still deferred LICENSE (F-20260901-08, seen 9×).
- **week-eng-loc** (`trig_01DFtor…`): added the same HEAD-SHA gate, and each report now records a `HEAD:` line.
- **week-obn-import** (`trig_01BG8S…`): its staleness check skips dated note files, which would otherwise be flagged forever after the move. It flags the newest daily note if it is more than 3 days old.

### Local scheduled tasks
- `daily-repo-sync` wrapper: its commit-scope line now names the `agent/notes/` dated files.
- `monthly-tire-kick` wrapper: a dirty stash checkout means the ledger goes to a human, not into a worktree (the stash gitleaks hook fails from a worktree).

### Memory
- New `project-serialize-routine-catchup`: fire catch-up runs one at a time (F-20260924-20).
- New `reference-cloud-routine-ids`: `RemoteTrigger list` doesn't paginate. The file lists the known IDs and how to find the rest.

### Ledger
- Marked **done** after re-verifying: F-20260924-04 and -24 (gcp#68/#69), F-20260923-01 and -02 (skyview#148/#149), F-20260924-19 (obn weekly pair folded into DAILY), F-20260924-20, F-20260904-02 (METRICS native path already existed from 9/19).
- Also **done**, although listed as open or awaiting a decision: F-20260924-14 (the 8 transcript-only routines have saved reports to `agent/reports/cloud/<routine>/` since 9/24, stash#111–#113), F-20260924-18 (all four push-escalating routines were rewritten to clone + read on 9/24; eng-mini today) and F-20260924-21 (cloud week-fin-sum is disabled and the local one reaches the fire MCP). These are the same "already fixed" trap TIRE hit, and #127 now guards against it.
- Added `quick` F-20260924-26…30 (skyview ×3, vigil CHANGELOG, darkmoon link), `human` -25 (done), and `routine` -31 (remaining gates, below).
- **Aging:** no open item is older than 21 days or has Seen ≥ 3. The only historical Seen ≥ 3 items (F-20260901-08 LICENSE, F-20260916-01, F-20260917-01/-02) are done. The week-eng-mini fix above addresses the root cause of LICENSE recurring. The loop is closing.

## Considered but not done
- **Changed-since gates on sun-vuln-patcher, sun-stale-worktrees, week-vigil-check and daily-pr-review** (addendum 2): not applied. `RemoteTrigger list` returns only 20 one-shot reminders and ignores the cursor, so those routines' trigger IDs couldn't be recovered from logs. Three unnamed IDs from a 9/24 transcript are in the `reference-cloud-routine-ids` memory for next cycle. Tracked as F-20260924-31.
- **Smaller model for daily-checkin / daily-email; moving the Sun/Mon cluster to Tue/Wed**: blocked on the same missing IDs. The move also needs a cheap check that the new times don't collide with daily-repo-sync. Next cycle.
- **Skyview, vigil and darkmoon quick fixes (F-26…30):** left for TIRE on 9/28, per addendum 3's sequencing and the quota posture.
- **Map "Known gap"** (account-level skills that don't match their routines): no new evidence this cycle, so it stays flagged.

## Decisions for the user (not taken)
1. **Transcript-only routines' reporting channel (F-14)** looks resolved already (log entries dated 2026-09-24, "user-approved"). Confirm, or say what's still missing.
2. **Delete the ~20 disabled one-shot "Re-check PR" triggers (F-13)?** This is irreversible, and the API has no delete, so it can only be done at claude.ai/code/routines. They also make `list` useless for finding the recurring fleet.
3. **Push escalation (F-18):** addendum 3 asks "sources vs rewrite", but every affected routine was already rewritten to clone + read. Confirm that's the chosen answer.
4. **week-fin-sum (F-21):** moot. The cloud version is disabled and the local one works.
5. **Auto-merge vs CodeRabbit** (options a/b/c in addendum 3): still open. Until it's decided, routines leave CodeRabbit-blocked PRs open (option a is the de facto state).

## Next (per addendum 3 sequencing, not started)
Re-run LOC/MINI now that both prompts changed. Run them serially, after the weekly reset (Tue ~1am ET). Then the state-of-the-union regen, then the six `pmo` refactor epics.
