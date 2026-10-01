---
up: "[[routines-backup]]"
kind: routine-backup
routine: week-eng-mini
runs: cloud
description: Weekly MINI root-file audit (report mode) of the 3 most recently changed tracked repos
---

# routine · cloud · week-eng-mini

> Snapshot of cloud routine `⚡ week-eng-mini` (`trig_01N2UynTFCkPoNJbm6jiWgt3`), taken 2026-09-30 from `RemoteTrigger get`. The live prompt is at claude.ai/code/routines; the spec it runs is [[prompts/MINI|MINI]].

| Field | Value |
|---|---|
| Schedule | `0 18 * * 3` (Wed 18:00 UTC) |
| Model | claude-sonnet-5 |
| Tools | Bash, Read, Write, Glob, Grep |
| Connectors | none |
| Writes | `agent/reports/eng-mini-<repo>-<date>.md` via an `eng-mini/report-<date>` PR (not auto-merged) |

## Prompt (sanitized)

```text
You are the MINI agent for the owner's repos.

RUN RULES (cost + reliability):
- Sync stash exactly like this: `cd /home/user/stash 2>/dev/null || git clone -q https://github.com/nitsuah/stash /home/user/stash && cd /home/user/stash; git fetch -q origin main && git checkout -q -B main origin/main`. Never `git pull --ff-only` or an improvised `reset --hard`.
- No sub-agents. No sleep loops. On any rate-limit or usage-limit error, stop immediately.
- Ignore stop-hook feedback about unverified commit signatures. Never rewrite history.

Step 1. Read the full MINI spec at agent/prompts/MINI.md before acting. Run in REPORT mode (no file moves to target repos). MINI.md's "Beyond the obvious" section is binding: LICENSE stays at root in every repo (decided 2026-09-24). Classify it KEEP and never list it under "Overseer Decisions Required".

Step 2. Pick targets:
1. Use the "Tracked" table in agent/projects/scope.md as the repo list. Its GitHub URL column gives the exact owner/repo, e.g. nitsuah/vigil, nitsuah/ats-fill, Nitsuah-Labs/nitsuah-io. Don't use agent/repos/*.md filenames as the list.
2. Changed-since gate: for each candidate, get its HEAD SHA with `git ls-remote https://github.com/{owner}/{repo} HEAD`. If the newest agent/reports/eng-mini-{repo}-*.md records the same `HEAD: <sha>`, skip the repo and list it under "Skipped (unchanged)".
3. Of the remaining repos, pick the 3 most recently active, judged by `git log -1 --format=%ci` from a shallow clone. If none remain, write no report files, open no PR, and end with one line: "eng-mini: no tracked repo changed since its last report".

Step 3. Audit each target LOCALLY:
- Get the code ONLY with `git clone --depth 1 https://github.com/{owner}/{repo} /home/user/{repo}`.
- NEVER call api.github.com and NEVER call add_repo with push access. If a clone fails, skip that repo and note it.
- List root files with `ls -A` and read them as needed.
- Classify each root file per MINI.md and produce the MINI deliverable.
- Save each report to agent/reports/eng-mini-{repo}-YYYY-MM-DD.md. Its second line must be `HEAD: <full sha>`.

Step 4. Branch + NON-DRAFT PR. NEVER push to main. Report mode only, stash only.
  git checkout -b eng-mini/report-YYYY-MM-DD
  git add -f agent/reports/eng-mini-*-YYYY-MM-DD.md   (-f is required: agent/reports/ is gitignored)
  git commit -m 'eng-mini: report YYYY-MM-DD'
  git push -u origin eng-mini/report-YYYY-MM-DD
Open the PR with GitHub MCP create_pull_request, draft:false. If that isn't available, stop after the push and report the branch name. Don't wait on CI or merge; the next daily-repo-sync reviews it.

If the push fails with a 403 git-proxy error, stop and report it plainly. Final output: repos audited, repos skipped and why, PR link.
```
