<#
Stage 0 foundations check + auto-start, for the local routine pipeline (see agent/prompts/DAILY.md, METRICS.md).

P0 foundations, confirmed 2026-09-16:
- Obsidian desktop app plus its Local REST API plugin (loopback :27123) - needed for any routine that
  wants live Obsidian access. Note: DAILY/METRICS/PMO today only touch the stash vault via plain git/file
  edits, not this API, so they work even without it - but this stays P0 because obn-* work and future
  Obsidian-native automation depend on it.
- Docker Desktop - needed for METRICS.md coverage runs (Docker-first) and for the Stage 3 skills
  (content-gen, site-gen) when those are back in scope.

agent-board's own containers (tool-content-gen :3200, tool-website :3201) are NOT a Stage 0 foundation -
they are only needed for Stage 3 (site-gen/content-gen), which is out of scope for now. Do not start them here.

Usage: powershell -File bootstrap-stage0.ps1 [-StartIfDown]
  -StartIfDown   Actually launch Obsidian/Docker Desktop if found down. Without it, this only reports state.
#>

param(
    [switch]$StartIfDown
)

$results = @()

# --- Obsidian: Local REST API. Plugin default is HTTPS :27124 (self-signed cert); the
# plain-HTTP :27123 port only works if "Enable Non-Encrypted HTTP Server" is turned on in the
# plugin's settings inside Obsidian. Confirmed 2026-09-16: this machine's mcp.json points at
# :27123 http, but the plugin was only actually listening on :27124 https - that mismatch, not
# a genuinely-down app, was the whole cause of the obsidian MCP server showing ConnectionRefused.
$obsidianUp = $false
$obsidianPort = $null
try {
    Invoke-WebRequest -Uri "http://127.0.0.1:27123/" -Method GET -TimeoutSec 3 -ErrorAction Stop | Out-Null
    $obsidianUp = $true
    $obsidianPort = "27123 (http)"
} catch {
    try {
        Invoke-WebRequest -Uri "https://127.0.0.1:27124/" -Method GET -TimeoutSec 3 -SkipCertificateCheck -ErrorAction Stop | Out-Null
        $obsidianUp = $true
        $obsidianPort = "27124 (https, self-signed cert)"
    } catch {
        $obsidianUp = $false
    }
}

if ($obsidianUp) {
    $results += "OK    Obsidian Local REST API reachable on $obsidianPort"
    if ($obsidianPort -like "*27124*") {
        $results += "      NOTE: mcp.json's obsidian entry points at :27123 http, which is not the port that's actually up - either enable"
        $results += "      'Non-Encrypted HTTP Server' in Obsidian's Local REST API plugin settings, or repoint mcp.json at :27124 https."
    }
} else {
    $results += "DOWN  Obsidian Local REST API not reachable on :27123 http or :27124 https"
    if ($StartIfDown) {
        $obsidianExe = "C:\Users\ajhar\AppData\Local\Programs\Obsidian\Obsidian.exe"
        if (Test-Path $obsidianExe) {
            Start-Process -FilePath $obsidianExe
            $results += "      started Obsidian.exe; give it 10-20s to start and enable the Local REST API plugin if not already enabled"
        } else {
            $results += "      Obsidian.exe not found at expected path ($obsidianExe), could not auto-start"
        }
    } else {
        $results += "      re-run with -StartIfDown to launch it automatically"
    }
}

# --- Docker Desktop ---
$dockerUp = $false
try {
    docker info *> $null
    if ($LASTEXITCODE -eq 0) { $dockerUp = $true }
} catch {
    $dockerUp = $false
}

if ($dockerUp) {
    $results += "OK    Docker Desktop is running"
} else {
    $results += "DOWN  Docker Desktop is not running or not responding"
    if ($StartIfDown) {
        $dockerExe = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
        if (Test-Path $dockerExe) {
            Start-Process -FilePath $dockerExe
            $results += "      started Docker Desktop; it can take 30-60s to finish starting the engine"
        } else {
            $results += "      Docker Desktop.exe not found at expected path ($dockerExe), could not auto-start"
        }
    } else {
        $results += "      re-run with -StartIfDown to launch it automatically"
    }
}

$results | ForEach-Object { Write-Output $_ }

if ((-not $obsidianUp) -or (-not $dockerUp)) { exit 1 } else { exit 0 }
