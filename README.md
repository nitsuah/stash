# CodeStash

> Austin J. Hardy's technical evolution from VBA wizard to AI architect — 15+ years of enterprise automation and developer productivity innovation.

## Overview

This repository chronicles my technical journey from complex VBA automation systems to modern AI-driven developer productivity tools. Each project represents real-world solutions that have served thousands of engineers and operational staff across Netflix, Coinbase, Blackboard, and other enterprise environments.

**Technical Philosophy**: Build tools that eliminate manual toil, scale human capabilities, and empower teams to focus on high-value work through intelligent automation.

---

## Artifact Index

A searchable reference to every artifact in this repository, organized by category.

### VBA / Microsoft Access Tools

| Artifact | What It Does | Technology | When To Use | Requirements |
|----------|-------------|-----------|-------------|-------------|
| [Remora](projects/remora/) | Privileged Access Management (PAM) — stores user access lists, links to authorized signatory documents, generates audit reports, automates quarterly access review emails | Microsoft Access, Excel, VBA | SecOps/compliance teams running RBAC audits, federal compliance programs, quarterly access certifications | Microsoft Access, Excel; shared drive for artifact storage |
| [Sampler](projects/sampler/) | PDF random-sampling — selects a statistically valid random page sample from a multi-page PDF matching a target string; used for compliance document spot-checks | Microsoft Access, VBA, Win32 API, Adobe Acrobat | Audit sampling of large PDF document sets; compliance spot-check workflows | Microsoft Access, Adobe Acrobat Standard or Pro |
| [VMT](projects/vmt/) | Vulnerability Management Tool — joins IT asset inventory against CVE scan exports to produce prioritized remediation reports; tracks change requests and approval workflows | Microsoft Access, Excel, VBA | IT security teams tracking CVE remediation across enterprise infrastructure; change management workflows | Microsoft Access, Excel |
| [LDAP Cleanup (VBA)](windows/vba/ldap-search-cleanup.vb) | Strips `member:` attribute prefixes from an OU export to produce a clean username list for Office integration | VBA (Excel/Access) | Post-processing LDAP exports for import into Office tools | Excel or Access with VBA |

### PowerShell Scripts

| Artifact | What It Does | Technology | When To Use | Requirements |
|----------|-------------|-----------|-------------|-------------|
| [compress-logs-v02a.ps1](windows/pwsh/compress-logs-v02a.ps1) | Intelligent log compression — detects JBoss app servers, applies NTFS compression, enforces retention policies, reports space savings | PowerShell 5.1+ | Automated log archival on Windows servers; storage cost reduction; capacity planning | PowerShell 5.1+, NTFS volume |
| [detect-server-v03d.ps1](windows/pwsh/detect-server-v03d.ps1) | JVM server type detection — identifies JBoss installations, maps environment topology, validates configs | PowerShell 5.1+ | Migration prep; environment discovery; server inventory audits | PowerShell 5.1+, domain access |
| [ConvertCSV-ToExcel.ps1](windows/pwsh/ConvertCSV-ToExcel.ps1) | Batch CSV to Excel conversion with auto-formatting, header styling, data type detection, and proper COM lifecycle management | PowerShell 5.1+, Excel COM | Recurring report generation; converting data exports to formatted Excel for stakeholders | PowerShell 5.1+, Microsoft Excel installed |
| [cleanup-branches.ps1](git/cleanup-branches.ps1) | Multi-repo branch cleanup — scans all repos under a root path, prunes merged branches locally and from origin; supports `-DryRun` and `-Force` | PowerShell 5.1+, git | Workspace hygiene; cleaning up merged branches across many repos after sprint cycles | PowerShell 5.1+, git in PATH |

### Batch Scripts (Windows CMD)

| Artifact | What It Does | Technology | When To Use | Requirements |
|----------|-------------|-----------|-------------|-------------|
| [ldap-search-users.bat](windows/bat/ldap-search-users.bat) | LDAP user search — by email, username, group membership, disabled accounts, stale logins; full set of `dsquery`/`dsget` patterns | CMD batch, dsquery | AD user lookups, account status checks, group membership audits | Windows with AD RSAT tools |
| [ldap-search-cleanup.bat](windows/bat/ldap-search-cleanup.bat) | Strips `member:` prefixes from an OU export file to produce a clean plain-text username list | CMD batch | Processing `dsget` / `ldifde` output for downstream tools | Windows CMD |
| [run-logger.bat](windows/bat/run-logger.bat) | Wraps any batch script with timestamped log output | CMD batch | Adding structured logging to existing batch scripts without modifying them | Windows CMD |

### Atlassian Cloud API Examples

| Artifact | What It Does | Technology | When To Use | Requirements |
|----------|-------------|-----------|-------------|-------------|
| [jira/examples.py](atlassian/jira/examples.py) | Jira Software, JSM, Assets, Automation API examples — projects, issues, comments, transitions, service desks, AQL asset search, automation rule export | Python 3.10+, requests | Building Jira integrations; learning the REST API; scripting bulk Jira operations | `JIRA_EMAIL`, `JIRA_TOKEN`, `JIRA_URL` env vars |
| [confluence/examples.py](atlassian/confluence/examples.py) | Confluence Cloud API — spaces, pages, labels, CQL search, create/update/delete | Python 3.10+, requests | Automating Confluence documentation; content migration; bulk page management | Same Jira credentials (shared account) |
| [bitbucket/examples.py](atlassian/bitbucket/examples.py) | Bitbucket Cloud API — repos, branches, commits, PRs, pipelines, issues, webhooks | Python 3.10+, requests | CI/CD integrations; repo automation; pipeline triggers | `BITBUCKET_WORKSPACE`, `BITBUCKET_USERNAME`, `BITBUCKET_APP_PASSWORD` |
| [statuspage/examples.py](atlassian/statuspage/examples.py) | Atlassian Statuspage API — pages, components, incidents, scheduled maintenance | Python 3.10+, requests | Incident automation; maintenance window scheduling; status page management | `STATUSPAGE_API_KEY`, `STATUSPAGE_PAGE_ID` |
| [jira/validate_project.py](atlassian/jira/validate_project.py) | Jira project configuration validator — checks workflows, issue types, custom fields; full lifecycle test suite | Python 3.10+, requests | Validating Jira project setup before go-live; regression testing project configs | Jira credentials + `--project` flag |
| [jira/groovy/users.groovy](atlassian/jira/groovy/users.groovy) | ScriptRunner Groovy script — lists all Jira Server users | Groovy, ScriptRunner | Jira Server/DC user audits via ScriptRunner console | Jira Server/DC + ScriptRunner plugin |
| [jira/automation/](atlassian/jira/automation/) | Jira Automation rule templates — reopen-on-reply, set-parent-on-resolve | Jira Automation JSON | Importing pre-built automation rules into Jira projects | Jira Cloud with Automation |

### AWS / Cloud IaC

| Artifact | What It Does | Technology | When To Use | Requirements |
|----------|-------------|-----------|-------------|-------------|
| [cloud/aws/examples.py](cloud/aws/examples.py) | boto3 examples across 10 AWS services: EC2, S3, IAM, SSM Parameter Store, CloudWatch, Lambda, RDS, ECS, CloudFormation, Route53 | Python 3.10+, boto3 | Learning AWS SDK patterns; building AWS integrations; reference for common boto3 calls | `boto3`, `python-dotenv`; AWS credentials |
| [cloud/iac/ubuntu-userdata.sh](cloud/iac/ubuntu-userdata.sh) | EC2 UserData bootstrap for Ubuntu 22.04 — Docker, CloudWatch agent, sysctl hardening, SSM secret retrieval | Bash, EC2 UserData | Bootstrapping Ubuntu EC2 instances at launch; golden AMI alternatives | Attach as EC2 UserData at instance launch |
| [cloud/iac/windows-userdata.ps1](cloud/iac/windows-userdata.ps1) | EC2 UserData bootstrap for Windows Server 2022 — Chocolatey, IIS, CloudWatch agent, TLS/SMB hardening | PowerShell, EC2 UserData | Bootstrapping Windows Server EC2 instances at launch | Attach as EC2 UserData at instance launch |

### SaaS Operations Platform APIs

| Artifact | What It Does | Technology | When To Use | Requirements |
|----------|-------------|-----------|-------------|-------------|
| [SAAS/okta/examples.py](SAAS/okta/examples.py) | Okta API — users, groups, apps, MFA factors, system logs; full user lifecycle | Python 3.10+, requests | IAM automation; user provisioning/deprovisioning scripts; MFA reporting | `OKTA_DOMAIN`, `OKTA_API_TOKEN` |
| [SAAS/servicenow/examples.py](SAAS/servicenow/examples.py) | ServiceNow REST API — incidents, change requests, CMDB, catalog items, KB articles | Python 3.10+, requests | ITSM automation; incident creation from monitoring; change management scripts | `SERVICENOW_INSTANCE`, `SERVICENOW_USER`, `SERVICENOW_PASSWORD` |
| [SAAS/pagerduty/examples.py](SAAS/pagerduty/examples.py) | PagerDuty REST + Events API v2 — incidents, services, escalation policies, on-call schedules, alert ingestion | Python 3.10+, requests | On-call automation; alert routing; incident lifecycle scripts | `PAGERDUTY_API_KEY`, `PAGERDUTY_ROUTING_KEY` |
| [SAAS/slack/examples.py](SAAS/slack/examples.py) | Slack Bot API — messages, channels, users, reactions, file uploads, webhooks, pins | Python 3.10+, requests | Slack bot development; ChatOps workflows; notification automation | `SLACK_BOT_TOKEN`; required scopes listed in README |
| [SAAS/github/examples.py](SAAS/github/examples.py) | GitHub REST API v3 — repos, issues, PRs, Actions workflows, releases, org management, webhooks | Python 3.10+, requests | GitHub automation; workflow triggers; org reporting; PR/issue management | `GITHUB_TOKEN` |
| [SAAS/datadog/examples.py](SAAS/datadog/examples.py) | Datadog API v1/v2 — metrics, monitors, dashboards, incidents, log search, downtimes | Python 3.10+, requests | Observability automation; monitor management; metric submission; maintenance windows | `DATADOG_API_KEY`, `DATADOG_APP_KEY` |

### Backend Reference Implementations

| Artifact | What It Does | Technology | When To Use | Requirements |
|----------|-------------|-----------|-------------|-------------|
| [backend/flask/app.py](backend/flask/app.py) | Flask REST API — JWT auth, SQLAlchemy ORM, input validation, pagination; covers `/auth`, `/users`, `/items`, `/health` | Python 3.10+, Flask, SQLAlchemy | Reference implementation for Python REST APIs; cross-language comparison with Express | `flask`, `flask-sqlalchemy`, `flask-jwt-extended`, `marshmallow` |
| [backend/express/app.js](backend/express/app.js) | Express REST API — same surface as Flask: JWT auth, Sequelize ORM, validation, pagination | Node.js 18+, Express, Sequelize | Reference implementation for Node.js REST APIs; cross-language comparison with Flask | `npm install` in `backend/express/` |

### Database Reference Implementations

| Artifact | What It Does | Technology | When To Use | Requirements |
|----------|-------------|-----------|-------------|-------------|
| [database/postgres/schema.sql](database/postgres/schema.sql) | PostgreSQL schema DDL — enums, domains, RLS, partitioning, triggers, views, GIN/trigram indexes | PostgreSQL 14+ | Setting up a production-grade Postgres schema; learning advanced DDL patterns | PostgreSQL 14+ instance |
| [database/postgres/queries.sql](database/postgres/queries.sql) | Advanced Postgres query patterns — CTEs, window functions, JSONB, full-text search, keyset pagination, upsert, EXPLAIN ANALYZE | PostgreSQL 14+ | Query optimization; learning advanced SQL patterns; interview prep | PostgreSQL 14+ + schema applied |
| [database/mongodb/examples.py](database/mongodb/examples.py) | MongoDB PyMongo examples — schema validation, indexes, aggregation pipeline, multi-doc transactions, text search | Python 3.10+, pymongo | Learning MongoDB patterns; building PyMongo integrations; aggregation pipeline reference | `pymongo`, MongoDB 5+ (local or Atlas) |

### SSO / Identity Examples

| Artifact | What It Does | Technology | When To Use | Requirements |
|----------|-------------|-----------|-------------|-------------|
| [sso/oauth2.py](sso/oauth2.py) | OAuth 2.0 / OIDC flows — auth code + PKCE, token exchange, refresh, introspection, client credentials, UserInfo | Python 3.10+, requests | Building OIDC integrations; learning OAuth flows; token management utilities | `SSO_CLIENT_ID`, `SSO_CLIENT_SECRET`, `SSO_ISSUER`, `SSO_REDIRECT_URI` |
| [sso/saml.py](sso/saml.py) | SAML 2.0 — IdP metadata parsing, AuthnRequest, SAMLResponse attribute extraction, SP metadata generation | Python 3.10+, requests | SP-initiated SSO integrations with Okta/ADFS/Azure AD; SAML debugging | `SAML_SP_ENTITY_ID`, `SAML_SP_ACS_URL`, `SAML_IDP_METADATA_URL` |
| [sso/aws_sso.py](sso/aws_sso.py) | AWS IAM Identity Center — device auth flow, list accounts/roles, get temporary credentials, Okta SCIM provisioning pattern | Python 3.10+, boto3 | AWS SSO automation; multi-account access; Okta→AWS user sync | `AWS_SSO_START_URL`, `AWS_SSO_REGION` |

### AI Agent System

| Artifact | What It Does | Technology | When To Use | Requirements |
|----------|-------------|-----------|-------------|-------------|
| [agent/projects/Finance.md](agent/projects/Finance.md) | CFO agent — tracks finances, runway, CDs; generates weekly financial summaries | Claude system prompt | Weekly financial review; runway calculations | Claude.ai or Anthropic SDK |
| [agent/projects/Career.md](agent/projects/Career.md) | Career agent — evaluates job listings, drafts outreach, tracks applications | Claude system prompt | Job searching; salary negotiation; outreach writing | Claude.ai or Anthropic SDK |
| [agent/projects/Builder.md](agent/projects/Builder.md) | Builder agent — finds leads, closes web design clients, manages project pipeline | Claude system prompt | Client acquisition; proposal writing; project scoping | Claude.ai or Anthropic SDK |
| [agent/prompts/PMO.md](agent/prompts/PMO.md) | PMO agent — audits products, maintains ROADMAP/TASKS, enforces governance across the portfolio | Claude system prompt | Quarterly planning; repo health audits; sprint governance | Claude.ai or Anthropic SDK |
| [agent/prompts/ENG.md](agent/prompts/ENG.md) | Software Engineer agent — implements features, refactors, fixes bugs per intake tasks | Claude system prompt | Implementation tasks from the delivery pipeline | Claude.ai or Anthropic SDK |
| [agent/prompts/](agent/prompts/) | Full delivery pipeline: Intake, OPS, QA, Oncall, AUTO, Growth, DAILY, HANDOFF prompt modules | Claude system prompts | Complete AI-driven product delivery pipeline | Claude.ai or Anthropic SDK |
| [agent/repos/](agent/repos/) | Per-repo context files — loaded alongside agent prompts for repo-specific guidance | Markdown context docs | Providing agents with repo-specific context | Any agent that reads context files |

### Portfolio & Physical Projects

| Artifact | What It Does | Technology | When To Use | Requirements |
|----------|-------------|-----------|-------------|-------------|
| [projects/pfa/](projects/pfa/) | Power Failure Alarm — USB-powered circuit that sounds a buzzer on power loss (capacitor-discharge design) | Analog circuit, PCB | Power monitoring for unattended equipment; UPS absence scenarios | Build from schematic; components: 1N4001, 2N2905, 200µF cap, resistors, 8Ω buzzer |
| [projects/auto/auto.html](projects/auto/auto.html) | Car project board — card-per-vehicle layout with checkbox task lists, status badges, localStorage persistence | HTML, CSS, JavaScript | Tracking vehicle maintenance tasks; no-backend single-file tool | Modern browser, no server required |
| [projects/resume/](projects/resume/) | Structured resume and portfolio data — standard JSON Resume format plus AI-focused variant | JSON | Populating portfolio sites; generating formatted resumes for different audiences | Any JSON Resume renderer |
| [projects/fps-tech/](projects/fps-tech/) | FPS Tech branding assets — banner and logo PNG files | PNG graphics | Marketing materials, portfolio branding, presentation slides | Image viewer |

---

## Directory Structure

```
stash/
├── agent/          AI agent prompts — personal ops + product delivery pipeline
├── atlassian/      Atlassian Cloud API examples (Python/requests)
├── backend/        REST API reference implementations (Flask, Express)
├── cloud/          AWS boto3 examples + EC2 bootstrap scripts
├── database/       PostgreSQL DDL + MongoDB PyMongo examples
├── docs/           Repo-level docs (ARCHITECTURE, FEATURES, ROADMAP, TASKS, METRICS)
├── git/            Git maintenance utilities (PowerShell)
├── projects/       Standalone tools: Remora (PAM), Sampler (PDF), VMT (CMDB), PFA, auto, resume
├── SAAS/           SaaS platform API examples (Okta, ServiceNow, PagerDuty, Slack, GitHub, Datadog)
├── sso/            SSO / Identity examples (OAuth 2.0, SAML 2.0, AWS IAM Identity Center)
└── windows/        Windows automation — batch (LDAP), PowerShell (logs, Excel, server detection), VBA
```

---

## Quick Start

All Python scripts share a common pattern:

```bash
# 1. Copy the env template for the relevant service and fill in credentials
cp <service>/.env.example <service>/.env

# 2. Install dependencies
pip install requests python-dotenv        # Atlassian, SAAS, SSO scripts
pip install boto3 python-dotenv           # AWS/cloud scripts

# 3. Run read-only (safe, lists resources)
python <service>/examples.py

# 4. Run write demo (creates then cleans up test resources)
python <service>/examples.py --demo-write
```

PowerShell scripts:
```powershell
# Always check -DryRun first for scripts that modify state
.\git\cleanup-branches.ps1 -DryRun
.\windows\pwsh\compress-logs-v02a.ps1
```

VBA/Access tools:
```
Open .accdb file in Microsoft Access to launch the tool GUI.
```

---

## Docs

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — Directory map, execution contexts, dependencies, risk notes
- [`docs/FEATURES.md`](docs/FEATURES.md) — Feature inventory
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — Planned improvements and future work
- [`docs/TASKS.md`](docs/TASKS.md) — Actionable task backlog
- [`docs/CHANGELOG.md`](docs/CHANGELOG.md) — Notable additions and changes
- [`docs/METRICS.md`](docs/METRICS.md) — Repository health metrics
- [`docs/API.md`](docs/API.md) — No external API decision record
- [`atlassian/jira/RUNBOOK.md`](atlassian/jira/RUNBOOK.md) — Safe execution runbook for Atlassian scripts

---

## Links

- **Portfolio:** [nitsuah.io](https://nitsuah.io)
- **LinkedIn:** [austinjhardy](https://www.linkedin.com/in/austinjhardy/)
- **GitHub:** [nitsuah](https://github.com/nitsuah)

---

*"Ut prosim" — That I may serve*

## Community Standards

Shared community policies are centralized in https://github.com/nitsuah/.github:
- Contributing: https://github.com/nitsuah/.github/blob/main/CONTRIBUTING.md
- Code of Conduct: https://github.com/nitsuah/.github/blob/main/CODE_OF_CONDUCT.md
- Security: https://github.com/nitsuah/.github/blob/main/SECURITY.md
