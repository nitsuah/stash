---
week: 2026-W41
kind: sotu
---

# Light work — 2026-W41

> 🧭 [[reports/sotu/sotu-2026-W39|undated]] → <!-- nav -->

Small, well-scoped tasks pulled from the [[sotu-2026-W41]] open-work list, for cheaper models (Sonnet/Haiku) while the weekly quota is low. Each repo has one paste-ready prompt that batches its tasks into a single branch and PR. Agents open the PR and stop; merging stays with a human or the next Opus session.

Left out on purpose: anything that needs the owner's accounts, credentials, wallet or DNS (ats-fill CWS token, skyview launch/email/analytics, nitsuah-io Amoy redeploy), real computer-vision or GPU work (vhs), product design calls (fire Drive round-trip P0, avatar notebook CI), the private `deployer` repo, and nitsuah-io ESLint (blocked on TypeScript 7 support upstream; see its TASKS P2).

## Task table

| Repo | # | Task | Source | Model |
|---|---|---|---|---|
| fire | 1 | Normalize Side Gig Ledger form controls to the site theme | TASKS P1 | Sonnet |
| fire | 2 | eBay connect completion: toast + automatic sync | TASKS P1 | Sonnet |
| fire | 3 | Model real eBay fee brackets in `calculateEbayFeesTotal` (+ tests) | TASKS P1 | Sonnet |
| fire | 4 | Provider-contract tests for the balance integrations (prices done in #177) | TASKS P1 | Sonnet |
| fire | 5 | Fix the 3 smallest open `bot:review` issues | TASKS P1 | Sonnet |
| fire | 6 | README feature-parity pass against FEATURES.md | TASKS P1 | Haiku |
| farm-3j | 1 | Barn: buttons to train animal units | TASKS P2 | Sonnet |
| farm-3j | 2 | Save-slot picker on the New Game screen (3 cloud slots exist) | TASKS P1 | Sonnet |
| farm-3j | 3 | Minimap: show dropped items and loot crates | TASKS P3 | Sonnet |
| farm-3j | 4 | Ambient audio loop with its own volume slider | TASKS P3 | Sonnet |
| farm-3j | 5 | Refresh README + deployment notes with the real release path | TASKS P3 | Haiku |
| games | 1 | Fix the 17 pre-existing `npm run lint` errors (untracked until now) | found 2026-10-09 | Sonnet |
| games | 2 | Memory Match: persist best time/moves in localStorage | TASKS P3 | Sonnet |
| games | 3 | Dodge Blocks: touch controls for mobile | TASKS P3 | Sonnet |
| games | 4 | Check whether `eslint-plugin-react` supports ESLint 10 yet; update the P3 note | TASKS P3 | Haiku |
| stash | 1 | Dependabot: add the `pip` ecosystem (npm + actions already covered) | TASKS P3 (partly done) | Haiku |
| stash | 2 | Pre-commit: add ruff/shellcheck alongside the existing gitleaks + PII hook | TASKS P3 (partly done) | Sonnet |
| stash | 3 | Add CodeQL (python) workflow | TASKS P3 | Haiku |
| stash | 4 | Add CONTRIBUTING.md (or link the org default) | TASKS P3 | Haiku |
| stash | 5 | Link the 4 loose SOTU/script attachments into the vault graph (F-20260930-02) | ledger | Haiku |
| stash | 6 | Document the VBA sources in Remora, Sampler and VMT | TASKS P2 | Sonnet |
| nitsuah-io | 1 | Rename the stale "agent-board" showcase item to motor-pool and build the section | TASKS P3 | Sonnet |
| nitsuah-io | 2 | Variable font + fluid typography scale | TASKS P2 | Sonnet |
| nitsuah-io | 3 | Measure the Spline scene weight and write up reduction options | TASKS P3 | Haiku |
| nitsuah-io | 4 | PWA manifest (installable; offline later) | TASKS P3 | Sonnet |
| avatar | 1 | Document `build_training_command` in the README | TASKS P3 | Haiku |
| avatar | 2 | Root CONTRIBUTING.md (link to nitsuah/.github) | TASKS P3 | Haiku |
| avatar | 3 | `run_notebook.sh` helper (per its TASKS spec) | TASKS P3 | Haiku |
| avatar | 4 | Export the notebook to `examples/*.html` without executing it | TASKS P3 | Haiku |
| skyview | 1 | Dependency audit and update (non-major bumps only) | TASKS P3 | Sonnet |
| skyview | 2 | Test/tooling debt from the 2026-09 auth + scheduling pass | TASKS P3 | Sonnet |
| darkmoon | 1 | Check whether `eslint-plugin-jsx-a11y` supports ESLint 10 yet; update the P3 note | TASKS P3 | Haiku |
| darkmoon | 2 | Re-baseline the large-file refactor list (measure, rewrite the P2) | TASKS P2 | Haiku |
| osrs | 1 | Bump `nltk` if a release patches GHSA-8mgp-746c-j5xp | TASKS P3 | Haiku |

## Prompts

Every prompt carries the same rules, so each one can be pasted on its own.

### fire

```text
Repo: nitsuah/fire (local clone C:\Users\ajhar\code\fire). Do these small tasks from docs/TASKS.md in ONE branch and ONE PR. Read each item and its sub-bullets first; follow its acceptance criteria. If a task turns out bigger than ~1 hour or needs a product decision, skip it and say why.

1. P1 "Normalize Side Gig Ledger form controls to the site theme": inputs, selects and buttons use the site's existing theme classes/tokens. No new design.
2. P1 "Make eBay connection completion a toast + automatic sync": after the eBay OAuth return, show a toast and trigger one sync instead of the current behavior.
3. P1 "Model real eBay fee brackets in calculateEbayFeesTotal (app/lib/side-gig.js)": implement the brackets the item describes, with unit tests for each bracket boundary.
4. P1 "Add provider-contract tests for all price/balance integrations": price providers are covered by tests/unit/prices-provider.test.mjs (fire#177). Add contract tests for the balance integrations (mocked HTTP, no real keys). Leave the item open with a progress note if any integration remains.
5. P1 "Fix the review-pass findings (label bot:review)": `gh issue list -R nitsuah/fire --label bot:review --state open`, fix the 3 smallest, reference them with "Fixes #N". If a fix changes a Playwright baseline, regenerate it in Docker in the same PR.
6. P1 "README feature-parity and product-story refresh": make README's feature list match docs/FEATURES.md (shipped items only). No marketing rewrite.

Rules:
- New worktree, never the shared checkout: git -C C:\Users\ajhar\code\fire fetch origin; git -C C:\Users\ajhar\code\fire worktree add ..\fire-wt-light -b chore/light-w41 origin/main. Confirm worktree HEAD == origin/main before committing.
- Run npm/tests/lint ONLY in Docker: MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd -W):/app" -w /app node:22-alpine sh -c "npm ci --no-audit --no-fund >/dev/null 2>&1; npx prettier --write <changed files>; npm run lint && npx vitest run --config config/vitest.config.ts <test files>". Lint must pass (prettier runs through ESLint).
- Tick each finished TASKS item ([x] + "Done 2026-10-<dd>: ..." sub-bullet), and add docs/CHANGELOG.md entries under Unreleased in the existing style.
- Commit with a "Co-Authored-By: Claude <model> <noreply@anthropic.com>" trailer, push, open a non-draft PR with gh pr create (body ends with "🤖 Generated with [Claude Code](https://claude.com/claude-code)"). Do NOT merge. Remove the worktree after pushing.
- Report: PR URL, which tasks were done or skipped (and why), and test/lint results.
```

### farm-3j

```text
Repo: nitsuah/farm-3j (local clone C:\Users\ajhar\code\farm-3j; pnpm). Do these small tasks from docs/TASKS.md in ONE branch and ONE PR. Read each item first; skip anything that grows past ~1 hour and say why.

1. P2 "Add buttons to train animal units from Barn": a Barn panel with train buttons, reusing the existing unit-training UI pattern and costs.
2. P1 "Save-slot picker UI on the New Game screen (3 cloud-backed slots already shipped)": pick a slot (show empty/used + last-saved time) before starting. Use the existing slot API.
3. P3 "Minimap: show dropped items and loot crate positions": small markers in distinct colors.
4. P3 "Background ambient audio loop with independent volume slider": loop an existing or tiny royalty-free asset; the slider persists in settings.
5. P3 "Refresh README and deployment notes with actual release path": document how it really deploys today (check workflows and netlify/vercel config).

Rules:
- New worktree: git -C C:\Users\ajhar\code\farm-3j fetch origin; git -C C:\Users\ajhar\code\farm-3j worktree add ..\farm-3j-wt-light -b chore/light-w41 origin/main. Confirm HEAD == origin/main.
- Run everything in Docker (node:22, `corepack enable`, `pnpm install --frozen-lockfile`): pnpm run lint (0 errors), `pnpm exec prettier --check --config config/.prettierrc <files>`, and vitest on touched areas (`--pool=threads` if forks time out). Add unit tests for new logic.
- Tick finished TASKS items ([x] + "Done 2026-10-<dd>: ..."), and add root CHANGELOG.md entries under [Unreleased].
- Commit with a "Co-Authored-By: Claude <model> <noreply@anthropic.com>" trailer, push, open a non-draft PR (body ends with "🤖 Generated with [Claude Code](https://claude.com/claude-code)"). Do NOT merge. Remove the worktree.
- Report: PR URL, done vs skipped, and test results.
```

### games

```text
Repo: nitsuah/games (local clone C:\Users\ajhar\code\games; the Next app lives in app/). Do these in ONE branch and ONE PR.

1. Fix the 17 pre-existing `npm run lint` errors (in _components/objects/HillyFloor.js, e2e/a11y.spec.js, lib/asteroid/_comp/Game/Game.jsx, next.config.js). Real fixes, no blanket eslint-disable. If a fix would change runtime behavior, stop on that one and list it. First add a TASKS item for it (it isn't tracked yet), then tick it when done.
2. P3 "Add high-score persistence to Memory Match": store best time/moves in localStorage; show them on the board. Extend app/e2e/memory-match.spec.js with one test.
3. P3 "Mobile touch controls for Dodge Blocks": on-screen left/right buttons (or swipe) that call the same move logic as the arrow keys. Extend app/e2e/dodge-blocks.spec.js with one test.
4. P3 "Revisit the eslint 10 bump ... once eslint-plugin-react supports it": check the latest eslint-plugin-react peerDependencies (`npm view eslint-plugin-react peerDependencies`). Only update the TASKS note with the finding; don't bump.

Rules:
- New worktree: git -C C:\Users\ajhar\code\games fetch origin; git -C C:\Users\ajhar\code\games worktree add ..\games-wt-light -b chore/light-w41 origin/main. Confirm HEAD == origin/main.
- Run everything in Docker. `npm ci` hangs on a Windows bind mount, so copy the repo into the container: docker run --rm -v "$(pwd -W)/app:/src:ro" mcr.microsoft.com/playwright:v1.63.0-noble sh -c "mkdir /w && cd /src && tar --exclude=node_modules --exclude=.next -cf - . | tar -xf - -C /w && cd /w && npm ci && npm run lint && (npx --yes http-server public -p 3000 -s &) && sleep 3 && CI=1 npx playwright test e2e/memory-match.spec.js e2e/dodge-blocks.spec.js". Prefix with MSYS_NO_PATHCONV=1 in Git Bash. Copy changed files back out, or edit on the host and re-run.
- Tick finished TASKS items ([x] + "Done 2026-10-<dd>: ..."), and add docs/CHANGELOG.md entries under Unreleased.
- Commit with a "Co-Authored-By: Claude <model> <noreply@anthropic.com>" trailer, push, open a non-draft PR (body ends with "🤖 Generated with [Claude Code](https://claude.com/claude-code)"). Do NOT merge. Remove the worktree.
- Report: PR URL, the lint error count before → after, and test results.
```

### stash

```text
Repo: nitsuah/stash (PUBLIC; local clone C:\Users\ajhar\code\stash). Scheduled routines commit in the shared checkout, so never touch it. Do these in ONE branch and ONE PR.

1. P3 "Add dependabot/renovate": .github/dependabot.yml already covers npm and github-actions. Add the `pip` ecosystem for the Python requirement files the repo actually has (weekly, grouped), then tick the item.
2. P3 "Add pre-commit hooks" (acceptance: Ruff, PSScriptAnalyzer, shellcheck locally): .githooks/pre-commit already runs gitleaks + agent/scripts/pii-scan.sh. Keep those and add ruff on staged .py and shellcheck on staged .sh, both run via Docker or skipped with a warning if Docker isn't available, so commits never hard-fail on a missing tool. PSScriptAnalyzer: note that CI covers it, rather than requiring pwsh locally. Tick the item.
3. P3 "Add CodeQL / SAST scanning": add .github/workflows/codeql.yml (python, default queries, on push/PR to main + weekly). Tick it.
4. P3 "Add CONTRIBUTING.md": a short root CONTRIBUTING.md (worktree-per-task, PR-only to main, Docker for tooling, the public-repo/PII rules from the pre-commit hook), or link nitsuah/.github's default if that already says it. Tick it.
5. Findings ledger F-20260930-02 (agent/reports/findings-ledger.md): `python3 agent/scripts/find-orphans.py --check` reports the loose SOTU attachments (agent/reports/sotu/*.json, agent/scripts/sotu-page.html) as unreachable. Link them from the right hub/report note so --check passes, then set the ledger row to done with the PR link.
6. P2 "Document the VBA source files inside Remora, Sampler, and VMT more precisely": per-module one-liners (purpose, entry points, key tables), from reading the exported .bas/.cls files. Docs only.

Rules:
- New worktree: git -C C:\Users\ajhar\code\stash fetch origin; git -C C:\Users\ajhar\code\stash worktree add .claude\worktrees\light-w41 -b chore/light-w41 origin/main. Confirm HEAD == origin/main.
- Python tooling in Docker: MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd -W):/app" -w /app python:3.12 sh -c "pip install -q ruff pytest responses requests && ruff check . && pytest <files in the ci.yml test-python job>".
- No secrets, emails or personal data (the pre-commit PII scan enforces this). Tick finished TASKS items ([x] + "Done 2026-10-<dd>: ..."), and add docs/CHANGELOG.md entries under [Unreleased].
- Commit with a "Co-Authored-By: Claude <model> <noreply@anthropic.com>" trailer, push, open a non-draft PR (body ends with "🤖 Generated with [Claude Code](https://claude.com/claude-code)"). Do NOT merge. Remove the worktree.
- Report: PR URL, done vs skipped, and the find-orphans --check output.
```

### nitsuah-io

```text
Repo: Nitsuah-Labs/nitsuah-io (local clone C:\Users\ajhar\code\nitsuah-io; Node version from .nvmrc, strip any \r). Do these in ONE branch and ONE PR. Copilot reviews PRs here, so keep the diff focused. Do NOT touch ESLint config or package.json's typescript entry (lint is deliberately skipped until TypeScript 7 support lands; see the TASKS P2).

1. P3 "agent-board (formerly motor-pool) showcase section": the repo was renamed the other way round (agent-board is now motor-pool). Fix the item's wording, then build a small showcase section for motor-pool using the existing project-card components and assets.
2. P2 "Variable font and fluid typography scale": switch to a variable font via next/font and a clamp()-based type scale in the global styles. No layout redesign.
3. P3 "Evaluate and reduce Spline 3D scene weight": measure the /3d route's bundle and scene size (next build output + network sizes) and write the numbers and 2–3 concrete reduction options into the TASKS item. Analysis only.
4. P3 "PWA manifest and offline support": add app/manifest (name, icons from public/, theme colors) so the site is installable. Leave offline/service-worker work as a follow-up note.

Rules:
- New worktree: git -C C:\Users\ajhar\code\nitsuah-io fetch origin; git -C C:\Users\ajhar\code\nitsuah-io worktree add ..\nitsuah-io-wt-light -b chore/light-w41 origin/main. Confirm HEAD == origin/main.
- Run in Docker only: docker run --rm -v "$(pwd -W):/app" -w /app node:<ver> sh -c "npm ci && npm run typecheck && npm test && npm run build:ci". Don't leave a host node_modules in the worktree (it breaks the husky pre-push hook); never use --no-verify.
- Tick finished TASKS items ([x] + "Done 2026-10-<dd>: ..."), and add docs/CHANGELOG.md entries under the existing [Unreleased] subsections (don't add duplicate headings).
- Commit with a "Co-Authored-By: Claude <model> <noreply@anthropic.com>" trailer, push, open a non-draft PR (body ends with "🤖 Generated with [Claude Code](https://claude.com/claude-code)"). Do NOT merge. Remove the worktree.
- Report: PR URL, done vs skipped, and typecheck/test/build results.
```

### avatar

```text
Repo: nitsuah/avatar (local clone C:\Users\ajhar\code\avatar). Small docs/tooling tasks from docs/TASKS.md (P3), in ONE branch and ONE PR:

1. "Document the build_training_command utility in README": show how to use it to reproduce the training command locally (read its source for args/defaults).
2. "Add a CONTRIBUTING.md entry (or link to nitsuah/.github)": a short root CONTRIBUTING.md that links the org default.
3. "Create run_notebook.sh helper": implement exactly what the TASKS item's sub-bullets specify (read them). It must not trigger training by default.
4. "Export notebook to examples/DreamBooth_Stable_Diffusion.html": jupyter nbconvert --to html WITHOUT --execute (no training), in Docker (python:3.11, pip install nbconvert).

Rules:
- New worktree: git -C C:\Users\ajhar\code\avatar fetch origin; git -C C:\Users\ajhar\code\avatar worktree add ..\avatar-wt-light -b chore/light-w41 origin/main. Confirm HEAD == origin/main. Leave the shared checkout alone.
- Any Python in Docker. Run `bash -n run_notebook.sh` and shellcheck (koalaman/shellcheck image) on the script.
- Tick finished TASKS items ([x] + "Done 2026-10-<dd>: ..."), and add docs/CHANGELOG.md entries under Unreleased.
- Commit with a "Co-Authored-By: Claude <model> <noreply@anthropic.com>" trailer, push, open a non-draft PR (body ends with "🤖 Generated with [Claude Code](https://claude.com/claude-code)"). Do NOT merge. Remove the worktree.
- Report: PR URL and done vs skipped.
```

### skyview

```text
Repo: nitsuah/skyview (local clone C:\Users\ajhar\code\skyview). Two P3 items from docs/TASKS.md, in ONE branch and ONE PR. Production launch, email domain and analytics need the owner's accounts, so don't touch them.

1. "Dependency audit and update": `npm outdated` + `npm audit` in Docker. Apply patch/minor bumps that keep tests green. List majors in the PR body; don't apply them.
2. "Test and tooling debt surfaced by the 2026-09 auth + scheduling pass": read the item's sub-bullets and fix the ones that are small and test-only/tooling-only. Leave the rest listed with a progress note.

Rules:
- New worktree: git -C C:\Users\ajhar\code\skyview fetch origin; git -C C:\Users\ajhar\code\skyview worktree add ..\skyview-wt-light -b chore/light-w41 origin/main. Confirm HEAD == origin/main.
- Run npm/tests/lint only in Docker (use the repo's Docker/compose test setup if present). The full test suite and lint must pass.
- Tick or annotate TASKS items, and add CHANGELOG entries if the repo keeps one.
- Commit with a "Co-Authored-By: Claude <model> <noreply@anthropic.com>" trailer, push, open a non-draft PR (body ends with "🤖 Generated with [Claude Code](https://claude.com/claude-code)"). Do NOT merge. Remove the worktree.
- Report: PR URL, the bumps applied, majors deferred, and test results.
```

### darkmoon + osrs (check-and-annotate, Haiku)

```text
Three tiny check-and-annotate tasks, one PR per repo. Use a new worktree per repo (git -C <clone> fetch origin; git -C <clone> worktree add ..\<repo>-wt-light -b chore/light-w41 origin/main), never the shared checkout.

A. nitsuah/darkmoon (C:\Users\ajhar\code\darkmoon), P3 "Revisit the eslint 10 bump ... once eslint-plugin-jsx-a11y supports it": run `npm view eslint-plugin-jsx-a11y peerDependencies` on the host (read-only lookup). If ESLint 10 is now supported, say so in the TASKS item and raise it to P2; otherwise add a dated "Checked 2026-10-<dd>: still eslint <=9" sub-bullet.
B. Same repo, P2 "Re-baseline the remaining large-file refactor work": count lines per source file (exclude node_modules, dist, lockfiles, assets), and rewrite the item's sub-bullets as the current top 5 files over 400 lines with counts. Docs only.
C. nitsuah/osrs (C:\Users\ajhar\code\osrs), P3 "Bump the nltk pin once a patched release ships (#39, GHSA-8mgp-746c-j5xp)": check the advisory's patched version (`gh api /advisories/GHSA-8mgp-746c-j5xp`) against `pip index versions nltk` (in Docker: python:3.12). If a patched version exists, bump the pin, run the test suite in Docker, and tick the item ("Fixes #39"). Otherwise add a dated "still unpatched" note.

For each PR: add a CHANGELOG entry if the repo keeps one, commit with a "Co-Authored-By: Claude <model> <noreply@anthropic.com>" trailer, push, open a non-draft PR (body ends with "🤖 Generated with [Claude Code](https://claude.com/claude-code)"). Do NOT merge. Remove the worktrees. Report the PR URLs and findings.
```
