# RSI

> Monthly self-improvement cycle for the *real* Claude routine stack (scheduled tasks, skills, memory) — not the simulated product pipeline; see [[AUTO]] for that. Reads [[USAGE|the usage report]] and [[PMO|the PMO audit]], diagnoses recurring problems in your actual routines, and applies fixes with full PMO-style PR governance.

**Status:** created 2026-09-16 following the routine-pipeline audit. Scope was explicitly confirmed by the user as **full auto-PR privileges** — same standing as [[PMO]]: this can open PRs across owned repos and edit scheduled-task prompts/memory files on its own, unattended. Read this whole file before running — it is the highest-autonomy routine in the stack.

## Mission

Keep the Claude Code routine stack healthy and improving month over month, using evidence from actual run history — never guesses.

## Inputs (read all before acting)

1. This month's `stash/agent/reports/usage-report-<YYYY-MM>.md` (produced by [[USAGE]] earlier the same cycle — if missing, run its steps yourself first).
2. This month's `stash/agent/reports/pmo-audit-<YYYY-MM-DD>.md` (produced by [[PMO]]).
3. `mcp__scheduled-tasks__list_scheduled_tasks` + `list_task_runs` for every task — live current state, not the reports' snapshot.
4. `daily-git-sync.log` and `stale-worktrees.log` tails.
5. `agent/projects/scope.md` — the canonical repo registry (added 2026-09-16). Cross-check it against `gh repo list nitsuah` / `gh repo list Nitsuah-Labs` each cycle: flag any repo that appeared/disappeared/changed visibility since scope.md was last touched, and flag any of `DAILY.md`/`PMO.md`/`METRICS.md`/the `monthly-pmo-audit` scheduled-task wrapper whose cached inline repo list has drifted from scope.md's Tracked table (they're meant to be synced manually until every routine reads scope.md live — see below).
6. Any `stash/agent/reports/routine-run-findings-<YYYY-MM-DD>.md` from this cycle. Manual catch-up and debug sessions write cited findings there. Example, 2026-09-24: serialize quota use, read-only cloud routines escalate to push access, the obn weekly pair is disconnected, daily-repo-sync never commits its stash writes. Treat each item as evidence to verify, not as a pre-approved change.
7. `stash/agent/reports/findings-ledger.md` and the latest `tire-kick-<date>.md` (from [[TIRE]], run on the 28th). Its **Aging** section is your loop-health metric. An item open more than 21 days, or with `Seen` of 3 or more, means a routine isn't closing the loop: work out which routine should have acted (TIRE for `quick`, PMO for `pmo`) and fix that routine. Items classed `routine` are yours to fix directly.

## Artifacts & cycles — what reads what, so nothing silently drifts

Before making changes, understand the full input/output graph. Verify it's still accurate each cycle — routines get added, and this map goes stale exactly like everything else in this stack.

**Substrate:** `agent/projects/scope.md` is the one file everything else should key off for "which repos are in scope." `LOC.md`, `MINI.md`, and three cloud routines (`stale-worktrees`, `vuln-patcher`, `gh-overseer`) already read it live (fixed 2026-09-16). `DAILY.md`, `METRICS.md`, and the `monthly-pmo-audit` scheduled-task wrapper still carry a manually-synced cached copy of the same list instead of reading scope.md live — that's real drift risk, and a good candidate for RSI to actually close out in a future cycle (replace the cached list with a live read) rather than just re-verifying the cache matches by hand every month.

**Stage 1 (sync) →Stage 2 (audit) → Stage 3 (notes/reports) → Stage 4 (report/govern)** — see the 2026-09-16 audit artifact for the full pipeline diagram. Concretely, per routine:

| Routine | Reads | Writes |
|---|---|---|
| `daily-repo-sync` (local, runs [[DAILY]]) | scope.md (cached), each tracked repo's git state | `daily-git-sync.log`, `stale-worktrees.log`, `obn-repo.log`, `obn-review.log`, `agent/repos/**`, `agent/notes/<date>.md` + Mon/Sat `agent/notes/<YYYY>-W<ww>.md` (PR, auto-merges the *previous* day's note once reviewed) |
| `monthly-pmo-audit` (local, runs [[PMO]]) | scope.md (cached), each tracked repo's docs | per-repo TASKS/ROADMAP/METRICS.md (PR), `agent/repos/<repo>.md`, `pmo-audit-<date>.md` |
| `metrics` (cloud, runs [[METRICS]]) | scope.md (live), `METRICS.md` | per-target-repo METRICS.md (PR, auto-merge on green), `metrics-<date>.md` (PR to stash) |
| `week-eng-loc` (cloud, Mon 17:00 UTC, runs `LOC.md`) | scope.md (live); `git clone --depth 1` only; skips repos whose HEAD matches the last report's `HEAD:` line (2026-09-25) | `agent/reports/eng-loc-<repo>-<date>.md` (PR) |
| `week-eng-mini` (cloud, Wed 18:00 UTC since 2026-09-24, runs `MINI.md`) | scope.md (live); `git clone --depth 1` only; same HEAD-SHA gate (2026-09-25) | `agent/reports/eng-mini-<repo>-<date>.md` (PR) |
| ~~`week-obn-notes` / `week-obn-review` (cloud)~~ | — | **Disabled 2026-09-24.** Weekly note (Mon) and week review (Sat) now run inside `daily-repo-sync` (DAILY.md step 4) and ship in that day's daily-note PR, because the cloud versions' PRs were never merged, which broke the Mon → Fri → Mon chain |
| `week-obn-import` (cloud, **weekly Mon 10:00 UTC** since 2026-09-24; was daily) | stash on GitHub | `agent/reports/cloud/obn-import/<date>.md` (PR, auto-merged on green) |
| `stale-worktrees` / `vuln-patcher` / `gh-overseer` (cloud) | scope.md (live, fixed 2026-09-16) | advisory report only, no writes |
| `import-memory` (cloud) | `agent/notes`, `agent/reports`, `agent/prompts`, `agent/repos`, `agent/jobs` | advisory report only |
| [[USAGE]] (local) | Claude session/task history, git log across scope.md repos | `usage-report-<month>.md` |
| `monthly-tire-kick` (local, runs [[TIRE]], 28th) | every report in `agent/reports/**` since last intake, daily notes' `## Notes` (`agent/notes/`), scope.md (live) | `findings-ledger.md`, `tire-kick-<date>.md` (stash PR, self-merge on green), `tire/<repo>/*` fix PRs (≤5/run) |
| RSI itself | inputs 1-7 above | routine prompts, memory files, `rsi-changes.log`, `rsi-report-<month>.md`, product-repo PRs |

**Known gap, not yet RSI's to fix alone:** several cloud routines (`obn-weekly`, `stale-worktrees`, `vuln-patcher`, `gh-overseer`, `daily-git-sync`, `eng-loc`, `eng-mini`) each have a same-named **account-level claude.ai skill** (`ListSkills`/`SearchSkills`) that describes a different, more elaborate, not-actually-wired-up system — "Odysseus notes," an "Overseer app DB," `config/*.toml` files, a `scope.md` meant for *local* git worktrees rather than this cloud setup. Every observed run has correctly recognized the mismatch and ignored the skill in favor of the routine's own prompt — but that's the model's judgment call each time, not a guarantee. If a future run ever follows one of those skills instead of the real task, that's the root cause to check first. Worth a real decision eventually (retire the mismatched skills, or actually build what they describe) — flag it in the monthly report if it keeps coming up, don't silently fix it by deleting account-level skills unattended.

## What it's allowed to touch, and how

**Scope, as of 2026-09-16: "all routines, and anything in `C:\Users\ajhar\code` or our claude config."** That's broader than a typical audit bot — it explicitly includes both routine systems (not just the local ones):

- **Local scheduled tasks** (`~/.claude/scheduled-tasks/*/SKILL.md`, via `mcp__scheduled-tasks`).
- **Cloud routines** (`RemoteTrigger` — the ~20 routines at claude.ai/code/routines: obn-repo, obn-notes, obn-weekly, obn-review, daily-git-sync, stale-worktrees, metrics, eng-loc, eng-mini, vuln-patcher, gh-overseer, morning, job-evaluator, lead-finder, outreach-writer, application-tracker, Email triage, Weekday PR review, import-memory, financial-summary, plus whatever exists when RSI runs — call `RemoteTrigger {action:"list"}` fresh each cycle rather than trusting this list). **As of 2026-09-25 `list` returns only the newest 20 triggers and ignores the cursor**, and those 20 are all disabled one-shot "Re-check PR" reminders. Get recurring IDs from `agent/logs/rsi-changes.log`, the `reference-cloud-routine-ids` memory, or `search_session_transcripts`, then `get` each one. These are NOT covered by "anything in `C:\Users\ajhar\code`" since they live in Anthropic's cloud, not on disk — but the user's instruction named "all routines" explicitly, so they're in scope for RSI regardless.
- Anything under `C:\Users\ajhar\code` (all owned repos, `stash`, scripts, configs).
- "Our claude config" — `~/.claude/` broadly (skills, scheduled-tasks, mcp.json, memory).

**Product/infra repos (the 17 owned repos + stash):** full [[PMO]]-style governance. Branch named `rsi/<repo>/<theme>-<date>`, own PR via `gh pr create`, never commit to a default branch, never fabricate evidence.

**Scheduled-task prompts, cloud routine prompts, skill files, and this vault's `agent/prompts/*.md` files:** no PR mechanism exists for these, so instead of a PR gate — before editing, append a dated entry to `stash/agent/logs/rsi-changes.log` (`| target | change | reason | evidence |`), then make the edit (`update_scheduled_task`, `RemoteTrigger {action:"update"}`, or a direct file write). Every edit must cite the specific run(s) that justify it — e.g. "5/11 daily-repo-sync failures and 16/20 cloud routines' most recent runs were all instant `rate_limit: rejected (seven_day)` failures — this is volume, not a per-routine bug; recommend cutting/consolidating before retiming anything."

**Memory files (`~/.claude/projects/.../memory/*.md`):** may add or update entries to keep future sessions accurate. Never delete one outright — mark it superseded instead if it's wrong.

**Still disallowed even under the broadened scope:** touching credentials, secrets, `.env` files, or account/billing settings; disabling or deleting a routine (local or cloud) without flagging it in the report first and getting the user to confirm (same as the human-in-the-loop cleanup done in the 2026-09-16 audit — RSI can propose a cut, not execute one silently, given how much personal/job-search context lives in the cloud routine fleet); cloud routines cannot be deleted via API at all (per the `schedule` skill, only claude.ai/code/routines can delete one) — RSI can disable (`enabled:false`) or update, and must tell the user which ones it thinks should be deleted there.

## Steps

1. Read Inputs 1-5, and re-verify the Artifacts & cycles map above is still accurate (routines get added/removed — if it's drifted, fix the map in this same file before moving on).
2. Diagnose: for each task/skill with a failure pattern, a stale/dead state, a scope.md/cached-list mismatch, or a proposal in the usage report's "automation candidates," decide a concrete fix.
3. Apply fixes per the rules above, logging every change as you go.
4. Write `stash/agent/reports/rsi-report-<YYYY-MM>.md`: what changed and why (with evidence), PRs opened (with links), scheduled-task/memory edits made, and anything considered but declined, with the reason.
5. Report a short summary to the user at the end, same shape as [[PMO]]'s.

## Rules

- Evidence-only, same standard as [[PMO]] and [[METRICS]]: a change needs a cited run or log line, not a hunch.
- One theme per PR — don't bundle unrelated fixes.
- If two months in a row show no actionable evidence, say so plainly instead of inventing busywork.
- This file itself is fair game for RSI to improve, under the same logging rule as other prompt edits.
