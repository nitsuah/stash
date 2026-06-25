# stash

> Reviewed: 2026-06-25

## Overview

Austin J. Hardy's technical evolution archive — 15+ years of enterprise automation tools and developer productivity scripts. Covers VBA/Access projects (Remora PAM, Sampler, VMT), Python API examples (Atlassian, SaaS platforms, AWS boto3, SSO/OIDC), PowerShell Windows automation, backend REST reference implementations (Flask, Express), database DDL (PostgreSQL, MongoDB), role-based AI agent system prompts, and git utilities.

## Current Goals / Roadmap Focus

**Q2 2026:** ✅ Completed — planning integrity reset, documentation baseline, security hygiene pass, open-source sanitization, backend/database/SSO examples, IaC consolidation

**Q3 2026 (planned):**
- Naming and consistency cleanup (normalize anomalous filenames, tighten cross-references)
- Lightweight validation harness for critical scripts (exploratory; dry-run smoke checks)

**Q4 2026 (exploratory):**
- Cross-repo automation catalog (discoverable script capabilities + ownership metadata)
- Operational metrics maturity (measurable quality metrics, not placeholders)
- Script dependency graph (Mermaid diagram from imports/source/require calls; CI artifact)
- Dry-run audit log (structured JSON summary of planned changes for high-impact scripts)

**Note from overseer:** Stash is being deprioritized — overseer TASKS P1 item to mark repo private, block PRs, add sanitization checklist.

## Open P0/P1 Tasks

- [ ] **P2** Frontend examples (React/Next.js, Svelte/SvelteKit, Vue/Nuxt.js)
- [ ] **P3** Cloud cost management examples (Cloudability, CloudHealth, CloudZero, Kubecost)
- [ ] **P3** SaaS inventory audit examples (Fortify-on-Demand, ZenGRC, Zylo)
- [ ] **P3** `API.md` decision record (no external contracts — confirm no hosted API)

No active P0/P1 tasks in this repo. Work is in low-contribution mode.

## Blockers

- No Docker execution path (no Dockerfile/docker-compose.yml)
- Overseer P1 task: mark private + block PRs + sanitization (external governance item)

## Recent Changes

- `CLOUD/aws/examples.py` — boto3 examples (EC2, S3, IAM, SSM, CloudWatch, Lambda, RDS, ECS, CloudFormation, Route53)
- `SAAS/github/examples.py`, `SAAS/datadog/examples.py`, `SAAS/slack/examples.py`, `SAAS/pagerduty/examples.py`
- `atlassian/` — Jira, Confluence, Bitbucket, Statuspage API examples with shared client + validator
- `IAS/` — Ubuntu + Windows EC2 UserData bootstrap scripts
- `git/cleanup-branches.ps1` — multi-repo merged branch cleanup
- `agent/` — personal agent system (CFO, Career, Builder) + product delivery pipeline (PMO → DevOps → QA)
- `projects/auto/` — single-page car project board
- `projects/resume/` — sanitized (MNPI, internal tool names, employee PII removed)
- `README.md` full rewrite; `.github/copilot-instructions.md` updated for actual stack
