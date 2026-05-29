# Architecture

This repository is a personal technical reference stash — scripts, API examples, automation tools, and agent prompts. There is no hosted service or external API contract.

---

## Directory Map

```
stash/
├── agent/          AI agent prompts — personal ops + product delivery pipeline
│   ├── docs/       Planning docs, roadmaps, feedback archives
│   ├── projects/   Personal agent definitions (Finance, Career, Builder, Intake)
│   ├── prompts/    Delivery pipeline roles + reusable prompt modules
│   └── repos/      Per-repo context files loaded alongside agent prompts
│
├── atlassian/      Atlassian Cloud API examples (Python/requests)
│   ├── jira/       Jira Software, JSM, Assets, Automation + project validator
│   ├── confluence/ Confluence Cloud
│   ├── bitbucket/  Bitbucket Cloud
│   └── statuspage/ Atlassian Statuspage
│
├── cloud/          AWS examples and EC2 bootstrap scripts
│   ├── aws/        boto3 examples — EC2, S3, IAM, SSM, CW, Lambda, RDS, ECS, CFN, R53
│   └── iac/        EC2 UserData scripts — Ubuntu 22.04, Windows Server 2022
│
├── git/            Git maintenance utilities (PowerShell)
│
├── projects/       Standalone tools and design artifacts
│   ├── pfa/        Power Failure Alarm circuit
│   ├── remora/     PAM tool (Access/VBA)
│   ├── sampler/    PDF random-sampling tool (Access/VBA)
│   ├── vmt/        Vulnerability management CMDB (Access/VBA)
│   ├── auto/       Car project board (HTML + localStorage)
│   ├── fps-tech/   Branding assets
│   └── resume/     Structured resume and portfolio JSON data
│
├── SAAS/           SaaS platform API examples (Python/requests)
│   ├── pagerduty/  REST + Events API v2
│   ├── slack/      Bot API
│   ├── github/     REST API v3
│   └── datadog/    API v1/v2
│
└── windows/        Windows automation scripts
    ├── bat/        Batch — LDAP search, log runner
    ├── pwsh/       PowerShell — log compression, CSV→Excel, server detection
    └── vba/        VBA — LDAP result cleanup
```

---

## Execution Contexts

| Directory | Runtime | Entry Point |
|-----------|---------|-------------|
| `atlassian/` | Python 3.10+ | `python <service>/examples.py --help` |
| `SAAS/` | Python 3.10+ | `python <service>/examples.py --help` |
| `cloud/aws/` | Python 3.10+ + boto3 | `python cloud/aws/examples.py --help` |
| `cloud/iac/` | EC2 UserData (root) | Paste into AWS EC2 launch config |
| `git/` | PowerShell 5.1+ | `.\git\cleanup-branches.ps1 -DryRun` |
| `windows/pwsh/` | PowerShell 5.1+ | `.\script.ps1` |
| `windows/bat/` | CMD | `script.bat` |
| `agent/` | Claude.ai / Anthropic SDK | Paste `.md` as system prompt |
| `projects/remora/` | Microsoft Access + VBA | Open `.accdb` |
| `projects/sampler/` | Microsoft Access + Adobe Acrobat | Open `.accdb` |
| `projects/vmt/` | Microsoft Access + VBA | Open `.accdb` |

---

## Dependencies

| Area | Dependencies |
|------|-------------|
| Python scripts | `requests`, `python-dotenv` |
| AWS examples | `boto3`, `python-dotenv` |
| EC2 UserData (Ubuntu) | `apt`, `curl`, `docker`, `awscli` (pre-installed on AMI or bootstrapped) |
| EC2 UserData (Windows) | Chocolatey (bootstrapped), `msiexec` |
| PowerShell scripts | PowerShell 5.1+, `git` in PATH |
| VBA/Access tools | Microsoft Access, Excel; Sampler also needs Adobe Acrobat |

---

## Risk Notes

| Script | Risk | Safeguard |
|--------|------|-----------|
| `git/cleanup-branches.ps1` | Deletes local and remote branches | `-DryRun` flag; interactive prompt by default |
| `atlassian/jira/validate_project.py` | Creates and deletes Jira issues | `--demo-write` opt-in; issues cleaned up in `finally` blocks |
| All `--demo-write` scripts | Creates live resources in external services | Opt-in flag; resources created with `[EXAMPLE]` prefix and cleaned up |
| `cloud/iac/` scripts | Runs as root/SYSTEM on EC2 boot | Review before attaching to instances; SSM secrets commented-out by default |
| `windows/pwsh/compress-logs-v02a.ps1` | Modifies log files | Review target paths before running |

---

## No External API

This repository does not expose any hosted API or external service contract. All scripts are client-side callers of third-party APIs. See `API.md` for the formal decision record.
