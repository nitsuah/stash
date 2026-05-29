# Features

A living inventory of what's in this repository.

## API Examples

| Area | Platforms |
|------|-----------|
| Atlassian Cloud | Jira, Confluence, Bitbucket, Statuspage |
| SaaS Operations | PagerDuty, Slack, GitHub, Datadog |
| Cloud (AWS) | EC2, S3, IAM, SSM, CloudWatch, Lambda, RDS, ECS, CloudFormation, Route53 |

All examples follow a consistent pattern: read-only by default, `--demo-write` flag for write operations, env vars via `.env` file.

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
