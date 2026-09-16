# METRICS

> Automated coverage-refresh routine. Re-measures test coverage for each repo and updates its `METRICS.md` with real, timestamped numbers — never fabricated or estimated.

**Status:** fixed 2026-09-02 — this file was corrupted (truncated mid-sentence) since it was created on 2026-06-25 and could not have run correctly as written. See [[PMO]] — its "Metrics Integrity Rules" section already covers metrics refresh as part of the monthly PMO cycle. Run this file standalone for an on-demand, coverage-only pass. A `monthly-pmo-audit` Claude Code scheduled task exists to run the full doc+metrics cycle monthly — that task lives outside this repo (`~/.claude/scheduled-tasks/monthly-pmo-audit`), so this file can't guarantee it's still enabled; check `list_scheduled_tasks` if you need to confirm it's actually running before relying on it.

## Scope

Canonical repo list: `agent/projects/scope.md`'s "Tracked" table. The list below is a cached copy kept in sync manually — if you notice it's drifted from scope.md, trust scope.md and fix this line: `agent-board`, `auto-apply-plugin`, `avatar`, `bb-mcp`, `darkmoon`, `deployer`, `farm-3j`, `fire`, `games`, `gcp`, `kryptos`, `nitsuah-io`, `osrs`, `overseer`, `skyview`, `stash`, `vhs` — override with an explicit repo list when invoked for a subset.

## Steps (per repo)

1. Confirm the local checkout at `C:\Users\<user>\code\<repo>` is on its default branch (`main` or `master`) and clean (`git status --short`). If dirty or on a non-default branch, skip and note why — never stash or discard someone else's in-progress work.
2. Pull latest (`git pull --ff-only`) so coverage is measured against current `main`.
3. Run the repo's coverage command in Docker (prefer Docker so no host toolchain is required):
   - Node/JS repos: `docker compose run --rm unit` or `npm test -- --coverage` inside a `node:22-alpine` container, per the repo's own README/CONTRIBUTING instructions.
   - Python repos: `pytest --cov` inside the repo's own Docker image.
   - If no coverage script exists, log `FAILED` with the reason and move to the next repo. If the Docker build fails, retry once; if it fails again, log `FAILED` with the reason and move to the next repo — never block the whole run on one repo.
4. Extract statement / branch / function / line coverage percentages from the tool's own output. Do not estimate or infer a number from partial output.
5. Update the repo's `METRICS.md`:
   - Replace the coverage table with the measured values.
   - Update the `Last Validated` (or `Last Updated`) date to today.
   - If a metric couldn't be measured, write `TBD` with a one-line reason — never leave a stale number in place uncorrected and never invent one.
6. Commit on a branch named `metrics/<repo>-coverage-<YYYY-MM-DD>`, push, and open a **regular, non-draft PR** (`gh pr create` — never `--draft`) titled `docs(metrics): refresh <repo> coverage (<YYYY-MM-DD>)`. Never commit directly to the repo's default branch.
7. **Auto-merge, don't leave it open.** This is a single-file, machine-verified doc update — the whole point of automating it is that nobody has to remember to click merge. After the checks in step 6's PR start running, poll `gh pr checks <PR> --repo <owner>/<repo>` (a few retries with a short wait is fine) until they resolve, then:
   - **All checks passed, PR is `MERGEABLE`/`CLEAN`, and the diff touches only `METRICS.md`/`docs/METRICS.md`:** `gh pr merge <PR> --repo <owner>/<repo> --squash --delete-branch`. Log `MERGED`.
   - **Any check failed, is still pending after a reasonable wait, or the diff touches anything beyond the metrics file:** leave it open, non-draft, for a human — log `OPEN_NEEDS_REVIEW` with the reason. Never force-merge a red or unresolved PR.
   - This is the one file in the whole agent stack allowed to merge its own PRs — every other routine (DAILY's `obn` notes, PMO, RSI) explicitly does not. That's because the diff here is fully machine-verified (a coverage number the CI run itself produced) rather than judgment-based.
8. After the push/PR/merge sequence, check the target repo's checkout back out to its default branch and pull (or do this whole step in a disposable worktree) — leaving it on the metrics branch will make step 1 skip that repo as "non-default branch" on the next run.
9. Log the result to the absolute path `C:\Users\<user>\code\stash\agent\logs\metrics-audit.log` (not a path relative to the repo being audited — this file always lives in the `stash` checkout, regardless of which repo's coverage is being measured) as one row per repo: `| repo | result (PULLED/SKIPPED/FAILED/MERGED/OPEN_NEEDS_REVIEW) | coverage delta | note |`. Write the log locally; don't commit or push it as part of this routine — leave that for a human to batch periodically, same as `daily-repo-sync`'s logs.

## Rules

- Never fabricate a coverage number. `TBD` is always an acceptable answer; a wrong number is not.
- Never overwrite a repo's custom METRICS.md sections (health score commentary, feature-completeness tables) — only touch the coverage table and its timestamp.
- Stop after a repo's Docker build fails twice; don't retry indefinitely.
- Never open these as draft PRs. Draft status is why they used to pile up unmerged (auto-apply-plugin #62, fire #97, vhs #53 all shipped draft and were eventually closed unmerged, never landing the coverage refresh) — a draft signals "not ready," and nothing in this routine ever comes back to mark it ready.

## Continuous improvement

After each run, if something about this routine's own instructions was wrong, ambiguous, or caused avoidable manual cleanup (e.g. this file previously created draft PRs that piled up unmerged for 5+ days across agent-board #72, darkmoon #447, fire #104, skyview #129 until fixed on 2026-09-16), fix this file directly and note briefly what changed and why, the same way DAILY.md's "Status" line documents its own past fixes.
