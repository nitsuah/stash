# Tire Kick — Repo Health Check Prompt

Run a full health check across all in-scope repos. Verify each is up to date, test it via Docker, fix any issues found, open PRs, wait for CI, and compile a report.

---

## Scope

In-scope repos are defined in `C:\Users\ajhar\code\stash\agent\projects\scope.md`:

```
- agent-board
- auto-apply-plugin
- darkmoon
- farm-3j
- fire
- games
- kryptos
- nitsuah-io
- overseer
- stash   ← code stash only; no docker/deploy
- vhs
```

---

## Instructions

### 1. Git Triage (per repo)

For each repo:
- Check current branch: `git branch --show-current`
- Check for active worktrees: `git worktree list`
- If not on `main`/`master`, or if an active user worktree exists (outside `.claude/worktrees/`): **SKIP** — note the branch name in the report
- If on main: `git pull --ff-only origin main` to ensure latest

### 2. Reconnaissance (parallel)

For each active repo, in parallel:
- Read `README.md`
- Read `docs/` folder (if present)
- Identify test/lint commands from: `Makefile`, `package.json`, `pyproject.toml`, `Cargo.toml`, `docker-compose.yml`, `Dockerfile`
- Note which CI workflows exist in `.github/workflows/`
- Check if config has moved to `config/` subdirectory (common pattern in these repos)

### 3. Pull Latest

- `git pull --ff-only origin main` for all active repos simultaneously

### 4. Docker Health Check (sequential per repo to avoid I/O contention)

Run checks in this order using Docker (not host toolchain). Prefer `docker compose run --rm` if a compose file exists; otherwise `docker build + docker run`.

Always use `--build` flag when building to avoid stale cached images. Watch for:
- **Image naming collisions**: If a repo uses `config/docker-compose.yml`, default image names like `config-test` collide across repos. Fix by adding explicit `image:` fields.

For each repo, run what applies:
1. **Lint** — ESLint, ruff, flake8, cargo clippy, etc.
2. **Type-check** — tsc, mypy (if in CI), etc.
3. **Unit tests** — vitest, jest, pytest, cargo test, etc.
4. **Smoke tests** — if defined and fast (<2 min)
5. Skip slow E2E/Playwright/network-dependent tests unless they run as part of the Docker CI pipeline

Special case — **stash**: no docker/deploy; just review directory structure and confirm no tests exist.

### 5. On Failure: Branch → Fix → PR → Monitor

If any check fails:
1. `git checkout -b fix/<descriptive-name>` in the affected repo
2. Fix the root cause (not a workaround — find the real issue)
3. Verify the fix locally via Docker before pushing
4. Commit with a clear message (what + why)
5. `git push -u origin fix/<name>`
6. `gh pr create --repo <org>/<repo> --head fix/<name> --base main ...`
7. Poll CI: `gh pr checks <PR#> --repo <org>/<repo>`
8. Once fully green: `gh pr merge <PR#> --repo <org>/<repo> --squash --auto` (or merge via web if branch protections require review)

Common issues to watch for:
- ESLint linting `.claude/worktrees/` directory → add `.claude/` to ignores
- `next lint` removed in Next.js 16 → replace with `eslint . --ext .js,.jsx,.ts,.tsx`
- Docker image name collisions (same `config/` dir layout across repos)
- `ruff` with `fix = true` in pyproject.toml auto-modifies files when run via mounted volume
- mypy pre-commit hook failures that are pre-existing (check if CI runs mypy; if not, note as pre-existing)

### 6. Report

After all repos are checked and all PRs merged (or noted as pending), write a report to:
```
C:\Users\ajhar\code\stash\agent\projects\TIRE\YYYY-MM-DD-tire-kick.md
```

Report structure:
```markdown
# Tire Kick Report — YYYY-MM-DD

## Scope
Table of repos with: branch tested, status (✅ tested / ⚠️ skipped)

## Test Results by Repo
Per repo:
- Language/stack
- What checks ran and their result (✅/❌)
- Issues found (specific error messages, file:line)
- Fix applied (PR link)

## Summary of Issues Found & Fixed
Table: Repo | Issue | PR | Severity

## Clean Repos
List of repos with zero issues

## Skipped Repos
List with reason (active branch name)

## Notes
- Docker version used
- What was NOT tested (E2E, slow tests, etc.)
```

---

## Tips From Previous Runs

- **Parallel recon, sequential Docker**: Spawn recon subagents in parallel; run Docker builds sequentially to avoid overwhelming the daemon.
- **Worktree detection**: `git worktree list` — skip if any non-`.claude/worktrees/` worktree exists (user is likely mid-work).
- **Background jobs use TIRE dir**: This prompt is designed to be run as a background agent. Write the report to `stash/agent/projects/TIRE/` as a persistent artifact.
- **EnterWorktree required**: Background sessions require `EnterWorktree` before editing files. The worktree must be within the target repo. Use `git -C <repo> diff > patch.diff` + `git apply` to transfer unstaged changes into the worktree if needed.
- **Pre-commit hooks that modify files**: After black/isort/etc. modify files and abort a commit, `git add -A` and retry — the second attempt should pass.
- **kryptos ruff**: `fix = true` in pyproject.toml means `ruff check` auto-modifies files when a volume is mounted. This is expected behavior; commit the result.
- **nitsuah-io lint**: Use `gh pr create --head <branch> --base main` explicitly when running `gh` from a different repo's worktree context.
