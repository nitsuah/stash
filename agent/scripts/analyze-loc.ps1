#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Lines of Code analysis script for eng-loc skill
.DESCRIPTION
    Walks all repos in scope.md, counts lines per file, flags large/small files
.OUTPUTS
    stash/agent/reports/eng-loc-<repo>-<date>.md
    stash/agent/logs/eng-loc.log
#>

param(
    [string]$ConfigPath = "config/eng-loc.toml",
    [string]$ScopePath = "stash/agent/projects/scope.md",
    [string]$ReportsDir = "stash/agent/reports",
    [string]$LogsDir = "stash/agent/logs"
)

# Load config
function Read-TOMLConfig {
    param([string]$Path)
    $content = Get-Content $Path -Raw

    $config = @{
        max_lines = 500
        min_lines = 30
        extensions = @(".ts", ".tsx", ".js", ".jsx", ".py", ".go", ".rs", ".cs", ".java", ".rb", ".php", ".swift", ".kt", ".scala", ".cpp", ".cc", ".c", ".h", ".hpp", ".vue", ".svelte")
        repo_overrides = @{}
    }

    $currentSection = ""
    foreach ($line in $content -split "`n") {
        $line = $line.Trim()
        if ($line -match '^\[repo\.(.+)\]$') {
            $currentSection = $matches[1]
            $config.repo_overrides[$currentSection] = @{}
        }
        elseif ($line -match '^(\w+)\s*=\s*(.+)$' -and $currentSection) {
            $key = $matches[1]
            $val = $matches[2].Trim('"'' ')
            if ($val -match '^\d+$') { $val = [int]$val }
            elseif ($val -match '^\[.+\]$') { $val = $val.Trim('[]') -split ',' | ForEach-Object { $_.Trim('"'' ') } }
            $config.repo_overrides[$currentSection][$key] = $val
        }
        elseif ($line -match '^(\w+)\s*=\s*(.+)$' -and !$currentSection) {
            $key = $matches[1]
            $val = $matches[2].Trim('"'' ')
            if ($val -match '^\d+$') { $val = [int]$val }
            elseif ($val -match '^\[.+\]$') { $val = $val.Trim('[]') -split ',' | ForEach-Object { $_.Trim('"'' ') } }
            $config[$key] = $val
        }
    }
    return $config
}

# Get repo list from scope.md
function Get-RepoList {
    param([string]$Path)
    $content = Get-Content $Path -Raw
    $repos = @()
    foreach ($line in $content -split "`n") {
        if ($line -match '^\-\s+\[(.+?)\]\(https://github\.com/nitsuah/(.+?)\)$') {
            $repos += @{ name = $matches[1]; slug = $matches[2] }
        }
    }
    return $repos
}

# Secondary scan for large files
function Scan-LargeFile {
    param([string]$FilePath, [string]$Extension)
    $findings = @()

    $content = Get-Content $FilePath -Raw -ErrorAction SilentlyContinue
    if (-not $content) { return $findings }

    $lines = $content -split "`n"

    # Check for unused imports (simple heuristic for JS/TS)
    if ($Extension -in @(".ts", ".tsx", ".js", ".jsx")) {
        $imports = $lines | Where-Object {
            $_ -match '^import\s+.*\s+from\s+["'\'']' -or $_ -match '^import\s+["'\'']'
        }
        foreach ($imp in $imports) {
            if ($imp -match 'import\s+\{([^}]+)\}') {
                $names = $matches[1] -split ',' | ForEach-Object { $_.Trim() }
                foreach ($name in $names) {
                    $name = $name.Trim()
                    if ($name -and $content -notmatch "(?<![a-zA-Z0-9_])$name(?![a-zA-Z0-9_])") {
                        $findings += "Unused import (heuristic): $name"
                    }
                }
            }
        }
    }

    # Check for functions defined but not referenced (very rough)
    if ($Extension -in @(".ts", ".tsx", ".js", ".jsx", ".py", ".go", ".rs")) {
        $funcs = @()
        if ($Extension -in @(".py")) {
            $funcs = $lines | Where-Object { $_ -match '^\s*def\s+(\w+)' } | ForEach-Object { $matches[1] }
        } elseif ($Extension -in @(".go")) {
            $funcs = $lines | Where-Object { $_ -match '^\s*func\s+(\w+)' } | ForEach-Object { $matches[1] }
        } elseif ($Extension -in @(".rs")) {
            $funcs = $lines | Where-Object { $_ -match '^\s*fn\s+(\w+)' } | ForEach-Object { $matches[1] }
        } else {
            $funcs = $lines | Where-Object {
                $_ -match '^\s*(?:async\s+)?function\s+(\w+)|^\s*(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(|^\s*(\w+)\s*\([^)]*\)\s*=>|^\s*(\w+)\s*\([^)]*\)\s*\{'
            } | ForEach-Object {
                for ($i=1; $i -lt $matches.Count; $i++) { if ($matches[$i]) { return $matches[$i] } }
            }
        }

        foreach ($fn in $funcs) {
            if ($fn -and $fn -notmatch '^(main|init|test|Test|main)$') {
                $refCount = ($content -split "(?<![a-zA-Z0-9_])$fn(?![a-zA-Z0-9_])").Count - 1
                if ($refCount -le 1) {
                    $findings += "Unused function (heuristic): $fn"
                }
            }
        }
    }

    # Check for copy-paste blocks (>10 lines repeated)
    if ($lines.Count -gt 20) {
        for ($i = 0; $i -le $lines.Count - 10; $i++) {
            $block = $lines[$i..($i+9)] -join "`n"
            if ($block.Trim().Length -gt 50) {
                $count = ($content -split [regex]::Escape($block)).Count - 1
                if ($count -gt 1) {
                    $findings += "Repeated block ($count occurrences, 10+ lines): $($block.Substring(0, [Math]::Min(80, $block.Length)))..."
                    break
                }
            }
        }
    }

    return $findings
}

# Main
$config = Read-TOMLConfig $ConfigPath
$repos = Get-RepoList $ScopePath

New-Item -ItemType Directory -Force -Path $ReportsDir | Out-Null
New-Item -ItemType Directory -Force -Path $LogsDir | Out-Null

$date = Get-Date -Format "yyyy-MM-dd"
$logPath = "$LogsDir/eng-loc.log"
$log = @()
$log += "=== ENG LOC Run: $date ==="

$allLargeFiles = @()
$allSmallFiles = @()

foreach ($repo in $repos) {
    $repoPath = $repo.slug
    if (-not (Test-Path $repoPath)) {
        $log += "SKIP: $repoPath does not exist locally"
        continue
    }

    $log += "Processing: $($repo.name) ($repoPath)"

    $maxLines = $config.max_lines
    if ($config.repo_overrides.ContainsKey($repo.slug) -and $config.repo_overrides[$repo.slug].ContainsKey('max_lines')) {
        $maxLines = $config.repo_overrides[$repo.slug]['max_lines']
    }
    $minLines = $config.min_lines
    $extensions = $config.extensions

    $excludeDirs = @("node_modules", ".git", "dist", "build", ".next", ".turbo", "coverage", ".pnpm-store", "vendor", "target", "bin", "obj", ".gradle", "out")

    $files = Get-ChildItem -Path $repoPath -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
        $ext = $_.Extension
        $inExt = $extensions -contains $ext
        $inExclude = $false
        $parent = $_.Directory
        while ($parent) {
            if ($excludeDirs -contains $parent.Name) { $inExclude = $true; break }
            $parent = $parent.Parent
        }
        $inExt -and !$inExclude
    }

    $largeFiles = @()
    $smallFiles = @()

    foreach ($file in $files) {
        try {
            $lineCount = (Get-Content $file.FullName -ErrorAction SilentlyContinue).Count
        } catch {
            $lineCount = 0
        }

        $relPath = $file.FullName.Substring($repoPath.Length + 1).Replace('\', '/')

        if ($lineCount -ge $maxLines) {
            $findings = Scan-LargeFile $file.FullName $file.Extension
            $largeFiles += @{ lines = $lineCount; path = $relPath; findings = $findings }
            $allLargeFiles += @{ repo = $repo.name; slug = $repo.slug; lines = $lineCount; path = $relPath; findings = $findings }
        } elseif ($lineCount -le $minLines -and $lineCount -gt 0) {
            $smallFiles += @{ lines = $lineCount; path = $relPath }
            $allSmallFiles += @{ repo = $repo.name; slug = $repo.slug; lines = $lineCount; path = $relPath }
        }
    }

    $largeFiles = $largeFiles | Sort-Object { -$_.lines }
    $smallFiles = $smallFiles | Sort-Object { $_.lines }

    $reportPath = "$ReportsDir/eng-loc-$($repo.slug)-$date.md"
    $report = @()
    $report += "# ENG LOC Report: $($repo.name)"
    $report += "**Date:** $date"
    $report += "**Repo:** $($repo.name) ($repoPath)"
    $report += "**Thresholds:** max_lines=$maxLines, min_lines=$minLines"
    $report += ""

    $report += "## Large Files (> $maxLines lines) — Refactor Candidates"
    $report += ""
    if ($largeFiles.Count -gt 0) {
        $report += "| Lines | Path | Secondary Findings |"
        $report += "|-------|------|---------------------|"
        foreach ($lf in $largeFiles) {
            $findingsStr = ($lf.findings -join "; ") -replace '\|', '\\|'
            if (-not $findingsStr) { $findingsStr = "—" }
            $report += "| $($lf.lines) | `$($lf.path)` | $findingsStr |"
        }
    } else {
        $report += "_None_"
    }
    $report += ""

    $report += "## Small Files (<= $minLines lines) — Merge Candidates"
    $report += ""
    if ($smallFiles.Count -gt 0) {
        $report += "| Lines | Path | Suggested Merge Target |"
        $report += "|-------|------|------------------------|"
        foreach ($sf in $smallFiles) {
            $dir = Split-Path $sf.path
            $siblings = $smallFiles | Where-Object { Split-Path $_.path -eq $dir -and $_.path -ne $sf.path }
            $target = if ($siblings.Count -gt 0) { $siblings[0].path } else { "—" }
            $report += "| $($sf.lines) | `$($sf.path)` | $target |"
        }
    } else {
        $report += "_None_"
    }
    $report += ""

    $report | Set-Content $reportPath -Encoding UTF8
    $log += "  Report: $reportPath (Large: $($largeFiles.Count), Small: $($smallFiles.Count))"
}

$log += ""
$log += "=== SUMMARY ==="
$log += "Total repos processed: $($repos.Count)"
$log += "Total large files: $($allLargeFiles.Count)"
$log += "Total small files: $($allSmallFiles.Count)"

$log | Set-Content $logPath -Encoding UTF8

# Output Odysseus notes for large files as JSON
$odysseusNotes = @()
foreach ($f in $allLargeFiles | Sort-Object { $_.repo }, { -$_.lines }) {
    $note = @{
        title = "[eng-loc] Refactor: $($f.Repo)/$($f.Path) ($($f.Lines) lines)"
        tags = @("eng-loc", "refactor")
        body = "File: $($f.Repo)/$($f.Path)`nLines: $($f.Lines)`n`n"
    }
    if ($f.Findings.Count -gt 0) {
        $note.body += "Secondary scan findings:`n"
        foreach ($finding in $f.Findings) {
            $note.body += "- $finding`n"
        }
        $note.body += "`n*Findings are heuristics, not ground truth.*"
    }
    $odysseusNotes += $note
}

$odysseusNotes | ConvertTo-Json -Depth 5