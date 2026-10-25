# imp-add-trailer.ps1 – ensure IMP brief includes required trailer
# This script is called by the brief‑generation pipeline (if you have one).
# It appends a standardized trailer line to the brief markdown file before the IMP gate runs.

param(
    [Parameter(Mandatory=$true)][string]$BriefPath
)

$trailer = "\n---\nImp trailer: auto‑generated on $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

if (Test-Path $BriefPath) {
    $content = Get-Content $BriefPath -Raw
    if ($content -notmatch "Imp\s+trailer") {
        Add-Content -Path $BriefPath -Value $trailer -Encoding utf8
        Write-Host "Added IMP trailer to $BriefPath"
    } else {
        Write-Host "IMP trailer already present in $BriefPath"
    }
} else {
    Write-Error "Brief file not found: $BriefPath"
}
