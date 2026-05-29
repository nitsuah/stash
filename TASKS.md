# Tasks

Last Updated: 2026-05-29

## Done

- [x] Re-align planning docs to repository reality.
  - README, CHANGELOG, CONTRIBUTING, SECURITY, FEATURES, ARCHITECTURE all rewritten to match actual repo.

- [x] Sensitive-data and hardcoded-hostname scan.
  - NDA/IP/MNPI pass completed: financials stripped, employee names generalized, internal URLs/keys removed, `friends/` deleted.

- [x] Open-source safety sanitization for docs/examples.
  - coinbase.json, projects.json, resume.json, resume-ai.json, bb.json, ldap-search-users.bat all sanitized.

- [x] Standardize file naming in infrastructure assets.
  - `ias/Windows-userdata..yml` (double-dot, malformed) removed along with entire `ias/` scratchpad folder.
  - Replaced by proper `cloud/iac/ubuntu-userdata.sh` and `cloud/iac/windows-userdata.ps1`.

- [x] Security checklist documented.
  - Moved to `agent/docs/SECURITY_CHECKLIST.md`. SECURITY.md updated with real contact and guidance.

- [x] Add script operations runbook.
  - Closed: runbook-style docs belong inline — argparse `--help`, docstrings, and per-folder READMEs.
  - Each script family has a README. Python scripts have `--help` via argparse. PowerShell scripts have `param()` with descriptions.

- [x] Add API examples across Atlassian, SaaS, and Cloud.
  - Atlassian (Jira, Confluence, Bitbucket, Statuspage), PagerDuty, Slack, GitHub, Datadog, AWS boto3.

- [x] Consolidate IAS into cloud/.
  - Scripts moved to `cloud/iac/`. IAS section removed from root README.

- [x] Fix stale `develop` branch image URLs across project READMEs.
  - pfa, remora, sampler all updated to `main`.

- [x] Update .github/copilot-instructions.md.
  - Rewritten for current stack (Python, PowerShell, Bash, VBA, Groovy).


## In Progress


## Todo

- [ ] Fill out ARCHITECTURE.md module map.
  - Priority: P1
  - Type: Docs
  - Acceptance Criteria: module boundaries, execution context, dependency notes, risk callouts for destructive scripts.

- [ ] SSO/Identity Management examples.
  - Priority: P2
  - Type: Examples
  - Candidates: ADFS integration, SAML/SSO onramp, Okta + AWS SSO group management, Atlassian + Okta, OAuth/mTLS.

- [ ] Frontend examples (from nitsuah.io stack).
  - Priority: P2
  - Type: Examples
  - Candidates: React/Next.js, Svelte/SvelteKit, Vue/Nuxt.js components.

- [ ] Backend API examples.
  - Priority: P2
  - Type: Examples
  - Candidates: Node.js/Express, Python/Flask, Go/Gin, Java/Spring Boot.

- [ ] Database schema examples.
  - Priority: P3
  - Type: Examples
  - Candidates: PostgreSQL, MySQL, MongoDB.

- [ ] Cloud cost management examples.
  - Priority: P3
  - Type: Examples
  - Candidates: Cloudability, CloudHealth, CloudZero, Kubecost APIs.

- [ ] SaaS inventory audit examples.
  - Priority: P3
  - Type: Examples
  - Candidates: Fortify-on-Demand, ZenGRC, Zylo.

- [ ] API.md decision record.
  - Priority: P3
  - Type: Docs
  - Note: This repo contains scripts and examples, not a hosted API. Decision record confirms no external contracts exist.


## Audit Notes

- Docker-first execution path not available (`Dockerfile` / `docker-compose.yml` absent).
- `.github/ISSUE_TEMPLATE` and `.github/pull_request_template.md` present and usable.
- Agent pipeline branch/PR conventions: `pmo/`, `delivery/`, `qa/` prefixes per `agent/README.md`.
