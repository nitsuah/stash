<# DETECT_SERVER_V0_3D.PS1
.SYNOPSIS 
Identifies the JVM server type depending on directories available.
.DESCRIPTION 
Server type specifies the log directories for cleanup of the compression script.
.NOTES
File Name  : detect-server.ps1
Version: v.0.3.c
Author: Austin Hardy
#>

#$JBOSS = "C:\users\hardya\desktop #$env:JBOSS_HOME #JBOSS Checkvar - DEV
$JBOSS6 = "C:\ORG_SAND_JBOSS\jboss-5.1.0.GA"
#$JBOSS6 = "C:\ORG_SAND_JBOSS\jboss-6.2.0.GA"
#$JBOSS6 = 'null' #DevCheckvar

<#INITIAL ENVARS#>
#$JBOSS6 = $env:JBOSS_HOME #JBOSS home dir
#$JBOSS5 = $env:JBOSS5_HOME #lamplite? /other

$ErrorActionPreference = "silentlycontinue"
$jboss_detect = Test-Path -path $JBOSS6
$ErrorActionPreference = "Pause"

<#JBOSS DETECTION#>
if ($jboss_detect -eq 'True')
{
Write-Host "JBOSS DETECTED" -ForegroundColor Blue -BackgroundColor Gray
Write-Host "ENVAR:" $jboss_detect -ForegroundColor green
Write-Host "PATH:" $JBOSS6

<#SERVER TYPE DETECTION#>
$JVMETL = Test-Path "C:\CRS5ETL\custom"
$JVMAPP = Test-Path $JBOSS6"\domain"
$CWA = Test-Path $JBOSS6"\server\ORG_backoffice"

<#JBOSS SERVER SET#>
if ($JVMETL -eq 'True') {
$logdirs=@(Join-Path (Resolve-path $JBOSS6"\domain\servers\*") "\log")
$srvType = "JVMETL"
}
Elseif($JVMAPP -eq 'True') {
$logdirs=@(Join-Path (Resolve-path $JBOSS6"\domain\servers\*") "\log")
$srvType = "JVMAPP"
}
Elseif ($CWA -eq 'True') {
$logdirs=@((Resolve-path $JBOSS6"\server\ORG_backoffice\log" ),(Resolve-path $JBOSS6"\server\ORG_borrower\log"),(Resolve-path $JBOSS6"\server\ORG_finrecon\log"),(Resolve-path $JBOSS6"\server\ORG_lender\log"),(Resolve-path $JBOSS6"\server\ORG_Operations\log"),(Resolve-path $JBOSS6"\server\ORG_partner\log"),(Resolve-path $JBOSS6"\server\ORG_TFA\log"))
$srvType = "CWA"
}
<#DETECTION OUTPUT#>
Write-Host "SERVER DETECTION" -ForegroundColor Blue -BackgroundColor Gray
Write-Host "TYPE:"$srvType 
Write-Host "LOGS:"
($logdirs | Format-Table -HideTableHeaders | Out-String).TrimStart()
}
Else 
{
<#WEBSERVER DETECTION #>
$WEBSRVR = Test-Path "C:\Program Files\Apache24"
if($WEBSRVR -eq 'True') {
$logdirs=@("C:\Program Files\Apache24\")
$srvType = "WEBSRVR"
}
Else {
$logdirs=@("Not detected")
$srvType = "Not detected"
Write-Host "NO JBOSS FOUND - PLEASE RERUN" -ForegroundColor RED -BackgroundColor Gray
}
Write-Host "NO JBOSS FOUND" -ForegroundColor RED -BackgroundColor Gray
Write-Host "SERVER DETECTION" -ForegroundColor Blue -BackgroundColor Gray
Write-Host "TYPE:"$srvType 
Write-Host "LOGS:"
($logdirs | Format-Table -HideTableHeaders | Out-String).TrimStart()
}