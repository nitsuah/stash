# Tasks

Last Updated: 2026-08-22

## In Progress

## Todo

### Documentation

- [ ] Complete `atlassian/jira/RUNBOOK.md` with full safe-execution guidance.
  - Priority: P1
  - Type: Docs
  - Note: Stub was present; content drafted in 2026-08-22 audit. Review and expand with environment-specific notes.

- [ ] Add usage examples to each SaaS script header (one-liner for most common operation).
  - Priority: P2
  - Type: Docs
  - Candidates: `SAAS/okta/examples.py`, `SAAS/servicenow/examples.py`, `SAAS/pagerduty/examples.py`.

- [ ] Document the VBA source files inside Remora, Sampler, and VMT more precisely.
  - Priority: P2
  - Type: Docs
  - Note: Source `.vb` files lack inline comments explaining business logic. Add docstrings or a companion `USAGE.md` per tool.

- [ ] Expand `projects/resume/README.md` to note last-updated date and schema version.
  - Priority: P3
  - Type: Docs

### CI / Quality

- [ ] Add Python linting via `ruff` in a GitHub Actions workflow.
  - Priority: P2
  - Type: CI
  - Acceptance: `.github/workflows/lint.yml` runs `ruff check .` on push; no errors on current codebase.

- [ ] Add PowerShell linting via PSScriptAnalyzer in CI.
  - Priority: P2
  - Type: CI
  - Acceptance: All `.ps1` files pass `Invoke-ScriptAnalyzer` at `Error` severity on push.

- [ ] Add `pytest` smoke tests for at least one Python example module using `responses` to mock HTTP.
  - Priority: P2
  - Type: Testing
  - Candidates: `atlassian/jira/examples.py` (most complex, highest-value to test).

### Examples

- [ ] Frontend examples (from nitsuah.io stack).
  - Priority: P2
  - Type: Examples
  - Candidates: React/Next.js, Svelte/SvelteKit, Vue/Nuxt.js components.

- [ ] Cloud cost management examples.
  - Priority: P3
  - Type: Examples
  - Candidates: Cloudability, CloudHealth, CloudZero, Kubecost APIs.

- [ ] SaaS inventory audit examples.
  - Priority: P3
  - Type: Examples
  - Candidates: Fortify-on-Demand, ZenGRC, Zylo.

### Decision Records

- [ ] API.md decision record review.
  - Priority: P3
  - Type: Docs
  - Note: This repo contains scripts and examples, not a hosted API. Decision record confirms no hosted API contracts exist (the repo does integrate with Jira and other SaaS APIs). Verify still accurate.

### Modernization

- [ ] Evaluate migration path for Remora from Access/VBA to a web-based alternative.
  - Priority: P3
  - Type: Modernization
  - Note: Dependency on Microsoft Access limits portability. Explore Python + PostgreSQL + minimal web UI.

- [ ] Evaluate migration path for Sampler from Access/VBA + Adobe Acrobat to a Python-native PDF tool.
  - Priority: P3
  - Type: Modernization
  - Candidates: `pypdf`, `pdfplumber`, `pymupdf` for page sampling logic.

## Audit Notes

- Docker-first execution path not available (`Dockerfile` / `docker-compose.yml` absent).
- `.github/ISSUE_TEMPLATE` and `.github/pull_request_template.md` present and usable.
- Agent pipeline branch/PR conventions: `pmo/`, `delivery/`, `qa/` prefixes per `agent/README.md`.
- `agent/REPO-README.md` is the agent directory's main doc — `agent/README.md` now created as the standard entry point.
- `projects/fps-tech/` contains only branding assets; `README.md` added in 2026-08-22 audit.
- `atlassian/jira/RUNBOOK.md` was a stub as of 2026-06-25; filled in during 2026-08-22 audit.
