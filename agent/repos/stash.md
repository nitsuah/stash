# stash

> Reviewed: 2026-09-11

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

No active P0/P1 tasks in this repo — work is in low-contribution mode. Highest-priority open items (P2) from TASKS.md:

- [ ] **P2** Add usage examples to each SaaS script header (`SAAS/okta`, `SAAS/servicenow`, `SAAS/pagerduty`)
- [ ] **P2** Document the VBA source files inside Remora, Sampler, VMT more precisely
- [ ] **P2** Add Python linting via `ruff` in GitHub Actions
- [ ] **P2** Add PowerShell linting via PSScriptAnalyzer in CI
- [ ] **P2** Add `pytest` smoke tests for at least one Python example module (candidate: `atlassian/jira/examples.py`)
- [ ] **P2** Frontend examples (React/Next.js, Svelte/SvelteKit, Vue/Nuxt.js)

Lower-priority (P3): cloud cost management examples, SaaS inventory audit examples, `API.md` decision record re-verification, Remora/Sampler modernization path evaluations.

## Blockers

- No Docker execution path (no Dockerfile/docker-compose.yml)
- Overseer P1 task: mark private + block PRs + sanitization (external governance item)

## Recent Changes

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
