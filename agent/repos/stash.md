# Stash Repository Runbook (PMO)

Last Validated: 2026-03-27

## Repository Type

Automation and tooling monorepo focused on scripts, infrastructure samples, and project-specific utilities.

## Verified Structure

Top-level directories observed locally:

- `.github/`
- `agent/`
- `atlassian/`
- `git/`
- `ias/`
- `projects/`
- `windows/`

Notable governance files confirmed:

- `.github/ISSUE_TEMPLATE/`
- `.github/pull_request_template.md`
- `LICENSE`
- `SECURITY.md`

## Runtime Validation Evidence

- Command executed successfully:
	- `powershell -NoProfile -ExecutionPolicy Bypass -File ./git/cleanup-branches.ps1 -Path . -DryRun`
- Observed behavior:
	- Script starts cleanly.
	- Reports dry-run mode.
	- Exits without unhandled exceptions.

## Operational Notes

- No Docker runtime path is currently available in this repository (`Dockerfile` and `docker-compose.yml` not present).
- `rg` was not available in the environment during audit; use PowerShell-native file discovery/search commands when needed.
- `ias/Windows-userdata..yml` appears to have a naming anomaly and should be normalized in a dedicated change.

## PMO Findings Snapshot

- Planning docs had stale references to unrelated VB.NET roadmap/task items.
- Parser-safe formatting was missing from `TASKS.md` and `ROADMAP.md` before the 2026-03-27 update.
- Architecture/API documentation gaps remain (`ARCHITECTURE.md`, `API.md` absent).

## Recommended PMO Workflow For This Repo

1. Re-validate at least one non-destructive script path before each planning cycle.
2. Keep `TASKS.md` labels explicit: Priority, Type, Confidence, Milestone.
3. Keep `ROADMAP.md` quarter headings with status text in heading.
4. Perform PMO updates on a branch named `pmo/stash/<theme>-<date>`.
5. Use commit prefix `docs(pmo):` and open a PR with evidence.

---

## Vault Index

*This is the stash repo itself — the vault root IS the stash repo. Key vault docs:*

**Agent System:** [[AGENT-MAIN]] · [[REPO-README]] · [[prompts/1FLOW|1FLOW]] · [[prompts/PMO|PMO]] · [[prompts/ENG|ENG]] · [[prompts/OPS|OPS]] · [[prompts/QA|QA]]

**Planning:** [[docs/2026Q2]] · [[docs/LOC-REPORT]] · [[docs/GAPS_AND_IMPROVEMENT_PLAN]] · [[docs/ENHANCEMENT_ROADMAP]] · [[docs/SECURITY_CHECKLIST]] · [[docs/MONEY-MAKERS]]

**Personal Agents:** [[projects/Builder|Builder]] · [[projects/Career|Career]] · [[projects/Finance|Finance]]

**Audits:** [[docs/AUDIT_GRAPH_2026_06_09|Graph Audit 2026-06-09]] · [[docs/AUDIT_GRAPH_2026_06_09b|Graph Audit 2026-06-09 (pass 2)]]
