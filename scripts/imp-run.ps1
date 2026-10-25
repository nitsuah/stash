#!/usr/bin/env pwsh
# imp‑run.ps1 – thin wrapper for IMP tool
param(
    [Parameter(Mandatory=$true)][string]$Args
)
# Load config (YAML) – simple parsing via PowerShell's ConvertFrom-Yaml (available in PS 7+)
$ConfigPath = Join-Path $PSScriptRoot "..\..\stash\.github\imps-config.yml"
$Config = Get-Content $ConfigPath -Raw | ConvertFrom-Yaml
$Kit = $Config.kit_path
# Execute IMP with passed args
node "$Kit\imps\imp.mjs" $Args
