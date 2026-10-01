# Tasks

> 🧭 [stash](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · **Tasks** · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

Last Updated: 2026-09-29

## In Progress

## Todo

### CI / Quality

- [x] Add Python linting via `ruff` in a GitHub Actions workflow.
  - Priority: P2
  - Type: CI
  - Acceptance: `.github/workflows/ci.yml` runs `ruff check .` on push; no errors on current codebase.
  - Done 2026-09-28: added `lint-python` job to `.github/workflows/ci.yml` (PR #157).

- [x] Add PowerShell linting via PSScriptAnalyzer in CI.
  - Priority: P2
  - Type: CI
  - Acceptance: All `.ps1` files pass `Invoke-ScriptAnalyzer` at `Error` severity on push.
  - Done 2026-09-28: added `lint-powershell` job to `.github/workflows/ci.yml` (PR #158).

- [x] Add `pytest` smoke tests for Jira examples using `responses` to mock HTTP.
  - Priority: P2
  - Type: Testing
  - Candidates: `atlassian/jira/examples.py` (most complex, highest-value to test).
  - Done 2026-09-28: added `test-python` job to `.github/workflows/ci.yml` with `atlassian/jira/test_examples.py` (PR #159).

- [ ] Add `pytest` smoke tests for other Atlassian examples (Bitbucket, Confluence, Statuspage) using `responses` to mock HTTP.
  - Priority: P2
  - Type: Testing
  - Candidates: `atlassian/bitbucket/examples.py`, `atlassian/confluence/examples.py`, `atlassian/statuspage/examples.py`.

- [ ] Expand test coverage to Python example files (target ≥30% on example files).
  - Priority: P2
  - Type: Testing
  - Note: Current example-file coverage is 84% (Jira only); Bitbucket, Confluence, Statuspage examples untested. Overall coverage 37% skewed by `validate_project.py` (0%).
  - Approach: build on `test_examples.py`, going from smoke tests to meaningful coverage.

- [ ] Add pre-commit hooks
  - Priority: P3
  - Type: CI
  - Acceptance: Ruff, PSScriptAnalyzer, shellcheck locally
  - Source: unsourced, added by PR #160 (2026-09-29) without a request. Confirm or drop.

- [ ] Add dependabot/renovate
  - Priority: P3
  - Type: CI
  - Acceptance: Auto-update GitHub Actions, Python deps
  - Source: unsourced, added by PR #160 (2026-09-29) without a request. Confirm or drop.

- [ ] Add CodeQL / SAST scanning
  - Priority: P3
  - Type: CI
  - Acceptance: GitHub Advanced Security or OSS equivalent
  - Source: unsourced, added by PR #160 (2026-09-29) without a request. Confirm or drop.

- [ ] Add changelog automation
  - Priority: P3
  - Type: CI
  - Acceptance: conventional-changelog or similar
  - Source: unsourced, added by PR #160 (2026-09-29) without a request. Confirm or drop.

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

### Documentation

- [ ] Add usage examples to each SaaS script header (one-liner for most common operation).
  - Priority: P2
  - Type: Docs
  - Candidates: `SAAS/okta/examples.py`, `SAAS/servicenow/examples.py`, `SAAS/pagerduty/examples.py`.
  - Note: restored 2026-09-30; PR #160 had replaced it with a garbled "SAAS quickstart" item.

- [ ] Document the VBA source files inside Remora, Sampler, and VMT more precisely.
  - Priority: P2
  - Type: Docs
  - Note: Source `.vb` files lack inline comments explaining business logic. Add docstrings or a companion `USAGE.md` per tool. (Restored 2026-09-30; PR #160 had pointed it at a nonexistent `atlassian/jira/vba`.)

- [ ] Add architecture diagrams
  - Priority: P3
  - Type: Docs
  - Mermaid/PlantUML in docs/
  - Source: unsourced, added by PR #160 (2026-09-29) without a request. Confirm or drop.

- [ ] Add CONTRIBUTING.md
  - Priority: P3
  - Type: Docs
  - Include PR template, issue template links
  - Source: unsourced, added by PR #160 (2026-09-29) without a request. Confirm or drop.

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

### Vault / Obsidian (circle back; from the 2026-09-25 vault overhaul, see `agent/projects/Vault.md`)

Done 2026-09-25 (stash #139-#144): flat INDEX files retired for generated hub links, mirror enrichment, `fix-doc-links.py`, CI vault graph check, properties + Bases, link suggestions, templates, archive, aliases, topic hubs. The old items in this section (prune, stale mirrors, the agent-board hub title, orphan routine) are covered by that work.

- [ ] Decide whether a monthly rollup note is worth it (`notes/archive/YYYY-MM/` summary built from that month's weekly reviews), or whether weekly notes plus the archive are enough.
  - Priority: P3
  - Type: Vault / Automation
  - Acceptance: either a generated `YYYY-MM` rollup linked from its archive folder, or a one-line "not needed" note in `agent/projects/Vault.md`.

- [ ] Diagrams and screenshots for app repos (Excalidraw/Mermaid architecture diagrams, Playwright screenshots) generated by CI, committed into each repo, and auto-embedded in the README by name and path.
  - Priority: P1
  - Type: Docs / CI
  - Status: on hold (2026-09-26). This is the next portfolio initiative, to be built into vigil itself once the current vigil work (MCP rollup, PMO UI) ships.
  - Note: vigil is the planned home for this (as a best-practice check and a reusable CI recipe); see the vigil session started 2026-09-25. The vault then mirrors these via `enrich-mirror.py`, since images already link to GitHub.

- [x] Cross-repo task rollup: tracked in vigil (MCP tool / `/api/context` over each repo's TASKS.md), not in the vault. Connect vigil's MCP to Claude Code once it lands, and drop the daily note's hand-built "Tasks" section in favor of it.
  - Priority: P2
  - Type: Integration
  - Done 2026-09-26: the vigil MCP (HTTP, ghoverseer.netlify.app/api/mcp) is connected to local Claude Code and verified; DAILY `## Tasks` now reads `get_open_tasks`. Cloud routines can call the same endpoint once `VIGIL_MCP_KEY` is set in the cloud environment.

- [ ] Tune topic hubs after a few weeks: review `agent/topics/topic-*.md` matches for noise or misses, and consider seeding new topics from Smart Connections clusters (`suggest-links.py` already reads the embeddings).
  - Priority: P3
  - Type: Vault

- [ ] Richer properties: add `status` (active/archived/superseded) where it is cheap to derive (e.g. `docs/archive/` → archived), and a Bases view that hides archived docs.
  - Priority: P3
  - Type: Vault

- [x] Smaller, single-idea notes: when a mirrored doc or report grows past a few screens, split concept sections into their own notes (agents read less per answer).
  - Priority: P3
  - Type: Docs
  - Done 2026-09-26: covered by PMO step 7, which runs `find-orphans.py --long 300` each cycle and splits the worst one or two notes into single-idea notes.

- [x] Graph labels: evaluate the *Front Matter Title* community plugin, so graph nodes show `title:` instead of generic file names (README, ROADMAP).
  - Priority: P3
  - Type: Vault / Obsidian config
  - Owner: you, for the install (plugin code is gitignored, so it's per machine). Vault side done 2026-09-26: `enrich-mirror.py` gives every mirrored repo doc a `title: "<repo> · <file>"` (applied on the next DAILY sync); hubs and notes already have unique file names.
  - Done 2026-09-27: plugin installed and kept; the mirrors got their titles in the 9/27 sync, and graph nodes now read `<repo> · <file>`.

- [x] Review the first weekly `reports/link-suggestions-*.md` and adopt or ignore; if most suggestions are noise, raise `MIN_SCORE` in `suggest-links.py`.
  - Priority: P3
  - Type: Vault
  - Done 2026-09-26: superseded by PMO step 7, which reviews the latest link-suggestions report every cycle, records accepted/ignored counts, and proposes a higher `MIN_SCORE` if they stay noisy.

### Public-vault leak follow-ups (2026-09-30 audit, see `agent/projects/obsidian-vault-guide.md` §5)

- [ ] Decide whether to purge removed private content from git history: the `deployer` mirror (2026-09-16 to 09-30) and three personal email addresses in `agent/projects/docs/MONEY-MAKERS.md`.
  - Priority: P2
  - Type: Security / human decision
  - Acceptance: either a `git filter-repo` purge plus a force-push of `main` (coordinated, after open PRs land), or a one-line "accepted, low sensitivity" note in the guide's audit section.

- [ ] Decide whether `projects/remora/remora.accdb` (16 MB Access DB from 2023, holds an employer-domain email address; binary files aren't PII-scanned) should stay public.
  - Priority: P2
  - Type: Security / human decision
  - Acceptance: file removed (and optionally purged), or kept with a note saying why.

- [ ] Remove the third-party email address from kryptos `docs/TASKS.md` upstream (it reaches the vault through the mirror).
  - Priority: P3
  - Type: Docs (kryptos)
  - Acceptance: next sync's `pii-scan.sh agent/repos/kryptos` shows no email hit.

- [ ] Drop the stale "agent/reports/ is gitignored" line from the week-eng-mini and week-eng-loc cloud prompts (reports have been tracked since 2026-09-24), then refresh `agent/routines/routine-cloud-week-eng-*.md`.
  - Priority: P3
  - Type: Routine

### Vault scorecard follow-ups (2026-09-25 review: overall 8.3/10)

Each item names its owner. **vigil**: app feature, tracked in nitsuah/vigil. **routine**: prompt change in `agent/prompts/` or a cloud routine. **stash**: scripts or vault. Items already listed above are referenced, not repeated.

**Semantic layer (7.5 → 9)**
- [ ] Embedding freshness: `suggest-links.py` reports notes missing a Smart Connections embedding, or embedded before their last edit, so suggestions aren't built on stale vectors.
  - Priority: P3 · Owner: stash
- [x] Close the loop on suggestions: the PMO audit reads the latest `reports/link-suggestions-*.md`, adds the links that reflect a real dependency (in the note body), and records accepted/ignored counts in its report. See also "Review the first weekly link-suggestions" and "Tune topic hubs" above.
  - Priority: P3 · Owner: routine (PMO.md) · Done 2026-09-26: PMO step 7 adds the real-dependency links and records accepted/ignored counts.

**Content quality (6.5 → 8)**
- [x] Long-note report: `find-orphans.py` lists notes outside the mirrors over a size threshold (e.g. 300 lines), and the PMO audit splits the worst offenders into single-idea notes. See also "Smaller, single-idea notes" above.
  - Priority: P3 · Owner: stash (report) + routine (PMO.md) · Done 2026-09-26: `find-orphans.py --long N`; PMO step 7 splits the worst one or two per cycle (5 notes over 300 lines today).
- [x] Stale hub prose: the generator flags repo hubs whose `Reviewed:`/`Last Validated` date is more than 30 days old in VAULT-MAP, and DAILY step 2 refreshes those first.
  - Priority: P2 · Owner: stash + routine (DAILY.md) · Done 2026-09-26: VAULT-MAP gets a generated **Stale hubs** line (over 30 days or no date); DAILY step 2 refreshes those first. None stale today.
- [ ] KB overviews drift (`projects/KB/*-overview.md`): either fold them into the repo hubs, or regenerate them from vigil's `/api/context` so there is one source per repo.
  - Priority: P2 · Owner: vigil (context source) + stash (decision)

**Work tracking (6 → 8)**
- [x] Cross-repo task rollup in vigil (MCP tool and/or `/api/context`): shipped in vigil #241 (2026-09-26) as the `get_open_tasks` MCP tool and the `open_work` block in `/api/context`. The Claude Code connection and the DAILY switch are also done (2026-09-26), as recorded above and below.
  - Priority: P2 · Owner: vigil
- [x] Once it lands, DAILY's "## Tasks" section reads open P0/P1 items from vigil's MCP instead of re-deriving them from hub notes.
  - Priority: P2 · Owner: routine (DAILY.md) · Done 2026-09-26 (hub notes remain the fallback).
- [x] Parser-safe TASKS.md everywhere: the PMO audit checks every repo's TASKS.md against the shared format (priority, status, type), so vigil's parser sees all items.
  - Priority: P2 · Owner: routine (PMO.md) · Done 2026-09-26: `check-tasks-format.py` (vigil's parsing rules) runs at the start of each PMO cycle; first run flagged 13 of 17 repos, 47 unprioritized items.

**Visuals (3 → 7)**
- [ ] Decide whether the vault mirrors image assets from repo `docs/` (small PNG/SVG only) so they render in Obsidian, or keeps linking them to GitHub as it does today. If mirroring, extend `sync-repos.ps1` + `enrich-mirror.py` and set a size cap.
  - Priority: P3 · Owner: stash

**Operational polish (7 → 9)**
- [x] Routine failure visibility: DAILY lists yesterday's failed cloud routine runs (RemoteTrigger `list_runs`), with the reason (e.g. spend or rate limit), in `## Notes`, and retries them one at a time per the serialize-catch-up rule.
  - Priority: P2 · Owner: routine (DAILY.md) · Done 2026-09-26: DAILY `## Notes` lists failed runs from `list_runs` plus `get_run_log`; retries are queued in `## Tasks`, one at a time.
- [x] Stale CodeRabbit "changes requested" reviews: enable CodeRabbit's `request_changes_workflow` (it approves once its comments are resolved) in the org/repo config, so a fixed PR isn't blocked on a manual dismiss.
  - Priority: P2 · Owner: stash (CodeRabbit config; human applies org setting) · Closed 2026-09-27: the setting is on, but CodeRabbit's free tier still leaves stale reviews; the workaround is commenting `@coderabbitai approve` once CI and threads are clean.
- [x] No pushes to a merged PR's branch: agent PR workflows check `gh pr view --json state` before pushing follow-ups, and open a new PR if the old one merged (commits were briefly stranded after #141).
  - Priority: P3 · Owner: routine (AGENT-MAIN / HANDOFF guidance) · Done 2026-09-26: rule added to AGENT-MAIN, and the DAILY push step checks it.
- [ ] Local-only Obsidian settings: decide which `.obsidian/` files to track (e.g. the Templater `templates_folder`, currently gitignored), so a fresh clone gets the same vault behavior.
  - Priority: P3 · Owner: stash

## Audit Notes

- Docker-first execution path not available (`Dockerfile` / `docker-compose.yml` absent).
- `.github/ISSUE_TEMPLATE` and `.github/pull_request_template.md` present and usable.
- Agent pipeline branch/PR conventions: `pmo/`, `delivery/`, `qa/` prefixes per `agent/README.md`.
- `agent/REPO-README.md` is the agent directory's main doc — `agent/README.md` now created as the standard entry point.
- `projects/fps-tech/` contains only branding assets; `README.md` added in 2026-08-22 audit.
- `atlassian/jira/RUNBOOK.md` was a stub as of 2026-06-25; filled in during 2026-08-22 audit, verified complete (all 7 scripts covered: prerequisites, risk levels, mitigations, troubleshooting) in 2026-09-02 audit — removed from Todo, ROADMAP item confirmed `[x]`. Fixed one stale reference in the runbook itself (`JIRA_URL` → `JIRA_HOST`, matching the actual env var table).
- `projects/resume/README.md` expanded with last-updated date and schema note in 2026-09-02 audit — removed from Todo.
- 2026-09-02 audit: found and fixed 14 broken path references left over from repo reorganization — 6 instances of `IAS/` (docs/CHANGELOG.md x2, cloud/iac/ubuntu-userdata.sh, cloud/iac/windows-userdata.ps1, .github/copilot-instructions.md, agent/repos/stash.md) should have read `cloud/iac/`, and 8 instances of `CLOUD/` (wrong case; docs/CHANGELOG.md, agent/repos/stash.md, cloud/README.md x2, cloud/aws/examples.py x4 — including its own usage examples/docstring) should have read `cloud/aws/`. The `CLOUD/` casing bug would break on case-sensitive filesystems (Linux/Mac) even though it worked on Windows. This is partial progress on the "Naming and Consistency Cleanup" roadmap item — a full repo-wide filename normalization pass is still open and out of scope for this audit.
- `projects/README.md` added in 2026-09-02 audit (index of the 7 project subdirectories, all of which already had their own READMEs) — closes the last gap in the per-directory README audit. `docs/` intentionally has no README.md (ROADMAP/TASKS/FEATURES/METRICS already serve as its index); `flipper/` is an empty, untracked directory with no content to document.

## Later

- [x] Vigil key follow-up: confirm the rotated key works locally (ask Claude to "check vigil"), and add `VIGIL_MCP_KEY` to the cloud environment so daily-brief can read vigil (the setting wasn't findable in the claude.ai UI on 2026-09-26).
  - Priority: P3
  - Type: Integration
  - Done 2026-09-29: completed separately
