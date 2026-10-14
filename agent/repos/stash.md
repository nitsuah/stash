---
kind: repo-hub
repo: stash
---

# stash

> Reviewed: 2026-10-10

## Overview

Austin J. Hardy's technical evolution archive — 15+ years of enterprise automation tools and developer productivity scripts. Covers VBA/Access projects (Remora PAM, Sampler, VMT), Python API examples (Atlassian, SaaS platforms, AWS boto3, SSO/OIDC), PowerShell Windows automation, backend REST reference implementations (Flask, Express), database DDL (PostgreSQL, MongoDB), role-based AI agent system prompts, and git utilities.

## Current Goals / Roadmap Focus

**Q1–Q2 2026:** ✅ Completed — planning integrity reset, documentation baseline, security hygiene pass, open-source sanitization, backend/database/SSO examples, IaC consolidation

**Q3 2026 (in progress):**
- [x] Complete the Jira Runbook — `atlassian/jira/RUNBOOK.md` filled in and verified complete (all 7 scripts covered) as of the 2026-09-02 audit
- [x] Per-directory READMEs audit — all top-level directories and all 7 `projects/*` subdirectories now have a README.md; `projects/README.md` added as the missing index
- [ ] Naming and consistency cleanup — partial progress: 14 broken cross-references from the `IAS/` → `cloud/iac/` and `CLOUD/` → `cloud/aws/` reorganization fixed in the 2026-09-02 audit (including a case-sensitivity bug that only broke on Linux/Mac); a full repo-wide filename-normalization pass is still open
- [ ] Lightweight validation harness for critical scripts (exploratory; dry-run smoke checks)

**Q4 2026 (exploratory/planned):**
- Cross-repo automation catalog (discoverable script capabilities + ownership metadata)
- Operational metrics maturity (measurable quality metrics, not placeholders)
- Script dependency graph (Mermaid diagram from imports/source/require calls; CI artifact)
- Dry-run audit log (structured JSON summary of planned changes for high-impact scripts)
- Python linting CI (`ruff`) and PowerShell linting CI (`PSScriptAnalyzer`) — newly added to ROADMAP.md

**2027 Q1+ (backlog):** Modernize VBA/Access tools (Remora, Sampler, VMT migration paths), add pytest coverage to Python examples, frontend examples, cloud cost management examples, SaaS inventory audit examples

**Note from overseer:** Stash is being deprioritized — overseer TASKS P1 item to mark repo private, block PRs, add sanitization checklist.

## Open P0/P1 Tasks

- [x] **P1 (added 2026-10-09, done same day)** Journeys rollout pilot on fire. fire#176 merged after nitsuah/.github#19, and the first `workflow_dispatch` run passed and created `bot/journeys`. Still needed: "Allow GitHub Actions to create and approve pull requests" in fire's Actions settings, for visual-docs. Next in the rollout (P2): vigil journeys, in nitsuah/vigil#282 (6 journeys, 12 baselines, soak 54/54; review pass filed vigil#275–#279 and #281). Earlier progress note: review pass filed fire#166–#175, 7 journeys / 19 baselines, soak 70/70, PR open on fire. Remaining: merge it after nitsuah/.github#19, then one `workflow_dispatch` run to create `bot/journeys` and confirm the reporter. Shared harness (nitsuah/.github#19) and the 1FLOW/RSI wiring are done.
- [ ] **P1 (on hold since 2026-09-26)** CI-generated diagrams and screenshots for app repos, auto-embedded in READMEs. Raised from P2; parked as the next portfolio initiative, to be built into vigil once the MCP rollup and PMO UI ship.

The Vault scorecard follow-ups were all closed 2026-09-26/27 (vigil MCP connected, Stale hubs line, failed-run reporting, `title:` frontmatter on mirrors). Highest-priority open items otherwise (P2) from TASKS.md:

- [ ] **P2** Document the VBA source files inside Remora, Sampler, VMT more precisely
- [ ] **P2** Add Python linting via `ruff` in GitHub Actions
- [ ] **P2** Add PowerShell linting via PSScriptAnalyzer in CI
- [ ] **P2** vigil `get_open_tasks` skips 6 tracked repos and drops line refs/acceptance criteria (fix belongs in nitsuah/vigil; SOTU gap-fills meanwhile)
- [ ] **P2** Frontend examples (React/Next.js, Svelte/SvelteKit, Vue/Nuxt.js)

Lower-priority (P3): cloud cost management examples, SaaS inventory audit examples, `API.md` decision record re-verification, Remora/Sampler modernization path evaluations.

## Blockers

- No Docker execution path (no Dockerfile/docker-compose.yml)
- Overseer P1 task: mark private + block PRs + sanitization (external governance item)

## Recent Changes

**2026-10-09 (later):** journeys page and `journeys-19s` spot added to stash Pages (`pages/journeys.html`, compose-only `promo/build.sh`); the Python example-file coverage P2 closed (Jira 84%, Bitbucket 82%, Confluence 72%, Statuspage 80%; 65 tests passing in Docker).

**2026-10-09:** stash#210 repointed SOTU and DAILY at `gh-vigil.netlify.app` (P1 closed) with a TASKS.md gap fill in `sotu.py`; #215 added the JOURNEYS playbook and wired `bot:journey` into 1FLOW/RSI; #216 closed the Atlassian smoke-tests and SaaS quick-start P2s.

**2026-09-25 vault overhaul (#139-#146):** flat INDEX files retired for generated hub links, mirror enrichment, `fix-doc-links.py`, CI vault graph check, properties + Bases, link suggestions, aliases, topic hubs. TASKS.md's old Vault P1 (prune + stale mirrors) is closed by that work; its new "Vault scorecard follow-ups" section (overall 8.3/10) lists P2/P3 items by owner (vigil / routine / stash). Cross-repo task rollup, one of those P2s, shipped in vigil the same day.

**2026-09-02 audit (most recent activity):**
- Fixed 14 broken cross-references left over from the `IAS/` → `cloud/iac/` and `CLOUD/` → `cloud/aws/` reorganization, across docs/CHANGELOG.md, .github/copilot-instructions.md, agent/repos/stash.md, cloud/README.md, and cloud/aws|iac scripts — the `CLOUD/` casing was a live bug that broke on case-sensitive filesystems
- `atlassian/jira/RUNBOOK.md` verified complete (all 7 scripts covered); one stale env-var reference fixed (`JIRA_URL` → `JIRA_HOST`)
- `projects/README.md` added — closes the last gap in the per-directory README audit
- `projects/resume/README.md` expanded with last-updated date and schema note

**Earlier (still unreleased/undated in CHANGELOG.md):**
- `cloud/aws/examples.py` — boto3 examples (EC2, S3, IAM, SSM, CloudWatch, Lambda, RDS, ECS, CloudFormation, Route53)
- `SAAS/github/examples.py`, `SAAS/datadog/examples.py`, `SAAS/slack/examples.py`, `SAAS/pagerduty/examples.py`
- `atlassian/` — Jira, Confluence, Bitbucket, Statuspage API examples with shared client + validator
- `cloud/iac/` — Ubuntu + Windows EC2 UserData bootstrap scripts
- `git/cleanup-branches.ps1` — multi-repo merged branch cleanup
- `agent/` — personal agent system (CFO, Career, Builder) + product delivery pipeline (PMO → DevOps → QA)
- `projects/auto/` — single-page car project board
- `projects/resume/` — sanitized (MNPI, internal tool names, employee PII removed)
- `README.md` full rewrite; `.github/copilot-instructions.md` updated for actual stack

<!-- vault-links:start -->
## Vault links

_Generated by `scripts/build-vault-indexes.py`; edits inside this block are overwritten._

- Docs: [[repos/stash/README|README]] (every doc hangs off its Docs Index)
- Overview: [[projects/KB/stash-overview|KB overview]]
- Latest LOC report: [[reports/eng-loc-stash-2026-10-08|2026-10-08]] (older ones chain from it)
- Latest MINI report: [[reports/eng-mini-stash-2026-10-07|2026-10-07]] (older ones chain from it)
<!-- vault-links:end -->
