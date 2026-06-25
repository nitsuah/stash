# OVERSEER Agent: Multi-Location File Detection

You are working in the `overseer` repo — a Next.js app that monitors repo health across the org.

repo: [[repos/overseer/README|README]]
## Mission

Update overseer's file detection logic so repos are not penalized for organizing files into `docs/` or `config/` subdirectories. All detection must grandfather root locations (existing repos should keep their current scores) while also accepting the new preferred locations as equally valid.

## Context

A MINI cleanup pass moved several files out of repo roots:

- Documentation files (ROADMAP.md, TASKS.md, FEATURES.md, METRICS.md, CHANGELOG.md, CONTRIBUTING.md) → `docs/`
- Config files (.pre-commit-config.yaml, .pylintrc) → `config/`

Overseer currently scores these as missing after the move. The goal is: **presence in `docs/` or `config/` counts as present — no downgrade, no warning.**

## How detection works (read this before touching anything)

Detection runs in `lib/sync.ts`. It calls `github.getRepoFileList()` which recursively walks the entire repo and returns **full paths** (e.g. `docs/ROADMAP.md`, `config/.pre-commit-config.yaml`, `.github/workflows/ci.yml`). The file list is already complete — no path is hidden.

Checks receive this list and match against it. Most checks lowercase the list first:

```typescript
const lowerFiles = fileList.map(f => f.toLowerCase());
```

**Substring matches** (`.some(f => f.includes('vitest.config'))`) already find files in subdirectories — no change needed for those.

**Exact path matches** (`.includes('roadmap.md')`) only match root — these need to be updated.

---

## Files to change

### 1. `lib/doc-health.ts` — documentation file detection

Audit every file existence check. For each doc file that can live in `docs/`, change:

```typescript
// Before
lowerFiles.includes('roadmap.md')

// After
lowerFiles.includes('roadmap.md') || lowerFiles.includes('docs/roadmap.md')
```

Apply this pattern to all of:

- `roadmap.md`
- `tasks.md`
- `features.md`
- `metrics.md`
- `changelog.md`
- `contributing.md` (also check `docs/contributing.md` in addition to existing `.github/contributing.md`)

**Do NOT change** `readme.md` — README stays root-only.

When a file is found at a non-root location, update the `details` field to include `foundAt: <actual path>` so the UI can surface this informationally. Status should be `healthy` regardless of whether it was found at root or in `docs/`.

### 2. `lib/best-practices.ts` — config file detection

Audit the `pre_commit_hooks` check. It likely checks for `.pre-commit-config.yaml` as an exact path. Update to also accept `config/.pre-commit-config.yaml`:

```typescript
// Before
const hasPreCommitConfig = lowerFiles.includes('.pre-commit-config.yaml');

// After
const hasPreCommitConfig = lowerFiles.includes('.pre-commit-config.yaml') ||
                           lowerFiles.includes('config/.pre-commit-config.yaml');
```

Also check the `linting` detection for `.pylintrc`:

```typescript
// Before
lowerFiles.includes('.pylintrc')

// After
lowerFiles.includes('.pylintrc') || lowerFiles.includes('config/.pylintrc')
```

For all other config checks (vitest, eslint, jest, playwright, etc.) — verify they use substring matching (`.some(f => f.includes('...'))`). If any use exact `.includes('filename')` equality, convert to substring matching. If they already use substring matching, leave them alone.

### 3. `lib/community-standards.ts` — community standards detection

Check `changelog` detection specifically — it may use exact path matching. Update to also accept `docs/changelog.md`.

Check `contributing` detection — update to also accept `docs/contributing.md` alongside existing `contributing.md` and `.github/contributing.md`.

FLOW-TASKS (`flow_tasks_prompt`) and HANDOFF (`handoff_prompt`) currently check `.github/prompts/flow-tasks.md` and `.github/prompts/handoff.md` respectively. These are repo-local only with no org fallback. **Leave them as-is for now** — do not add org fallback unless explicitly requested separately.

---

## What NOT to change

- `README.md` — root only, no `docs/` fallback
- `LICENSE` — root only
- `.gitignore` — root only
- `.env.example` / `.env.template` — root only
- `Dockerfile` / `docker-compose.yml` — root only
- Any `.github/` paths — already at a non-root location, no change needed
- Branch protection check — GitHub API, no file paths involved
- CI/CD check — already uses substring on workflow file paths
- Deploy badge check — scans README.md content, no path change needed
- Dependabot check — `.github/dependabot.yml`, already correct

---

## Details field convention

When you update a check to support multiple locations, record the actual found path in details so the UI can use it later. Pattern:

```typescript
const roadmapPath = lowerFiles.includes('roadmap.md') ? 'ROADMAP.md'
                  : lowerFiles.includes('docs/roadmap.md') ? 'docs/ROADMAP.md'
                  : null;

{
    type: 'roadmap',
    status: roadmapPath ? 'healthy' : 'missing',
    details: {
        exists: !!roadmapPath,
        foundAt: roadmapPath,  // add this
    }
}
```

Use the original casing of the path, not lowercase, in `foundAt`.

---

## Required validation before committing

1. Run `npm run typecheck` — no TypeScript errors.
2. Run `npm test` — all existing tests pass.
3. If there are tests for the detection functions in `lib/`, add test cases covering:
   - File found at root path → `healthy`
   - File found at `docs/` path → `healthy`
   - File found at `config/` path → `healthy`
   - File absent entirely → `missing`
4. Do a manual audit: search the codebase for every string `'roadmap'`, `'tasks'`, `'features'`, `'metrics'`, `'pre-commit-config'`, `'pylintrc'` to make sure you haven't missed any detection sites.

---

## Branch and PR

Branch: `feat/multi-location-file-detection`  
PR title: `feat(detection): accept docs/ and config/ as valid file locations`  
PR body should include a table mapping each updated check to the paths it now accepts.

## Related

- `stash/agent/prompts/MINI.md` — MINI run that prompted this change; includes the full table of moved files per repo
- `stash/agent/projects/MINI/2026-06-20-root-cleanup.md` — per-repo move log with exact old → new paths
