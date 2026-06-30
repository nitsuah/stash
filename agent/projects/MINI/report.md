# Root Directory Minimization Opportunities

This report summarizes files in the root directories of various repositories that are candidates for relocation, following the guidelines set out in `MINI.md`. The goal is to reduce clutter in the root folder by moving documentation, configuration, scripts, and other non-critical files to more appropriate subdirectories, thereby improving repository organization and discoverability without breaking core functionality.

## Summary Table of Files Applicable for Minimization

The table below lists each repository and the count of files found in its root directory that are identified as applicable for minimization according to the `MINI.md` rules. These counts reflect files that are candidates for moving to subdirectories like `docs/`, `config/`, `scripts/`, `data/`, `logs/`, or `artifacts/`.

| Repository | Files Applicable for MINI (Count) |
| :--------- | :-------------------------------- |
| `stash` | 5 |
| `9router` | 8 |
| `motor-pool` | 5 |
| `auto-apply-plugin` | 6 |
| `darkmoon` | 8 |
| `farm-3j` | 11 |
| `fire` | 8 |
| `games` | 10 |
| `kryptos` | 7 |
| `nitsuah-io` | 10 |
| `odysseus` | 20 |
| `overseer` | 15 |
| `vhs` | 15 |

## Detailed Breakdown of Minimization Opportunities

### `stash`

**Files Proposed for Moving:**
- `CHANGELOG.md` → `docs/CHANGELOG.md`
- `FEATURES.md` → `docs/FEATURES.md`
- `METRICS.md` → `docs/METRICS.md`
- `ROADMAP.md` → `docs/ROADMAP.md`
- `TASKS.md` → `docs/TASKS.md`

**Key Considerations:**
- All proposed moves are documentation files to an existing `docs/` folder, which is low risk.
- The `README.md` reference to `FEATURES.md` would need an update.

### `9router`

**Files Proposed for Moving:**
- `CHANGELOG.md` → `docs/CHANGELOG.md`
- `DOCKER.md` → `docs/DOCKER.md`
- `README.zh-CN.md` → `docs/README.zh-CN.md`
- `captain-definition` → `config/captain-definition`
- `custom-server.js` → `scripts/custom-server.js`
- `eslint.config.mjs` → `config/eslint.config.mjs`
- `jsconfig.json` → `config/jsconfig.json`
- `next.config.mjs` → `config/next.config.mjs`
- `postcss.config.mjs` → `config/postcss.config.mjs`

**Key Considerations:**
- Moving config files (ESLint, Next.js, PostCSS, JSConfig) to `config/` will require explicit path updates in scripts/CI, as highlighted in `MINI.md`.

### `motor-pool`

**Files Proposed for Moving:**
- `CHANGELOG.md` → `docs/CHANGELOG.md`
- `FEATURES.md` → `docs/FEATURES.md`
- `METRICS.md` → `docs/METRICS.md`
- `ROADMAP.md` → `docs/ROADMAP.md`
- `TASKS.md` → `docs/TASKS.md`

**Key Considerations:**
- All proposed moves are documentation files to an existing `docs/` folder, which is low risk.

### `auto-apply-plugin`

**Files Proposed for Moving:**
- `CHANGELOG.md` → `docs/CHANGELOG.md`
- `FEATURES.md` → `docs/FEATURES.md`
- `METRICS.md` → `docs/METRICS.md`
- `ROADMAP.md` → `docs/ROADMAP.md`
- `TASKS.md` → `docs/TASKS.md`
- `c.txt` → `data/c.txt` (or delete)

**Key Considerations:**
- `c.txt` should be investigated; moving config files (`.eslintrc.json`) might require updates.

### `darkmoon`

**Files Proposed for Moving:**
- `CHANGELOG.md` → `docs/CHANGELOG.md`
- `FEATURES.md` → `docs/FEATURES.md`
- `METRICS.md` → `docs/METRICS.md`
- `ROADMAP.md` → `docs/ROADMAP.md`
- `TASKS.md` → `docs/TASKS.md`
- `netlify.toml` → `config/netlify.toml`
- `render.yaml` → `config/render.yaml`
- `tsconfig.json` → `config/tsconfig.json`
- `vite.config.js` → `config/vite.config.js`
- `C:Usersajharcoderouter4c.txt` → Delete or investigate (artifact)
- `c.txt` → `data/c.txt` (or delete)

**Key Considerations:**
- Artifacts (`C:Users...c.txt`, `c.txt`) require investigation/removal.
- Moving config files (Netlify, Render, TSConfig, Vite) to `config/` will require updates in build/deployment config.

### `farm-3j`

**Files Proposed for Moving:**
- `CHANGELOG.md` → `docs/CHANGELOG.md`
- `FEATURES.md` → `docs/FEATURES.md`
- `METRICS.md` → `docs/METRICS.md`
- `ROADMAP.md` → `docs/ROADMAP.md`
- `TASKS.md` → `docs/TASKS.md`
- `components.json` → `config/components.json`
- `coverage_summary.txt` → `reports/coverage_summary.txt`
- `global.d.ts` → `lib/global.d.ts`
- `next-env.d.ts` → `lib/next-env.d.ts`
- `next.config.mjs` → `config/next.config.mjs`
- `postcss.config.mjs` → `config/postcss.config.mjs`
- `tsconfig.json` → `config/tsconfig.json`
- `tsconfig.tsbuildinfo` → `config/tsconfig.tsbuildinfo`

**Key Considerations:**
- `pyproject.toml` is strongly recommended to stay at root.
- Moving config files, TypeScript declaration files, and coverage reports to subdirectories will require updates to build scripts, IDE configurations, or the TypeScript compilation process.

### `fire`

**Files Proposed for Moving:**
- `CHANGELOG.md` → `docs/CHANGELOG.md`
- `FEATURES.md` → `docs/FEATURES.md`
- `METRICS.md` → `docs/METRICS.md`
- `ROADMAP.md` → `docs/ROADMAP.md`
- `TASKS.md` → `docs/TASKS.md`
- `c.txt` → `data/c.txt` (or delete)
- `coverage_summary.txt` → `reports/coverage_summary.txt`
- `C:Usersajharcoderouter4c.txt` → Delete or investigate (artifact)

**Key Considerations:**
- Artifacts (`C:Users...c.txt`, `c.txt`) require investigation/removal.
- `.prettierrc` should remain at root due to editor behavior, as per `MINI.md` note.

### `games`

**Files Proposed for Moving:**
- `CHANGELOG.md` → `docs/CHANGELOG.md`
- `FEATURES.md` → `docs/FEATURES.md`
- `METRICS.md` → `docs/METRICS.md`
- `ROADMAP.md` → `docs/ROADMAP.md`
- `TASKS.md` → `docs/TASKS.md`
- `extracted_tools.txt` → `logs/extracted_tools.txt`
- `netlify.toml` → `config/netlify.toml`
- `tool_calls.log` → `logs/tool_calls.log`
- `tool_counts.txt` → `logs/tool_counts.txt`
- `C:Usersajharcodegamesc.txt` → Delete or investigate (artifact)
- `c.txt` → `data/c.txt` (or delete)

**Key Considerations:**
- Artifacts (`C:Users...c.txt`, `c.txt`) require investigation/removal.
- Moving `netlify.toml` might require updates to CI/CD pipelines.

### `kryptos`

**Files Proposed for Moving:**
- `CHANGELOG.md` → `docs/CHANGELOG.md`
- `FEATURES.md` → `docs/FEATURES.md`
- `METRICS.md` → `docs/METRICS.md`
- `ROADMAP.md` → `docs/ROADMAP.md`
- `TASKS.md` → `docs/TASKS.md`
- `.coverage` → `artifacts/.coverage`
- `.coveragerc` → `config/.coveragerc`
- `coverage_run.log` → `logs/coverage_run.log`
- `pyproject.toml` → `config/pyproject.toml` (Strongly recommended to stay at root)

**Key Considerations:**
- **Strongly recommend keeping `pyproject.toml` at the root.**
- Moving `.coverage` and `.coveragerc` might require updates to test runners or CI configurations.

### `nitsuah-io`

**Files Proposed for Moving:**
- `CHANGELOG.md` → `docs/CHANGELOG.md`
- `FEATURES.md` → `docs/FEATURES.md`
- `METRICS.md` → `docs/METRICS.md`
- `ROADMAP.md` → `docs/ROADMAP.md`
- `TASKS.md` → `docs/TASKS.md`
- `.eslintrc.json` → `config/.eslintrc.json`
- `netlify.toml` → `config/netlify.toml`
- `next-env.d.ts` → `lib/next-env.d.ts`
- `next.config.js` → `config/next.config.js`
- `tsconfig.json` → `config/tsconfig.json`
- `tsconfig.tsbuildinfo` → `config/tsconfig.tsbuildinfo`

**Key Considerations:**
- Moving config files and TypeScript declaration files will require updates in build/CI configuration or IDE settings.

### `odysseus`

**Files Proposed for Moving:**
- `ACKNOWLEDGMENTS.md` → `docs/ACKNOWLEDGMENTS.md`
- `CONTRIBUTING.md` → `docs/CONTRIBUTING.md`
- `Odysseus.spec` → `config/Odysseus.spec`
- `ROADMAP.md` → `docs/ROADMAP.md`
- `SECURITY.md` → `docs/SECURITY.md`
- `THREAT_MODEL.md` → `docs/THREAT_MODEL.md`
- `app.py` → `src/app.py`
- `build-macos-app.sh` → `scripts/build-macos-app.sh`
- `build-windows-portable.ps1` → `scripts/build-windows-portable.ps1`
- `debug.log` → `logs/debug.log`
- `docker-compose.gpu-amd.yml` → `docker/docker-compose.gpu-amd.yml`
- `docker-compose.gpu-nvidia.yml` → `docker/docker-compose.gpu-nvidia.yml`
- `install-service.sh` → `scripts/install-service.sh`
- `launch-windows.ps1` → `scripts/launch-windows.ps1`
- `launcher.py` → `src/launcher.py`
- `odysseus-ui.service` → `config/odysseus-ui.service`
- `pyproject.toml` → `config/pyproject.toml` (Strongly recommended to stay at root)
- `requirements-optional.txt` → `config/requirements-optional.txt`
- `requirements.txt` → `config/requirements.txt`
- `setup.py` → `scripts/setup.py`
- `start-macos.sh` → `scripts/start-macos.sh`
- `update_windows.bat` → `scripts/update_windows.bat`

**Key Considerations:**
- **High Risk:** `pyproject.toml` should likely remain at root.
- Many core application/build scripts and Docker compose overrides are proposed for moving, requiring extensive path updates across the codebase, build system, and service installations.

### `overseer`

**Files Proposed for Moving:**
- `CHANGELOG.md` → `docs/CHANGELOG.md`
- `FEATURES.md` → `docs/FEATURES.md`
- `METRICS.md` → `docs/METRICS.md`
- `ROADMAP.md` → `docs/ROADMAP.md`
- `TASKS.md` → `docs/TASKS.md`
- `.coverage` → `coverage/.coverage`
- `.prettierignore` → `config/.prettierignore` (Conflict in `MINI.md` rules, flag for user decision)
- `.prettierrc.json` → `config/.prettierrc.json` (Conflict in `MINI.md` rules, flag for user decision)
- `auth.ts` → `lib/auth.ts`
- `c.txt` → `data/c.txt` (or delete)
- `netlify.toml` → `config/netlify.toml`
- `next-env.d.ts` → `lib/next-env.d.ts`
- `next.config.ts` → `config/next.config.ts`
- `playwright.config.ts` → `config/playwright.config.ts`
- `postcss.config.mjs` → `config/postcss.config.mjs`
- `proxy.ts` → `lib/proxy.ts`
- `tsconfig.json` → `config/tsconfig.json`
- `tsconfig.tsbuildinfo` → `config/tsconfig.tsbuildinfo`

**Key Considerations:**
- Artifact `c.txt` requires investigation/removal.
- Conflict in `MINI.md` for `.prettierrc` location (config vs. root).
- Many config and core logic files proposed for move, requiring significant updates.

### `vhs`

**Files Proposed for Moving:**
- `C:Usersajhar.claudeprojectsC--Users-ajhar-code-vhsmemoryMEMORY.md` → Delete or investigate (artifact)
- `CHANGELOG.md` → `docs/CHANGELOG.md`
- `FEATURES.md` → `docs/FEATURES.md`
- `METRICS.md` → `docs/METRICS.md`
- `ROADMAP.md` → `docs/ROADMAP.md`
- `TASKS.md` → `docs/TASKS.md`
- `c.txt` → `data/c.txt` (or delete)
- `.eslintrc.json` → `config/.eslintrc.json`
- `.htmlhintrc` → `config/.htmlhintrc`
- `jest.cjs` → `config/jest.cjs`
- `nginx.conf.template` → `config/nginx.conf.template`
- `playwright.config.js` → `config/playwright.config.js`
- `server.js` → `src/server.js`
- `start.ps1` → `scripts/start.ps1`
- `start.sh` → `scripts/start.sh`

**Key Considerations:**
- Artifacts (`C:Users...MEMORY.md`, `c.txt`) require investigation/removal.
- Moving `server.js` and many config files requires careful updates to startup scripts, build processes, and tool configurations.

This report provides a consolidated view of potential root file minimization opportunities across your repositories, identifying files that are candidates for relocation based on the `MINI.md` guidelines.
