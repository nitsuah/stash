# Repo Docs Index

> 🧭 [[AGENT-MAIN]] · [[projects/scope|Scope]] · [[REPO-README]]

Light connector between the tracked repos: it links only each repo's hub note and README. Everything else
hangs off that README through the `> 🧭` breadcrumbs and README Docs Index added upstream, so each repo forms its
own cluster instead of one star around this note.
Lives **outside** `repos/` on purpose: `scripts/sync-repos.ps1` rewrites that tree. Context: [[reports/pmo-ff-2026-09-24]].

Until the upstream `pmo-ff` PRs merge and the next sync runs, the mirrored docs have no breadcrumbs yet, so most of
them still show as orphans. That's the true state, and it resolves on re-sync.

Repo list comes from [[projects/scope|scope.md]]'s Tracked table (minus `stash`, which is the vault itself).
`overseer` is mirrored under `repos/vigil/` but its local clone and GitHub repo are named `vigil`.

| Repo hub                                       | Docs entry point                           |
| ---------------------------------------------- | ------------------------------------------ |
| [[repos/agent-board\|agent-board]]             | [[repos/agent-board/README\|README]]       |
| [[repos/ats-fill\|ats-fill]]                   | [[repos/ats-fill/README\|README]]          |
| [[repos/avatar\|avatar]]                       | [[repos/avatar/README\|README]]            |
| [[repos/bb-mcp\|bb-mcp]]                       | [[repos/bb-mcp/README\|README]]            |
| [[repos/darkmoon\|darkmoon]]                   | [[repos/darkmoon/README\|README]]          |
| [[repos/deployer\|deployer]]                   | [[repos/deployer/README\|README]]          |
| [[repos/farm-3j\|farm-3j]]                     | [[repos/farm-3j/README\|README]]           |
| [[repos/fire\|fire]]                           | [[repos/fire/README\|README]]              |
| [[repos/games\|games]]                         | [[repos/games/README\|README]]             |
| [[repos/gcp\|gcp]]                             | [[repos/gcp/README\|README]]               |
| [[repos/kryptos\|kryptos]]                     | [[repos/kryptos/README\|README]]           |
| [[repos/nitsuah-io\|nitsuah-io]]               | [[repos/nitsuah-io/README\|README]]        |
| [[repos/osrs\|osrs]]                           | [[repos/osrs/README\|README]]              |
| [[repos/vigil\|vigil]]                         | [[repos/vigil/README\|README]]             |
| [[repos/skyview\|skyview]]                     | [[repos/skyview/README\|README]]           |
| [[repos/vhs\|vhs]]                             | [[repos/vhs/README\|README]]               |
| [[repos/stash\|stash]]                         | [[README\|README]] (vault root)            |

Links go live after the upstream PRs merge and the next `sync-repos.ps1` run. Run it with `-Prune` once to clear
mirror copies that no longer exist upstream (old root-level duplicates, since-archived docs); preview with
`-Prune -DryRun`.
