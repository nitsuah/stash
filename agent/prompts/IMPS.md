# IMPS

Headless Claude workers (via 9router) that turn **one GitHub issue into one small PR**, behind a deterministic gate. Pair with [[JOURNEYS]]: journeys find and verify; imps fix the small, diagnosed slice.

- **Contract and code:** [nitsuah/.github `imps/`](https://github.com/nitsuah/.github/tree/main/imps). Start with `STANDARD.md`. Entry points: `dispatch.mjs`, `imp.mjs`, `lib.mjs`, `review.mjs`, `fix.mjs`, `precheck.mjs`.
- **This file:** inventory, how stash wires the kit, the human/triage prompts, and the RSI / run log. Not a second copy of the runner.
- **Target architecture:** [[repos/motor-pool/docs/IMPS-PLAN|motor-pool IMPS-PLAN]] (durable queue, `imp-runner` container, GitHub App). Today's kit is the smoke-test loop that already runs from a desktop scheduled task.
- **Showcase page:** [pages/imps.html](https://nitsuah.github.io/stash/imps.html).

## Split (do not vendor the kit here)

| Layer | Where | Why |
| --- | --- | --- |
| Runnable kit | `nitsuah/.github/imps/` | One public source for every repo; hourly runner resets a detached checkout to `origin/main` |
| Playbook / inventory / RSI log | this file (`agent/prompts/IMPS.md`) | Same Obsidian benefits as [[JOURNEYS]]: shared memory, links, routines |
| Per-repo adopt notes | `agent/repos/<repo>.md` or the inventory table below | Vault-native; no code duplication |
| Machine config | stash `.github/imps-config.yml` + ignored `.imps/kit-path.txt` | Path to the detached kit only — never commit absolute personal paths |
| Thin wrapper | `scripts/imp-run.ps1` | Resolves kit path and runs `node <kit>/imps/imp.mjs …` |

`agent/` holds prompts and knowledge. The detached `imps-runner` checkout holds the code that actually runs. Copying `imps/*.mjs` into `agent/` would fork the contract and break the "only merged kit code runs unattended" rule.

## Topology: one warlock, many imps, many machines

Three words, and the count that goes with each. Contract: `.github` [`imps/WARLOCK.md`](https://github.com/nitsuah/.github/blob/main/imps/WARLOCK.md); check it with `node <kit>/imps/warlock.mjs`.

| Word | What it is | How many per machine |
| --- | --- | --- |
| **warlock** | the one `dispatch.mjs` cycle — no LLM of its own, just the queue | **exactly 1** |
| **imp-runner** | the detached kit checkout the warlock executes | 1 (shared by every imp) |
| **imp** | a headless `claude -p` worker through 9router | many — `--concurrency` / `--per-repo` / `--wip` / `--daily-cap` |

The warlock holds a lock and picks work; it never edits a repo. Wanting more throughput is a request for **more imps**, never a second warlock — two warlocks see the same `imp:ready` labels, pick the same briefs, and race on one `imp-nm-<repo>` node_modules volume, which corrupts `npm ci` and shows up as gate failures that look like bad briefs.

`dispatch.lock` skips a cycle when the lock is under 3 h old, so it stops *overlap*, not *duplication* — two warlocks started 4 h apart both run. One Scheduled Task per machine is the invariant the code cannot enforce, which is why `warlock.mjs` checks it.

Machines are independent: own warlock, own runner, own `~/.imps`. They coordinate **only through GitHub labels** — `imp:ready` → `imp:working` is the queue's lock, coarse and accepted, since a duplicate run produces a duplicate PR a human closes, not a corrupted repo. The ledger is per-machine, so a warlock cannot fix-sweep a PR another machine opened; fix rounds happen on the machine that opened it. Never point two machines at one `IMPS_HOME`.

**Why this is written down:** on 2026-10-26 `~/code/imps-runner` was a 78-byte `dispatch.mjs` stub with no `.git`, so `hourly.cmd` logged `IMP dispatch stub executed` on schedule and the hourly loop was inert while the real cycles came from hand-run `/imp`. "Is `dispatch.mjs` there" was the only question anything asked. `warlock.mjs` refuses to pass a directory that merely contains the file.

## Flow (verified against the kit)

```
imp:ready + <!-- imp-brief --> comment
        │
        ▼
dispatch.mjs (hourly, no LLM) ── fix-sweep open imp PRs first
        │
        ▼
imp.mjs run  → clean worktree, 9router worker, local commits
        │
        ▼
imp.mjs gate → Docker tests, maxLines, allow/deny, Co-Authored-By …imp
        │ pass                      │ fail
        ▼                           ▼
imp.mjs pr → review.mjs → fix.mjs   imp:failed (+ comment reasons)
             (≤2 fix rounds, then imp:needs-human)
```

Labels: `imp:ready` → `imp:working` → `imp:pr` / `imp:failed`, plus `imp:needs-human`.

**Honest vs older docs:** PRs are opened ready for the auto-merge path (not kept as permanent drafts). The runner may arm `gh pr merge --auto --squash` when the recomputed review verdict is approve and checks look green. Branch **required status checks** are what actually stop a red merge — stash learned this on #305.

## Caps (code defaults today)

| Limit | Default | Source |
| --- | --- | --- |
| Gate `maxLines` | 15 | `lib.mjs` `gate()`, `imp.mjs` |
| Fix slack | +30 lines | `fix.mjs --slack` |
| Per cycle / WIP / per-repo / concurrency / daily | 5 / 8 / 4 / 4 / 15 | `dispatch.mjs` flags |
| Fix rounds | 2 → `imp:needs-human` | `fix.mjs` |
| Repo cooldown | 24 h after 2 straight gate fails | `loopBudget` |

Diff size is set on the **brief** (`maxLines`), not by a stash `max_diff_lines` config key (that key is unused and removed from `.github/imps-config.yml`).

## A. Triage (hypervisor / paid model, once a day)

> Read new issues. For each: either post an `<!-- imp-brief -->` comment (front matter + body) and add `imp:ready`, or label for a human. Re-brief `imp:failed` from the gate reasons and PREAMBLE lessons — do not resend the same brief. Prefer already-diagnosed `bot:review` work. Keep briefs mechanical: exact files, exact change, no nested markdown fences.

## B. Brief shape

```markdown
<!-- imp-brief -->
---
repo: fire
issue: 166
test: docker run --rm -v {wt}://app -v imp-nm-fire://app/node_modules -w //app node:22 sh -c "npm ci --no-audit --no-fund >/dev/null 2>&1 && npx vitest run"
maxLines: 40
allow: app/lib/, docs/CHANGELOG.md
---
## Issue nitsuah/fire#166
…
```

Required: `repo`, `issue`. The runner runs `test` / `lint` / optional `format`. Every imp commit must include `Co-Authored-By: 9router imp <noreply@anthropic.com>` (gate regex: `/Co-Authored-By: .*imp/i`).

## C. RSI (after a batch of runs)

> `node imps/imp.mjs report` and `node imps/stats.mjs`. One recurring failure → one PREAMBLE / REVIEW / FIX / gate line with run ids → its own kit PR. Delete lessons that stop firing. Weekly token review: move paid triage steps into scripts or free models when possible (`precheck.mjs` pattern).

## Inventory

| Repo | Imp status | Notes |
| --- | --- | --- |
| stash | wrappers + Pages + this playbook | `.github/imps-config.yml`, `scripts/imp-run.ps1`; showcase at `pages/imps.html` |
| fire / vigil / vhs / … | live consumers via shared kit | Briefs and labels live on each repo's issues |
| motor-pool | plan only | [[repos/motor-pool/docs/IMPS-PLAN]] — durable service, not the desktop loop |

## Machine wiring (stash)

1. Detached kit checkout (outside this repo). Prefer the kit setup script when the `.github` PR that adds it has landed; otherwise STANDARD § Scheduling (`imps-dispatch` → hourly wrapper that resets the checkout then runs `dispatch.mjs`).
2. Point this repo at the kit: `IMPS_KIT_PATH`, or ignored `.imps/kit-path.txt`, or `kit_path` in `.github/imps-config.yml`.
3. `pwsh scripts/imp-run.ps1 <command> …` → `node <kit>/imps/imp.mjs …`. Optional: `IMPS_VAULT_PROMPT` points at this file for humans and future kit hooks.
4. Commit trailer helper: `scripts/imp-add-trailer.ps1` amends/creates the **commit** `Co-Authored-By` line the gate checks (it does not write a fake trailer into the brief file).

## Run log

### 2026-10-26 · topology contract + topology check

- Named the three parts in `.github` [`imps/WARLOCK.md`](https://github.com/nitsuah/.github/blob/main/imps/WARLOCK.md): **one warlock per machine, many imps per machine, many machines** (nitsuah/.github#52).
- Added `<kit>/imps/warlock.mjs`: read-only checks, no mutation, exit 1 on any failure. Performs **local checks (always) plus one HTTP `MAX` probe to 9router**. Runner-specific checks (is a real git checkout, has `imps/dispatch.mjs`, no tracked edits, current with `origin/main`, `hourly.cmd` points at it and is stamped from the current sha) **only run once a runner path is configured**; the rest always run — exactly one dispatch task, lock not stale, ledger parseable.
- Found while writing it: this machine's `~/code/imps-runner` is a 78-byte `dispatch.mjs` stub with **no `.git`**, and `~/.imps/kit-path.txt` does not exist. `hourly.cmd` therefore logged `IMP dispatch stub executed` on schedule — the hourly loop was inert, and the real cycles came from hand-run `/imp`. `warlock.mjs` reports both as failures.
- Repair is operator action, not a kit change: `pwsh imps/setup.ps1 -RunnerPath <fresh path>`, then re-run `warlock.mjs` until clean.

### 2026-10-26 · stash · Pages + vault wiring

- Verified kit defaults against `nitsuah/.github` `imps/` (gate 15, dispatch per-repo/concurrency 4, auto-merge on approve+green).
- Added `pages/imps.html`, this playbook, and aligned stash wrappers with the real gate contract.
- Products CI breakage from stash#305 (generic Strapi/Gatsby patterns) tracked separately; required status checks on the `protect` ruleset remain a human toggle.
