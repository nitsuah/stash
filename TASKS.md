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
  - Atlassian (Jira, Confluence, Bitbucket, Statuspage), PagerDuty, Slack, GitHub, Datadog, Okta, ServiceNow, AWS boto3.

- [x] Backend API examples.
  - Flask (Python) + Express (Node.js) — JWT auth, ORM (SQLAlchemy / Sequelize), validation, pagination.
  - `backend/flask/app.py` and `backend/express/app.js` with shared endpoint surface.

- [x] Database schema examples.
  - PostgreSQL: `database/postgres/schema.sql` (enums, domains, RLS, partitioning, triggers, views) + `queries.sql` (CTEs, window functions, JSONB, full-text, keyset pagination).
  - MongoDB: `database/mongodb/examples.py` (schema validation, indexes, aggregation pipeline, multi-doc transactions, text search).

- [x] SSO/Identity Management examples.
  - `sso/oauth2.py`: OAuth 2.0 auth code + PKCE, refresh, introspection, client credentials, UserInfo (any OIDC provider).
  - `sso/saml.py`: SAML 2.0 IdP metadata parsing, AuthnRequest, SAMLResponse attribute extraction, SP metadata.
  - `sso/aws_sso.py`: IAM Identity Center device auth, account/role listing, temp credential vending, Okta SCIM pattern.

- [x] Consolidate IAS into cloud/.
  - Scripts moved to `cloud/iac/`. IAS section removed from root README.

- [x] Fix stale `develop` branch image URLs across project READMEs.
  - pfa, remora, sampler all updated to `main`.

- [x] Update .github/copilot-instructions.md.
  - Rewritten for current stack (Python, PowerShell, Bash, VBA, Groovy).


## In Progress


## Todo

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

- [ ] API.md decision record.
  - Priority: P3
  - Type: Docs
  - Note: This repo contains scripts and examples, not a hosted API. Decision record confirms no external contracts exist.


## Audit Notes

- Docker-first execution path not available (`Dockerfile` / `docker-compose.yml` absent).
- `.github/ISSUE_TEMPLATE` and `.github/pull_request_template.md` present and usable.
- Agent pipeline branch/PR conventions: `pmo/`, `delivery/`, `qa/` prefixes per `agent/README.md`.
