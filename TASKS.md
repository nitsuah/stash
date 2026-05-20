# Tasks

Last Updated: 2026-04-03 (pmo/q2-2026-planning)

## Done


## In Progress

- [ ] Re-align planning docs to repository reality and parser-safe format.
  - Priority: P0
  - Type: Docs
  - Confidence: High
  - Milestone: 2026 Q2
  - Problem Statement: existing planning docs referenced VB.NET product work that does not match this repository's current script/tooling scope.
  - Why It Matters: stale planning creates execution drift, incorrect prioritization, and onboarding confusion.
  - Acceptance Criteria:
    - `TASKS.md` uses exact sections `Done`, `In Progress`, `Todo`.
    - `ROADMAP.md` uses quarter headings with status in heading text.
    - Tasks and milestones align with validated repository structure.
  - Dependencies: none.


## Todo

- [ ] Add architecture baseline documentation (ARCHITECTURE.md stub created; fill out in Q2).
  - Priority: P1
  - Type: Docs
- [ ] Add script operations runbook (RUNBOOK.md stub created; fill out in Q2).
  - Priority: P1
  - Type: Docs
- [ ] Add security & sanitization checklist (SECURITY_CHECKLIST.md stub created; fill out in Q2).
  - Priority: P1
  - Type: Docs
  - Confidence: High
  - Milestone: 2026 Q2
  - Problem Statement: `ARCHITECTURE.md` is missing and current boundaries between `atlassian/`, `git/`, `ias/`, `projects/`, and `windows/` are undocumented.
  - Why It Matters: contributors cannot quickly understand ownership, script boundaries, or safe change surfaces.
  - Acceptance Criteria:
    - `ARCHITECTURE.md` created with module boundaries, execution context, and dependency map.
    - Includes risk notes for destructive operations (branch cleanup, log compression, access scripts).
    - Cross-linked from `README.md`.
  - Dependencies: none.

- [ ] Add script runbook and safety matrix for operational scripts.
  - Priority: P1
  - Type: Docs
  - Confidence: High
  - Milestone: 2026 Q2
  - Problem Statement: script discovery exists, but no unified runbook defines prerequisites, expected inputs, and dry-run behavior per script.
  - Why It Matters: operational scripts can be destructive when used without clear guardrails.
  - Acceptance Criteria:
    - Add a top-level runbook section in `README.md` linking to each script family.
    - For each PowerShell script, document parameters, safe invocation, and expected output.
    - Include examples for `-DryRun` where supported.
  - Dependencies: architecture baseline task.

- [ ] Complete sensitive-data and hardcoded-hostname scan using PowerShell-native search.
  - Priority: P0
  - Type: Security
  - Confidence: Medium
  - Milestone: 2026 Q2
  - Problem Statement: no verified repository-wide sanitization pass exists, and `rg` is unavailable in this environment.
  - Why It Matters: leaked credentials or internal hostnames can cause security incidents and compliance failures.
  - Acceptance Criteria:
    - Run search for `token|password|secret|credential|apikey|private key` across tracked files.
    - Log any findings with remediation plan or confirm zero findings.
    - Update `.gitignore` for local credential artifacts if needed.
  - Dependencies: none.

- [ ] Perform open-source safety sanitization for docs/examples.
  - Priority: P1
  - Type: Security
  - Confidence: Medium
  - Milestone: 2026 Q2
  - Problem Statement: documentation may include over-specific company/process details that are unnecessary for public release.
  - Why It Matters: reducing proprietary exposure lowers sharing and compliance risk.
  - Acceptance Criteria:
    - Review markdown/docs examples for sensitive business details.
    - Replace with generalized wording while preserving technical intent.
    - Record sanitization results and any deferred items.
  - Dependencies: none.

- [ ] Standardize file naming and typo cleanup in infrastructure assets.
  - Priority: P2
  - Type: Tech Debt
  - Confidence: High
  - Milestone: 2026 Q3
  - Problem Statement: `ias/Windows-userdata..yml` contains a double-dot naming anomaly.
  - Why It Matters: inconsistent naming harms discoverability and increases automation script fragility.
  - Acceptance Criteria:
    - Rename file to a normalized name.
    - Update references in docs/scripts.
    - Verify no broken links remain.
  - Dependencies: none.

- [ ] Add repository-level API contract decision record.
  - Priority: P3
  - Type: Docs
  - Confidence: Medium
  - Milestone: 2026 Q3
  - Problem Statement: `API.md` is missing and repository currently appears script-centric rather than service/API-centric.
  - Why It Matters: teams need explicit confirmation whether external contracts exist.
  - Acceptance Criteria:
    - Create `API.md` as either concrete interface spec or explicit "No external API" decision record.
    - Link the decision from `README.md` and `ARCHITECTURE.md`.
  - Dependencies: architecture baseline task.

## Audit Notes

- Docker-first execution path is not currently available (`Dockerfile` and `docker-compose.yml` not found).
- `.github/ISSUE_TEMPLATE` and `.github/pull_request_template.md` are present.
- PMO updates should continue via branch + PR workflow (`docs(pmo):` commit prefix).