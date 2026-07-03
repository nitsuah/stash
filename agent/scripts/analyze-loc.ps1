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

# Exclude directories (aligned with Python EXCLUDE_DIRS)
$EXCLUDE_DIRS = @(
    "node_modules", ".git", "dist", "build", ".next", ".turbo",
    "coverage", ".pnpm-store", "vendor", "target", "bin", "obj",
    ".gradle", "out", ".claude", ".venv", "venv", ".obsidian", "env", ".env"
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
    $lines = $content -split "`n"
    $i = 0
    while ($i -lt $lines.Count) {
        $line = $lines[$i].Trim()

        # Skip empty lines and comments
        if (-not $line -or $line.StartsWith('#')) {
            $i++
            continue
        }

        # Section headers [repo.name]
        if ($line -match '^\[repo\.(.+)\]$') {
            $currentSection = $matches[1]
            $config.repo_overrides[$currentSection] = @{}
            $i++
            continue
        }

        # Key-value pairs
        if ($line -match '^(\w+)\s*=\s*(.*)$') {
            $key = $matches[1]
            $rawVal = $matches[2]

            # Strip inline comments (not inside quotes)
            $valClean = $rawVal
            if ($rawVal -match '^([^#]*?)\s*#') {
                # Check if # is outside quotes
                $beforeHash = $matches[1]
                $quoteCount = ($beforeHash.ToCharArray() | Where-Object { $_ -eq '"' -or $_ -eq "'" }).Count
                if ($quoteCount % 2 -eq 0) {
                    $valClean = $beforeHash
                }
            }
            $valClean = $valClean.Trim()

            # Parse value by type
            $val = $null

            # Boolean
            if ($valClean -eq 'true') {
                $val = $true
            }
            elseif ($valClean -eq 'false') {
                $val = $false
            }
            # Integer
            elseif ($valClean -match '^\d+$') {
                $val = [int]$valClean
            }
            # Float
            elseif ($valClean -match '^\d+\.\d+$') {
                $val = [double]$valClean
            }
            # Array (single or multi-line)
            elseif ($valClean.StartsWith('[')) {
                $arrayContent = $valClean
                # Handle multi-line arrays
                while (-not $arrayContent.TrimEnd().EndsWith(']') -and ($i + 1) -lt $lines.Count) {
                    $i++
                    $arrayContent += " " + $lines[$i].Trim()
                }
                # Strip [ ]
                $arrayContent = $arrayContent.Trim()
                if ($arrayContent.StartsWith('[') -and $arrayContent.EndsWith(']')) {
                    $arrayContent = $arrayContent.Substring(1, $arrayContent.Length - 2)
                }
                # Parse array elements
                $elements = @()
                $currentElement = ""
                $inQuote = $false
                $quoteChar = $null
                for ($c = 0; $c -lt $arrayContent.Length; $c++) {
                    $char = $arrayContent[$c]
                    if ($char -eq '"' -or $char -eq "'") {
                        if (-not $inQuote) {
                            $inQuote = $true
                            $quoteChar = $char
                        } elseif ($char -eq $quoteChar) {
                            $inQuote = $false
                            $quoteChar = $null
                        }
                    } elseif ($char -eq ',' -and -not $inQuote) {
                        $elem = $currentElement.Trim().Trim('"', "'").Trim()
                        if ($elem) { $elements += $elem }
                        $currentElement = ""
                        continue
                    }
                    $currentElement += $char
                }
                $elem = $currentElement.Trim().Trim('"', "'").Trim()
                if ($elem) { $elements += $elem }
                $val = $elements
            }
            # Quoted string
            elseif (($valClean.StartsWith('"') -and $valClean.EndsWith('"')) -or ($valClean.StartsWith("'") -and $valClean.EndsWith("'"))) {
                $val = $valClean.Substring(1, $valClean.Length - 2)
            }
            # Unquoted string
            else {
                $val = $valClean
            }

            # Store in config
            if ($currentSection) {
                $config.repo_overrides[$currentSection][$key] = $val
            } else {
                $config[$key] = $val
            }
        }
        $i++
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
function Get-LargeFileFinding {
    param([string]$FilePath, [string]$Extension)
    $findings = @()

    $content = Get-Content $FilePath -Raw -ErrorAction SilentlyContinue
    if (-not $content) { return $findings }

    $lines = $content -split "`n"

    # Check for unused imports (simple heuristic for JS/TS)
    if ($Extension -in @(".ts", ".tsx", ".js", ".jsx")) {
        $imports = $lines | Where-Object {
            $_ -match '^import\s+.*\s+from\s+["'']' -or $_ -match '^import\s+["'']'
        }
        foreach ($imp in $imports) {
            if ($imp -match 'import\s+\{([^}]+)\}') {
                $names = $matches[1] -split ',' | ForEach-Object { $_.Trim() }
                foreach ($name in $names) {
                    $name = $name.Trim()
                    if ($name) {
                        $escapedName = [regex]::Escape($name)
                        if ($content -notmatch "(?<![a-zA-Z0-9_])$escapedName(?![a-zA-Z0-9_])") {
                            $findings += "Unused import (heuristic): $name"
                        }
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
            if ($fn -and $fn -notmatch '^(main|init|test|Test)$') {
                $escapedFn = [regex]::Escape($fn)
                $refCount = ($content -split "(?<![a-zA-Z0-9_])$escapedFn(?![a-zA-Z0-9_])").Count - 1
                if ($refCount -le 1) {
                    $findings += "Unused function (heuristic): $fn"
                }
            }
        }
    }

    # Check for copy-paste blocks (>10 lines repeated)
    if ($lines.Count -gt 20) {
        $blockCounts = @{}
        $firstOccurrence = @{}
        for ($i = 0; $i -le $lines.Count - 10; $i++) {
            $block = $lines[$i..($i+9)] -join "`n"
            if ($block.Trim().Length -gt 50) {
                if ($blockCounts.ContainsKey($block)) {
                    $blockCounts[$block]++
                } else {
                    $blockCounts[$block] = 1
                    $firstOccurrence[$block] = $block
                }
            }
        }
        foreach ($block in $blockCounts.Keys) {
            if ($blockCounts[$block] -gt 1) {
                $findings += "Repeated block ($($blockCounts[$block]) occurrences, 10+ lines): $($block.Substring(0, [Math]::Min(80, $block.Length)))..."
                break
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

    $files = Get-ChildItem -Path $repoPath -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
        $ext = $_.Extension
        $inExt = $extensions -contains $ext
        $inExclude = $false
        $parent = $_.Directory
        while ($parent) {
            if ($EXCLUDE_DIRS -contains $parent.Name) { $inExclude = $true; break }
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
            $findings = Get-LargeFileFinding $file.FullName $file.Extension
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
            $siblings = $smallFiles | Where-Object { (Split-Path $_.path) -eq $dir -and $_.path -ne $sf.path }
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
        title = "[eng-loc] Refactor: $($f.repo)/$($f.path) ($($f.lines) lines)"
        tags = @("eng-loc", "refactor")
        body = "File: $($f.repo)/$($f.path)`nLines: $($f.lines)`n`n"
    }
    if ($f.findings.Count -gt 0) {
        $note.body += "Secondary scan findings:`n"
        foreach ($finding in $f.findings) {
            $note.body += "- $finding`n"
        }
        $note.body += "`n*Findings are heuristics, not ground truth.*"
    }
    $odysseusNotes += $note
}

$odysseusNotes | ConvertTo-Json -Depth 5