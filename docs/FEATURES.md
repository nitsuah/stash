# Features

> 🧭 [stash](../README.md) · **Features** · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

A living inventory of what's in this repository.

## API Examples

| Area | Platforms |
| ------ | ----------- |
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
- **9router** — local/remote AI gateway config; OpenAI-compatible REST for chat, image, TTS, embeddings, web search, and web fetch; device-specific tool and model setup documented
- **eng-loc skill** — LOC analysis automation integrated into agent delivery pipeline
- **eng-mini skill** — lightweight engineering task runner for low-cost model delegation

## Vault Tooling

- **Repo docs sync** - `agent/scripts/sync-repos.ps1` mirrors each tracked repo's root PMO docs and every `docs/**/*.md` into `agent/repos/<repo>/` (paths preserved); `-Prune` removes mirror copies that no longer exist upstream.
- **Vault hub links** - `agent/scripts/build-vault-indexes.py` links every routine-written note through its hub instead of flat INDEX files: repo hubs link their README, KB overview and latest LOC/MINI reports; reports and dated notes chain prev/next; project subfolders hang off folder hubs; the *Vault map* in `AGENT-MAIN.md` links the latest notes, the latest report of each kind, and every project. The graph forms per-repo and per-project clusters.
- **Mirror enrichment** - `agent/scripts/enrich-mirror.py` (run by `sync-repos.ps1`) gives each mirrored doc `up:`/`source:` frontmatter and turns links to un-mirrored files into GitHub URLs, so repo docs cluster around a named hub and are never orphaned.
- **Doc link fixer** - `agent/scripts/fix-doc-links.py` repairs broken relative links in a repo (run by the PMO audit) or in vault notes (`--vault`). It only rewrites a link when exactly one target is plausible, and it unlinks dead references in archived docs.
- **Routine-owned diff gate** - `agent/scripts/check-generated-diff.py` passes an auto-merge PR only when every change is a dated note, a repo mirror, or generated nav/block text.
- **Orphan finder** - `agent/scripts/find-orphans.py` reports notes with no links in or out (and unreferenced notes), by folder, resolving wikilinks and markdown links the way Obsidian does. It also reports reachability from `AGENT-MAIN` by hop count and flags star hubs. `--check` fails when a note outside the repo mirrors can't be reached.
- **Jira runbook** - `atlassian/jira/RUNBOOK.md` covers prerequisites, parameters, dry-run steps, risk levels, and troubleshooting for all 7 Atlassian scripts.
- **Per-directory READMEs** - every top-level directory and all 7 `projects/*` subdirectories have a README (`docs/` and `flipper/` are intentional exceptions).

## Projects

- **Remora** — Privileged Access Management (PAM) tool (Access/VBA)
- **Sampler** — PDF random-sampling tool (Access/VBA + Adobe Acrobat)
- **VMT** — Vulnerability and asset management CMDB (Access/VBA)
- **PFA** — USB-powered power failure alarm circuit
- **Auto** — Single-page car project board (HTML + localStorage)
