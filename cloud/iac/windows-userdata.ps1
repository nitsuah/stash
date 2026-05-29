<powershell>
# =============================================================================
# Windows EC2 UserData — PowerShell Bootstrap Script
# =============================================================================
# Usage:
#   Paste into AWS EC2 "User data" field (wrapped in <powershell> tags as shown)
#   or supply via AWS CLI:
#     aws ec2 run-instances --user-data file://IAS/windows-userdata.ps1 ...
#
# Runs once as SYSTEM on first boot.
# Tested on Windows Server 2022 Base AMI — adapt for 2019 as needed.
# =============================================================================

$ErrorActionPreference = "Stop"
$LogFile = "C:\bootstrap.log"

function Write-Log {
    param([string]$Message)
    "$((Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))  $Message" | Tee-Object -FilePath $LogFile -Append
}

Write-Log "Bootstrap started"

# ── Set computer name ─────────────────────────────────────────────────────────
try {
    $InstanceId = (Invoke-RestMethod -Uri "http://169.254.169.254/latest/meta-data/instance-id" -TimeoutSec 5)
    $ShortId    = $InstanceId -replace "^i-", ""
    $NewName    = "APP-$($ShortId.Substring(0, [Math]::Min(8, $ShortId.Length)).ToUpper())"
    Rename-Computer -NewName $NewName -Force
    Write-Log "Hostname set to $NewName"
} catch {
    Write-Log "WARNING: Could not retrieve instance ID — hostname unchanged"
}

# ── Install Chocolatey ────────────────────────────────────────────────────────
Write-Log "Installing Chocolatey..."
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# ── Install packages ──────────────────────────────────────────────────────────
Write-Log "Installing packages..."
foreach ($pkg in @("git", "awscli", "python3", "7zip", "notepadplusplus", "googlechrome")) {
    try   { choco install $pkg -y --no-progress; Write-Log "Installed: $pkg" }
    catch { Write-Log "WARNING: Failed to install $pkg — $_" }
}

# ── Install IIS ───────────────────────────────────────────────────────────────
Write-Log "Installing IIS..."
Install-WindowsFeature -Name Web-Server -IncludeManagementTools
Install-WindowsFeature -Name Web-Asp-Net45
Write-Log "IIS installed"

# ── Firewall rules ────────────────────────────────────────────────────────────
Write-Log "Configuring firewall rules..."
New-NetFirewallRule -DisplayName "Allow HTTP"  -Direction Inbound -Protocol TCP -LocalPort 80   -Action Allow
New-NetFirewallRule -DisplayName "Allow HTTPS" -Direction Inbound -Protocol TCP -LocalPort 443  -Action Allow
New-NetFirewallRule -DisplayName "Allow RDP"   -Direction Inbound -Protocol TCP -LocalPort 3389 -Action Allow

# ── Install CloudWatch Agent ──────────────────────────────────────────────────
Write-Log "Installing CloudWatch agent..."
New-Item -ItemType Directory -Force -Path "C:\Temp" | Out-Null
$CWAgentMsi = "C:\Temp\amazon-cloudwatch-agent.msi"
Invoke-WebRequest -Uri "https://s3.amazonaws.com/amazoncloudwatch-agent/windows/amd64/latest/amazon-cloudwatch-agent.msi" -OutFile $CWAgentMsi
Start-Process msiexec.exe -Wait -ArgumentList "/i $CWAgentMsi /quiet"

@'
{
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          { "file_path": "C:\\bootstrap.log",                        "log_group_name": "/ec2/windows/bootstrap",     "log_stream_name": "{instance_id}/bootstrap" },
          { "file_path": "C:\\inetpub\\logs\\LogFiles\\W3SVC1\\*.log", "log_group_name": "/ec2/windows/iis",           "log_stream_name": "{instance_id}/iis"       }
        ]
      },
      "windows_events": {
        "collect_list": [
          { "event_name": "System", "event_levels": ["WARNING","ERROR","CRITICAL"], "log_group_name": "/ec2/windows/system-events", "log_stream_name": "{instance_id}/system" }
        ]
      }
    }
  }
}
'@ | Out-File -FilePath "C:\ProgramData\Amazon\AmazonCloudWatchAgent\amazon-cloudwatch-agent.json" -Encoding utf8

& "C:\Program Files\Amazon\AmazonCloudWatchAgent\amazon-cloudwatch-agent-ctl.ps1" `
    -a fetch-config -m ec2 -s `
    -c "file:C:\ProgramData\Amazon\AmazonCloudWatchAgent\amazon-cloudwatch-agent.json"

# ── Security hardening ────────────────────────────────────────────────────────
Write-Log "Applying security hardening..."
Set-SmbServerConfiguration -EnableSMB1Protocol $false -Force
foreach ($svc in @("Fax","XblGameSave","XboxNetApiSvc")) {
    try { Set-Service -Name $svc -StartupType Disabled } catch {}
}
foreach ($path in @(
    "HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Server",
    "HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Server"
)) {
    New-Item -Path $path -Force | Out-Null
    New-ItemProperty -Path $path -Name "Enabled"           -Value 0 -PropertyType DWORD -Force | Out-Null
    New-ItemProperty -Path $path -Name "DisabledByDefault"  -Value 1 -PropertyType DWORD -Force | Out-Null
}
Write-Log "Security hardening applied"

# ── SSM Parameter Store (example — requires ssm:GetParameter IAM permission) ─
# $DbPassword = (aws ssm get-parameter `
#     --name "/myapp/prod/db-password" --with-decryption `
#     --query "Parameter.Value" --output text --region us-east-1)
# [System.Environment]::SetEnvironmentVariable("DB_PASSWORD", $DbPassword, "Machine")

# ── CloudFormation signal (if launched via CFN stack) ────────────────────────
# cfn-signal.exe -e $LASTEXITCODE `
#     --stack $env:AWS_STACK_NAME --resource AutoScalingGroup --region $env:AWS_REGION

Write-Log "Bootstrap complete"
</powershell>
