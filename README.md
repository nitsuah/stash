# CodeStash

> Austin J. Hardy's technical evolution from VBA wizard to AI architect — 15+ years of enterprise automation and developer productivity innovation.

## Overview

This repository chronicles my technical journey from complex VBA automation systems to modern AI-driven developer productivity tools. Each project represents real-world solutions that have served thousands of engineers and operational staff across Netflix, Coinbase, Blackboard, and other enterprise environments.

**Technical Philosophy**: Build tools that eliminate manual toil, scale human capabilities, and empower teams to focus on high-value work through intelligent automation.

---

## [Atlassian](atlassian/README.md)

Python API examples for the Atlassian Cloud suite — Jira, Confluence, Bitbucket, and Statuspage. Includes a Jira project configuration validator with full lifecycle test suites.

---

## [IAS](IAS/)

EC2 UserData bootstrap scripts for common instance configurations.

- [`ubuntu-userdata.sh`](IAS/ubuntu-userdata.sh) — Ubuntu 22.04: Docker, CloudWatch agent, sysctl hardening
- [`windows-userdata.ps1`](IAS/windows-userdata.ps1) — Windows Server 2022: Chocolatey, IIS, CloudWatch agent, TLS/SMB hardening

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

Python API examples for SaaS operations platforms — PagerDuty (incidents, on-call, Events API v2) and Slack (messages, channels, users, webhooks).

---

## [Agent System](agent/README.md)

Role-based AI agent prompts for personal operations and a product delivery pipeline. Covers personal agents (CFO, Career, Builder) and a full delivery pipeline (PMO → Intake → DevOps → QA → Oncall → Growth). Each agent is a standalone `.md` file used as a system prompt in Claude or run locally via the Anthropic SDK.

---

## [Git Utilities](git/README.md)

PowerShell scripts for git repository maintenance. [`cleanup-branches.ps1`](git/cleanup-branches.ps1) scans all repos under a root path and removes merged local and remote branches — supports `-DryRun` and `-Force` flags.

---

## Windows

Utilities for Windows automation, Active Directory, and log management. See [`windows/`](windows/) for scripts covering LDAP user search, PowerShell log management, and VBA Office automation.

- [`bat/ldap-search-users.bat`](windows/bat/ldap-search-users.bat) — LDAP user search, group membership, disabled account detection
- [`bat/run-logger.bat`](windows/bat/run-logger.bat) — Wraps any batch script with timestamped log output
- [`pwsh/`](windows/pwsh/) — Log compression, CSV-to-Excel conversion, JVM server detection (see [`pwsh/README.md`](windows/pwsh/README.md))
- [`vba/ldap-search-cleanup.vb`](windows/vba/ldap-search-cleanup.vb) — LDAP result formatting for Office

---

## Other Projects

- [`projects/auto/`](projects/auto/) — Single-page car project board (HTML + localStorage, no backend)
- [`projects/fps-tech/`](projects/fps-tech/) — FPS Tech branding assets

---

## 🔗 Links

- **Portfolio:** [nitsuah.io](https://nitsuah.io)
- **LinkedIn:** [austinjhardy](https://www.linkedin.com/in/austinjhardy/)
- **GitHub:** [nitsuah](https://github.com/nitsuah)

---

*"Ut prosim" — That I may serve*
