<#
.SYNOPSIS
  Syncs repo docs from live repos into stash/agent/repos/[name]/
  Copies root PMO files and docs/ .md files.
  Updates "Last Validated" in each summary .md.
  Reports newly detected HANDOFF-*.md files for vault index updates.

.PARAMETER Repos
  One or more repo names to sync. Defaults to all known repos.

.PARAMETER DryRun
  Preview what would be copied without making changes.

.EXAMPLE
  .\sync-repos.ps1
  .\sync-repos.ps1 -Repos overseer, nitsuah-io
  .\sync-repos.ps1 -DryRun
#>
param(
    [string[]]$Repos  = @(),
    [switch]  $DryRun
)

$VaultRoot = (Resolve-Path "$PSScriptRoot\..").Path
$CodeRoot  = "C:\Users\$env:USERNAME\code"
$Today     = Get-Date -Format 'yyyy-MM-dd'

$AllRepos = @(
    'motor-pool', 'auto-apply-plugin', 'avatar', 'bb-mcp', 'darkmoon',
    'farm-3j', 'fire', 'games', 'gcp', 'kryptos', 'nitsuah-io',
    'opencut', 'opencut-controller', 'osrs', 'overseer', 'skyview', 'vhs'
)

$TargetRepos = if ($Repos.Count -gt 0) { $Repos } else { $AllRepos }

# Root-level files to sync (if present in source repo)
$RootFiles = @(
    'CHANGELOG.md', 'FEATURES.md', 'METRICS.md', 'README.md',
    'ROADMAP.md', 'TASKS.md', 'PRIVACY.md', 'PROMPTS.md', 'README.es.md'
)

$TotalCopied = 0
$TotalNewHandoffs = 0

foreach ($repo in $TargetRepos) {
    $src  = "$CodeRoot\$repo"
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

    # --- docs/ .md files ---
    $srcDocs = "$src\docs"
    if (Test-Path $srcDocs) {
        Get-ChildItem $srcDocs -File -Filter '*.md' | ForEach-Object {
            $destFile = "$dest\docs\$($_.Name)"
            $isNew    = -not (Test-Path $destFile)
            if (-not $DryRun) { Copy-Item $_.FullName $destFile -Force }
            Write-Host "  $(if ($isNew){'[NEW]'}else{'[upd]'}) docs/$($_.Name)"
            $copied++
            if ($_.Name -match '^HANDOFF-' -and $isNew) { $newHandoffs += $_.Name }
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
