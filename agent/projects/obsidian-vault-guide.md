# How we use Obsidian (stash/agent vault)

> Reviewed: 2026-09-30. Read this before adding a routine, a script, or a folder that writes into the vault.

`stash/agent/` is an Obsidian vault **and** a folder in a **public** GitHub repo (`nitsuah/stash`). This guide covers what the vault holds, what keeps it in sync, which routines write to it, and how private data stays out while the useful roll-ups get committed.

The short version of the privacy model: **raw stays local, synthesis gets committed.** Logs, plugin state, inbox and calendar contents, financial data and private repos never leave the machine. What reaches GitHub is a summary written for a public reader: counts, statuses, PR titles, repo-level prose.

---

## 1. Vault layout

| Path | What it is | In git? |
|---|---|---|
| `VAULT-MAP.md` | Vault home. Its generated block links the latest note, report and hub of every kind | yes |
| `notes/` | Daily notes `YYYY-MM-DD.md` and weekly notes `YYYY-Www.md`, written by `daily-repo-sync` | yes (roll-up) |
| `repos/<repo>.md` | One synthesized hub per tracked repo | yes (roll-up) |
| `repos/<repo>/` | Mirror of the repo's merged `.md` docs (public repos only) | yes (copy of public docs) |
| `reports/` | Routine reports. `reports/cloud/<routine>/` holds the cloud routines' reports | yes (sanitized) |
| `prompts/` | Canonical routine and agent specs (DAILY, PMO, TIRE, SOTU, ...) | yes |
| `projects/` | Hand-written project docs, `scope.md` (the repo registry), folder hubs | yes |
| `topics/` | Cross-repo maps by subject, driven by a `match:` pattern | yes |
| `routines/` | Public-safe backups of the routine definitions ([[routines-backup]]) | yes |
| `templates/` | Templater templates for hand-written notes | yes |
| `scripts/` | The vault's tooling (section 3) | yes |
| `logs/` | Routine run logs (`*.log`) | **no**: `*.log` in `.gitignore`, hidden from the vault in `app.json` |
| `.obsidian/plugins/*/data.json` | Plugin settings, including the Local REST API key and private key | **no**: `**/.obsidian/plugins/*/data.json` |
| `.obsidian/workspace*.json`, `cache/` | Window state | **no** |
| `.smart-env/` | Smart Connections embeddings of every note | **no** |
| `Nexus/` | Nexus plugin data | **no** |
| `reports/*.txt` | Stray background-task dumps | **no** |

Navigation and naming rules (unique names, generated `<!-- nav -->` and `vault-links` blocks, `up:` frontmatter, archive moves) are in the vault [README](../README.md#vault-linking-conventions). Follow them. CI's vault graph check fails a PR that breaks them.

## 2. Plugins and how agents reach the vault

| Plugin | Used for |
|---|---|
| Local REST API + mcp-tools | The `obsidian` MCP server at `http://127.0.0.1:27123/mcp/`. Loopback only, so no cloud routine can use it. `scripts/bootstrap-stage0.ps1` checks it and starts Obsidian if needed (run with `pwsh`, not Windows PowerShell 5.1) |
| Smart Connections / Lookup / Context | Local embeddings in `.smart-env/`. `scripts/suggest-links.py` reads them for the Monday link-suggestions report |
| Templater | `templates/tpl-note.md` and `tpl-decision.md`, which ask for the parent hub and write `up:` |
| Front Matter Title | Shows `title:` (e.g. `vigil · ROADMAP`) instead of a bare file name in the graph |
| Nexus, Excalidraw, Importer | Workspace memory, diagrams, imports |

No scheduled routine depends on the app running. They all read and write the vault as plain files through git. The MCP server is for interactive sessions.

Obsidian rewrites its own settings JSON on every launch. A git clean filter (`scripts/obsidian-json-clean.py`, wired in `.gitattributes`) hides that churn, so `main` stays clean and the daily sync doesn't skip stash as dirty. Set it up once per clone:

```bash
git config filter.obsidian-json.clean "python agent/scripts/obsidian-json-clean.py %f"
```

Plugin binaries (`main.js`, `styles.css`, the MCP server exe) are gitignored and re-downloaded on a new machine.

## 3. The sync pipeline

`daily-repo-sync` runs [[prompts/DAILY|DAILY]] once a day. Its vault steps, in order:

1. **Close the loop.** Merge yesterday's `obn:` PRs, but only when the PR comes from the `nitsuah` account and isn't from a fork, the branch is `obn/…`, and `scripts/check-generated-diff.py` shows every changed file is a dated note, a repo mirror or hub, or generator output. A hand edit or a stranger's PR is never auto-merged.
2. **Mirror repo docs.** `scripts/sync-repos.ps1 -Prune` exports every `.md` from each tracked repo's **remote default branch** (`origin/HEAD`) with `git archive`. Untracked, staged, locally modified and unmerged files can't leak. **Private repos are skipped** (Visibility column in `projects/scope.md`). `scripts/enrich-mirror.py` then adds `up:`/`source:` frontmatter, rewrites links to unmirrored files as GitHub URLs, and strips any credentials from the origin URL. If one still looks present, it refuses to write.
3. **Synthesize hubs.** Rewrite `repos/<repo>.md` from the mirrored docs. This roll-up is the part people actually read.
4. **Write the daily note** (and the weekly note on Monday, the week review on Saturday). It's a factual roll-up of the local logs: PULLED/SKIPPED counts, worktrees pruned, files staged. The logs themselves stay local.
5. **Regenerate links and check the graph.** `build-vault-indexes.py` (nav lines, hub link blocks, VAULT-MAP), `fix-doc-links.py --vault`, `find-orphans.py --check`.
6. **Commit by exact path** onto `obn/daily-note-<date>`: `repos/**`, the dated notes, and the files the generator reported changing. Never `git add` a whole folder.

Other scripts: `sotu.py` builds the weekly State of the Union (private repos reduced to titles only), `repo-breadcrumbs.py` adds doc indexes upstream, `analyze-loc.*` backs the LOC reports, `check-tasks-format.py` lints TASKS.md files, `export-routines.py` refreshes the routine backups.

## 4. The routines

Two fleets share one usage quota.

- **Local** scheduled tasks (`~/.claude/scheduled-tasks/`) run on this machine and can use Docker, local clones and private data.
- **Cloud** routines (claude.ai/code/routines) clone stash from GitHub, so they only ever see what's merged to `main`.

Full definitions are backed up in [[routines-backup]].

| Routine | Where | When | Writes to the vault |
|---|---|---|---|
| daily-repo-sync | local | daily | notes, repo mirrors and hubs (via the `obn:` PR) |
| daily-brief | cloud | weekdays | `reports/cloud/daily-brief/`: counts only, no mail or calendar content |
| week-sotu | local | Mon | SOTU data and report; publishes the Portfolio Checklist artifact |
| week-fin-sum | local | Mon | **nothing**: session output only, never commits |
| week-obn-import | cloud | Wed | `reports/cloud/obn-import/` health check |
| week-eng-mini | cloud | Wed | `reports/eng-mini-*` |
| ops-catchup | local | Wed | one line in `logs/ops-catchup.log` (local) |
| week-vuln | cloud | Thu | `reports/cloud/week-vuln/`: package names and public advisory IDs only |
| week-eng-loc | cloud | Thu | `reports/eng-loc-*` |
| monthly tire-kick / pmo / usage / rsi | local | 28th, 1st, 1st, 2nd | ledger, audit, usage and RSI reports |

The monthlies run a usage preflight and print `DEFERRED:` instead of starting when quota is tight. `ops-catchup` re-schedules them after the weekly reset.

## 5. Keeping private data out (semi-public by design)

The vault is public on purpose: cloud routines need to read it, and the roll-ups are useful to show. So the protection is layered. Any single layer can fail without a leak.

| Layer | What it stops |
|---|---|
| **1. Exclusion**: `.gitignore` plus `app.json` `userIgnoreFilters` | Logs, plugin data and keys, embeddings, workspace state and `.env` can't be staged by accident while they're untracked. An ignore rule doesn't cover a file that's already tracked (see rule 6 below) |
| **2. Source discipline**: `sync-repos.ps1` | Only merged, committed docs of **public** repos are mirrored. Never a working tree, a branch, or a private repo |
| **3. URL hygiene**: `enrich-mirror.py` | Credentials embedded in a remote URL never reach a `source:` link |
| **4. Prompt rules** in every publishing routine | daily-brief: counts only. week-vuln, TIRE: package names and public advisory IDs only. SOTU: private repos reduced to titles. fin-sum: never commits. USAGE: never scrapes platforms or handles credentials |
| **5. Merge gates**: `check-generated-diff.py`, the obn author/fork filter | Routines can auto-merge only their own generated files |
| **6. Pre-commit hook** (`.githooks/pre-commit`; enable with `git config core.hooksPath .githooks`) | gitleaks on staged changes, plus `pii-scan.sh` on staged files in the scanned folders |
| **7. CI** | `pii-scan.sh` (emails, phone numbers, token formats) over reports, notes, projects, prompts, topics, templates and routines; gitleaks over every new commit. A leaky report can't auto-merge |

`pii-scan.sh` prints file and line only, never the match, so CI logs don't become a second copy of a leak.

### Rules for anything new that writes here

1. **Decide the tier first.** Is it raw (keep it local: `logs/`, a gitignored path, or session output only) or a roll-up (commit it)? If you're unsure, it's raw.
2. **Roll-ups carry counts, statuses and public identifiers.** No names, addresses, email or calendar content, amounts, health or job-search details, or anything copied from a private repo beyond titles.
3. **Write the rule into the routine's prompt.** "stash is PUBLIC: …", plus an explicit list of what the report **may** contain. An allow-list holds up better than a deny-list.
4. **Publish through a PR** that CI gates. Never push straight to `main`.
5. **New folder?** Add it to the default scope in `pii-scan.sh` and to the `case` in `.githooks/pre-commit`.
6. **New plugin?** Confirm its `data.json` is ignored (`git check-ignore -v <path>`). If the file was ever committed, `git rm --cached` it, because an ignore rule doesn't untrack a file that's already tracked.
7. **New private repo?** Mark it `**private**` in scope.md's Visibility column before the next sync.

### Audit, 2026-09-30

Full-repo scans: `pii-scan.sh` over every tracked folder, and gitleaks over all 230 commits on `main`.

Fixed in this change:

- **The private `deployer` repo's docs were mirrored into the public vault** from 2026-09-16 (six files under `repos/deployer/`). They held no credentials, only placeholder env var names, but private-repo content shouldn't be public at all. The mirror is deleted and `sync-repos.ps1` now skips private repos. The `repos/deployer.md` hub (a roll-up) remains.
- **Three personal email addresses** in `projects/docs/MONEY-MAKERS.md` were replaced with role labels.
- **`smart-connections/data.json`** was tracked despite the ignore rule. It's untracked now.
- **gitleaks history scan:** 2 findings, both the already-triaged Jira `clientKey` installation IDs. The allowlist regex never matched them in git mode, which is fixed now, so all 230 commits scan clean.
- **The PII scan only covered `reports/` and `notes/`.** It now also covers projects, prompts, topics, templates and routines, in both CI and the pre-commit hook.

Still open. These need a human decision:

- **Git history still holds the removed content** (the deployer mirror, the email addresses). Deleting a file doesn't remove it from history. Purging it means rewriting history (`git filter-repo`) and force-pushing `main`, which breaks every open PR and clone. The alternative is accepting the exposure: the deployer docs are low sensitivity, and the addresses are already known to correspondents.
- **`projects/remora/remora.accdb`** (a 16 MB Access DB from 2023) contains an employer-domain email address. Binary files aren't scanned. Decide whether the file should be public at all.
- **`repos/kryptos/docs/TASKS.md`** mirrors a third party's email address from the public kryptos repo. Fix it upstream; the next sync picks up the change.
- **The eng-mini and eng-loc cloud prompts** still say `agent/reports/` is gitignored. It has been tracked since 2026-09-24. Harmless (`git add -f` still works), but the claim is stale.

### Follow-up sweep, 2026-10-01

The default `pii-scan.sh` scope covers only the routine-written folders, so this pass ran it over **every tracked path** and ran gitleaks over the full history (239 commits on `main`, clean) and the working tree. It also grepped for categories regex can't catch: income, holdings, health, relationships and location.

Fixed:

- **Personal memory exports** `projects/ARGUS/user_memory_index.csv` and `usermem2.csv` (location, vehicles, health and fitness goals) were removed. The Odysseus ecosystem CSV lost one personal detail.
- **Career and CFO prompts** carried an income figure and health context. Both now point at a local file under `~/.claude/private/` that's read if it exists and never committed.
- **Two daily-checkin reports** had health-adjacent "grounding thoughts"; they were reworded.
- **kryptos third-party email:** fixed upstream (nitsuah/kryptos#237) and in the mirror.
- **`.playwright-mcp/`** browser snapshots (signed-out GitHub pages, nothing personal) were committed by accident in #157. They're removed and gitignored.

Remaining whole-tree scan hits are placeholders (example email, 555 phone number, an `.env.example` Slack token stub), a test fixture, and a client business's public contact address in the skyview mirror.

Private context for a prompt goes in `~/.claude/private/<agent>-context.md`, never in the vault.
