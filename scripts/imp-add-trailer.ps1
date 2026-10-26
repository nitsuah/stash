# imp-add-trailer.ps1 - ensure an IMP brief includes the required trailer.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$BriefPath
)

$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $BriefPath -PathType Leaf)) {
    throw "Brief file not found: $BriefPath"
}

$Content = Get-Content -LiteralPath $BriefPath -Raw
if ($Content -notmatch '(?im)^Imp\s+trailer\s*:') {
    $Trailer = "`n---`nImp trailer: auto-generated on $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    Add-Content -LiteralPath $BriefPath -Value $Trailer -Encoding utf8
    Write-Host "Added IMP trailer to $BriefPath" -ForegroundColor Green
} else {
    Write-Host "IMP trailer already present in $BriefPath" -ForegroundColor Yellow
}
