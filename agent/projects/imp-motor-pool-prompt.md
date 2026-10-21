# Imps in motor-pool: build prompt

Hand this to a session working in `~/code/motor-pool` (default branch `master`). Use its own worktree, never the shared checkout.

Usage: `/imps`

---

## Goal

Add **imps** to motor-pool. An imp is a short-lived, headless Claude Code worker (`claude -p`) that takes one task off motor-pool's work queue, does it in an isolated git worktree of the target repo, opens a PR, and reports back. Imps route through **9router**, not straight to Anthropic, so routine grunt work (journey bug fixes, doc refreshes, the heavy lifting in today's non-cloud routines) stops spending Opus quota. Opus effort goes to reviewing the PRs imps open.

Anything should be able to dispatch an imp with one call: a routine, a webhook, a Claude session (`/imp`), or the dashboard. motor-pool owns the queue, the run and the record of what happened.

## What exists today (read before designing)

- `dashboard/routes/tasks.js` + `dashboard/task-runner.js`: a task queue with priority ordering. It's an in-memory `Map`, ticks every 5 s, runs one task at a time, and dispatches a task by sending its title as a chat message to a session. It isn't durable and doesn't run processes.
- `POST /api/webhooks/trigger`: HMAC-signed external events that can create tasks.
- `docs/ROADMAP.md`: has a planned durable audit record. Austin also plans a **durable work queue**. Imps should be its first consumer, not a parallel queue. If the durable queue doesn't exist yet, build the minimum durable version (persisted, survives restarts, claim/lease so a task runs once) as phase 1, shaped so it can grow into the general queue.
- motor-pool already runs in Docker and has a sandbox-workspace pattern (`workspace-seed`, `agent_workspace` volume). Reuse its ideas, but imps work on *other* repos under `~/code`.

## Design

**Imp task** (a queue item of kind `imp`):
- `repo`: folder under `~/code`
- `baseBranch`: default is the repo's default branch
- `brief`: markdown
- `source`: e.g. `issue:nitsuah/vigil#123`, `routine:<name>`, `manual`
- `priority`
- `model`: default 9router combo `MAX`
- `limits`: max minutes, max cost
- `labels`
- Server fills in: `status`, `attempts`, `worktree`, `branch`, `sessionId`, `prUrl`, `result`, `costUsd`, timestamps

**Lifecycle:** `queued → claimed → running → pr_opened | no_change | failed | timed_out`
- A claim is a lease with a heartbeat. If the runner dies, the lease expires and the task requeues with `attempts+1`.
- Cap attempts at 2. After that it's `failed`, with the imp's last report attached, and it doesn't retry again.

**Runner:**
1. Create a worktree from `origin/<baseBranch>` on branch `imp/<slug>-<id>`. Verify the base hash matches origin before starting.
2. Launch `claude -p "<filled brief>" --model <model> --permission-mode acceptEdits --allowedTools <allowlist> --output-format stream-json --verbose < /dev/null`.
   - Env starts clean (drop any inherited `CLAUDE*`/`ANTHROPIC*`), then `ANTHROPIC_BASE_URL=<9router>/v1` and `ANTHROPIC_API_KEY=<9router key from config/secret>`.
3. Stream the JSON events onto motor-pool's event bus. That's how it's watched live: a dashboard panel per running imp (tool calls, files touched, cost, elapsed), plus the CLI session ID for `claude --resume` afterwards.
4. On exit, parse the final result event (summary, `total_cost_usd`, session ID) and the PR URL (`gh pr list --head <branch>`), then set the terminal status.
5. Enforce time and cost limits by killing the process. Clean up the worktree when the PR is merged or closed, or on `no_change`/`failed` after the record is saved.
6. Concurrency default is 1 and configurable. Running six at once has blown the quota before.

**API:**
- `POST /api/imps`: create an imp task.
- `GET /api/imps` / `GET /api/imps/:id`: status, live tail, result.
- `POST /api/imps/:id/cancel`: cancel a task.
- Auth on the create endpoint (bearer or HMAC like the webhook) before it's reachable beyond localhost.

**Dispatchers (thin, after the core works):**
- A `/imp` skill or command for Claude sessions that POSTs a brief.
- A webhook rule: GitHub `issues.opened`/`labeled` with `bot:journey` → imp task using the journey-fix brief template. Label the issue `imp:working`, then `imp:pr` or `imp:failed`.
- A routine-offload path, so cloud and local routines can enqueue their mechanical steps as imps.

**Guardrails:**
- Imps never merge.
- Never touch auth, billing or secrets paths (reject at enqueue by a path/keyword rule, or have the brief tell the imp to stop and report).
- Allowlist only: `Read Edit Write Glob Grep` plus `Bash(git *) Bash(docker *) Bash(gh *)`. No host npm/node: Docker only.
- During a 9router fallback window (the router reports a non-Anthropic model serving), only run tasks tagged `low-risk`. Hold the rest.
- Commits carry `Co-Authored-By: 9router imp <noreply@anthropic.com>`, so imp work stays distinguishable in history.

## Brief template (what the runner fills per task)

```
You are an imp working in the git worktree {worktree} (branch {branch}, cut from origin/{base}). Work only there.

## Task
{brief}

## Rules
- Match the surrounding code style. Keep the diff small and focused.
- Read AGENTS.md / CLAUDE.md in the repo first.
- Never run npm/node on the host. Use Docker (docker run --rm -v "{worktree}:/app" -w /app node:<.nvmrc> ...). Type check and the relevant tests must pass.
- Close tracked work in the same branch: TASKS.md / ROADMAP.md / CHANGELOG.md (Unreleased) / FEATURES.md as the repo's AGENTS.md says.
- Commit with a message ending in "Co-Authored-By: 9router imp <noreply@anthropic.com>", push, and open a PR against {base}. Body: what changed, how it was tested, "{closes_line}", "Written by an imp (motor-pool task {id})". Do not merge.
- If blocked (tests you can't fix, unclear design, the task touches auth/billing/secrets), commit nothing broken. Stop and explain.

## Finish
Report: files changed, test/typecheck results with counts, PR URL (or why there is none).
```

## Lessons from the first manual imp (2026-10-15, vigil tier-sort)
- 9router answers on `http://[::1]:20128` and the LAN IP. `127.0.0.1:20128` hangs on a stale wslrelay, so don't hard-code `127.0.0.1`. Inside Docker, use `host.docker.internal:20128`.
- `claude -p` launched from a non-TTY parent can wait on stdin. Always use `< /dev/null`.
- The `unrecognized_model` warning for 9router combo names (`MAX`) is harmless.
- Track progress with stream events and the transcript, not by grepping router logs. We misjudged a working imp as stuck that way and killed it.
- Desktop-app sessions can't be routed through 9router: the app overwrites `ANTHROPIC_BASE_URL`. That's why imps live in motor-pool.

## Done when
- Phase 1 durable queue (or integration with the existing one) with claim/lease, persisted across restarts.
- Imp runner + `/api/imps` + dashboard panel. Tests for lifecycle, lease expiry/requeue, limits and cancel.
- One real end-to-end run: an imp fixes a `bot:journey` issue in some repo and opens a PR.
- README/FEATURES/ROADMAP/TASKS/CHANGELOG updated in the same PR(s).
