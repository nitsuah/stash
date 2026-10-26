#!/usr/bin/env pwsh
# imp-add-trailer.ps1 - ensure the latest commit has the Co-Authored-By line the
# imps gate checks (`/Co-Authored-By: .*imp/i` in lib.mjs). This is a commit
# trailer, not a field in the issue brief file.
[CmdletBinding()]
param(
    [Parameter()]
    [string]$Trailer = 'Co-Authored-By: 9router imp <noreply@anthropic.com>',

    [Parameter()]
    [switch]$Amend
)

$ErrorActionPreference = 'Stop'

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'git is required but was not found on PATH.'
}

$Head = git rev-parse --verify HEAD 2>$null
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($Head)) {
    throw 'No HEAD commit. Create a commit first, then re-run with -Amend.'
}

$Message = git log -1 --format=%B
if ($Message -match '(?im)^Co-Authored-By:\s*.*imp') {
    Write-Host 'Latest commit already has an imp Co-Authored-By trailer.' -ForegroundColor Yellow
    exit 0
}

if (-not $Amend) {
    Write-Host "Latest commit is missing the trailer. Re-run with -Amend to add:`n  $Trailer" -ForegroundColor Red
    exit 1
}

# Refuse to rewrite a commit that has already been pushed.
$Upstream = git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>$null
if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($Upstream)) {
    git merge-base --is-ancestor HEAD $Upstream 2>$null
    if ($LASTEXITCODE -eq 0) {
        throw "HEAD is already reachable from $Upstream; refusing to amend a pushed commit."
    }
}

$NewMessage = ($Message.TrimEnd() + "`n`n" + $Trailer + "`n")
$Tmp = [System.IO.Path]::GetTempFileName()
try {
    [System.IO.File]::WriteAllText($Tmp, $NewMessage)
    git commit --amend -F $Tmp
    if ($LASTEXITCODE -ne 0) { throw 'git commit --amend failed.' }
}
finally {
    Remove-Item -LiteralPath $Tmp -ErrorAction SilentlyContinue
}

Write-Host "Amended HEAD with: $Trailer" -ForegroundColor Green
