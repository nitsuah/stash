# eng-mini: skyview — 2026-09-23 (REPORT MODE / DRY RUN)

> 🧭 [[repos/skyview|skyview]] · ← [[reports/eng-mini-skyview-2026-09-16|2026-09-16]] <!-- nav -->

> Report only — no moves executed, no changes made to the target repo. Selected as one of the 3 most recently updated in-scope repos (last commit 2026-09-19T07:43:16Z / 2026-09-19T03:43:12-04:00, PR #139 "Native operator scheduling" — real feature work, not an automated metrics-bot commit). Repo discovery used `search_repositories` (`user:nitsuah`, sort=updated) and root-file discovery used `search_code` (`repo:nitsuah/skyview path:/`), since this session's git proxy scopes direct repo/content access (`get_file_contents`, `list_commits`) to `nitsuah/stash` only. **Root listing caveat:** the repo reports `total_count: 21` root entries but `search_code` returned only 20 — GitHub's code-search index is known to exclude some generated/lockfile-shaped files (e.g. `package-lock.json`) and possibly `.gitignore`; the missing entry is most likely one of those two and is not expected to change the findings below (both are required-root regardless).

## Root Audit — skyview/

| File | Category | MINI Rule | Proposed Action |
|------|----------|-----------|-----------------|
| `.dockerignore` | Build/Deploy | Docker reads from build context root | **KEEP** |
| `.env.example` | Config/Env | Must stay root | **KEEP** |
| `.pre-commit-config.yaml` | Config | Root OR `config/` accepted per MINI.md Overseer table — but needs `--config` flag added to scripts/CI/hooks (`core.hooksPath` gotcha documented in MINI.md) | **CANDIDATE-MOVE → config/** |
| `CHANGELOG.md` | Documentation | root OR `docs/` accepted; `docs/` already exists in this repo | **MOVE → docs/** |
| `config.js` | App runtime | Client-side config loaded by `index.html`/other scripts at a root-relative path | **KEEP** (unknown blast radius of a path change; not a documented MINI candidate) |
| `docker-compose.dev.yml` | Build/Deploy | Compose files conventionally sit beside the Dockerfile they orchestrate | **KEEP** |
| `Dockerfile` | Build/Deploy | Must stay root | **KEEP** |
| `Dockerfile.dev` | Build/Deploy | Same build-context-root constraint as `Dockerfile` | **KEEP** |
| `FEATURES.md` | Documentation | root OR `docs/` accepted | **MOVE → docs/** |
| `index.html` | App entry point | Static-site entry point must stay root | **KEEP** |
| `LICENSE` | Legal | Overseer decision — flag for human review | **DEFER (Overseer)** |
| `METRICS.md` | Documentation | Protected until global doc folder standards are established | **KEEP** |
| `netlify.toml` | Build/Deploy | Netlify reads from repo root | **KEEP** |
| `package.json` | Package Manifest | Must stay root | **KEEP** |
| `playwright.config.ts` | Config | Root OR `config/` — MINI.md's own tool-specific table documents the exact path fix needed (`testDir`/`globalSetup` resolve from config location, not CWD) | **CANDIDATE-MOVE → config/** |
| `README.md` | Documentation | root-only (deploy badges) | **KEEP** |
| `robots.txt` | Web convention | Must be served at `/robots.txt` | **KEEP** |
| `ROADMAP.md` | Documentation | Explicit Overseer note: do not move without validation | **DEFER (Overseer)** |
| `SETUP.md` | Documentation | Not covered by MINI.md's root-or-docs table; 10 inbound references found | **UNKNOWN — deferred (destination unclear + high reference count)** |
| `sitemap.xml` | Web convention | Must be served at `/sitemap.xml`, referenced by `robots.txt` | **KEEP** |
| `TASKS.md` | Documentation | Explicit Overseer note: do not move without validation | **DEFER (Overseer)** |

## Proposed Moves (Dry Run — Not Executed)

| From | To | Risk | Rationale |
|------|-----|------|-----------|
| `CHANGELOG.md` | `docs/CHANGELOG.md` | **Low** | 0 inbound references found |
| `FEATURES.md` | `docs/FEATURES.md` | **Low** | 4 references to update, but `docs/` is an established location in this repo and Overseer already accepts `docs/features.md` |
| `.pre-commit-config.yaml` | `config/.pre-commit-config.yaml` | **Medium** | Needs `--config` flag added to scripts, CI, and (if `core.hooksPath` is Husky-managed) a direct edit of `.git/hooks/pre-commit` per MINI.md's documented gotcha |
| `playwright.config.ts` | `config/playwright.config.ts` | **Medium** | `testDir`/`globalSetup` paths resolve from the config file's own location, not CWD — every relative path inside the config needs a `../` prefix per MINI.md's tool-specific table |

## References That Would Need Updating

| File | Reference |
|------|-----------|
| `CHANGELOG.md` | `FEATURES.md` |
| `docs/archive/README.md` | `FEATURES.md` |
| `README.md` | `FEATURES.md` |
| `ROADMAP.md` | `FEATURES.md` |

`CHANGELOG.md` itself has no inbound references from other tracked files.

## Files Left Exempt (with rationale)

| File | Reason |
|------|--------|
| `README.md` | Root-only per MINI.md (deploy badges live here) |
| `LICENSE` | Overseer decision — requires human review |
| `METRICS.md` | Explicitly protected in MINI.md until global doc folder standards are established |
| `index.html`, `robots.txt`, `sitemap.xml` | Static-site/crawler conventions require root-relative URLs |
| `config.js` | Runtime config with unverified consumers; left in place absent a documented MINI rule |
| `package.json` / `Dockerfile` / `Dockerfile.dev` / `docker-compose.dev.yml` / `.dockerignore` / `netlify.toml` | Standard root-required build/tooling/deploy files |
| `.env.example` | Standard root-required file |

## Overseer Decisions Required

| Item | Recommendation | Notes |
|------|----------------|-------|
| `LICENSE` | Consider `.github/LICENSE` | Per MINI.md — requires human validation of root sensitivity |
| `ROADMAP.md` | Hold at root | Per MINI.md Overseer note |
| `TASKS.md` | Hold at root | Per MINI.md Overseer note |
| `SETUP.md` | Needs an explicit MINI.md rule | Not in the root-or-docs table at all; 10 references (`docs/archive/*`, `docs/GETTING_STARTED.md`, `docs/OWNER_GUIDE.md`, `README.md`) make any move high-effort regardless of destination |

## Out-of-Scope Observations (not a root-file move, flagging for CLEANUP)

- `docs/archive/` already holds several superseded setup docs (`MANUAL_SETUP.md`, `CONFIG_README.md`, `QUICKSTART.md`, `PROJECT_STATUS.md`, `QUICK_REFERENCE.md`, `SESSION_SUMMARY.md`) alongside the still-referenced `SETUP.md` at root — worth a CLEANUP pass to confirm which are genuinely superseded vs. still authoritative.

## Errors Encountered

- `search_code path:/` for this repo returned 20 of a reported 21 root entries (see caveat above). No other errors.

## Suggested Follow-up

1. Execute the two low-risk doc moves (`CHANGELOG.md`, `FEATURES.md`) on a dedicated `mini/skyview/root-hygiene-2026-09-23` branch, updating the 4 references listed above, then open a PR per MINI.md branch/PR governance.
2. Bring `LICENSE`, `ROADMAP.md`, `TASKS.md`, and `SETUP.md` (destination-unclear) to the Overseer.
3. If the Overseer confirms `config/` as a valid destination for tooling configs in this repo, execute the two medium-risk config moves (`.pre-commit-config.yaml`, `playwright.config.ts`) as a separate, more carefully validated pass — each needs the specific path-resolution fixes MINI.md documents, not a blind move.

---

*Report generated by eng-mini (report mode / dry run) — no changes made to `nitsuah/skyview`.*
