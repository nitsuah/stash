<#
.SYNOPSIS
Compresses and zips log files older than 5 days in the specified folders.
.DESCRIPTION 
The script selects files older than 5 days. The file is then NTFS compressed, archived (.zip) and the orignal file removed.  
.NOTES Modified By: Austin J. Hardy 20171213
Initial File Name:compress-logs.ps1
Initial Author: Nikolay Petkov http://power-shell.com/
#>
<#VARS/PARMS#>
$srvType ="Not detected"
$ErrorActionPreference = "Stop"
$CurDate=(get-date -Format FileDate)
$LastWrite=(get-date).AddDays(-5).ToString("MM/dd/yyyy")

<#START LOG#>
Write-Output "||PROCESS STARTING||$CurDate"
Write-Host -ForegroundColor Cyan "||PROCESS STARTING||$CurDate"

<#START TIMER#>
$StopWatch = New-Object System.Diagnostics.Stopwatch
$StopWatch.Start()
<# DETECT_SERVER_V0_3D.PS1
.SYNOPSIS 
Identifies the server type depending on directories available.
.DESCRIPTION 
Server type specifies the log directories for cleanup of the compression script.
.NOTES
File Name  : detect_server.ps1
Version: v.0.3.c
Author: Austin Hardy
#>

<#INITIAL ENVARS#>
#$JBOSS = "C:\users\hardya\desktop #$env:JBOSS_HOME #JBOSS Checkvar - DEV
#$JBOSS6 = 'null' #DevCheckvar
#$JBOSS6 = $env:JBOSS_HOME #JBOSS home dir
#$JBOSS6 = $env:JBOSS5_HOME #lamplite? /other
#$JBOSS6 = "C:\ORG_SAND_JBOSS\jboss-6.2.0.GA"
$JBOSS6 = "C:\ORG_SAND_JBOSS\jboss-5.1.0.GA"


$ErrorActionPreference = "silentlycontinue"
$jboss_detect = Test-Path -path $JBOSS6
$ErrorActionPreference = "Pause"

<#JBOSS DETECTION#>
if ($jboss_detect -eq 'True')
{
Write-Host "JBOSS DETECTED" -ForegroundColor Blue -BackgroundColor Gray
Write-Host "ENVAR:" $jboss_detect -ForegroundColor green
Write-Host "PATH:" $JBOSS6
Set-Variable $srvJBOSS = $JBOSS6
$srvJBOSSDIR="{0:N2} GB" -f ((Get-ChildItem $srvJBOSS -Recurse | Measure-Object -Property Length -Sum -ErrorAction Stop).Sum / 1GB)

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

<#CWA LOG DIRECTORIES#>
#$logdirs=@("ORG_backoffice\log","ORG_borrower\log","ORG_finrecon\log","ORG_lender\log","ORG_Operations\log","ORG_partner\log","ORG_TFA\log")
#$logdirs=@("ORG_backoffice","ORG_borrower","ORG_finrecon","ORG_lender","ORG_Operations","ORG_partner","ORG_TFA")

<#JVMA LOG DIRECTORIES UNDER DOMAIN#>
#$logdirs=@("$JBOSS\domain\log","$JBOSS\domain\servers\*host*inst*\log","$JBOSS5\server\lamplite\log")
# do test-path of lamplite before JVM cleanup in case server is WS instead of app

<#JVMWS LOG DIRECTORIES UNDER DOMAIN#>
#$logdirs=@("$JBOSS\domain\log","$JBOSS\domain\servers\*host*inst*\log")
#Test-Path $JBOSS"\domain\servers\*host*inst*\log\" #if true then type = JVMWS

<#begin compression#>

if ($srvType -eq "Not detected") {
Write-Output "||NO LOG FILES FOUND" 
Write-Host "||NO LOG FILES FOUND"
}
#Write-Host $logdirs
else {
Write-Output "||SERVER TYPE=$srvType" 
Write-Host "||SERVER TYPE=$srvType"
<#LOG DIRECTORY LOOP#>
foreach ($logdirectory in $logdirs)
{
Write-Output "||"$logdirectory.toUpper()
$LogFiles="$logdirectory\*.*"
$LogFolder="$logdirectory\"

<#OUTPUT DIRECTORY SIZE BEFORE#>
$DIRB4="{0:N2} MB" -f ((Get-ChildItem $LogFolder -Recurse | Measure-Object -Property Length -Sum -ErrorAction Stop).Sum / 1MB)
Write-Output "||BEFORE: $DIRB4"

<#COMPRESS,ZIP,REMOVE OLD#>
If ($Logs = get-childitem $LogFiles | Where-Object {$_.LastWriteTime -le $LastWrite -and !($_.PSIsContainer)} | sort-object LastWriteTime)
{foreach ($L in $Logs){
$FullName=$L.FullName
$WMIFileName= $FullName.Replace("\", "\\")
$WMIQuery = Get-WmiObject -Query “SELECT * FROM CIM_DataFile WHERE Name='$WMIFileName'“
If ($WMIQuery.Compress()) {
$ArcName="$FullName.zip"
Compress-Archive -Force -Path $FullName -CompressionLevel Fastest -DestinationPath $ArcName 
$FileChk = Test-Path $ArcName
#add counter here to increment files archived
#Write-Host "||"$CurDate"-------------||$FullName compressed & archived successfully."-ForegroundColor Green}
If($FileChk -eq 'True'){Remove-Item $FullName} else {Write-Output "||-------------||Archive not found, skipping removal."}
}
else{
Write-Output "||-------------||Found no log files older than 5 days." 
Write-Host "||$logdirectory||Found no log files older than 5 days." -ForegroundColor Green}
}
}
<#OUTPUT DIRECTORY SIZE AFTER#>
$DIRAFT="{0:N2} MB" -f ((Get-ChildItem $LogFolder -Recurse | Measure-Object -Property Length -Sum -ErrorAction Stop).Sum / 1MB)
Write-Output "||AFTER: $DIRAFT"
}
$StopWatch.Stop()
$srvJBOSSAFT="{0:N2} GB" -f ((Get-ChildItem $srvJBOSS -Recurse | Measure-Object -Property Length -Sum -ErrorAction Stop).Sum / 1GB)
$Duration = $StopWatch.Elapsed.ToString('dd\.hh\:mm\:ss')
Write-Host "||"
Write-Host -ForegroundColor Cyan "||PROCESS COMPLETED IN:||"$StopWatch.Elapsed
Write-Host "||DIR BEFORE: $srvJBOSSDIR" -ForegroundColor Red
Write-Host "||DIR AFTER: $srvJBOSSAFT" -ForegroundColor Green
Write-Output "||"
Write-Output "||PROCESS COMPLETED IN:||" $Duration
Write-Output "||DIR TOTAL BEFORE:$srvJBOSSDIR"
Write-Output "||DIR TOTAL AFTER:$srvJBOSSAFT"
}