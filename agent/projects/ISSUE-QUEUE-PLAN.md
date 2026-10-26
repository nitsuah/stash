# Issue queue: autonomous issue completion (plan, 2026-10-22)

## 1. Audit of what we tried

stash\agent\projects\imp-motor-pool-prompt.md

| Pilot | Where | Verdict | Why |
| --- | --- | --- | --- |
| `github-issue-to-pr` skill | nitsuah/ats-fill#157 (+2,089 lines, 25 CodeRabbit findings) | **Close** | It never calls an LLM. "Implement" is a regex keyword → folder map (`/popup/` → `src/popup/`, paths that don't even exist). It plans, it can't fix anything. |
| `github-issue-to-pr` workflow | nitsuah/fire#204 (74 lines) | **Close** | Runs `node skills/github-issue-to-pr/index.js`, which doesn't exist in fire. Copy-pasted from ats-fill (installs Chrome-extension skills into fire). Passes `GITHUB_RUN_NUMBER` as the PR number. |
| Both, structurally | GitHub Actions | **Wrong place** | A hosted runner can't reach your local 9router, so a real version would need a paid API key per run, and it auto-merged chore/docs PRs. |
| `agents/L6.agent.md` | .github | **Keep, trim** | Good SDLC rules for an *interactive* session. Its tail (vhs-only docker commands, "continuously monitor CI" RSI line) is wrong for a general agent and contradicts the no-polling rule. Not a queue worker. |
| `prompts/` (AUDIT, FLOW-TASKS, HANDOFF, MASTER) | .github | **Prune** | `MASTER.md` is empty; FLOW-TASKS/HANDOFF are duplicated in `.github/prompts/`. Nothing invokes them. |
| journeys | .github + 8 repos | **Keep: this is the model** | Deterministic, no AI at runtime, files evidence-backed issues. One fix needed below. |
| motor-pool imps (IMPS-PLAN) | motor-pool | **Keep the runner, reorder** | 0 of 4 PRs built. PRs 1–2 (principals, tokens, Postgres queue) are plumbing for multi-tenant gov/edu, not for "issues get fixed while I'm AFK". GitHub labels already are a durable queue. |
| `~/.claude/skills/pr-babysitter` | user skills | **Delete or fix** | A single 18 KB file, not a skill folder, so it never loads. |

**Journeys bug found during the audit:** vigil #300–#304 are five issues for one root cause. Dependabot bumped `@playwright/test` to 1.64 while the container is still `playwright:v1.63.0-jammy`. motor-pool (#103) and any other repo that took the same bump will do the same tonight. The reporter should treat `browserType.launch` / environment errors as one `bot:infra` issue per repo, not one per journey.

## 2. Queue today

~51 open issues: vigil 21, fire 17, vhs 6, darkmoon 3, 1 each elsewhere.

- **Good autonomous candidates now** (narrow, area-labelled, verifiable): `bot:review` UI bugs. fire #166–#173, vhs #77–#79, vigil #275–#277/#279, plus the 5 vigil journey issues (one fix).
- **Need a brief first** (Opus triage): `[FEATURE]` issues like fire #221–#224, vigil #307–#312.

## 3. Design: as little LLM as possible, at the right chokepoints

GitHub issues are the queue. Labels are the state machine. Claiming must be an exclusive transition: a worker must never process an issue that still has `q:ready` or already has `q:working`. Scripts do everything that has a right answer. A model is called only at three chokepoints:

```
issue opened ──► [1 TRIAGE: Opus] ──► q:ready ──► [2 WORKERS: claude -p via 9router, N in parallel]
                    │                                        │
                    └► q:needs-human                         ▼
                                                 deterministic gate (tests in docker,
                                                 diff cap, gitleaks, docs touched)
                                                             │ survivors
                                                             ▼
                                                 [3 JUDGE: Opus] picks one ──► runner pushes, opens PR "Closes #n" ──► q:pr
                                                                                       │
                                                                       you / CodeRabbit review; nothing auto-merges
```

| Chokepoint | Model | Input → output |
| --- | --- | --- |
| 1. Triage | Opus 5.5, one call | Issue + repo TASKS/FEATURES → a brief (files likely touched, acceptance criteria, test command) posted as an issue comment, plus `q:ready` / `q:needs-human` / `q:wontfix`. Features always go to `q:needs-human` until you thumbs-up the brief. |
| 2. Workers | Whatever 9router serves: MAX, plus 1–3 other combos (Codex/GPT, Gemini, GLM/Qwen…) | Brief → a commit in its own worktree. No GitHub token, no push, time/cost cap. |
| 3. Judge | Opus 5.5, one call | The diffs that passed the gate + the brief → winner + a one-paragraph reason, appended to the PR body. |

**Competition is the RSI signal.** Every run appends a row to `scoreboard.jsonl`: issue, repo, area label, model, gate result, judge pick, later merged/closed-unmerged/review-rounds. That tells you which provider wins which kind of issue, so racing can shrink to "send fire UI bugs to X, send vigil backend to Y" and stop paying for N workers.

**The hypervisor (Opus) doesn't babysit the loop.** It runs triage, judging, and a weekly RSI pass: read the scoreboard and the failed runs, then open a PR against the brief template / worker prompt. That's the RSI loop: prompts improve by PR, with evidence.

## 4. Build order (replaces IMPS-PLAN's PR order)

| # | PR | Where | Done when |
| --- | --- | --- | --- |
| 0 | Close #204/#157, prune .github prompts, fix journeys infra-dedup + Playwright image pin | .github, fire, ats-fill, vigil | Clean slate; vigil's 5 journey issues closed by one fix |
| 1 | **Runner v0** (IMPS-PLAN PR 3, minus Postgres): `imp-runner` script that polls `gh issue list --label q:ready` across `config/imp-repos.json`, claims by verifying the issue has `q:ready` and lacks `q:working`, then atomically removing `q:ready` and adding `q:working` plus a claim comment (runner ID and timestamp; the desktop can run a second runner), worktree from `origin/main`, `claude -p` via 9router with the IMPS-PLAN flags, gate; on success, push/open the PR; on success or terminal failure, release `q:working` before adding exactly one terminal label (`q:pr`, `q:held`, or `q:needs-human`) and record the reason | motor-pool | One real fire `bot:review` bug → open PR with no human touch |
| 2 | **Race mode**: `q:race` (or a default per repo) fans out to N models in parallel worktrees; gate; Opus judge; scoreboard | motor-pool | Same issue, 3 models, one PR, scoreboard row |
| 3 | **Triage**: Opus brief + label on `issues.opened` (polling routine first; webhook later) | motor-pool | New issues arrive with a brief and a label |
| 4 | **Weekly RSI pass** as a scheduled task: scoreboard → PR to prompts/templates | motor-pool | First evidence-backed prompt PR |
| later | IMPS-PLAN PRs 1, 2, 4 (principals, Postgres queue, dashboard panel) | motor-pool | When there's a second human dispatcher or the gov/edu story needs it |

**Stale claim recovery:** A `q:working` claim must include runner ID, issue number, claimed-at timestamp, and a lease expiry. A runner may reclaim only after the lease expires and it verifies the prior runner is not actively renewing the claim; it must post a recovery comment, remove `q:working`, and re-claim atomically where possible. Never treat a stale label alone as proof that a worker is dead. Workers should renew leases while active and stop before pushing if they lose the claim.

**Terminal label transition:** After a successful PR is created, remove `q:working` before adding `q:pr`. On terminal gate, model, push, or PR-creation failure, remove `q:working` before adding `q:held` or `q:needs-human`. Make the transition idempotent and record the outcome in a claim comment; never leave `q:working` on completed work.

**Distributed compute:** the runner is stateless and GitHub holds the state, so a second runner on the Ryzen/4080 desktop is just the same container with `RUNNER_ID=desktop` and its own local 9router. Claims are first-comment-wins. Use `IMP_CONCURRENCY` to give the desktop the race fan-out.

## 5. Guardrails carried over from IMPS-PLAN

The runner pushes, never the worker. No GitHub token in the worker. When one consolidated fix resolves multiple issues, include a `Closes #n` reference for every issue in the PR body (one closing keyword per issue), or record an explicit post-merge reconciliation step for issues that cannot be linked to that PR. Deny paths (`.github/workflows`, `.env*`, auth/billing). Diff cap. gitleaks. A branch ruleset means nothing auto-merges. 9router fallback gate: if a served `model` isn't what the run asked for, that run is held, not judged.
# IMP 302 placeholder
