# Scope

> The canonical repo registry for every routine (local and cloud) — paths, GitHub URLs, org, visibility. `LOC.md`, `MINI.md`, and the cloud skills (`stale-worktrees`, `obn-weekly`, `gh-overseer`) were already written assuming this file exists and is authoritative; it just wasn't kept up to date. Rebuilt 2026-09-16 from `gh repo list nitsuah` / `gh repo list Nitsuah-Labs` (ground truth) cross-checked against `C:\Users\$username\code\*` (local clones).

**Rule for every routine, local or cloud: read this file for the repo list. Don't hardcode a separate one.** If you add or drop a repo from active tracking, update this file in the same change — that's the whole point of having one source of truth instead of five.

**For cloud routines specifically:** this environment only serves GitHub API/git-push access to repos explicitly attached via the `add_repo` MCP tool (`mcp__Claude_Code_Remote__add_repo`) — the generic `/users/{user}/repos` listing endpoint is blocked (`sessions are bound to their configured repositories`). Read the `GitHub URL` column below and call `add_repo` with the exact `owner`/`repo` for each one you need, instead of discovering the list via WebFetch/`list_repos` trial-and-error. Public repos get anonymous read for free; `deployer` is **private** and needs an explicit `add_repo {access:"read"}` (or `"push"` if you're actually committing) before anything will resolve.

## Tracked (active audit/automation scope)

These 17 are what `DAILY.md`, `PMO.md`, `METRICS.md` and the cloud `metrics`/`eng-loc`/`eng-mini`/`stale-worktrees`/`vuln-patcher`/`gh-overseer` routines operate on.

**Tier column**: pulled from vigil's live `repos.tier` (`GET https://gh-vigil.netlify.app/api/context` with `$VIGIL_MCP_KEY`, same call `routine-cloud-daily-brief.md` already makes) on 2026-10-15, re-checked 2026-10-21 (skyview now unregistered in vigil, so `—`). `sotu.py` now reads the live tiers on every run and reports drift, and SOTU covers only T1/T2 repos. It's user-assigned in vigil, never auto-detected, so it drifts out of date here — re-pull before trusting it for a prioritization call more than a few weeks old. `—` means the repo isn't registered in vigil yet (no tier to read), not that it's unimportant. T1 Critical, T2 Important, T3 Standard, T4 Low (see vigil's README for the full rubric).

### usernames

Now that stash is deployed to many machines we may need to review references for usernames like $username and use them interchangably with the "current" user or host of a machine to ensure that the pathing works as expected on any given host. ex $username: ajhar, apok

| Repo | Tier | Local path | GitHub URL | Org | Visibility |
|---|---|---|---|---|---|
| motor-pool | T1 | `C:\Users\$username\code\motor-pool` (formerly `agent-board`; clone moved to `code\motor-pool` by 2026-10-09, default branch `master`; vault mirror at `repos/motor-pool/`) | https://github.com/nitsuah/motor-pool (renamed from `nitsuah/agent-board` in 2026-10; old URL redirects, but `gh pr list --search` against the old name returns nothing) | nitsuah | public |
| ats-fill | T1 | `C:\Users\$username\code\ats-fill` (formerly `auto-apply-plugin`; vault mirror at `repos/ats-fill/`) | https://github.com/nitsuah/ats-fill (renamed from `nitsuah/auto-apply-plugin`; old URL redirects, but `gh pr list --search` against the old name returns nothing) | nitsuah | public |
| avatar | — | `C:\Users\$username\code\avatar` | https://github.com/nitsuah/avatar | nitsuah | public |
| bb-mcp | T2 | `C:\Users\$username\code\bb-mcp` | https://github.com/nitsuah/bb-mcp | nitsuah | public |
| darkmoon | — | `C:\Users\$username\code\darkmoon` | https://github.com/nitsuah/darkmoon | nitsuah | public |
| deployer | — | `C:\Users\$username\code\deployer` | https://github.com/Nitsuah-Labs/deployer | Nitsuah-Labs | **private** |
| farm-3j | — | `C:\Users\$username\code\farm-3j` | https://github.com/nitsuah/farm-3j | nitsuah | public |
| fire | T1 | `C:\Users\$username\code\fire` | https://github.com/nitsuah/fire | nitsuah | public |
| games | — | `C:\Users\$username\code\games` | https://github.com/nitsuah/games | nitsuah | public |
| gcp | — | `C:\Users\$username\code\gcp` | https://github.com/nitsuah/gcp | nitsuah | public |
| kryptos | — | `C:\Users\$username\code\kryptos` | https://github.com/nitsuah/kryptos | nitsuah | public |
| nitsuah-io | T3 | `C:\Users\$username\code\nitsuah-io` | https://github.com/Nitsuah-Labs/nitsuah-io | Nitsuah-Labs | public |
| osrs | — | `C:\Users\$username\code\osrs` | https://github.com/nitsuah/osrs | nitsuah | public |
| vigil | T1 | `C:\Users\$username\code\vigil` (formerly `overseer`; vault mirror at `repos/vigil/`. Older routines and logs may still say `overseer`) | https://github.com/nitsuah/vigil (renamed from `nitsuah/overseer`; old URL redirects) | nitsuah | public |
| skyview | — | `C:\Users\$username\code\skyview` | https://github.com/nitsuah/skyview | nitsuah | public |
| stash | T3 | `C:\Users\$username\code\stash` | https://github.com/nitsuah/stash | nitsuah | public |
| vhs | T2 | `C:\Users\$username\code\vhs` | https://github.com/nitsuah/vhs | nitsuah | public |

`stash` is the vault these prompts live in — audited for metrics/docs by the routines above, but skipped by name in `PMO.md`'s repo loop ("it's the vault, not a product repo").

8 of the 17 (avatar, darkmoon, deployer, farm-3j, games, gcp, kryptos, osrs) aren't registered in vigil, so they have no tier yet — that's a gap worth closing if tier-weighted prioritization (see `LOC.md`) is going to cover the whole portfolio rather than just the 9 repos vigil already knows about.

## Not tracked — forks and utility repos

Exist on GitHub, cloned or not, but out of scope for PMO/metrics/LOC/MINI automation. Forks of other people's projects don't get audited like owned products.

| Repo | Local path | GitHub URL | Why excluded |
|---|---|---|---|
| 9router | `C:\Users\$username\code\9router` | https://github.com/nitsuah/9router | fork |
| windirstat-mcp | `C:\Users\$username\code\windirstat-mcp` | https://github.com/nitsuah/windirstat-mcp | fork |
| gods-eye-view | not cloned locally | https://github.com/nitsuah/gods-eye-view | fork |
| odysseus | not cloned locally | https://github.com/nitsuah/odysseus | fork |
| opencut-classic | not cloned locally as this name (see the `project-opencut` Claude memory — cloned as `opencut` from a different fork, `nitsuah/opencut-classic` on GitHub isn't the same working copy) | https://github.com/nitsuah/opencut-classic | fork |
| initiative-opensource-release | not cloned locally | https://github.com/nitsuah/initiative-opensource-release | stale fork (last push 2023) |
| .github (nitsuah) | not cloned locally | https://github.com/nitsuah/.github | community-health defaults repo, not a product |
| .github (Nitsuah-Labs) | not cloned locally | https://github.com/Nitsuah-Labs/.github | fork, community-health defaults |

## Known gaps / notes

- **`motor-pool`**: the 2026-09-16 version of this note said it didn't exist. It does now. `nitsuah/agent-board` was renamed to `nitsuah/motor-pool` upstream in 2026-10 (the old URL redirects), and the Tracked table, vault hub and mirror use the new name. Older reports and notes keep `agent-board` in their filenames as records; `build-vault-indexes.py` maps them to the motor-pool hub through the `formerly` note in the table.
- The 17 tracked repos above match exactly what `DAILY.md`'s local repo-sync list already used — this file and that list should never drift apart. If you edit one, edit both, or better, replace `DAILY.md`'s inline list with a pointer here (not yet done as of 2026-09-16, since not every routine has been switched over to read this file at runtime yet — see [[RSI]] for follow-up).
