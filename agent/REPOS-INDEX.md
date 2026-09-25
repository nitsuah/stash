# Repo Docs Index

> 🧭 [[AGENT-MAIN]] · [[projects/scope|Scope]] · [[REPO-README]]

Light connector between the tracked repos: it links only each repo's hub note and README. Everything else
hangs off that README through the `> 🧭` breadcrumbs and README Docs Index added upstream, so each repo forms its
own cluster instead of one star around this note.
Lives **outside** `repos/` on purpose: `scripts/sync-repos.ps1` rewrites that tree. Context: [[reports/pmo-ff-2026-09-24]].

Until the upstream `pmo-ff` PRs merge and the next sync runs, the mirrored docs have no breadcrumbs yet, so most of
them still show as orphans. That's the true state, and it resolves on re-sync.

Repo list comes from [[projects/scope|scope.md]]'s Tracked table (minus `stash`, which is the vault itself).
`overseer` is mirrored under `repos/overseer/` but its local clone and GitHub repo are named `vigil`.

| Repo hub | Docs entry point | pmo-ff PR |
|---|---|---|
| [[repos/agent-board\|agent-board]] | [[repos/agent-board/README\|README]] | [PR](https://github.com/nitsuah/agent-board/pull/80) |
| [[repos/auto-apply-plugin\|auto-apply-plugin]] | [[repos/auto-apply-plugin/README\|README]] | [PR](https://github.com/nitsuah/ats-fill/pull/98) |
| [[repos/avatar\|avatar]] | [[repos/avatar/README\|README]] | [PR](https://github.com/nitsuah/avatar/pull/29) |
| [[repos/bb-mcp\|bb-mcp]] | [[repos/bb-mcp/README\|README]] | [PR](https://github.com/nitsuah/bb-mcp/pull/129) |
| [[repos/darkmoon\|darkmoon]] | [[repos/darkmoon/README\|README]] | [PR](https://github.com/nitsuah/darkmoon/pull/461) |
| [[repos/deployer\|deployer]] | [[repos/deployer/README\|README]] | [PR](https://github.com/Nitsuah-Labs/deployer/pull/166) |
| [[repos/farm-3j\|farm-3j]] | [[repos/farm-3j/README\|README]] | [PR](https://github.com/nitsuah/farm-3j/pull/350) |
| [[repos/fire\|fire]] | [[repos/fire/README\|README]] | [PR](https://github.com/nitsuah/fire/pull/122) |
| [[repos/games\|games]] | [[repos/games/README\|README]] | [PR](https://github.com/nitsuah/games/pull/345) |
| [[repos/gcp\|gcp]] | [[repos/gcp/README\|README]] | [PR](https://github.com/nitsuah/gcp/pull/70) |
| [[repos/kryptos\|kryptos]] | [[repos/kryptos/README\|README]] | [PR](https://github.com/nitsuah/kryptos/pull/222) |
| [[repos/nitsuah-io\|nitsuah-io]] | [[repos/nitsuah-io/README\|README]] | [PR](https://github.com/Nitsuah-Labs/nitsuah-io/pull/532) |
| [[repos/osrs\|osrs]] | [[repos/osrs/README\|README]] | [PR](https://github.com/nitsuah/osrs/pull/45) |
| [[repos/overseer\|overseer]] | [[repos/overseer/README\|README]] | [PR](https://github.com/nitsuah/vigil/pull/234) |
| [[repos/skyview\|skyview]] | [[repos/skyview/README\|README]] | [PR](https://github.com/nitsuah/skyview/pull/150) |
| [[repos/vhs\|vhs]] | [[repos/vhs/README\|README]] | [PR](https://github.com/nitsuah/vhs/pull/62) |

Links go live after the upstream PRs merge and the next `sync-repos.ps1` run. Run it with `-Prune` once to clear
mirror copies that no longer exist upstream (old root-level duplicates, since-archived docs); preview with
`-Prune -DryRun`.
