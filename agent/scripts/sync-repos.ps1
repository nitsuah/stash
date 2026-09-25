<#
.SYNOPSIS
  Syncs repo docs from live repos into stash/agent/repos/[name]/
  Copies root PMO files and every .md under docs/ (including subfolders such as
  docs/archive/ and docs/analysis/, keeping their relative paths so the
  breadcrumb links added upstream in the 2026-09-24 pmo-ff pass resolve).
  Updates "Last Validated" in each summary .md.
  Reports newly detected HANDOFF-*.md files for vault index updates.

.PARAMETER Repos
  One or more repo names to sync. Defaults to all known repos.

.PARAMETER DryRun
  Preview what would be copied without making changes.

.PARAMETER Prune
  Also delete mirrored .md files under repos/[name]/ that no longer exist in the
  source repo (e.g. a root FEATURES.md left behind after the repo moved it to
  docs/, or a doc since archived upstream). Off by default; combine with -DryRun
  to preview.

.EXAMPLE
  .\sync-repos.ps1
  .\sync-repos.ps1 -Repos overseer, nitsuah-io
  .\sync-repos.ps1 -DryRun
  .\sync-repos.ps1 -Prune -DryRun
#>
param(
    [string[]]$Repos  = @(),
    [switch]  $DryRun,
    [switch]  $Prune
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

# Root-level files to sync (if present in source repo)
$RootFiles = @(
    'CHANGELOG.md', 'FEATURES.md', 'METRICS.md', 'README.md',
    'ROADMAP.md', 'TASKS.md', 'PRIVACY.md', 'PROMPTS.md', 'README.es.md'
)

$TotalCopied = 0
$TotalNewHandoffs = 0

foreach ($repo in $TargetRepos) {
    $src  = if ($RepoPaths.ContainsKey($repo)) { $RepoPaths[$repo] } else { "$CodeRoot\$repo" }
    $dest = "$VaultRoot\repos\$repo"

    if (-not (Test-Path $src)) {
        Write-Host "  [SKIP] $repo — source not found at $src" -ForegroundColor Yellow
        continue
    }

    Write-Host "`n[$repo]" -ForegroundColor Cyan
    $copied      = 0
    $newHandoffs = @()

    if (-not $DryRun) {
        New-Item -ItemType Directory -Path $dest           -Force | Out-Null
        New-Item -ItemType Directory -Path "$dest\docs"    -Force | Out-Null
    }

    # --- Root PMO files ---
    foreach ($f in $RootFiles) {
        $srcFile = "$src\$f"
        if (-not (Test-Path $srcFile)) { continue }
        $destFile = "$dest\$f"
        $isNew    = -not (Test-Path $destFile)
        if (-not $DryRun) { Copy-Item $srcFile $destFile -Force }
        Write-Host "  $(if ($isNew){'[NEW]'}else{'[upd]'}) $f"
        $copied++
    }

    # --- docs/ .md files (recursive, relative paths preserved) ---
    $srcDocs = "$src\docs"
    $expected = @{}   # vault-relative paths this run produced, for -Prune
    foreach ($f in $RootFiles) { if (Test-Path "$src\$f") { $expected["$f".ToLower()] = $true } }
    if (Test-Path $srcDocs) {
        Get-ChildItem $srcDocs -File -Filter '*.md' -Recurse |
            Where-Object { $_.FullName -notmatch '\\node_modules\\' } |
            ForEach-Object {
                $rel      = $_.FullName.Substring($srcDocs.Length + 1)
                $destFile = "$dest\docs\$rel"
                $isNew    = -not (Test-Path $destFile)
                if (-not $DryRun) {
                    New-Item -ItemType Directory -Path (Split-Path $destFile) -Force | Out-Null
                    Copy-Item $_.FullName $destFile -Force
                }
                Write-Host "  $(if ($isNew){'[NEW]'}else{'[upd]'}) docs/$($rel -replace '\\','/')"
                $copied++
                $expected["docs\$rel".ToLower()] = $true
                if ($_.Name -match '^HANDOFF-' -and $isNew) { $newHandoffs += $_.Name }
            }
    }

    # --- optional: prune mirrored .md files that no longer exist upstream ---
    if ($Prune -and (Test-Path $dest)) {
        Get-ChildItem $dest -File -Filter '*.md' -Recurse | ForEach-Object {
            $rel = $_.FullName.Substring($dest.Length + 1)
            if (-not $expected.ContainsKey($rel.ToLower())) {
                if (-not $DryRun) { Remove-Item $_.FullName -Force }
                Write-Host "  [prune] $($rel -replace '\\','/')" -ForegroundColor DarkYellow
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

    # --- Report new HANDOFF files ---
    if ($newHandoffs.Count -gt 0) {
        Write-Host "`n  [ACTION REQUIRED] New HANDOFF files — add wikilinks to $repo.md Vault Index:" -ForegroundColor Green
        $newHandoffs | ForEach-Object { Write-Host "    [[repos/$repo/docs/$($_ -replace '\.md$','')]]" -ForegroundColor Green }
        $TotalNewHandoffs += $newHandoffs.Count
    }

    Write-Host "  $copied file(s) $(if ($DryRun){'would be '}else{''})copied"
    $TotalCopied += $copied
}

Write-Host "`n--- Sync $(if ($DryRun){'preview (dry run)'}else{'complete'}) ---" -ForegroundColor Cyan
Write-Host "Total files: $TotalCopied"
if ($TotalNewHandoffs -gt 0) {
    Write-Host "New HANDOFF files needing vault index updates: $TotalNewHandoffs" -ForegroundColor Green
}
