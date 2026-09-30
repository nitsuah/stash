---
HEAD: eeaa7557d987173957ff9c221980c5daf4ca6cce
kind: eng-mini
repo: farm-3j
date: 2026-09-30
---

# eng-mini: farm-3j — 2026-09-30 (REPORT MODE / DRY RUN)

> 🧭 [[repos/farm-3j|farm-3j]] <!-- nav -->

> Report only — no moves executed, no changes made to the target repo. Selected as the #2 most recently active tracked repo (`git log -1 --format=%ci` from a fresh `--depth 1` clone: 2026-09-30T14:04:37Z, HEAD `eeaa755` "chore(deps): bump typescript-eslint from 8.70.0 to 8.70.1 (#364)"). Root audited from a throwaway clone at `/tmp/mini-scan/farm-3j`. First eng-mini report for this repo — no prior report to diff against.

## Root Audit — farm-3j/

| File | Category | MINI Rule | Proposed Action |
|------|----------|-----------|-----------------|
| `.dockerignore` | Build/Deploy | Docker reads from build context root; moving without Dockerfile breaks build | **KEEP** |
| `.env.example` | Config/Env | Must stay root | **KEEP** |
| `.gitattributes` | VCS | Must stay root | **KEEP** |
| `.github/` | CI | Must stay root | **KEEP** |
| `.gitignore` | VCS | Must stay root | **KEEP** |
| `.nvmrc` | Tooling | `nvm`/Node version managers read it from the invocation directory; convention is repo root | **KEEP** |
| `CHANGELOG.md` | Documentation | root OR `docs/` accepted; no `docs/CHANGELOG.md` exists, so no duplicate | **DEFER** — low-risk candidate-move to `docs/CHANGELOG.md` for consistency with `docs/{FEATURES,METRICS,ROADMAP,TASKS}.md`, but optional (root is already a valid location, no functional issue) |
| `Dockerfile` | Build/Deploy | Must stay root | **KEEP** |
| `LICENSE` | Legal | **Decided 2026-09-24: stays at root in every repo** | **KEEP** |
| `README.md` | Documentation | root-only | **KEEP** |
| `components.json` | Tooling | shadcn/ui CLI reads this from the project root by convention | **KEEP** |
| `coverage_summary.txt` | Generated artifact | Tracked in git, not referenced by any config/script/doc; `/coverage` (the actual coverage dir) is gitignored but this summary file isn't | **OUT OF SCOPE** — looks like a stray committed build artifact, not a misplaced source file; flagged below |
| `global.d.ts` | TS source | Matched by `tsconfig.json`'s `"**/*.ts"` include glob regardless of location — not root-pinned by tooling | **DEFER** — no canonical destination folder (e.g. `types/`) exists yet; per MINI.md, keep in place when destination is unclear |
| `next.config.mjs` | Framework config | Next.js requires this at project root | **KEEP** |
| `package.json` | Manifest | Must stay root | **KEEP** |
| `pnpm-lock.yaml` | Lockfile | Must stay root | **KEEP** |
| `postcss.config.mjs` | Build/Deploy | Next.js/PostCSS convention reads from root | **KEEP** |
| `tsconfig.json` | Tooling | TypeScript and most editors/tools resolve this from root | **KEEP** |

Root-level directories (`app/`, `components/`, `config/`, `docs/`, `lib/`, `patches/`, `public/`, `scripts/`, `styles/`) are pre-existing and already organized — no action, out of MINI's root-*file*-hygiene scope. Notably `config/` already exists and holds `docker-compose*.yml`, `eslint.config.mjs`, `vitest.config.mjs`, `vitest.setup.ts` — this repo has already had a prior config reorg pass.

## Duplicate / Destination Checks

Checked root vs. `docs/` for ROADMAP, TASKS, FEATURES, METRICS, CHANGELOG, CONTRIBUTING: `docs/` holds `FEATURES.md`, `METRICS.md`, `ROADMAP.md`, `TASKS.md` (root has none of these — no duplicate). `CHANGELOG.md` exists only at root (no `docs/` copy — no duplicate). No conflicts found.

## Proposed Moves (Dry Run — Not Executed)

**None.** `CHANGELOG.md` → `docs/CHANGELOG.md` is a plausible low-risk consistency move but not required (root is a valid, already-working location); left as a deferred/optional item rather than a firm proposal since it has no functional upside beyond matching siblings.

## References That Would Need Updating

N/A — no moves proposed this run.

## Files Left Exempt (with rationale)

| File | Reason |
|------|--------|
| `README.md` | Root-only per MINI.md |
| `LICENSE` | Root-placement decided 2026-09-24 |
| `Dockerfile` / `.dockerignore` | Docker build context reads both from root |
| `.env.example` / `.gitattributes` / `.gitignore` / `.nvmrc` | Standard root-required files |
| `next.config.mjs` / `postcss.config.mjs` / `components.json` / `tsconfig.json` / `package.json` / `pnpm-lock.yaml` | Framework/tooling conventions require root location |

## Overseer Decisions Required

None. (`LICENSE` is resolved per the 2026-09-24 decision.)

## Out-of-Scope Observations

- `coverage_summary.txt` at root appears to be a stray, unreferenced committed artifact (last touched incidentally by an unrelated dependency-bump commit, not by any coverage-generating script or CI step found in this pass). `/coverage` itself is gitignored but this summary file isn't. Recommend a human confirm whether it's still needed; if not, removal is a deletion and out of scope for this non-destructive pass.
- `global.d.ts` would be a reasonable candidate for a `types/` directory if one is ever introduced, but creating a new folder for a single file is a broader reorg than this pass should make unilaterally.

## Errors Encountered

None — root read from a clean `--depth 1` clone at `/tmp/mini-scan/farm-3j`.

## Suggested Follow-up

1. No moves to execute this run — root is already well-organized (this repo has previously had files sorted into `config/`, `docs/`, `scripts/`, etc.).
2. Human review: is `coverage_summary.txt` still needed at root, or can it be removed / added to `.gitignore`?
3. Optional, non-urgent: move `CHANGELOG.md` → `docs/CHANGELOG.md` for consistency with the other planning docs, on a dedicated `mini/farm-3j/root-hygiene-2026-09-30` branch if/when a human wants to action it.

---

*Report generated by eng-mini (report mode / dry run) — no changes made to `nitsuah/farm-3j`.*
