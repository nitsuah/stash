# Features

A living inventory of what's in this repository.

## API Examples

| Area | Platforms |
|------|-----------|
| Atlassian Cloud | Jira, Confluence, Bitbucket, Statuspage |
| SaaS Operations | PagerDuty, Slack, GitHub, Datadog |
| Cloud (AWS) | EC2, S3, IAM, SSM, CloudWatch, Lambda, RDS, ECS, CloudFormation, Route53 |

All examples follow a consistent pattern: read-only by default, `--demo-write` flag for write operations, env vars via `.env` file.

## Backend API Examples

- **Flask (Python)** — `backend/flask/app.py`: JWT auth, SQLAlchemy ORM, input validation, pagination
- **Express (Node.js)** — `backend/express/app.js`: JWT auth, Sequelize ORM, validation, pagination
- Both expose the same endpoint surface for cross-language comparison

## Database Schema Examples

- **PostgreSQL** — `database/postgres/schema.sql`: enums, domains, RLS, partitioning, triggers, views; `queries.sql`: CTEs, window functions, JSONB, full-text search, keyset pagination
- **MongoDB** — `database/mongodb/examples.py`: schema validation, indexes, aggregation pipeline, multi-doc transactions, text search

## SSO / Identity Management Examples

- **OAuth 2.0 / OIDC** — `sso/oauth2.py`: auth code + PKCE flow, refresh, introspection, client credentials, UserInfo (any OIDC provider)
- **SAML 2.0** — `sso/saml.py`: IdP metadata parsing, AuthnRequest, SAMLResponse attribute extraction, SP metadata generation
- **AWS SSO / IAM Identity Center** — `sso/aws_sso.py`: device auth, account/role listing, temp credential vending, Okta SCIM pattern

## Infrastructure

- EC2 UserData bootstrap scripts for Ubuntu 22.04 and Windows Server 2022
- Covers: package install, Docker, IIS, CloudWatch agent, sysctl/TLS hardening, SSM secret retrieval

## Automation & Tooling

- Atlassian Jira project configuration validator with full lifecycle test suites
- Multi-repo merged branch cleanup (PowerShell)
- LDAP user search, group membership, disabled account detection (Batch)
- Log compression, CSV-to-Excel, JVM server detection (PowerShell)

## AI Agent System

- Personal agents: CFO, Career, Builder
- Product delivery pipeline: PMO → Intake → SoftwareEng → DevOps → QA → Oncall → Growth
- Reusable prompt modules: handoff template, task flow, test strategy, LOC analysis

## Projects

- **Remora** — Privileged Access Management (PAM) tool (Access/VBA)
- **Sampler** — PDF random-sampling tool (Access/VBA + Adobe Acrobat)
- **VMT** — Vulnerability and asset management CMDB (Access/VBA)
- **PFA** — USB-powered power failure alarm circuit
- **Auto** — Single-page car project board (HTML + localStorage)
