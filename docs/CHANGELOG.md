# Changelog

> 🧭 [stash](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · **Changelog** · [Metrics](./METRICS.md) <!-- nav -->

Notable additions and changes to this repository.

---

## [Unreleased]

### 2026-09-25 — vault hub links replace flat indexes

- Removed `agent/reports/INDEX.md`, `agent/projects/INDEX.md`, `agent/notes/INDEX.md` and `agent/REPOS-INDEX.md`. `build-vault-indexes.py` now writes prev/next nav lines into reports and dated notes, plus generated *Vault links* blocks in repo and project-folder hubs and a *Vault map* in `AGENT-MAIN.md`. New stub folder hubs: `projects/{CLEANUP,COSTS,LOC,MINI,TIRE,docs}.md`.
- `find-orphans.py` reports reachability from `AGENT-MAIN` and gains `--check`. Result: 406/422 notes reachable. The 16 unreachable notes are stale repo mirrors that the next sync fixes.
- `check-generated-diff.py` replaces DAILY's path allowlist for auto-merging `obn:` PRs.
- `agent/README.md` documents the linking conventions. `prompts/DAILY.md` is updated to match.

### 2026-09-24 — `pmo-ff` 2027 planning reset

- `agent/scripts/sync-repos.ps1` now mirrors `docs/` recursively (subfolder paths preserved, so upstream breadcrumb links such as `../../README.md` resolve in the vault) and gains an opt-in `-Prune` switch for stale mirror copies.
- `agent/scripts/find-orphans.py` — vault orphan finder; baseline 486 notes / 241 orphans.
- `agent/REPOS-INDEX.md` — repo docs hub (outside `agent/repos/`, which the sync rewrites) linked from `AGENT-MAIN.md`.
- `agent/reports/pmo-ff-2026-09-24.md` — cross-repo summary of the 16 upstream `pmo-ff` PRs and next week's vault plan.
- Planning docs: completed 2026 items condensed into FEATURES/CHANGELOG, open 2026 Q3/Q4 items carried into 2027 Q1, breadcrumb navigation + README docs index added.

### Added
- `cloud/aws/examples.py` — boto3 examples for EC2, S3, IAM, SSM, CloudWatch, Lambda, RDS, ECS, CloudFormation, Route53
- `SAAS/github/examples.py` — GitHub REST API examples: repos, issues, PRs, Actions, orgs, webhooks
- `SAAS/datadog/examples.py` — Datadog API examples: metrics, monitors, dashboards, incidents, logs, downtimes
- `SAAS/slack/examples.py` — Slack Bot API examples: messages, channels, users, reactions, files, webhooks
- `SAAS/pagerduty/examples.py` — PagerDuty REST + Events API v2 examples
- `atlassian/` — Full Atlassian Cloud suite examples (Jira, Confluence, Bitbucket, Statuspage) with shared client and validator
- `cloud/iac/ubuntu-userdata.sh` — Ubuntu 22.04 EC2 bootstrap with Docker, CloudWatch, sysctl hardening
- `cloud/iac/windows-userdata.ps1` — Windows Server 2022 EC2 bootstrap with Chocolatey, IIS, CloudWatch, TLS hardening
- `git/cleanup-branches.ps1` — Multi-repo merged branch cleanup utility
- `git/sync-fork.ps1` — Fast-forward-only fork + local clone sync from upstream, with `-Install` scheduled task
- `agent/prompts/SECURITY.md` — Open-source security reconciliation playbook (audit matrix, negative-control tests, live before/after, private disclosure, CI gates, Windows/Docker pitfalls)
- `agent/` — Personal agent system (CFO, Career, Builder) and full product delivery pipeline (PMO → DevOps → QA)
- `projects/auto/` — Single-page car project board (HTML + localStorage)

### Changed
- `README.md` — Full rewrite; each section links to folder-level READMEs
- `.github/copilot-instructions.md` — Updated to reflect actual stack (Python, PowerShell, Bash, VBA, Groovy)
- `windows/bat/ldap-search-users.bat` — Expanded from one line to full set of LDAP search examples
- `projects/resume/` — Sanitized MNPI, internal tool names, employee PII, internal URLs/project keys

### Removed
- `ias/` (lowercase) — malformed scratchpad duplicate of `IAS/` scripts
- `projects/resume/friends/` — PII removed

---

## [0.1.0] — 2018

### Added
- Initial project structure: VBA/Access tools (Remora, Sampler, VMT)
- Power Failure Alarm circuit design
- Windows PowerShell and batch utilities
- Resume project data

[Unreleased]: https://github.com/nitsuah/stash/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/nitsuah/stash/releases/tag/v0.1.0
