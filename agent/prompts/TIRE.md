# Tire Kick: Findings Fix Queue + Repo Health Check

TIRE closes the loop on the report routines. Most routines only report: eng-mini, eng-loc, week-vuln, daily-brief and obn-import. Since 2026-09-26 TIRE also owns the monthly coverage refresh ([[METRICS]], moved here from the retired cloud week-metrics) and remote stale-branch pruning (from the retired sun-stale-worktrees). TIRE reads what they found, keeps one **findings ledger**, fixes the small safe items with PRs, and hands the rest on. After that it runs the Docker health check sweep across the tracked repos.

**Runs:** monthly on the 28th (`monthly-tire-kick` scheduled task), so the ledger is current before [[PMO]] (1st) and [[RSI]] (2nd). It can also be run on demand at any time.

**Who owns what:**
- Reports **find** things.
- TIRE **fixes the small ones** and tracks everything in the ledger.
- [[PMO]] takes the items TIRE marks `pmo`.
- [[RSI]] checks whether items age out. An item open more than 3 weeks means a routine isn't closing the loop, and RSI fixes that routine rather than the item.

---

## Scope

Repos: the **"Tracked" table** in `C:\Users\ajhar\code\stash\agent\projects\scope.md` (local path, GitHub URL, org). Read it live every run; don't keep a copy of the list here. For stash itself, do the findings intake and ledger only, with no Docker/deploy checks.

---

## 1. Git triage (per repo)

- `git -C <path> branch --show-current` and `git -C <path> worktree list`.
- If the repo isn't on `main`/`master`, is dirty, or has a user worktree outside `.claude/worktrees/`: **skip changes to it**. Note the branch in the report. Its findings still go in the ledger.
- Otherwise run `git pull --ff-only`.

## 2. Findings intake → ledger

Ledger: `C:\Users\ajhar\code\stash\agent\reports\findings-ledger.md`. Create it from the template below if it's missing.

1. **Window:** reports dated after the ledger's `Last intake:` date (first run: the last 35 days).
2. **Sources:** read every report in the window:
   - `agent/reports/eng-mini-*`, `eng-loc-*`, `metrics-*`, `pmo-audit-*`, `routine-run-findings-*`
   - `agent/reports/cloud/**` (week-vuln, daily-brief's PR section, obn-import, plus older vuln-patcher / stale-worktrees / daily-pr-review files)
   - **week-vuln's `## For TIRE` section** is pre-classified: each `quick | <repo> | bump ...` line becomes a `quick` ledger item as written. Re-verify it in §2.5 before fixing, and treat a `peer-dep risk` note as a reason to pin exact versions (see the darkmoon#450 / farm-3j#338 pattern in `rsi-changes.log`).
   - the `## Notes` section of the daily notes (`agent/notes/YYYY-MM-DD.md`) in the window
   - Skip `daily-email`, `daily-checkin`, daily-brief's calendar and inbox sections, and `week-fin-sum` output. That's personal, not repo work.
3. **Extract actionable items only.** An item is actionable if it has a concrete repo, file or package and a concrete change: untrack a generated file, bump a package past a published advisory, delete a merged stale branch, fix a broken CI step, refresh a stale `agent/repos/<repo>.md` claim. Observations that say "no action needed" don't go in.
4. **Deduplicate** by repo + target (file, package or branch) + problem. If the item already exists, bump `Seen` and `Last seen` instead of adding a row. Repeated sightings are the signal that the loop isn't closing.
5. **Re-verify before trusting a report.** Check the current state on `main`, since reports go stale. If it's already fixed, mark the item `done` with the evidence, such as the commit or PR that fixed it. **This includes `routine`-class items:** re-read the current prompt, scheduled-task `SKILL.md` or script the finding names (and `agent/logs/rsi-changes.log`, where RSI and manual sessions log prompt edits) before carrying one forward as open. The first run (2026-09-24) listed three `routine` items as open that had already been fixed.
6. **Classify** each open item:
   - `quick`: small, mechanical, low risk, and verifiable with tests or CI. Examples: `git rm --cached` a generated file, a patch/minor dependency bump for an advisory, `.gitignore` or lint-config fixes, a doc fact that is provably wrong, deleting remote branches whose PR is merged or closed.
   - `pmo`: planning or roadmap work, anything that needs product judgment, and multi-file refactors. **Most eng-loc (LOC) findings belong here.**
   - `human`: security-sensitive, destructive, licensing, touching secrets or credentials, major-version upgrades with breaking changes, or anything that needs an account or setting change.
   - `routine`: the finding is really a bug in a routine or prompt. Leave it for [[RSI]].

## 3. Fix `quick` items (budget: at most 5 PRs per run)

Pick the oldest or most-repeated `quick` items first, and group items for the same repo into one PR where that makes sense.

1. `git checkout -b tire/<repo>/<short-theme>-<YYYY-MM-DD>` in the repo's main checkout, if it is clean and on the default branch. If it isn't, skip the repo and log it (see Tips for why not a worktree).
2. Fix the root cause, not a workaround. Verify via Docker, not the host toolchain (see §4 for commands).
3. Commit with what and why, and reference the ledger IDs (`Fixes F-20260924-03`).
4. `git push -u origin <branch>`, then `gh pr create --repo <owner>/<repo> --base main`. List the ledger IDs and the source report in the PR body.
5. Poll `gh pr checks`. When all checks are green, `gh pr merge --squash --delete-branch`. If a required review blocks the merge, leave the PR open and mark the item `pr-open`.
6. If CI fails and the fix isn't obvious within one retry, close nothing and leave the PR open. Mark the item `blocked` with the reason.
7. Update the ledger row: status, PR link, date.

Never force-push, rewrite history, or change repo settings, rulesets or secrets. Those are always `human`.

## 4. Docker health check sweep

Only if budget remains after §3. Skip a repo if a `tire-kick-*.md` report from the last 14 days already swept it; say so in the report. Otherwise run the sweep sequentially per repo to avoid I/O contention, preferring repos with no health check in the last 60 days.

- Use Docker: `docker compose -p <repo> ... run --rm` if a compose file exists, else `docker build` + `docker run`. Always `--build`. Always pass `-p <name>` for `config/docker-compose*.yml`, because several repos share the inferred project name `config` and would collide.
- Checks: lint, then type-check, then unit tests, then fast smoke tests (<2 min). Skip slow E2E, Playwright and network tests unless CI runs them in Docker.
- Each failure becomes a ledger item (source `tire-health`). Fix it under §3's budget if it's `quick`; otherwise classify it and leave it.

Common issues from past runs:
- ESLint linting `.claude/worktrees/` → add `.claude/` to ignores.
- `next lint` was removed in Next.js 16 → use `eslint .`.
- `ruff` with `fix = true` modifies files through a mounted volume (kryptos). That's expected; commit the result.
- mypy pre-commit failures that CI doesn't run: note them as pre-existing, don't fix them.

## 4b. Monthly coverage refresh + remote branch pruning

Only if budget remains after §3 and §4. Both were weekly cloud routines until 2026-09-26. They need Docker or local git, so they live here.

- **Coverage ([[METRICS]]):** for up to 3 repos whose `METRICS.md` coverage line is older than 30 days, run the repo's coverage command in Docker and update `METRICS.md` on a `tire/<repo>/metrics-<date>` branch. It uses the same PR and merge rules as §3 and **counts toward the 5-PR budget**. Never write a number you didn't measure this run.
- **Remote stale branches:** per repo, run `git branch -r --merged origin/<default>` plus `gh pr list --state merged --search "head:<branch>"` for squash-merges. Remote branches whose PR **merged** more than 14 days ago (or that `--merged` lists) are `quick`. A branch whose PR was closed **without** merging may hold unmerged work: it's `human`, like any other unmerged stale branch, and is never deleted here. Delete them with `gh api -X DELETE repos/<owner>/<repo>/git/refs/heads/<branch>` (the classifier blocks `git push --delete`), at most 20 per run, and log them in the report. Unmerged stale branches go in the ledger as `human`.

## 5. Report + ledger PR (stash)

stash is a **PUBLIC** repo. Ledger and report entries name repos, files, package names, versions and public advisory IDs only. Never include secrets, tokens, email addresses, private personal details or working exploit steps.

1. Write `C:\Users\ajhar\code\stash\agent\reports\tire-kick-<YYYY-MM-DD>.md` with these sections:
   - **Intake:** sources read, items added, items deduplicated, items found already fixed.
   - **Fixed:** repo, ledger ID, PR, status.
   - **Handed off:** the `pmo`, `human` and `routine` items, one line each.
   - **Health check:** per repo: checks run and result (✅/❌), or skipped and why.
   - **Aging:** open items with `Seen` ≥ 3 or first seen more than 21 days ago. This is RSI's input.
2. Set the ledger's `Last intake:` to today.
3. In stash: branch `tire/stash/ledger-<YYYY-MM-DD>`, commit **only** `agent/reports/findings-ledger.md` and `agent/reports/tire-kick-<date>.md`, then open a PR. It's a report-only PR, so once `Install & syntax check` passes, squash-merge **that PR only**.

### Ledger template

```markdown
# Findings ledger

Maintained by [[TIRE]]. Read by [[PMO]] (`pmo` items) and [[RSI]] (aging).
Last intake: YYYY-MM-DD

| ID | First seen | Last seen | Seen | Source | Repo | Finding | Class | Status | Link |
|----|-----------|-----------|------|--------|------|---------|-------|--------|------|
```

- **ID:** `F-<first-seen YYYYMMDD>-<NN>`.
- **Status:** one of `open`, `pr-open`, `blocked`, `done`, `wontfix`.
- Keep rows marked `done` or `wontfix` for one cycle, then move them under a `## Closed` heading at the bottom.

---

## Tips from previous runs

- **Parallel recon, sequential Docker.** Recon subagents can run in parallel; run Docker builds one at a time.
- **Commit on a branch in the main checkout when the repo is clean; don't use worktrees.** Several repos' hooks break from a worktree (2026-09-24): vigil's husky pre-commit always runs lint-staged on the Windows host; darkmoon's runs on the host from a worktree, otherwise it starts the `darkmoon-solo` container and leaves it running; stash's gitleaks hook runs in Docker against the repo root and fails from a worktree. If the main checkout is dirty or on another branch, that's someone's work in progress: skip the repo.
- **Don't `docker stop` containers that hooks start.** The auto-mode classifier blocks it ("Interfere With Workloads"). Name the container (e.g. `darkmoon-solo`) in the report for a human instead.
- **Pre-commit hooks that modify files:** after black/isort abort a commit, `git add -A` and retry.
- **Cross-repo `gh`:** always pass `--repo <owner>/<repo>` (and `--head`), because `gh` otherwise infers the repo from the cwd.
- **stash's pre-commit hook** runs gitleaks and the PII scan. If it blocks the ledger commit, fix the content; never use `--no-verify`.
