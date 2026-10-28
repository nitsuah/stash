#!/usr/bin/env pwsh
# imp-run.ps1 - run the detached IMP kit from any checkout or worktree.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateNotNullOrEmpty()]
    [string]$Command,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ImpArgs = @()
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
$ConfigPath = Join-Path $RepoRoot '.github/imps-config.yml'
$LocalKitPath = Join-Path $RepoRoot '.imps/kit-path.txt'

if (-not (Test-Path -LiteralPath $ConfigPath -PathType Leaf)) {
    throw "IMP configuration not found: $ConfigPath"
}

# Read the small scalar config without relying on a non-standard YAML module.
$Config = @{}
foreach ($line in Get-Content -LiteralPath $ConfigPath) {
    if ($line -match '^\s*#' -or $line -match '^\s*$') { continue }
    if ($line -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*?)\s*$') {
        $value = $Matches[2].Trim()
        if ($value.Length -ge 2 -and (($value.StartsWith('"') -and $value.EndsWith('"')) -or ($value.StartsWith("'") -and $value.EndsWith("'")))) {
            $value = $value.Substring(1, $value.Length - 2)
        }
        $Config[$Matches[1]] = $value
    }
}

$Kit = $env:IMPS_KIT_PATH
if ([string]::IsNullOrWhiteSpace($Kit) -and (Test-Path -LiteralPath $LocalKitPath -PathType Leaf)) {
    $Kit = (Get-Content -LiteralPath $LocalKitPath -Raw).Trim()
}
if ([string]::IsNullOrWhiteSpace($Kit)) {
    $Kit = [string]$Config['kit_path']
}
if ([string]::IsNullOrWhiteSpace($Kit)) {
    throw "IMP kit path is not configured. Set IMPS_KIT_PATH or create '$LocalKitPath' with the absolute path to the detached IMP checkout."
}

$EntryPoint = Join-Path $Kit 'imps/imp.mjs'
if (-not (Test-Path -LiteralPath $EntryPoint -PathType Leaf)) {
    throw "IMP entry point not found: $EntryPoint. Check IMPS_KIT_PATH or $LocalKitPath."
}
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    throw 'Node.js is required but was not found on PATH.'
}

# Point humans / future kit hooks at the vault playbook without forking the kit.
$VaultPrompt = $env:IMPS_VAULT_PROMPT
if ([string]::IsNullOrWhiteSpace($VaultPrompt) -and -not [string]::IsNullOrWhiteSpace([string]$Config['vault_prompt'])) {
    $candidate = [string]$Config['vault_prompt']
    if (-not [System.IO.Path]::IsPathRooted($candidate)) {
        $candidate = Join-Path $RepoRoot $candidate
    }
    if (Test-Path -LiteralPath $candidate -PathType Leaf) {
        $env:IMPS_VAULT_PROMPT = $candidate
    }
}

& node $EntryPoint $Command @ImpArgs
$ExitCode = $LASTEXITCODE
if ($null -eq $ExitCode) { $ExitCode = 1 }
exit $ExitCode
