<#
.SYNOPSIS
  Registers the code-driven routines in Windows Task Scheduler (schedule as code).
.DESCRIPTION
  Idempotent: each task is created with /F, so re-running replaces it. Prints the schtasks
  commands without -Apply. Registers nothing on its own: run it by hand after the Nov 4 reset,
  then disable the matching Claude-plan tasks (daily-repo-sync, week-sotu, monthly-tire-kick,
  monthly-pmo-audit, week-fin-sum). Paths must not contain spaces.
.EXAMPLE
  pwsh -File agent/scripts/install-tasks.ps1            # print only
  pwsh -File agent/scripts/install-tasks.ps1 -Apply     # register
  pwsh -File agent/scripts/install-tasks.ps1 -Apply -StartDate 2026-11-04   # register, first runs on/after that date
  pwsh -File agent/scripts/install-tasks.ps1 -Apply -Remove   # unregister
.NOTES
  Set VIGIL_MCP_KEY as a user environment variable for daily-run's Tasks section; the key is
  never stored in this repo. Add each task name to KNOWN_TASKS in local-audit.mjs (done for these).
#>
param(
    [switch]$Apply,
    [switch]$Remove,
    [string]$StartDate = '',   # yyyy-MM-dd: first run on or after this date (e.g. 2026-11-04)
    [string]$StashRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path,
    [string]$FireRoot = (Join-Path (Split-Path $StashRoot -Parent) 'fire')
)

$ErrorActionPreference = 'Stop'
$logDir = Join-Path $StashRoot 'agent\logs'
# schtasks wants the date in the machine's short-date format.
$sd = @()
if ($StartDate) { $sd = @('/SD', (Get-Date $StartDate).ToString('d')) }
$node = 'node'

# name, schtasks schedule args, working dir, command
$tasks = @(
    @{ Name = 'routine-daily-run'; Sched = @('/SC', 'WEEKLY', '/D', 'MON,WED,FRI,SAT', '/ST', '07:00'); Dir = $StashRoot
       Cmd = "$node agent\scripts\daily-run.mjs --apply --root $StashRoot"; Log = (Join-Path $logDir 'daily-run.log') }
    @{ Name = 'routine-sotu'; Sched = @('/SC', 'WEEKLY', '/D', 'MON', '/ST', '05:10'); Dir = $StashRoot
       Cmd = "$node agent\scripts\pipeline-run.mjs sotu --apply --root $StashRoot"; Log = (Join-Path $logDir 'pipeline-sotu.log') }
    @{ Name = 'routine-tire'; Sched = @('/SC', 'MONTHLY', '/D', '28', '/ST', '08:00'); Dir = $StashRoot
       Cmd = "$node agent\scripts\pipeline-run.mjs tire --apply --root $StashRoot"; Log = (Join-Path $logDir 'pipeline-tire.log') }
    @{ Name = 'routine-pmo'; Sched = @('/SC', 'MONTHLY', '/D', '1', '/ST', '08:00'); Dir = $StashRoot
       Cmd = "$node agent\scripts\pipeline-run.mjs pmo --apply --root $StashRoot"; Log = (Join-Path $logDir 'pipeline-pmo.log') }
    @{ Name = 'routine-fin-checkin'; Sched = @('/SC', 'MONTHLY', '/D', '1', '/ST', '17:33'); Dir = $FireRoot
       Cmd = "$node scripts\fin-checkin.mjs --no-model"; Log = (Join-Path $env:USERPROFILE '.fire\weekly-checkin.log') }
)

foreach ($t in $tasks) {
    if ($Remove) {
        $args = @('/Delete', '/TN', $t.Name, '/F')
    } else {
        $tr = "cmd /c cd /d $($t.Dir) && $($t.Cmd) >> $($t.Log) 2>&1"
        $args = @('/Create', '/TN', $t.Name, '/TR', $tr, '/F') + $t.Sched + $sd
    }
    if (-not $Apply) { Write-Host "schtasks $($args -join ' ')"; continue }
    if (-not $Remove) { New-Item -ItemType Directory -Force -Path (Split-Path $t.Log -Parent) | Out-Null }
    & schtasks.exe @args
    if ($LASTEXITCODE -ne 0) { Write-Warning "$($t.Name): schtasks exited $LASTEXITCODE" }
}
if (-not $Apply) { Write-Host 'Dry run only. Re-run with -Apply to register.' }
