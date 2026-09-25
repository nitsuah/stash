<#
.SYNOPSIS
  Syncs repo docs from live repos into stash/agent/repos/[name]/
  Mirrors every MERGED .md in each repo (git ls-tree origin/HEAD, any depth, paths
  preserved) so the breadcrumb/Docs Index links added upstream resolve in the
  vault. Content comes from the default branch on the remote (origin/HEAD), never
  the working tree or the checked-out branch, so untracked, staged, locally
  modified, or unmerged-branch files are never published into this public vault.
  Updates "Last Validated" in each summary .md.

.PARAMETER Repos
  One or more repo names to sync. Defaults to all known repos.

.PARAMETER DryRun
  Preview what would be copied without making changes.

.PARAMETER Prune
  Also delete mirrored .md files under repos/[name]/ that no longer exist in the
  source repo (e.g. a root FEATURES.md left behind after the repo moved it to
  docs/, or a doc since archived upstream). Off by default; combine with -DryRun
  to preview.

.PARAMETER MaxPrune
  Per-repo safety cap for -Prune (default 25). If a repo has more stale files
  than this, nothing is deleted for that repo and a [prune-held] line is printed;
  review with -Repos <repo> -Prune -DryRun, then re-run with a higher -MaxPrune.

.EXAMPLE
  .\sync-repos.ps1
  .\sync-repos.ps1 -Repos overseer, nitsuah-io
  .\sync-repos.ps1 -DryRun
  .\sync-repos.ps1 -Prune -DryRun
#>
param(
    [string[]]$Repos  = @(),
    [switch]  $DryRun,
    [switch]  $Prune,
    [int]     $MaxPrune = 25
)

$VaultRoot = (Resolve-Path "$PSScriptRoot\..").Path
$CodeRoot  = "C:\Users\$env:USERNAME\code"
$Today     = Get-Date -Format 'yyyy-MM-dd'

# Repo list comes from the "## Tracked" table in agent/projects/scope.md (the
# canonical registry), minus stash itself. It used to be hardcoded here and
# drifted (still had motor-pool/opencut*, missed agent-board/deployer).
$ScopeFile = Join-Path $VaultRoot 'projects\scope.md'
$AllRepos = @()
$RepoPaths = @{}
$inTracked = $false
foreach ($line in Get-Content -LiteralPath $ScopeFile) {
    if ($line -match '^## ') { $inTracked = $line -match '^## Tracked'; continue }
    if (-not $inTracked) { continue }
    if ($line -match '^\|\s*([A-Za-z0-9._-]+)\s*\|') {
        $name = $Matches[1]
        if ($name -notin @('Repo', 'stash') -and $name -notmatch '^-+$') {
            $AllRepos += $name
            # Local path column may differ from the repo name (overseer is cloned as code\vigil).
            if ($line -match '^\|[^|]*\|\s*`([^`]+)`') { $RepoPaths[$name] = $Matches[1] }
        }
    }
}
if ($AllRepos.Count -eq 0) { throw "No repos parsed from the Tracked table in $ScopeFile" }

$TargetRepos = if ($Repos.Count -gt 0) { $Repos } else { $AllRepos }

$TotalCopied = 0
$TotalHeld   = 0

foreach ($repo in $TargetRepos) {
    $src  = if ($RepoPaths.ContainsKey($repo)) { $RepoPaths[$repo] } else { "$CodeRoot\$repo" }
    $dest = "$VaultRoot\repos\$repo"

    if (-not (Test-Path $src)) {
        Write-Host "  [SKIP] $repo — source not found at $src" -ForegroundColor Yellow
        continue
    }

    Write-Host "`n[$repo]" -ForegroundColor Cyan

    # --- Every .md on the default branch (git ls-tree origin/HEAD), any depth ---
    # origin/HEAD, not HEAD: a clone checked out on a feature branch (e.g. fire
    # on agent-prompts, 2026-09-25) would otherwise publish unmerged work.
    # Committed-only on purpose: copying the working tree once leaked a
    # user's staged-but-uncommitted private doc (fire/docs/weekly-checkin-prompt.md)
    # into this public vault. Untracked, staged, and modified files never sync.
    # .github/ (copilot instructions, issue/PR templates) and a root templates/
    # folder are repo config, not knowledge; mirroring them only added orphans.
    # fetch only updates remote refs; it never touches the checkout or local work,
    # so repos the daily routine skipped as dirty/on-a-branch still mirror current main.
    if (-not $DryRun) { git -C $src fetch -q origin 2>$null }
    $ref = 'origin/HEAD'
    git -C $src rev-parse --verify --quiet $ref *> $null
    if ($LASTEXITCODE -ne 0) { Write-Host "  [SKIP] $repo — no origin/HEAD (run: git -C $src remote set-head origin -a)" -ForegroundColor Yellow; continue }
    $files = @(git -C $src ls-tree -r --name-only $ref 2>$null |
        Where-Object { $_ -match '\.md$' -and $_ -notmatch '(^|/)node_modules/' -and
                       $_ -notmatch '(^|/)\.github/' -and $_ -notmatch '^templates/' })
    if ($files.Count -eq 0) {
        Write-Host "  [SKIP] $repo — no committed .md files (or not a git repo)" -ForegroundColor Yellow
        continue
    }
    $expected = @{}
    foreach ($f in $files) {
        $expected[($f -replace '/','\').ToLower()] = $true
        $isNew = -not (Test-Path "$dest\$($f -replace '/','\')")
        Write-Host "  $(if ($isNew){'[NEW]'}else{'[upd]'}) $f"
    }
    if (-not $DryRun) {
        New-Item -ItemType Directory -Path $dest -Force | Out-Null
        # git archive exports exactly the committed bytes; tar (bsdtar, built
        # into Windows 10+) unpacks them with paths preserved.
        $tar = Join-Path ([System.IO.Path]::GetTempPath()) "sync-$repo-$PID.tar"
        git -C $src archive --format=tar -o $tar $ref -- @files
        if ($LASTEXITCODE -ne 0) { Write-Host "  [ERROR] git archive failed for $repo" -ForegroundColor Red; continue }
        tar -xf $tar -C $dest
        Remove-Item $tar -Force -ErrorAction SilentlyContinue
    }
    $copied = $files.Count

    # --- optional: prune mirrored .md files that no longer exist upstream ---
    # The per-repo cap lives here (not in the calling routine) so a mass
    # deletion is held BEFORE anything is removed; a count that high usually
    # means a repo moved/renamed its docs rather than a normal cleanup.
    if ($Prune -and (Test-Path $dest)) {
        $stale = @(Get-ChildItem $dest -File -Filter '*.md' -Recurse | Where-Object {
            -not $expected.ContainsKey($_.FullName.Substring($dest.Length + 1).ToLower())
        })
        if ($stale.Count -gt $MaxPrune -and -not $DryRun) {
            Write-Host "  [prune-held] $($stale.Count) stale files exceed -MaxPrune $MaxPrune; nothing deleted. Review with: -Repos $repo -Prune -DryRun" -ForegroundColor Red
            $TotalHeld++
        } else {
            foreach ($f in $stale) {
                if (-not $DryRun) { Remove-Item $f.FullName -Force }
                Write-Host "  [prune] $($f.FullName.Substring($dest.Length + 1) -replace '\\','/')" -ForegroundColor DarkYellow
            }
            # drop directories the prune left empty
            if (-not $DryRun) {
                Get-ChildItem $dest -Directory -Recurse | Sort-Object { $_.FullName.Length } -Descending |
                    Where-Object { -not (Get-ChildItem $_.FullName -Force) } | Remove-Item -Force
            }
        }
    }

    # --- Update "Last Validated" in summary file ---
    $summaryFile = "$VaultRoot\repos\$repo.md"
    if ((Test-Path $summaryFile) -and (-not $DryRun)) {
        $raw     = Get-Content $summaryFile -Raw
        $updated = $raw -replace '(\*\*Last Validated:\*\* )\d{4}-\d{2}-\d{2}', "`${1}$Today"
        if ($updated -ne $raw) {
            Set-Content $summaryFile $updated -Encoding UTF8 -NoNewline
            Write-Host "  [sync] $repo.md Last Validated → $Today"
        }
    }

    Write-Host "  $copied file(s) $(if ($DryRun){'would be '}else{''})copied"
    $TotalCopied += $copied
}

Write-Host "`n--- Sync $(if ($DryRun){'preview (dry run)'}else{'complete'}) ---" -ForegroundColor Cyan
Write-Host "Total files: $TotalCopied"
if ($TotalHeld -gt 0) {
    Write-Host "Repos with a held prune (over -MaxPrune): $TotalHeld" -ForegroundColor Red
}
