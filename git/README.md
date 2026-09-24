# Git Utilities

PowerShell scripts for git repository maintenance across local workspaces.

## Scripts

### `cleanup-branches.ps1`

Scans all git repositories under a root path and removes merged local and remote branches.

```powershell
# Dry run — preview what would be deleted
.\git\cleanup-branches.ps1 -DryRun

# Run interactively (prompts before each delete)
.\git\cleanup-branches.ps1

# Non-interactive (deletes without prompting)
.\git\cleanup-branches.ps1 -Force

# Target a different root path
.\git\cleanup-branches.ps1 -Path C:\Users\you\repos
```

**What it does:**
- Finds all directories under `-Path` that contain a `.git` folder
- For each repo: fetches + prunes remote refs, detects the default branch (`main` or `master`), pulls latest
- Lists branches already merged into the default branch
- Deletes them locally and from `origin` — skipping the default branch and anything currently checked out

### `sync-fork.ps1`

Keeps a GitHub fork **and** its local clone level with the upstream repo, so you never press "Sync fork" again and never start work on a stale `master`.

```powershell
# One-off sync (fork on GitHub + local clone)
.\git\sync-fork.ps1 -Fork nitsuah/9router -RepoPath C:\Users\ajhar\code\9router

# Install as a scheduled task: every hour + at logon (runs as you, hidden window)
.\git\sync-fork.ps1 -Fork nitsuah/9router -RepoPath C:\Users\ajhar\code\9router -Install

# Remove the scheduled task
.\git\sync-fork.ps1 -Fork nitsuah/9router -RepoPath C:\Users\ajhar\code\9router -Uninstall
```

Options: `-Branch` (default `master`), `-UpstreamRemote` (default `upstream`), `-LogPath` (default `git\logs\<repo>-sync.log`, gitignored), `-IntervalHours` (default `1`).

**What it does:**
- `gh repo sync <fork> -b <branch>`: same as GitHub's "Sync fork" button. If the fork's branch has diverged it fails and logs rather than overwriting.
- Fetches `upstream` in the local clone and fast-forwards the local branch:
  - If you're on another branch, the ref moves in the background.
  - If you're on it with uncommitted changes, that run is skipped.
- Never merges, rebases or force-pushes, and leaves feature branches alone.
- If any step fails (fork sync, fetch, fast-forward), it logs why and exits `1`, so Task Scheduler's "Last Run Result" shows the failure. Relative `-RepoPath`/`-LogPath` are resolved before installing, since tasks run from `system32`.

**Requirements:** `gh` logged in, and a local clone with an `upstream` remote. Your token needs the `workflow` scope (`gh auth status`), otherwise any upstream commit that touches `.github/workflows/` is rejected.

**Why a local task rather than a GitHub Actions workflow in the fork:**
- **Token:** the Actions `GITHUB_TOKEN` can't write workflow files, so you'd need a personal access token stored as a secret.
- **Branch:** scheduled workflows only run from the default branch, which would stop `master` being a clean mirror.
- **Enablement:** GitHub disables schedules on forks until you enable them, and again after about 60 days of inactivity.
- **Local clone:** a local task also updates your clone, which Actions can't.

> **Gotcha: packaged apps (MSIX) see `%LOCALAPPDATA%` redirected.** The Claude desktop app (and other Store/MSIX apps) get a private copy of `AppData\Local`, so a log the real scheduled task writes there looks missing or stale from inside the app's terminals. That's why the default log lives next to the script, not under AppData.
