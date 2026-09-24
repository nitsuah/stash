# Scope

> The canonical repo registry for every routine (local and cloud) — paths, GitHub URLs, org, visibility. `LOC.md`, `MINI.md`, and the cloud skills (`stale-worktrees`, `obn-weekly`, `gh-overseer`) were already written assuming this file exists and is authoritative; it just wasn't kept up to date. Rebuilt 2026-09-16 from `gh repo list nitsuah` / `gh repo list Nitsuah-Labs` (ground truth) cross-checked against `C:\Users\ajhar\code\*` (local clones).

**Rule for every routine, local or cloud: read this file for the repo list. Don't hardcode a separate one.** If you add or drop a repo from active tracking, update this file in the same change — that's the whole point of having one source of truth instead of five.

**For cloud routines specifically:** this environment only serves GitHub API/git-push access to repos explicitly attached via the `add_repo` MCP tool (`mcp__Claude_Code_Remote__add_repo`) — the generic `/users/{user}/repos` listing endpoint is blocked (`sessions are bound to their configured repositories`). Read the `GitHub URL` column below and call `add_repo` with the exact `owner`/`repo` for each one you need, instead of discovering the list via WebFetch/`list_repos` trial-and-error. Public repos get anonymous read for free; `deployer` is **private** and needs an explicit `add_repo {access:"read"}` (or `"push"` if you're actually committing) before anything will resolve.

## Tracked (active audit/automation scope)

These 17 are what `DAILY.md`, `PMO.md`, `METRICS.md` and the cloud `metrics`/`eng-loc`/`eng-mini`/`stale-worktrees`/`vuln-patcher`/`gh-overseer` routines operate on.

| Repo | Local path | GitHub URL | Org | Visibility |
|---|---|---|---|---|
| agent-board | `C:\Users\ajhar\code\agent-board` | https://github.com/nitsuah/agent-board | nitsuah | public |
| auto-apply-plugin | `C:\Users\ajhar\code\auto-apply-plugin` | https://github.com/nitsuah/ats-fill (renamed from `nitsuah/auto-apply-plugin`; old URL redirects, but `gh pr list --search` against the old name returns nothing) | nitsuah | public |
| avatar | `C:\Users\ajhar\code\avatar` | https://github.com/nitsuah/avatar | nitsuah | public |
| bb-mcp | `C:\Users\ajhar\code\bb-mcp` | https://github.com/nitsuah/bb-mcp | nitsuah | public |
| darkmoon | `C:\Users\ajhar\code\darkmoon` | https://github.com/nitsuah/darkmoon | nitsuah | public |
| deployer | `C:\Users\ajhar\code\deployer` | https://github.com/Nitsuah-Labs/deployer | Nitsuah-Labs | **private** |
| farm-3j | `C:\Users\ajhar\code\farm-3j` | https://github.com/nitsuah/farm-3j | nitsuah | public |
| fire | `C:\Users\ajhar\code\fire` | https://github.com/nitsuah/fire | nitsuah | public |
| games | `C:\Users\ajhar\code\games` | https://github.com/nitsuah/games | nitsuah | public |
| gcp | `C:\Users\ajhar\code\gcp` | https://github.com/nitsuah/gcp | nitsuah | public |
| kryptos | `C:\Users\ajhar\code\kryptos` | https://github.com/nitsuah/kryptos | nitsuah | public |
| nitsuah-io | `C:\Users\ajhar\code\nitsuah-io` | https://github.com/Nitsuah-Labs/nitsuah-io | Nitsuah-Labs | public |
| osrs | `C:\Users\ajhar\code\osrs` | https://github.com/nitsuah/osrs | nitsuah | public |
| overseer | `C:\Users\ajhar\code\overseer` | https://github.com/nitsuah/vigil (renamed from `nitsuah/overseer`; old URL redirects) | nitsuah | public |
| skyview | `C:\Users\ajhar\code\skyview` | https://github.com/nitsuah/skyview | nitsuah | public |
| stash | `C:\Users\ajhar\code\stash` | https://github.com/nitsuah/stash | nitsuah | public |
| vhs | `C:\Users\ajhar\code\vhs` | https://github.com/nitsuah/vhs | nitsuah | public |

`stash` is the vault these prompts live in — audited for metrics/docs by the routines above, but skipped by name in `PMO.md`'s repo loop ("it's the vault, not a product repo").

## Not tracked — forks and utility repos

Exist on GitHub, cloned or not, but out of scope for PMO/metrics/LOC/MINI automation. Forks of other people's projects don't get audited like owned products.

| Repo | Local path | GitHub URL | Why excluded |
|---|---|---|---|
| 9router | `C:\Users\ajhar\code\9router` | https://github.com/nitsuah/9router | fork |
| windirstat-mcp | `C:\Users\ajhar\code\windirstat-mcp` | https://github.com/nitsuah/windirstat-mcp | fork |
| gods-eye-view | not cloned locally | https://github.com/nitsuah/gods-eye-view | fork |
| odysseus | not cloned locally | https://github.com/nitsuah/odysseus | fork |
| opencut-classic | not cloned locally as this name (see [[project-opencut]] memory — cloned as `opencut` from a different fork, `nitsuah/opencut-classic` on GitHub isn't the same working copy) | https://github.com/nitsuah/opencut-classic | fork |
| initiative-opensource-release | not cloned locally | https://github.com/nitsuah/initiative-opensource-release | stale fork (last push 2023) |
| .github (nitsuah) | not cloned locally | https://github.com/nitsuah/.github | community-health defaults repo, not a product |
| .github (Nitsuah-Labs) | not cloned locally | https://github.com/Nitsuah-Labs/.github | fork, community-health defaults |

## Known gaps / notes

- **`motor-pool`** was in the old version of this file and referenced in `PMO.md`'s audit history (2026-03-27) as an active repo, but does not exist under either `nitsuah` or `Nitsuah-Labs` on GitHub as of 2026-09-16. Renamed, merged into another repo (`agent-board`? `bb-mcp`?), or deleted — unconfirmed. Don't re-add it to the tracked table until someone confirms what happened to it.
- The 17 tracked repos above match exactly what `DAILY.md`'s local repo-sync list already used — this file and that list should never drift apart. If you edit one, edit both, or better, replace `DAILY.md`'s inline list with a pointer here (not yet done as of 2026-09-16, since not every routine has been switched over to read this file at runtime yet — see [[RSI]] for follow-up).
