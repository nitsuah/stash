# CodeStash

> Austin J. Hardy's technical evolution from VBA wizard to AI architect — 15+ years of enterprise automation and developer productivity innovation.

## Overview

This repository chronicles my technical journey from complex VBA automation systems to modern AI-driven developer productivity tools. Each project represents real-world solutions that have served thousands of engineers and operational staff across Netflix, Coinbase, Blackboard, and other enterprise environments.

**Technical Philosophy**: Build tools that eliminate manual toil, scale human capabilities, and empower teams to focus on high-value work through intelligent automation.

---

## [Atlassian](atlassian/README.md)

Python API examples for the Atlassian Cloud suite — Jira, Confluence, Bitbucket, and Statuspage. Includes a Jira project configuration validator with full lifecycle test suites.

---

## Projects

### [Power Failure Alarm (PFA)](projects/pfa/README.md)

![pfa_pcb.png](https://raw.githubusercontent.com/nitsuah/stash/main/projects/pfa/pfa_pcb.png)

USB-powered circuit that sounds a buzzer on power loss. When power is present, D1 (1N4001) charges C2 (200 µF) through R1 (5 kΩ) while R2 (10 kΩ) holds Q1 (2N2905 PNP) off. When power is removed, Q1 switches on and C2 discharges through BUZZ1 (8 Ω), producing an audible alarm until depleted.

### [Remora](projects/remora/)

![remora-home.png](https://raw.githubusercontent.com/nitsuah/stash/main/projects/remora/assets/remora-home.png)

Privileged Access Management (PAM) tool — stores user access lists, links to authorized signatory documents, and generates audit reports. Built in Microsoft Access, Excel, and VBA.

### [Sampler](projects/sampler/)

![sampler-home.png](https://raw.githubusercontent.com/nitsuah/stash/main/projects/sampler/assets/sampler-home.png)

PDF random-sampling tool — selects a statistically valid sample of pages matching a target string across a multi-page PDF. Built in Microsoft Access with Adobe Acrobat.

### [VMT](projects/vmt/)

Asset and vulnerability management (CMDB) tool — joins asset inventory against CVE scan exports to produce prioritized remediation reports. Built in Microsoft Access, Excel, and VBA.

---

## [SAAS](SAAS/README.md)

Python API examples for SaaS operations platforms — Okta, ServiceNow, PagerDuty, Slack, GitHub, and Datadog. See [`SAAS/README.md`](SAAS/README.md) for full docs.

---

## [Backend](backend/README.md)

REST API reference implementations — Flask (Python) and Express (Node.js) — covering JWT auth, ORM, validation, and pagination. See [`backend/README.md`](backend/README.md) for full docs.

---

## [Cloud](cloud/README.md)

AWS boto3 examples (EC2, S3, IAM, SSM, CloudWatch, Lambda, RDS, ECS, CloudFormation, Route53) and EC2 UserData bootstrap scripts for Ubuntu and Windows. See [`cloud/README.md`](cloud/README.md) for full docs.

---

## [Agent System](agent/README.md)

Role-based AI agent prompts for personal operations and a product delivery pipeline. Covers personal agents (CFO, Career, Builder) and a full delivery pipeline (PMO → Intake → DevOps → QA → Oncall → Growth). Each agent is a standalone `.md` file used as a system prompt in Claude or run locally via the Anthropic SDK.

---

## [Git Utilities](git/README.md)

PowerShell scripts for git repository maintenance. [`cleanup-branches.ps1`](git/cleanup-branches.ps1) scans all repos under a root path and removes merged local and remote branches — supports `-DryRun` and `-Force` flags.

---

## [Windows](windows/README.md)

Scripts for Windows automation, Active Directory, and log management — LDAP search/cleanup, PowerShell log management, CSV→Excel conversion, and VBA Office automation. See [`windows/README.md`](windows/README.md).

---

## Other Projects

- [`projects/auto/`](projects/auto/) — Single-page car project board (HTML + localStorage, no backend)
- [`projects/fps-tech/`](projects/fps-tech/) — FPS Tech branding assets

---

## Docs

- [`ARCHITECTURE.md`](ARCHITECTURE.md) — Directory map, execution contexts, dependencies, risk notes
- [`API.md`](API.md) — No external API decision record
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — Setup, PR checklist, coding standards
- [`SECURITY.md`](SECURITY.md) — Vulnerability reporting and credential hygiene

---

## 🔗 Links

- **Portfolio:** [nitsuah.io](https://nitsuah.io)
- **LinkedIn:** [austinjhardy](https://www.linkedin.com/in/austinjhardy/)
- **GitHub:** [nitsuah](https://github.com/nitsuah)

---

*"Ut prosim" — That I may serve*
