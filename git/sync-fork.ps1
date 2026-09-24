# Keeps a GitHub fork AND its local clone level with the upstream repository.
#   1. `gh repo sync <fork> -b <branch>` (same as the "Sync fork" button on GitHub)
#   2. fetches `upstream` locally and fast-forwards the local <branch>
# Fast-forward only: never merges, rebases, force-pushes, or touches a dirty checkout.
# Exits 1 when a sync step fails (after logging), so Task Scheduler shows the failure.
# Use -Install to register an hourly + at-logon Windows scheduled task running this script.

param(
    [Parameter(Mandatory = $true)]
    [string]$Fork,                          # e.g. nitsuah/9router
    [Parameter(Mandatory = $true)]
    [string]$RepoPath,                      # local clone with an `upstream` remote
    [string]$Branch = "master",
    [string]$UpstreamRemote = "upstream",
    [string]$LogPath = "",                  # default: <this folder>\logs\<repo>-sync.log
    [int]$IntervalHours = 1,
    [switch]$Install = $false,
    [switch]$Uninstall = $false
)

$ErrorActionPreference = "Stop"
$repoName = ($Fork -split "/")[-1]
$taskName = "Sync fork $Fork"
if (-not $LogPath) { $LogPath = Join-Path $PSScriptRoot "logs\$repoName-sync.log" }
# Absolute paths: a scheduled task runs from %windir%\system32, not the install directory.
$RepoPath = (Resolve-Path -LiteralPath "$RepoPath").Path
$LogPath  = [System.IO.Path]::GetFullPath("$LogPath")

if ($Uninstall) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "Removed scheduled task '$taskName'" -ForegroundColor Yellow
    return
}

if ($Install) {
    $pwsh = (Get-Command pwsh -ErrorAction SilentlyContinue).Source
    if (-not $pwsh) { $pwsh = (Get-Command powershell).Source }
    $scriptArgs = "-NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$PSCommandPath`" " +
                  "-Fork $Fork -RepoPath `"$RepoPath`" -Branch $Branch -UpstreamRemote $UpstreamRemote -LogPath `"$LogPath`""
    $user = "$env:USERDOMAIN\$env:USERNAME"
    $action = New-ScheduledTaskAction -Execute $pwsh -Argument $scriptArgs -WorkingDirectory "$RepoPath"
    $triggers = @(
        (New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(5) -RepetitionInterval (New-TimeSpan -Hours $IntervalHours)),
        (New-ScheduledTaskTrigger -AtLogOn -User $user)
    )
    # StartWhenAvailable: catch up after sleep/boot. Interactive: runs as you, so `gh` uses your login.
    $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
        -ExecutionTimeLimit (New-TimeSpan -Minutes 10) -MultipleInstances IgnoreNew
    $principal = New-ScheduledTaskPrincipal -UserId $user -LogonType Interactive -RunLevel Limited
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $triggers -Settings $settings -Principal $principal `
        -Description "Fast-forwards $Fork and $RepoPath ($Branch) from upstream. Log: $LogPath" -Force | Out-Null
    Write-Host "Registered '$taskName' (every $IntervalHours h + at logon). Log: $LogPath" -ForegroundColor Green
    return
}

New-Item -ItemType Directory -Force (Split-Path "$LogPath") | Out-Null
function Write-Log($msg) { "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $msg" | Add-Content -Path "$LogPath" -Encoding utf8 }
$failed = $false

try {
    # 1. GitHub fork. Refuses (and logs) instead of overwriting if the fork branch diverged.
    $out = gh repo sync $Fork -b $Branch 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) { $failed = $true; Write-Log "fork sync FAILED: $($out.Trim())" }
    else { Write-Log "fork: $(if ($out.Trim()) { $out.Trim() } else { "$Fork $Branch synced with upstream" })" }

    # 2. Local clone. A failed fetch would leave stale refs, so stop rather than report "up to date".
    $out = git -C "$RepoPath" fetch --quiet --prune $UpstreamRemote 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) { throw "fetch $UpstreamRemote failed: $($out.Trim())" }
    $out = git -C "$RepoPath" fetch --quiet --prune origin 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) { throw "fetch origin failed: $($out.Trim())" }

    $current = (git -C "$RepoPath" rev-parse --abbrev-ref HEAD).Trim()
    $count   = git -C "$RepoPath" rev-list --count "$Branch..$UpstreamRemote/$Branch" 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) { throw "rev-list failed: $($count.Trim())" }
    $behind  = [int]$count.Trim()

    if ($behind -eq 0) {
        Write-Log "local: $Branch already up to date"
    } elseif ($current -eq $Branch) {
        if (git -C "$RepoPath" status --porcelain --untracked-files=no) {
            Write-Log "local: $Branch is checked out with uncommitted changes; skipped ($behind behind)"
        } else {
            $out = git -C "$RepoPath" merge --ff-only --quiet "$UpstreamRemote/$Branch" 2>&1 | Out-String
            if ($LASTEXITCODE -eq 0) { Write-Log "local: fast-forwarded checked-out $Branch by $behind" }
            else { $failed = $true; Write-Log "local: fast-forward refused (diverged?): $($out.Trim())" }
        }
    } else {
        # Not checked out: move the branch ref directly (git refuses anything but a fast-forward).
        $out = git -C "$RepoPath" fetch --quiet $UpstreamRemote "${Branch}:${Branch}" 2>&1 | Out-String
        if ($LASTEXITCODE -eq 0) { Write-Log "local: fast-forwarded $Branch by $behind (on '$current')" }
        else { $failed = $true; Write-Log "local: fast-forward refused (diverged?): $($out.Trim())" }
    }
} catch {
    $failed = $true
    Write-Log "ERROR: $($_.Exception.Message)"
}

# Keep the log small.
$lines = Get-Content "$LogPath" -ErrorAction SilentlyContinue
if ($lines.Count -gt 1000) { $lines | Select-Object -Last 500 | Set-Content "$LogPath" -Encoding utf8 }

if ($failed) { exit 1 }
