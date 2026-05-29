# Changelog

Notable additions and changes to this repository.

---

## [Unreleased]

### Added
- `CLOUD/aws/examples.py` — boto3 examples for EC2, S3, IAM, SSM, CloudWatch, Lambda, RDS, ECS, CloudFormation, Route53
- `SAAS/github/examples.py` — GitHub REST API examples: repos, issues, PRs, Actions, orgs, webhooks
- `SAAS/datadog/examples.py` — Datadog API examples: metrics, monitors, dashboards, incidents, logs, downtimes
- `SAAS/slack/examples.py` — Slack Bot API examples: messages, channels, users, reactions, files, webhooks
- `SAAS/pagerduty/examples.py` — PagerDuty REST + Events API v2 examples
- `atlassian/` — Full Atlassian Cloud suite examples (Jira, Confluence, Bitbucket, Statuspage) with shared client and validator
- `IAS/ubuntu-userdata.sh` — Ubuntu 22.04 EC2 bootstrap with Docker, CloudWatch, sysctl hardening
- `IAS/windows-userdata.ps1` — Windows Server 2022 EC2 bootstrap with Chocolatey, IIS, CloudWatch, TLS hardening
- `git/cleanup-branches.ps1` — Multi-repo merged branch cleanup utility
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
