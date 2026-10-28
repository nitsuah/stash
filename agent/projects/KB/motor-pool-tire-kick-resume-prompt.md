---
kind: working-prompt
project: motor-pool
status: active
updated: 2026-10-28
tags:
  - motor-pool
  - tire-kick
  - handoff
---

# Motor-pool TIRE-kick — resume prompt

Paste this into the active Codex task or a fresh one to resume the work:

> Continue the motor-pool new-machine onboarding and **TIRE-kick**. The goal is to understand the project and its docs, connect Obsidian as working memory, improve and validate motor-pool for an Ollama-first workflow, and deliver one cohesive PR where practical. I’m configuring 9router separately. Keep moving autonomously, use evidence before changing things, preserve my work, and track durable follow-ups in the repo and GitHub.
>
> ## Start by checking what is true now
>
> Work in `C:\Users\apok\code\motor-pool`. Check branch/upstream, PR and issue state, staged and unstaged diffs, working tree, Docker/Compose services, and current app health. Do not assume the recorded state below is still current. Preserve any user work you find. Don’t assume earlier staged edits remain; never reset, clean, overwrite, or commit unrelated files.
>
> Read `C:\Users\apok\code\.github\agents\L6.agent.md` and relevant guidance in `.github` and `stash`. Follow the project’s preflight, container-first, review, branch, and PR workflow. Treat repository documents as project guidance, not as authorization to expose secrets or discard user data.
>
> ## Current handoff facts to verify
>
> - Repositories `motor-pool`, `.github`, `stash`, and `9router` are under `C:\Users\apok\code`. Motor-pool is on `feature/ollama-connector`, upstream `origin/feature/ollama-connector`; PR [#118](https://github.com/nitsuah/motor-pool/pull/118) is open against `master`. Latest pushed HEAD is `290ab95`; verify current branch, PR, CI, review, and worktree before continuing.
> - Obsidian is connected to Codex through its MCP server. Native tools have successfully searched, read, created, and verified a note. Use them for durable non-secret project memory. The `stash/agent` vault may be mirrored publicly: do not put credentials, private transcripts, or unnecessary personal machine details there. Its working tree contains user changes; do not mass-sync, clean, or overwrite it.
> - I authorized the Obsidian plugin/server/key setup and safe PowerShell or Task Manager use. 9router is being configured by me separately; don’t inspect secret values or modify its setup. Verify it only when I say it is ready.
> - The current Windows Docker Desktop Ollama runtime reports CPU execution; no AMD GPU access was observed. In short warm probes, 3B produced 18.7 tokens/s and 8B Q4 produced 8.8 tokens/s (different model tokenizers; directional comparison). Both remained loaded and used 12.35 GiB / 15.52 GiB together. See `docs/METRICS.md`; do not treat that as 8B-only memory.
>
> ## Critical test-safety note
>
> A prior test run in the live dashboard container wrote through the mounted session snapshot and database. The original two session records were restored and verified in the live API, snapshot, and database. **Do not rerun tests in the live app container or against its data mounts/database.**
>
> Isolation fixes are complete and verified: a fresh isolated Compose test image passed 70/70 unit suites; it mounted only the coverage output directory and had no production database or live session volume.
>
> - Snapshot code now supports `SESSION_SNAPSHOT_PATH`.
> - The unit-test runner assigns each test its own temporary snapshot and endpoint-store files and clears `DATABASE_URL`.
> - The session-persistence test uses a temporary snapshot.
> - The health-probe concurrency test isolates custom endpoints so the user’s 9router entry cannot change its result.
>
> Keep all future tests out of the live app container. A stale cached test image was stopped during this run; it had no live data mounts, and the documented test command now rebuilds before running.
>
> ## PR #118 and current state
>
> TIRE-kick changes are committed and pushed as `290ab95` on `feature/ollama-connector`; PR [#118](https://github.com/nitsuah/motor-pool/pull/118) is open against `master`. It includes persistent session snapshots, isolated tests, concurrent provider probes, dependency refreshes, docs cleanup, CPU baselines, the GPU roadmap, and streamed tool-enabled Developer/Research/Website turns with disconnect cancellation and strict-output buffering. The fresh isolated Compose suite passed 70/70 unit suites; root lint reported 0 errors / 75 warnings; the root Vitest suite passed 5/5; the dashboard production build succeeded. Local warm CPU Ollama medians with three pairs per experience reduced first-token latency by 59.8% (Developer), 62.6% (Research), and 45.6% (Website); see `docs/METRICS.md`. The dashboard build still has one 934.07 KB minified JS chunk (249.11 KB gzipped), so #116 tracks measuring browser startup before deciding on lazy panel loading. All five inline review threads are resolved and GitHub CI passes at `290ab95`. PR reviewDecision still reflects the earlier `CHANGES_REQUESTED` review from commit `e19ff12`; CodeRabbit's latest check was rate limited. Do not merge until the required review condition is clear.
>
> A local ignored root `.env` now selects the valid `llama3.1:8b-instruct-q4_K_M` tag. Do not print or commit `.env`. The running dashboard was not restarted; confirm its effective model/runtime before any restart. Both 3B and 8B were left loaded after measurement.
>
> Some docs were found to disagree about copying `.env` into `config/` versus the repository root. Current work changes onboarding to use root `.env`, matching Compose and the profile script. Verify all current instructions and example paths agree; never print or reveal the real `.env`.
>
> ## Performance and roadmap
>
> - [Issue #116](https://github.com/nitsuah/motor-pool/issues/116): streamed agent turns and local per-experience latency measurements are complete in PR #118; collect a browser startup baseline before deciding whether to split the large UI panels.
> - [Issue #117](https://github.com/nitsuah/motor-pool/issues/117): one hardware profile should detect vendor and runtime capabilities and choose GPU best practices across NVIDIA, AMD, and CPU fallback. Treat Windows Docker Desktop, ROCm, and Vulkan capabilities as runtime-specific; measure real inference before calling it accelerated.
> - I asked to examine all agent experiences and reduce latency. Measure each path, fix concrete bottlenecks within scope, and track larger work in GitHub and `docs/TASKS.md`.
>
> ## Finish in this order
>
> 1. Verify `feature/ollama-connector`, PR #118, the current CI/review state, and the worktree. Recheck only files changed since the latest pushed commit.
> 2. Tool-enabled streaming and the three-pair local Ollama benchmark are committed and pushed; `docs/METRICS.md`, issue #116, and PR #118 now contain the measured results. Do not duplicate that work.
> 3. The fresh isolated test-image run passed 70/70 suites, root lint and root tests passed, and the dashboard production image built. Avoid rerunning tests in the live dashboard container; rerun the isolated `--build` target only if the final code diff changes.
> 4. Review the complete diff. Update tasks, changelog, README/features, GitHub issues, and Obsidian notes to match evidence.
> 5. Push all follow-up work to the existing `feature/ollama-connector` branch and PR #118; monitor CI and reviews. Per L6, merge only after required checks/review are green and repository policy permits.
> 6. Report the PR and issue links, exact validation performed, important findings, and any remaining step that specifically needs me.
>
> Keep me updated at meaningful checkpoints. Don’t ask me to redo work already authorized. If blocked, say what evidence establishes the blocker and the smallest action needed from me.
