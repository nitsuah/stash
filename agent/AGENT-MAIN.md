# Autonomous Agent Delivery Flow

> 🧭 [[VAULT-MAP|Vault Map]] (latest notes, reports, repo and project hubs) · [[README|Vault README]] · [[projects/scope|Scope]] · [[REPO-README]]

This document defines the happy path for running agents autonomously against a repository in the product delivery pipeline.

## Agent Run Order (Happy Path)

1. **[[prompts/PMO|PMO]]**
   - Audit the repository, update ROADMAP/TASKS, and define/approve the implementation brief.
   - Output: Updated planning docs and a clear implementation brief (handoff artifact).

2. **[[prompts/OPS|DevOps]]**
   - Prepare infrastructure, CI/CD, and delivery environment.
   - **MANDATORY:** Create and switch to a new delivery branch before making any codebase edits.
   - Output: Ready-to-implement branch, validated environment, and updated status.

3. **[[prompts/ENG|Software Engineer]]**
   - Implement features, bugfixes, or refactors as defined in the brief.
   - **MANDATORY:** All codebase changes must be committed to the delivery branch. Do not add new MDs unless required by acceptance criteria—update only existing relevant MDs (e.g., README, ROADMAP, TASKS).
   - Output: Code changes, tests, and documentation updates on the delivery branch.

4. **[[prompts/QA|QA]]**
   - Validate delivered work against acceptance criteria, tests, and documentation.
   - Output: QA report with pass/fail, defects, and improvement suggestions (in existing relevant MDs if required).

5. **[[prompts/Oncall|Oncall]]** (as needed)
   - Handle incidents, user feedback, and urgent triage during or after QA.
   - Output: Incident reports, user feedback summaries, and routed action items.

6. **Loop**
   - PMO reviews QA/Oncall findings, updates plans, and the cycle repeats for new work or closes out if complete.
   - **MANDATORY:** When work is complete, open a pull request from the delivery branch to the default branch. Do not leave branches unmerged.

---

## Handoff Artifacts

- Implementation brief (from [[prompts/PMO|PMO]])
- Delivery branch and environment (from [[prompts/OPS|DevOps]])
- Code, tests, and docs (from [[prompts/ENG|Software Engineer]])
- QA report (from [[prompts/QA|QA]])
- Incident/feedback report (from [[prompts/Oncall|Oncall]])

## Supporting Agents

[[prompts/AUTO|Automation]] and [[prompts/Growth|Growth]] agents run in parallel at any stage. [[prompts/LOC|LOC]], [[prompts/MINI|MINI]], [[prompts/TEST|Test]], and [[prompts/CLEANUP|Cleanup]] agents apply within individual repos as needed.

---

## Autonomous Agent Guidance

- Each agent must respect and update handoff artifacts.
- **Agents must create a new branch before any codebase edits and must open a pull request when work is complete.**
- **Close the tracked item in the same PR, in this order** (week-sotu and vigil read TASKS.md from `main`, so an unmarked item keeps showing as open work):
  1. Finish the code and tests.
  2. Before the **last** push, update the docs in the same branch: mark the `TASKS.md` item `- [x]` with a one-line `Done <date>: <what> (PR #n)` note (or record partial progress), tick or condense the matching `ROADMAP.md` line, add a `CHANGELOG.md` Unreleased line, and fix `README.md` / `FEATURES.md` if the change alters what they claim. Findings-ledger rows too.
  3. Commit and push, then open the PR. Say in its description which items it closes.
  4. **Pre-merge check**, next to CI and review threads: `git diff origin/main...HEAD --stat` must include the tracking docs whenever the PR completes a tracked item. If it doesn't, add the docs commit before merging. Never merge first and "follow up with a docs PR"; that's how stash#158/#159 and avatar#35 left finished work open (2026-09-30).
- **A docs-only status PR changes status, nothing else.** When you do have to close items after the fact, touch only the lines for the items you cite (tick, `Done` note, PR link). Don't add, reword, reorder or delete other items, and don't regenerate the file from a template. stash#160 did, and it invented six tasks, garbled two and dropped their originals (2026-09-29).
- **Never push to a merged PR's branch.** Before pushing a follow-up commit to an existing PR branch, run `gh pr view <branch> --json state -q .state`. If it prints `MERGED` or `CLOSED`, branch again from an up-to-date default branch, cherry-pick the new commits, and open a new PR that links the old one. A push to a merged branch strands the commits (it happened after stash#141).
- Agents should not proceed to the next step until the previous agent’s outputs are complete and validated.
- The loop continues until all acceptance criteria are met and no critical issues remain.
- This flow can be run in parallel across multiple repositories, but only one agent should own a given file/branch at a time.

---

## Example Invocation

> "Run the autonomous agent flow for [repo] using AGENT-MAIN.md as the process guide."

This will:

- Start with PMO audit and planning
- Proceed through DevOps, Software Engineer, QA, and Oncall as needed
- Loop until the work is complete and validated

---

## TASK/ROADMAP-Driven Agent Flow

**All agents must follow the [prompts/1FLOW.md](prompts/1FLOW.md) workflow:**

- Always begin by parsing TASKS.md and ROADMAP.md
- Select the next actionable item(s) based on priority and status
- **Create and switch to a new branch before any codebase edits.**
- **Commit all codebase changes to the branch.**
- **Open a pull request to the default branch when work is complete.**
- Create/update handoff artifacts and branches accordingly
- Run the full agent delivery loop for each item
- Repeat until backlog is clear or paused
