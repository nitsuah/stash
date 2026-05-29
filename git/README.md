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
