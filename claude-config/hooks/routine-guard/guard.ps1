# PreToolUse guard for manual routine runs (added 2026-09-26, stash routine-audit-2026-09-26).
# Forces a confirmation prompt on RemoteTrigger run / run_scheduled_task, with a cost tier and a same-day repeat warning.
$ErrorActionPreference = 'SilentlyContinue'
$in = [Console]::In.ReadToEnd() | ConvertFrom-Json
$tool = $in.tool_name
$ti = $in.tool_input
if ($tool -eq 'RemoteTrigger') {
  if ($ti.action -ne 'run') { exit 0 }
  $id = $ti.trigger_id
} elseif ($tool -like '*run_scheduled_task') {
  $id = $ti.taskId
} else { exit 0 }

$heavy = @('monthly-pmo-audit','monthly-self-improvement','monthly-tire-kick','trig_01DFtorzK5HJ9js31HhYun7L','trig_01N2UynTFCkPoNJbm6jiWgt3')
$medium = @('week-sotu','monthly-usage-report','daily-repo-sync','trig_01BbYVwcsZPFV4QrQrTZAhJb','trig_01LZ1JrGn9J2FRPBuTnrPxvA')
$tier = if ($heavy -contains $id) { 'HEAVY (multi-repo, can eat a large share of the 5-hour window)' } elseif ($medium -contains $id) { 'MEDIUM' } else { 'LIGHT' }

$log = Join-Path $PSScriptRoot 'manual-runs.log'
$today = (Get-Date).ToString('yyyy-MM-dd')
$again = ''
if (Test-Path $log) {
  if (Select-String -Path $log -SimpleMatch "$today $id" -Quiet) { $again = ' ALREADY FIRED MANUALLY TODAY: a repeat usually burns quota for the same result.' }
}
Add-Content -Path $log -Value "$today $id $(Get-Date -Format HH:mm)"

$reason = "Manual routine run: $id, cost tier $tier.$again Check get_usage first. If the weekly window is above ~75% or the 5-hour window above ~50%, let ops-catchup schedule it after the Wed 05:00 UTC reset. Fire catch-ups one at a time, never several together."
@{ hookSpecificOutput = @{ hookEventName = 'PreToolUse'; permissionDecision = 'ask'; permissionDecisionReason = $reason } } | ConvertTo-Json -Compress
exit 0
