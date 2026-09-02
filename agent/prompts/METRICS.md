# METRICS

> Automated coverage-refresh routine. Re-measures test coverage for each repo and updates its `METRICS.md` with real, timestamped numbers — never fabricated or estimated.

**Status:** fixed 2026-09-02 — this file was corrupted (truncated mid-sentence) since it was created on 2026-06-25 and could not have run correctly as written. See [[PMO]] — its "Metrics Integrity Rules" section already covers metrics refresh as part of the monthly PMO cycle. Run this file standalone for an on-demand, coverage-only pass; the monthly `monthly-pmo-audit` scheduled task covers the full doc+metrics cycle automatically.

## Scope

Repos: `agent-board`, `auto-apply-plugin`, `avatar`, `bb-mcp`, `darkmoon`, `deployer`, `farm-3j`, `fire`, `games`, `gcp`, `kryptos`, `nitsuah-io`, `osrs`, `overseer`, `skyview`, `stash`, `vhs` — override with an explicit repo list when invoked for a subset.

## Steps (per repo)

1. Confirm the local checkout at `C:\Users\<user>\code\<repo>` is on its default branch (`main` or `master`) and clean (`git status --short`). If dirty or on a non-default branch, skip and note why — never stash or discard someone else's in-progress work.
2. Pull latest (`git pull --ff-only`) so coverage is measured against current `main`.
3. Run the repo's coverage command in Docker (prefer Docker so no host toolchain is required):
   - Node/JS repos: `docker compose run --rm unit` or `npm test -- --coverage` inside a `node:22-alpine` container, per the repo's own README/CONTRIBUTING instructions.
   - Python repos: `pytest --cov` inside the repo's own Docker image.
   - If no coverage script exists, or the Docker build fails, log `FAILED` with the reason and move to the next repo — never block the whole run on one failure.
4. Extract statement / branch / function / line coverage percentages from the tool's own output. Do not estimate or infer a number from partial output.
5. Update the repo's `METRICS.md`:
   - Replace the coverage table with the measured values.
   - Update the `Last Validated` (or `Last Updated`) date to today.
   - If a metric couldn't be measured, write `TBD` with a one-line reason — never leave a stale number in place uncorrected and never invent one.
6. Commit on a branch named `metrics/<repo>-coverage-<YYYY-MM-DD>`, push, and open a PR titled `docs(metrics): refresh <repo> coverage (<YYYY-MM-DD>)`. Never commit directly to the repo's default branch.
7. Log the result to `stash/agent/logs/metrics-audit.log` as one row per repo: `| repo | result (PULLED/SKIPPED/FAILED) | coverage delta | note |`.

## Rules

- Never fabricate a coverage number. `TBD` is always an acceptable answer; a wrong number is not.
- Never overwrite a repo's custom METRICS.md sections (health score commentary, feature-completeness tables) — only touch the coverage table and its timestamp.
- Stop after a repo's Docker build fails twice; don't retry indefinitely.
