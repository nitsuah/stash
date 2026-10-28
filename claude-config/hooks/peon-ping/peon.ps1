# peon-ping hook for Claude Code (Windows native)
# Called by Claude Code hooks on SessionStart, Stop, Notification, PermissionRequest, PostToolUseFailure, PreCompact

param(
    [string]$Command = "",
    [string]$Arg1 = "",
    [string]$Arg2 = "",
    [Parameter(ValueFromRemainingArguments)]$ExtraArgs = @()
)

# 8-second self-timeout safety net â€” kills this process if anything blocks unexpectedly.
# Uses System.Timers.Timer (not Forms.Timer) so it works in headless PowerShell without a message pump.
# Must fire before ANY I/O (config read, state read, stdin read).
if (-not $Command) {
    $safetyTimer = New-Object System.Timers.Timer
    $safetyTimer.Interval = 8000
    $safetyTimer.AutoReset = $false
    Register-ObjectEvent -InputObject $safetyTimer -EventName Elapsed -Action { [Environment]::Exit(1) } | Out-Null
    $safetyTimer.Start()
}

# Diagnostic logging: set PEON_DEBUG=1 to surface silent failure diagnostics on stderr
$peonDebug = $env:PEON_DEBUG -eq "1"

# Raw config read; repair is done at install/update time, so hook only needs plain read.
function Get-PeonConfigRaw {
    param([string]$Path)
    return Get-Content $Path -Raw
}

# Write a config object to a JSON file with culture-safe serialization.
# Saves and restores CurrentCulture in a try/finally to guarantee no culture leak,
# preventing locale-damaged decimals (e.g. "volume": 0,5 on European locales).
function Set-PeonConfig {
    param($Config, [string]$Path)
    $prevCulture = [System.Threading.Thread]::CurrentThread.CurrentCulture
    try {
        [System.Threading.Thread]::CurrentThread.CurrentCulture = [System.Globalization.CultureInfo]::InvariantCulture
        $Config | ConvertTo-Json -Depth 10 | Set-Content $Path -Encoding UTF8
    } finally {
        [System.Threading.Thread]::CurrentThread.CurrentCulture = $prevCulture
    }
}

# Resolve the active pack from config using the default_pack -> active_pack -> "peon" fallback chain.
# Accepts any object with optional default_pack and/or active_pack properties.
function Get-ActivePack($config) {
    if ($config.default_pack) { return $config.default_pack }
    if ($config.active_pack) { return $config.active_pack }
    return "peon"
}

function Normalize-IdeId {
    param([string]$Value)
    if (-not $Value) { return "" }
    $key = $Value.Trim().ToLowerInvariant().Replace("_", "-").Replace(" ", "-")
    switch ($key) {
        "claude" { return "claude" }
        "claude-code" { return "claude" }
        "claudecode" { return "claude" }
        "codex" { return "codex" }
        "openai-codex" { return "codex" }
        "cursor" { return "cursor" }
        "opencode" { return "opencode" }
        "open-code" { return "opencode" }
        "kilo" { return "kilo" }
        "kiro" { return "kiro" }
        "gemini" { return "gemini" }
        "copilot" { return "copilot" }
        "windsurf" { return "windsurf" }
        "kimi" { return "kimi" }
        "antigravity" { return "antigravity" }
        "amp" { return "amp" }
        "deepagents" { return "deepagents" }
        "deep-agents" { return "deepagents" }
        "openclaw" { return "openclaw" }
        "open-claw" { return "openclaw" }
        "rovodev" { return "rovodev" }
        "rovo" { return "rovodev" }
        "qwen" { return "qwen" }
        "qwen-code" { return "qwen" }
        "iflow" { return "iflow" }
        "iflow-cli" { return "iflow" }
        "trae" { return "trae" }
        "kiro-ide" { return "kiro-ide" }
        "eca" { return "eca" }
        default { return $key }
    }
}

function Get-KnownIdeIds {
    return @("claude", "codex", "cursor", "opencode", "kilo", "kiro", "gemini", "copilot", "windsurf", "kimi", "antigravity", "amp", "deepagents", "openclaw", "rovodev")
}

function Expand-UserPath {
    param([string]$PathValue)
    if (-not $PathValue) { return "" }
    $expanded = $PathValue
    if ($expanded.StartsWith("~")) {
        $homeDir = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
        $expanded = Join-Path $homeDir $expanded.Substring(1).TrimStart('\','/')
    }
    return [Environment]::ExpandEnvironmentVariables($expanded)
}

function Normalize-PathForRules {
    param([string]$PathValue)
    if (-not $PathValue) { return "" }
    $expanded = Expand-UserPath $PathValue
    if (-not $expanded) { return "" }
    $normalized = $expanded -replace '\\', '/'
    return $normalized.TrimEnd('/')
}

function Test-PathRuleMatch {
    param([string]$PathValue, [string]$Pattern)
    $pathNorm = Normalize-PathForRules $PathValue
    $patternNorm = Normalize-PathForRules $Pattern
    if (-not $pathNorm -or -not $patternNorm) { return $false }
    $hasWildcard = ($patternNorm.IndexOf('*') -ge 0) -or ($patternNorm.IndexOf('?') -ge 0) -or ($patternNorm.IndexOf('[') -ge 0)
    if ($hasWildcard) {
        return $pathNorm -like $patternNorm
    }
    return ($pathNorm -eq $patternNorm) -or $pathNorm.StartsWith($patternNorm + "/", [System.StringComparison]::OrdinalIgnoreCase)
}

function Detect-SessionIde {
    param($Event, [string]$SessionId, [string]$Source)
    $sourceId = Normalize-IdeId $Source
    if ($sourceId -and $sourceId -notin @("resume", "compact")) { return $sourceId }
    if ($Event -and $Event.workspace_roots) { return "cursor" }
    $sid = if ($SessionId) { $SessionId.ToLowerInvariant() } else { "" }
    $prefixes = [ordered]@{
        "codex-" = "codex"
        "cursor-" = "cursor"
        "oc-" = "opencode"
        "kilo-" = "kilo"
        "kiro-ide-" = "kiro-ide"
        "kiro-" = "kiro"
        "gemini-" = "gemini"
        "copilot-" = "copilot"
        "windsurf-" = "windsurf"
        "kimi-" = "kimi"
        "antigravity-" = "antigravity"
        "amp-" = "amp"
        "deepagents-" = "deepagents"
        "openclaw-" = "openclaw"
        "rovodev-" = "rovodev"
        "qwen-" = "qwen"
        "iflow-" = "iflow"
        "trae-" = "trae"
        "eca-" = "eca"
    }
    foreach ($prefix in $prefixes.Keys) {
        if ($sid.StartsWith($prefix)) { return $prefixes[$prefix] }
    }
    return "claude"
}

# Install a pack from the registry by name. Returns $true on success, $false on failure.
function Get-PackRegistry {
    $regUrl = "https://peonping.github.io/registry/index.json"
    try {
        $regResp = Invoke-WebRequest -Uri $regUrl -UseBasicParsing -ErrorAction Stop
        return ($regResp.Content | ConvertFrom-Json)
    } catch {
        Write-Host "Error: could not fetch registry." -ForegroundColor Red
        return $null
    }
}

function Get-InstalledPackNames {
    param([string]$PacksDir)

    if (-not (Test-Path $PacksDir)) {
        return @()
    }

    return @(Get-ChildItem -Path $PacksDir -Directory | Where-Object {
        (Get-ChildItem -Path (Join-Path $_.FullName "sounds") -File -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0
    } | ForEach-Object { $_.Name } | Sort-Object)
}

function Get-NextPackName {
    param([string[]]$Available, [string]$CurrentPack)

    if (-not $Available -or $Available.Count -eq 0) {
        return $null
    }

    $idx = [array]::IndexOf($Available, $CurrentPack)
    if ($idx -lt 0) {
        return $Available[0]
    }

    return $Available[($idx + 1) % $Available.Count]
}

function Set-SelectedPack {
    param([string]$ConfigPath, [string]$PackName)

    $raw = Get-Content $ConfigPath -Raw
    $updated = $raw -replace '"default_pack"\s*:\s*"[^"]*"', "`"default_pack`": `"$PackName`""
    $updated = $updated -replace '"active_pack"\s*:\s*"[^"]*"', "`"active_pack`": `"$PackName`""
    if ($updated -ne $raw) {
        Set-Content $ConfigPath -Value $updated -Encoding UTF8
    }
}

function Install-PackFromRegistryEntry {
    param($PackInfo, [string]$PacksDir)

    if (-not $PackInfo -or -not $PackInfo.name) { return $false }

    $PackName = $PackInfo.name
    $regUrl = "https://peonping.github.io/registry/index.json"
    $srcRepo = $PackInfo.source_repo
    $srcRef = $PackInfo.source_ref
    $srcPath = $PackInfo.source_path
    if (-not $srcRepo -or -not $srcRef -or ($null -eq $srcPath)) {
        Write-Host "Error: incomplete registry entry for '$PackName'." -ForegroundColor Red
        return $false
    }
    $packBase = if ($srcPath) { "https://raw.githubusercontent.com/$srcRepo/$srcRef/$srcPath" } else { "https://raw.githubusercontent.com/$srcRepo/$srcRef" }
    $pDir = Join-Path $PacksDir $PackName
    $sDir = Join-Path $pDir "sounds"
    New-Item -ItemType Directory -Path $sDir -Force | Out-Null
    try {
        Invoke-WebRequest -Uri "$packBase/openpeon.json" -OutFile (Join-Path $pDir "openpeon.json") -UseBasicParsing -ErrorAction Stop
    } catch {
        Write-Host "Error: could not download manifest for '$PackName'." -ForegroundColor Red
        return $false
    }
    $mf = Get-Content (Join-Path $pDir "openpeon.json") -Raw | ConvertFrom-Json
    $total = 0
    $downloaded = 0
    foreach ($catN in $mf.categories.PSObject.Properties.Name) {
        $total += $mf.categories.$catN.sounds.Count
    }
    foreach ($catN in $mf.categories.PSObject.Properties.Name) {
        foreach ($snd in $mf.categories.$catN.sounds) {
            $sf = Split-Path $snd.file -Leaf
            $sp = Join-Path $sDir $sf
            $downloaded++
            if (-not (Test-Path $sp)) {
                Write-Host "`r[$PackName] $downloaded/$total downloading..." -NoNewline
                Invoke-WebRequest -Uri "$packBase/sounds/$sf" -OutFile $sp -UseBasicParsing -ErrorAction SilentlyContinue
            }
        }
    }
    Write-Host "`r[$PackName] $total/$total done.          "
    return $true
}

function Install-PackFromRegistry {
    param([string]$PackName, [string]$PacksDir)

    $reg = Get-PackRegistry
    if (-not $reg) { return $false }

    $packInfo = $reg.packs | Where-Object { $_.name -eq $PackName }
    if (-not $packInfo) { return $false }

    return (Install-PackFromRegistryEntry -PackInfo $packInfo -PacksDir $PacksDir)
}

function Install-PackFromLocal {
    param([string]$SourceDir, [string]$PacksDir)

    if (-not $SourceDir) {
        Write-Host "Usage: peon packs install-local <path>" -ForegroundColor Yellow
        return $null
    }

    if (-not (Test-Path $SourceDir -PathType Container)) {
        Write-Host "Error: local pack path not found: $SourceDir" -ForegroundColor Red
        return $null
    }

    $resolvedSource = (Resolve-Path -LiteralPath $SourceDir).Path
    $manifestPath = Join-Path $resolvedSource "openpeon.json"
    $legacyManifestPath = Join-Path $resolvedSource "manifest.json"
    $soundsDir = Join-Path $resolvedSource "sounds"

    if (-not (Test-Path $soundsDir -PathType Container)) {
        Write-Host "Error: local pack must contain a sounds directory." -ForegroundColor Red
        return $null
    }

    if (-not (Test-Path $manifestPath) -and -not (Test-Path $legacyManifestPath)) {
        Write-Host "Error: local pack must contain openpeon.json or manifest.json." -ForegroundColor Red
        return $null
    }

    $packName = Split-Path $resolvedSource -Leaf
    $targetDir = Join-Path $PacksDir $packName

    if (Test-Path $targetDir) {
        Remove-Item -Path $targetDir -Recurse -Force
    }

    Copy-Item -Path $resolvedSource -Destination $targetDir -Recurse -Force
    return $packName
}

# Helper function to convert PSCustomObject to hashtable (PS 5.1 compat)
# Defined here (before CLI block) so both CLI commands and hook mode can use it.
function ConvertTo-Hashtable {
    param([Parameter(ValueFromPipeline)]$obj)
    if ($null -eq $obj) { return $obj }
    if ($obj -is [hashtable]) { return $obj }
    # Check value types before PSCustomObject â€” PS 5.1 pipeline wraps primitives
    # in PSObject, making them match [PSCustomObject] when received via ValueFromPipeline.
    if ($obj -is [System.ValueType] -or $obj -is [string]) { return $obj }
    if ($obj -is [System.Collections.IEnumerable]) {
        return ,@($obj | ForEach-Object { ConvertTo-Hashtable $_ })
    }
    if ($obj -is [PSCustomObject]) {
        $ht = @{}
        foreach ($prop in $obj.PSObject.Properties) {
            $ht[$prop.Name] = ConvertTo-Hashtable $prop.Value
        }
        return $ht
    }
    return $obj
}

# --- Atomic state I/O helpers ---
# Defined here (before CLI block) so both CLI commands and hook mode can use them.
function Write-StateAtomic {
    param([hashtable]$State, [string]$Path)
    $dir = Split-Path $Path -Parent
    if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    $tmp = "$Path.$PID.tmp"
    $prevCulture = [System.Threading.Thread]::CurrentThread.CurrentCulture
    try {
        [System.Threading.Thread]::CurrentThread.CurrentCulture = [System.Globalization.CultureInfo]::InvariantCulture
        $State | ConvertTo-Json -Depth 3 | Set-Content $tmp -Encoding UTF8
        if ($PSVersionTable.PSVersion.Major -ge 7) {
            # PS 7+ / .NET Core: Move-Item -Force performs atomic overwrite (no delete gap).
            Move-Item -Path $tmp -Destination $Path -Force
        } else {
            # PS 5.1: delete target then move (atomic on NTFS same-volume, sub-ms gap).
            if (Test-Path $Path) { [System.IO.File]::Delete($Path) }
            [System.IO.File]::Move($tmp, $Path)
        }
    } catch {
        Remove-Item $tmp -ErrorAction SilentlyContinue
    } finally {
        [System.Threading.Thread]::CurrentThread.CurrentCulture = $prevCulture
    }
}

function Read-StateWithRetry {
    param([string]$Path)
    # Clean up orphaned .tmp files left by safety timer [Environment]::Exit(1),
    # which skips finally blocks and may leave partial writes behind.
    $dir = Split-Path $Path -Parent
    if ($dir -and (Test-Path $dir)) {
        $base = Split-Path $Path -Leaf
        Get-ChildItem -Path $dir -Filter "$base.*.tmp" -ErrorAction SilentlyContinue |
            ForEach-Object { Remove-Item $_.FullName -Force -ErrorAction SilentlyContinue }
    }
    $delays = @(50, 100, 200)
    for ($i = 0; $i -le $delays.Count; $i++) {
        try {
            if (Test-Path $Path) {
                $raw = Get-Content $Path -Raw
                if ($raw -and $raw.Trim().Length -gt 0) {
                    $stateObj = $raw | ConvertFrom-Json
                    $converted = ConvertTo-Hashtable $stateObj
                    if ($converted -is [hashtable]) { return $converted }
                }
            }
            return @{}
        } catch {
            if ($i -lt $delays.Count) {
                Start-Sleep -Milliseconds $delays[$i]
            }
        }
    }
    return @{}
}

function Resolve-TemplateKey {
    param(
        [string]$Category,
        [string]$Event,
        [string]$Ntype
    )

    # Category-to-key mapping (matches peon.sh template resolution)
    # Shared by notification templates and TTS text resolution.
    $keyMap = @{
        "task.complete" = "stop"
        "task.error"    = "error"
    }
    $tplKey = $keyMap[$Category]
    if ($Event -eq "Notification") {
        if ($Ntype -eq "idle_prompt") { $tplKey = "idle" }
        elseif ($Ntype -eq "elicitation_dialog") { $tplKey = "question" }
    } elseif ($Event -eq "PermissionRequest") {
        $tplKey = "permission"
    }

    return $tplKey
}

function Resolve-NotificationTemplate {
    param(
        [object]$Templates,
        [string]$Category,
        [string]$Event,
        [string]$Ntype,
        [string]$Project,
        [string]$Summary,
        [string]$ToolName,
        [string]$Status,
        [string]$DefaultMsg
    )

    $tplKey = Resolve-TemplateKey -Category $Category -Event $Event -Ntype $Ntype

    if (-not $tplKey -or -not $Templates.$tplKey) {
        return $DefaultMsg
    }

    $template = $Templates.$tplKey
    if (-not $template) { return $DefaultMsg }

    # Truncate summary to 120 chars
    $safeSummary = if ($Summary) {
        if ($Summary.Length -gt 120) { $Summary.Substring(0, 120) } else { $Summary }
    } else { '' }

    $vars = @{
        project   = $Project
        summary   = $safeSummary
        tool_name = $ToolName
        status    = $Status
        event     = $Event
    }

    # Replace known variables via .Replace() (PS 5.1 compatible)
    $rendered = $template
    foreach ($vk in $vars.Keys) {
        $rendered = $rendered.Replace("{$vk}", $vars[$vk])
    }
    # Strip any remaining unknown {word} placeholders
    $rendered = [regex]::Replace($rendered, '\{(\w+)\}', '')

    return $rendered
}

function Resolve-TemplateSummary {
    param([object]$Event)

    foreach ($key in @('last_assistant_message', 'last-assistant-message', 'prompt_response', 'transcript_summary', 'message')) {
        $prop = $Event.PSObject.Properties[$key]
        if ($prop) {
            $value = [string]$prop.Value
            if ($value) {
                $value = $value.Trim()
                if ($value) {
                    if ($value.Length -gt 120) { return $value.Substring(0, 120) }
                    return $value
                }
            }
        }
    }

    return ''
}

# --- TTS backend resolution ---
function Resolve-TtsBackend {
    param([string]$Backend = "auto")
    switch ($Backend) {
        "native"     { return "tts-native.ps1" }
        "elevenlabs" { return "tts-elevenlabs.ps1" }
        "piper"      { return "tts-piper.ps1" }
        "auto" {
            # Probe in priority order: prefer premium when installed.
            foreach ($b in @("elevenlabs", "piper", "native")) {
                $scriptName = Resolve-TtsBackend -Backend $b
                $full = Join-Path $InstallDir "scripts\$scriptName"
                if (Test-Path $full) { return $scriptName }
            }
            return $null
        }
        default { return $null }
    }
}

# --- TTS speak function ---
function Invoke-TtsSpeak {
    param(
        [string]$Text,
        [string]$Backend = "auto",
        [string]$Voice = "default",
        [double]$Rate = 1.0,
        [double]$Volume = 0.5
    )
    if (-not $Text) { return }

    # Kill previous TTS
    $pidFile = Join-Path $InstallDir ".tts.pid"
    if (Test-Path $pidFile) {
        $oldPid = Get-Content $pidFile -ErrorAction SilentlyContinue
        if ($oldPid) {
            try { Stop-Process -Id $oldPid -Force -ErrorAction SilentlyContinue } catch { $null }
        }
        Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
    }

    $scriptName = Resolve-TtsBackend -Backend $Backend
    if (-not $scriptName) { return }
    $scriptPath = Join-Path $InstallDir "scripts\$scriptName"
    if (-not (Test-Path $scriptPath)) { return }

    # Text is Base64-encoded to avoid shell metacharacter injection. Dynamic text
    # from template variables ({summary}, {project}) can contain double quotes,
    # dollar signs, backticks, and other PowerShell-interpreted characters that
    # would corrupt or break a directly-interpolated -Command string.
    $b64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Text))
    $proc = Start-Process -FilePath "powershell.exe" `
        -ArgumentList "-NoProfile", "-NonInteractive", "-Command",
            "[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('$b64')) | & '$scriptPath' -voice '$Voice' -rate $Rate -vol $Volume" `
        -WindowStyle Hidden -PassThru
    $proc.Id | Set-Content $pidFile
}

# --- CLI commands ---
if ($Command) {
    $InstallDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $ConfigPath = Join-Path $InstallDir "config.json"

    # Ensure config exists
    if (-not (Test-Path $ConfigPath)) {
        Write-Host "Error: peon-ping not configured. Config not found at $ConfigPath" -ForegroundColor Red
        exit 1
    }

    switch -Regex ($Command) {
        "^(--)?toggle$" {
            $raw = Get-PeonConfigRaw $ConfigPath
            $cfg = $raw | ConvertFrom-Json
            $newState = -not $cfg.enabled
            $raw = Get-Content $ConfigPath -Raw
            $updated = $raw -replace '"enabled"\s*:\s*(true|false)', "`"enabled`": $($newState.ToString().ToLower())"
            if ($updated -ne $raw) { Set-Content $ConfigPath -Value $updated -Encoding UTF8 }
            $state = if ($newState) { "ENABLED" } else { "PAUSED" }
            Write-Host "peon-ping: $state" -ForegroundColor Cyan
            return
        }
        "^(--)?(pause|mute)$" {
            $raw = Get-Content $ConfigPath -Raw
            $updated = $raw -replace '"enabled"\s*:\s*(true|false)', '"enabled": false'
            if ($updated -ne $raw) { Set-Content $ConfigPath -Value $updated -Encoding UTF8 }
            Write-Host "peon-ping: PAUSED" -ForegroundColor Yellow
            return
        }
        "^(--)?(resume|unmute)$" {
            $raw = Get-Content $ConfigPath -Raw
            $updated = $raw -replace '"enabled"\s*:\s*(true|false)', '"enabled": true'
            if ($updated -ne $raw) { Set-Content $ConfigPath -Value $updated -Encoding UTF8 }
            Write-Host "peon-ping: ENABLED" -ForegroundColor Green
            return
        }
        "^(--)?status$" {
            try {
                $cfg = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
                $isVerbose = ($Arg1 -eq "--verbose" -or $Arg1 -eq "verbose")

                # --- Essential info (always shown) ---
                $state = if ($cfg.enabled) { "ENABLED" } else { "PAUSED" }
                $versionFile = Join-Path $InstallDir "VERSION"
                $version = if (Test-Path $versionFile) { (Get-Content $versionFile -Raw).Trim() } else { "unknown" }
                Write-Host "peon-ping: $state | version $version | pack: $(Get-ActivePack $cfg) | volume: $($cfg.volume)" -ForegroundColor Cyan

                # Pack count
                $packsDir = Join-Path $InstallDir "packs"
                $packCount = 0
                if (Test-Path $packsDir) {
                    $packCount = @(Get-ChildItem -Path $packsDir -Directory | Where-Object {
                        (Test-Path (Join-Path $_.FullName "openpeon.json")) -or
                        (Test-Path (Join-Path $_.FullName "manifest.json"))
                    }).Count
                }
                Write-Host "peon-ping: $packCount pack(s) installed" -ForegroundColor Cyan

                if (-not $isVerbose) {
                    Write-Host 'peon-ping: run "peon status --verbose" for full details' -ForegroundColor DarkGray
                }

                # --- Informational (verbose only) ---
                if ($isVerbose) {
                    # Desktop notifications
                    $dn = $cfg.desktop_notifications
                    if ($null -eq $dn) { $dn = $true }
                    $dnStatus = if ($dn) { "on" } else { "off (sounds still play)" }
                    Write-Host "peon-ping: desktop notifications $dnStatus" -ForegroundColor Cyan

                    # Mobile notifications
                    $mn = $cfg.mobile_notify
                    if ($mn -and $mn.service) {
                        $mnEnabled = if ($null -eq $mn.enabled) { $true } else { $mn.enabled }
                        $mnStatus = if ($mnEnabled) { "on ($($mn.service))" } else { "off" }
                        Write-Host "peon-ping: mobile notifications $mnStatus" -ForegroundColor Cyan
                    } else {
                        Write-Host "peon-ping: mobile notifications not configured" -ForegroundColor Cyan
                    }

                    # Notification templates
                    $tpls = $cfg.notification_templates
                    if ($tpls -and ($tpls.PSObject.Properties | Measure-Object).Count -gt 0) {
                        Write-Host "peon-ping: notification templates:" -ForegroundColor Cyan
                        foreach ($prop in $tpls.PSObject.Properties) {
                            Write-Host "  $($prop.Name) = `"$($prop.Value)`"" -ForegroundColor Cyan
                        }
                    }

                    # Headphones-only mode
                    $headphonesOnly = $cfg.headphones_only
                    if ($headphonesOnly) {
                        Write-Host "peon-ping: headphones_only: on" -ForegroundColor Cyan
                    } else {
                        Write-Host "peon-ping: headphones_only: off" -ForegroundColor Cyan
                    }

                    $statusIde = Normalize-IdeId ($env:PEON_IDE)
                    if (-not $statusIde) { $statusIde = Normalize-IdeId ($env:PEON_SESSION_SOURCE) }
                    if (-not $statusIde) { $statusIde = Normalize-IdeId ($env:PEON_SOURCE) }
                    if (-not $statusIde) { $statusIde = "claude" }
                    Write-Host "peon-ping: IDE source (status): $statusIde" -ForegroundColor Cyan

                    # Path rules
                    $rules = @()
                    if ($cfg.path_rules) { $rules = @($cfg.path_rules) }
                    $excludeDirs = @()
                    if ($cfg.exclude_dirs) { $excludeDirs = @($cfg.exclude_dirs) }
                    $silencedPath = $null
                    foreach ($pattern in $excludeDirs) {
                        if (Test-PathRuleMatch $PWD.Path $pattern) {
                            $silencedPath = $pattern
                            break
                        }
                    }
                    if ($rules.Count -gt 0) {
                        $activeRule = $null
                        foreach ($r in $rules) {
                            if (Test-PathRuleMatch $PWD.Path $r.pattern) {
                                $activeRule = $r
                                break
                            }
                        }
                        if ($activeRule) {
                            Write-Host "peon-ping: active path rule: $($activeRule.pattern) -> $($activeRule.pack)" -ForegroundColor Cyan
                        }
                        Write-Host "peon-ping: path rules: $($rules.Count) configured" -ForegroundColor Cyan
                    }
                    Write-Host "peon-ping: silenced dirs (exclude_dirs): $($excludeDirs.Count) configured" -ForegroundColor Cyan
                    if ($silencedPath) {
                        Write-Host "peon-ping: SILENCED here: cwd matched exclude_dirs -> $silencedPath" -ForegroundColor Yellow
                    }

                    $ideRules = @()
                    if ($cfg.ide_rules) { $ideRules = @($cfg.ide_rules) }
                    if ($ideRules.Count -gt 0) {
                        $activeIdeRule = $null
                        foreach ($rule in $ideRules) {
                            if ((Normalize-IdeId $rule.ide) -eq $statusIde) {
                                $activeIdeRule = $rule
                                break
                            }
                        }
                        if ($activeIdeRule) {
                            Write-Host "peon-ping: active IDE rule: $($activeIdeRule.ide) -> $($activeIdeRule.pack)" -ForegroundColor Cyan
                        }
                    }
                    Write-Host "peon-ping: IDE rules: $($ideRules.Count) configured" -ForegroundColor Cyan

                    # Debug logging state
                    $debugEnabled = $env:PEON_DEBUG -eq "1"
                    $debugStatus = if ($debugEnabled) { "enabled" } else { "disabled" }
                    Write-Host "peon-ping: debug logging: $debugStatus" -ForegroundColor Cyan
                    if ($debugEnabled) {
                        $logDir = Join-Path $InstallDir "logs"
                        Write-Host "peon-ping: log dir: $logDir" -ForegroundColor Cyan
                    }
                }
            } catch {
                Write-Host "Error reading config: $_" -ForegroundColor Red
                exit 1
            }
            return
        }
        "^(--)?packs$" {
            $packsDir = Join-Path $InstallDir "packs"
            $cfg = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
            $available = Get-InstalledPackNames -PacksDir $packsDir
            $packsAction = if ($Arg1) { $Arg1 } else { "list" }
            if ($packsAction -eq "list" -and $Arg2 -eq "--registry") {
                $packsAction = "community"
            }

            switch ($packsAction) {
                "use" {
                    $installRequested = $false
                    if ($Arg2 -eq "--install") {
                        $installRequested = $true
                        $newPack = if ($ExtraArgs.Count -gt 0) { $ExtraArgs[0] } else { "" }
                    } else {
                        $newPack = $Arg2
                    }

                    if (-not $newPack) {
                        Write-Host "Usage: peon packs use [--install] <pack-name>" -ForegroundColor Yellow
                        return
                    }

                    if ($installRequested -or $newPack -notin $available) {
                        Write-Host "Pack '$newPack' not installed locally. Fetching from registry..." -ForegroundColor Yellow
                        $ok = Install-PackFromRegistry -PackName $newPack -PacksDir $packsDir
                        if (-not $ok) {
                            Write-Host "Pack '$newPack' not found in registry." -ForegroundColor Red
                            return
                        }
                        $available = Get-InstalledPackNames -PacksDir $packsDir
                        Write-Host "peon-ping: installed and switched to '$newPack'" -ForegroundColor Green
                    } else {
                        Write-Host "peon-ping: switched to '$newPack'" -ForegroundColor Green
                    }
                    Set-SelectedPack -ConfigPath $ConfigPath -PackName $newPack
                    return
                }
                "install" {
                    if (-not $Arg2) {
                        Write-Host "Usage: peon packs install <pack1,pack2> | --all" -ForegroundColor Yellow
                        return
                    }

                    $targets = @()
                    if ($Arg2 -eq "--all") {
                        $reg = Get-PackRegistry
                        if (-not $reg) { return }
                        $targets = @($reg.packs | ForEach-Object { $_.name })
                    } else {
                        $targets = @($Arg2 -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ })
                    }

                    if ($targets.Count -eq 0) {
                        Write-Host "Usage: peon packs install <pack1,pack2> | --all" -ForegroundColor Yellow
                        return
                    }

                    $failed = @()
                    foreach ($packName in $targets) {
                        if (Install-PackFromRegistry -PackName $packName -PacksDir $packsDir) {
                            Write-Host "peon-ping: installed '$packName'" -ForegroundColor Green
                        } else {
                            $failed += $packName
                        }
                    }

                    if ($failed.Count -gt 0) {
                        Write-Host "Error: failed to install: $($failed -join ', ')" -ForegroundColor Red
                    }
                    return
                }
                "install-local" {
                    $installedPack = Install-PackFromLocal -SourceDir $Arg2 -PacksDir $packsDir
                    if ($installedPack) {
                        Write-Host "peon-ping: installed local pack '$installedPack'" -ForegroundColor Green
                    }
                    return
                }
                "next" {
                    $currentPack = Get-ActivePack $cfg
                    $newPack = Get-NextPackName -Available $available -CurrentPack $currentPack
                    if (-not $newPack) {
                        Write-Host "No packs installed." -ForegroundColor Yellow
                        return
                    }
                    Set-SelectedPack -ConfigPath $ConfigPath -PackName $newPack
                    Write-Host "peon-ping: switched to '$newPack'" -ForegroundColor Green
                    return
                }
                "remove" {
                    if (-not $Arg2) {
                        Write-Host "Usage: peon packs remove <pack1,pack2>" -ForegroundColor Yellow
                        return
                    }

                    $targets = @($Arg2 -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ })
                    $currentPack = Get-ActivePack $cfg
                    $removedCurrent = $false
                    foreach ($packName in $targets) {
                        if ($packName -notmatch '^[A-Za-z0-9_-]+$') {
                            Write-Host "Error: invalid pack name '$packName'." -ForegroundColor Red
                            continue
                        }
                        $packPath = Join-Path $packsDir $packName
                        if (-not (Test-Path $packPath -PathType Container)) {
                            Write-Host "Warning: pack '$packName' is not installed." -ForegroundColor Yellow
                            continue
                        }
                        Remove-Item -LiteralPath $packPath -Recurse -Force
                        Write-Host "peon-ping: removed '$packName'" -ForegroundColor Green
                        if ($packName -eq $currentPack) {
                            $removedCurrent = $true
                        }
                    }

                    if ($removedCurrent) {
                        $available = Get-InstalledPackNames -PacksDir $packsDir
                        $fallbackPack = if ($available.Count -gt 0) { $available[0] } else { "peon" }
                        Set-SelectedPack -ConfigPath $ConfigPath -PackName $fallbackPack
                        Write-Host "peon-ping: active pack removed, switched to '$fallbackPack'" -ForegroundColor Yellow
                    }
                    return
                }
                "bind" {
                    if (-not $Arg2) {
                        Write-Host "Usage: peon packs bind <pack> [--pattern <glob>] [--install]" -ForegroundColor Yellow
                        return
                    }
                    $packName = $Arg2
                    $bindPattern = ""
                    $bindInstall = $false
                    # Parse extra args for --pattern and --install flags
                    for ($i = 0; $i -lt $ExtraArgs.Count; $i++) {
                        switch ($ExtraArgs[$i]) {
                            "--pattern" {
                                if ($i + 1 -lt $ExtraArgs.Count) {
                                    $bindPattern = $ExtraArgs[$i + 1]
                                    $i++  # Intentionally advance loop counter to skip the next arg (the pattern value)
                                }
                            }
                            "--install" { $bindInstall = $true }
                            default {
                                if ($ExtraArgs[$i] -match "^--pattern=(.+)$") {
                                    $bindPattern = $Matches[1]
                                }
                            }
                        }
                    }

                    # If --install, download pack first
                    if ($bindInstall) {
                        if (Install-PackFromRegistry -PackName $packName -PacksDir $packsDir) {
                            $available = Get-InstalledPackNames -PacksDir $packsDir
                        } else {
                            Write-Host "Warning: could not download pack '$packName'" -ForegroundColor Yellow
                        }
                    }

                    # Validate pack exists
                    if ($packName -notin $available) {
                        Write-Host "Error: pack `"$packName`" not found." -ForegroundColor Red
                        Write-Host "Available packs: $($available -join ', ')" -ForegroundColor Red
                        exit 1
                    }

                    # Default pattern is current directory
                    if (-not $bindPattern) {
                        $bindPattern = $PWD.Path
                    }

                    # Load config as object for manipulation
                    $cfgObj = Get-Content $ConfigPath -Raw | ConvertFrom-Json
                    $pathRules = @()
                    if ($cfgObj.path_rules) {
                        $pathRules = @($cfgObj.path_rules)
                    }

                    # Update existing rule or append new one
                    $found = $false
                    for ($i = 0; $i -lt $pathRules.Count; $i++) {
                        if ($pathRules[$i].pattern -eq $bindPattern) {
                            $pathRules[$i] = [PSCustomObject]@{ pattern = $bindPattern; pack = $packName }
                            $found = $true
                            break
                        }
                    }
                    if (-not $found) {
                        $pathRules += [PSCustomObject]@{ pattern = $bindPattern; pack = $packName }
                    }

                    if ($cfgObj.PSObject.Properties['path_rules']) {
                        $cfgObj.path_rules = $pathRules
                    } else {
                        $cfgObj | Add-Member -NotePropertyName 'path_rules' -NotePropertyValue $pathRules
                    }
                    Set-PeonConfig $cfgObj $ConfigPath
                    Write-Host "peon-ping: bound $packName to $bindPattern"
                    if (-not ($ExtraArgs -contains "--pattern") -and -not ($ExtraArgs -match "^--pattern=")) {
                        $dirName = Split-Path $PWD.Path -Leaf
                        Write-Host "Tip: use --pattern `"*/$dirName`" to match any directory named $dirName"
                    }
                    return
                }
                "unbind" {
                    $unbindPattern = ""
                    # Arg2 could be --pattern or empty. Also check ExtraArgs.
                    if ($Arg2 -eq "--pattern") {
                        if ($ExtraArgs.Count -gt 0) {
                            $unbindPattern = $ExtraArgs[0]
                        }
                    } elseif ($Arg2 -match "^--pattern=(.+)$") {
                        $unbindPattern = $Matches[1]
                    } else {
                        # Check ExtraArgs for --pattern
                        for ($i = 0; $i -lt $ExtraArgs.Count; $i++) {
                            if ($ExtraArgs[$i] -eq "--pattern" -and ($i + 1) -lt $ExtraArgs.Count) {
                                $unbindPattern = $ExtraArgs[$i + 1]
                                break
                            } elseif ($ExtraArgs[$i] -match "^--pattern=(.+)$") {
                                $unbindPattern = $Matches[1]
                                break
                            }
                        }
                    }

                    # Load config
                    $cfgObj = Get-Content $ConfigPath -Raw | ConvertFrom-Json
                    $pathRules = @()
                    if ($cfgObj.path_rules) {
                        $pathRules = @($cfgObj.path_rules)
                    }

                    if ($pathRules.Count -eq 0) {
                        Write-Host "No pack bindings configured."
                        return
                    }

                    # Determine target pattern
                    $target = if ($unbindPattern) { $unbindPattern } else { $PWD.Path }

                    # Try exact match
                    $newRules = @($pathRules | Where-Object { $_.pattern -ne $target })
                    if ($newRules.Count -lt $pathRules.Count) {
                        if ($cfgObj.PSObject.Properties['path_rules']) {
                            $cfgObj.path_rules = $newRules
                        } else {
                            $cfgObj | Add-Member -NotePropertyName 'path_rules' -NotePropertyValue $newRules
                        }
                        Set-PeonConfig $cfgObj $ConfigPath
                        Write-Host "peon-ping: unbound $target"
                        return
                    }

                    # No exact match â€” check if any rules match cwd via -like
                    if (-not $unbindPattern) {
                        $matching = @($pathRules | Where-Object { $PWD.Path -like $_.pattern })
                        if ($matching.Count -gt 0) {
                            Write-Host "No binding for `"$target`", but found rules matching this directory:" -ForegroundColor Red
                            foreach ($r in $matching) {
                                Write-Host "  $($r.pattern) -> $($r.pack)" -ForegroundColor Red
                            }
                            Write-Host "Use --pattern to remove a specific rule." -ForegroundColor Red
                            exit 1
                        }
                    }

                    Write-Host "No binding found for `"$target`"."
                    return
                }
                "bindings" {
                    $cfgObj = Get-Content $ConfigPath -Raw | ConvertFrom-Json
                    $pathRules = @()
                    if ($cfgObj.path_rules) {
                        $pathRules = @($cfgObj.path_rules)
                    }

                    if ($pathRules.Count -eq 0) {
                        Write-Host "No pack bindings configured."
                        return
                    }

                    foreach ($rule in $pathRules) {
                        $marker = if (Test-PathRuleMatch $PWD.Path $rule.pattern) { " *" } else { "" }
                        Write-Host "  $($rule.pattern) -> $($rule.pack)$marker"
                    }
                    return
                }
                "ide-bind" {
                    if (-not $Arg2 -or $ExtraArgs.Count -eq 0) {
                        Write-Host "Usage: peon packs ide-bind <ide> <pack> [--install]" -ForegroundColor Yellow
                        return
                    }
                    $ideName = Normalize-IdeId $Arg2
                    $packName = $ExtraArgs[0]
                    $installPack = ($ExtraArgs -contains "--install")
                    if (-not $ideName) {
                        Write-Host "Error: IDE id must not be empty." -ForegroundColor Red
                        return
                    }
                    if ($installPack -and $packName -notin $available) {
                        $ok = Install-PackFromRegistry -PackName $packName -PacksDir $packsDir
                        if (-not $ok) { return }
                        $available = Get-ChildItem -Path $packsDir -Directory | Where-Object {
                            (Get-ChildItem -Path (Join-Path $_.FullName "sounds") -File -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0
                        } | ForEach-Object { $_.Name } | Sort-Object
                    }
                    if ($packName -notin $available) {
                        Write-Host "Error: pack `"$packName`" not found." -ForegroundColor Red
                        Write-Host "Available packs: $($available -join ', ')" -ForegroundColor Red
                        return
                    }
                    $cfgObj = Get-Content $ConfigPath -Raw | ConvertFrom-Json
                    $ideRules = @()
                    if ($cfgObj.ide_rules) { $ideRules = @($cfgObj.ide_rules) }
                    $found = $false
                    for ($i = 0; $i -lt $ideRules.Count; $i++) {
                        if ((Normalize-IdeId $ideRules[$i].ide) -eq $ideName) {
                            $ideRules[$i] = [PSCustomObject]@{ ide = $ideName; pack = $packName }
                            $found = $true
                            break
                        }
                    }
                    if (-not $found) {
                        $ideRules += [PSCustomObject]@{ ide = $ideName; pack = $packName }
                    }
                    if ($cfgObj.PSObject.Properties['ide_rules']) {
                        $cfgObj.ide_rules = $ideRules
                    } else {
                        $cfgObj | Add-Member -NotePropertyName 'ide_rules' -NotePropertyValue $ideRules
                    }
                    Set-PeonConfig $cfgObj $ConfigPath
                    Write-Host "peon-ping: bound $packName to IDE $ideName"
                    if ($ideName -notin (Get-KnownIdeIds)) {
                        Write-Host "Known IDE ids: $((Get-KnownIdeIds) -join ', ')" -ForegroundColor DarkGray
                    }
                    return
                }
                "ide-unbind" {
                    if (-not $Arg2) {
                        Write-Host "Usage: peon packs ide-unbind <ide>" -ForegroundColor Yellow
                        return
                    }
                    $ideName = Normalize-IdeId $Arg2
                    $cfgObj = Get-Content $ConfigPath -Raw | ConvertFrom-Json
                    $ideRules = @()
                    if ($cfgObj.ide_rules) { $ideRules = @($cfgObj.ide_rules) }
                    $newRules = @($ideRules | Where-Object { (Normalize-IdeId $_.ide) -ne $ideName })
                    if ($newRules.Count -eq $ideRules.Count) {
                        Write-Host "No IDE binding found for `"$ideName`"."
                        return
                    }
                    if ($cfgObj.PSObject.Properties['ide_rules']) {
                        $cfgObj.ide_rules = $newRules
                    } else {
                        $cfgObj | Add-Member -NotePropertyName 'ide_rules' -NotePropertyValue $newRules
                    }
                    Set-PeonConfig $cfgObj $ConfigPath
                    Write-Host "peon-ping: unbound IDE $ideName"
                    return
                }
                "ide-bindings" {
                    $cfgObj = Get-Content $ConfigPath -Raw | ConvertFrom-Json
                    $ideRules = @()
                    if ($cfgObj.ide_rules) { $ideRules = @($cfgObj.ide_rules) }
                    if ($ideRules.Count -eq 0) {
                        Write-Host "No IDE bindings configured."
                    } else {
                        $currentIde = Normalize-IdeId ($env:PEON_IDE)
                        if (-not $currentIde) { $currentIde = Normalize-IdeId ($env:PEON_SESSION_SOURCE) }
                        if (-not $currentIde) { $currentIde = Normalize-IdeId ($env:PEON_SOURCE) }
                        if (-not $currentIde) { $currentIde = "claude" }
                        foreach ($rule in $ideRules) {
                            $marker = if ((Normalize-IdeId $rule.ide) -eq $currentIde) { " *" } else { "" }
                            Write-Host "  $($rule.ide) -> $($rule.pack)$marker"
                        }
                    }
                    $stateObj = @{}
                    try { $stateObj = Get-Content $StatePath -Raw | ConvertFrom-Json } catch { $stateObj = @{} }
                    if ($stateObj.recent_ide_sources) {
                        $recent = @($stateObj.recent_ide_sources.PSObject.Properties | Sort-Object { [double]$_.Value } -Descending | Select-Object -First 5 | ForEach-Object { $_.Name })
                        if ($recent.Count -gt 0) {
                            Write-Host "Recent IDEs: $($recent -join ', ')"
                        }
                    }
                    Write-Host "Supported IDE ids: $((Get-KnownIdeIds) -join ', ')"
                    return
                }
                "exclude" {
                    $action = if ($Arg2) { $Arg2 } else { "list" }
                    $pattern = if ($ExtraArgs.Count -gt 0) { $ExtraArgs[0] } else { "" }
                    $cfgObj = Get-Content $ConfigPath -Raw | ConvertFrom-Json
                    $excludeDirs = @()
                    if ($cfgObj.exclude_dirs) { $excludeDirs = @($cfgObj.exclude_dirs) }
                    switch ($action) {
                        "add" {
                            if (-not $pattern) {
                                Write-Host "Usage: peon packs exclude add <glob-or-dir>" -ForegroundColor Yellow
                                return
                            }
                            if ($pattern -in $excludeDirs) {
                                Write-Host "peon-ping: already silencing sounds in: $pattern"
                                return
                            }
                            $excludeDirs += $pattern
                            if ($cfgObj.PSObject.Properties['exclude_dirs']) {
                                $cfgObj.exclude_dirs = $excludeDirs
                            } else {
                                $cfgObj | Add-Member -NotePropertyName 'exclude_dirs' -NotePropertyValue $excludeDirs
                            }
                            Set-PeonConfig $cfgObj $ConfigPath
                            Write-Host "peon-ping: sounds & notifications silenced for $pattern"
                            return
                        }
                        "remove" {
                            if (-not $pattern) {
                                Write-Host "Usage: peon packs exclude remove <glob-or-dir>" -ForegroundColor Yellow
                                return
                            }
                            $newDirs = @($excludeDirs | Where-Object { $_ -ne $pattern })
                            if ($newDirs.Count -eq $excludeDirs.Count) {
                                Write-Host "No silenced path found for `"$pattern`"."
                                return
                            }
                            if ($cfgObj.PSObject.Properties['exclude_dirs']) {
                                $cfgObj.exclude_dirs = $newDirs
                            } else {
                                $cfgObj | Add-Member -NotePropertyName 'exclude_dirs' -NotePropertyValue $newDirs
                            }
                            Set-PeonConfig $cfgObj $ConfigPath
                            Write-Host "peon-ping: no longer silencing $pattern"
                            return
                        }
                        "list" {
                            if ($excludeDirs.Count -eq 0) {
                                Write-Host "No silenced paths configured."
                                return
                            }
                            Write-Host "Silenced paths (no sounds or notifications when cwd matches):"
                            foreach ($item in $excludeDirs) {
                                $marker = if (Test-PathRuleMatch $PWD.Path $item) { " *" } else { "" }
                                Write-Host "  $item$marker"
                            }
                            return
                        }
                        default {
                            Write-Host "Usage: peon packs exclude <add|remove|list> [glob-or-dir]" -ForegroundColor Yellow
                            return
                        }
                    }
                }
                "community" {
                    $reg = Get-PackRegistry
                    if (-not $reg) { return }
                    $packs = $reg.packs
                    Write-Host ""
                    Write-Host "  Registry packs ($($packs.Count) available)" -ForegroundColor Cyan
                    Write-Host ""
                    $grouped = @{}
                    foreach ($p in $packs) {
                        $tier = if ($p.trust_tier) { $p.trust_tier } else { "unknown" }
                        if (-not $grouped.ContainsKey($tier)) { $grouped[$tier] = @() }
                        $grouped[$tier] += $p
                    }
                    $maxName = ($packs | ForEach-Object { $_.name.Length } | Measure-Object -Maximum).Maximum
                    $nameWidth = [Math]::Max($maxName + 2, 24)
                    # Show official first, then community, then others
                    $tierOrder = @("official") + @($grouped.Keys | Where-Object { $_ -ne "official" } | Sort-Object)
                    foreach ($tier in $tierOrder) {
                        if (-not $grouped.ContainsKey($tier)) { continue }
                        $tierPacks = @($grouped[$tier] | Sort-Object { $_.name })
                        $tierLabel = (Get-Culture).TextInfo.ToTitleCase($tier)
                        $installedInTier = @($tierPacks | Where-Object { $_.name -in $available }).Count
                        $tierInfo = "$($tierPacks.Count) packs"
                        if ($installedInTier -gt 0) { $tierInfo += ", $installedInTier installed" }
                        Write-Host "  --- $tierLabel ($tierInfo) ---" -ForegroundColor DarkGray
                        foreach ($p in $tierPacks) {
                            $isInstalled = $p.name -in $available
                            $soundStr = if ($p.sound_count) { "$($p.sound_count)".PadLeft(4) } else { "   ?" }
                            $displayName = if ($p.display_name) { $p.display_name } else { "" }
                            if ($isInstalled) {
                                Write-Host "  $([char]0x2713) " -NoNewline -ForegroundColor Green
                            } else {
                                Write-Host "    " -NoNewline
                            }
                            Write-Host ($p.name.PadRight($nameWidth)) -NoNewline -ForegroundColor White
                            Write-Host "$soundStr sounds" -NoNewline -ForegroundColor DarkGray
                            if ($displayName) {
                                Write-Host "   $displayName" -NoNewline -ForegroundColor DarkGray
                            }
                            Write-Host ""
                        }
                        Write-Host ""
                    }
                    return
                }
                "search" {
                    if (-not $Arg2) {
                        Write-Host "Usage: peon packs search <query>" -ForegroundColor Yellow
                        return
                    }
                    $query = $Arg2.ToLower()
                    $reg = Get-PackRegistry
                    if (-not $reg) { return }
                    $matches = @($reg.packs | Where-Object { $_.name.ToLower().Contains($query) })
                    if ($matches.Count -eq 0) {
                        Write-Host "No packs matching '$Arg2'." -ForegroundColor Yellow
                        return
                    }
                    Write-Host ""
                    Write-Host "  Search results for '$Arg2' ($($matches.Count) found)" -ForegroundColor Cyan
                    Write-Host ""
                    $maxName = ($matches | ForEach-Object { $_.name.Length } | Measure-Object -Maximum).Maximum
                    $nameWidth = [Math]::Max($maxName + 2, 24)
                    foreach ($p in ($matches | Sort-Object { $_.name })) {
                        $isInstalled = $p.name -in $available
                        $tier = if ($p.trust_tier) { $p.trust_tier } else { "unknown" }
                        $soundStr = if ($p.sound_count) { "$($p.sound_count)".PadLeft(4) } else { "   ?" }
                        $displayName = if ($p.display_name) { $p.display_name } else { "" }
                        if ($isInstalled) {
                            Write-Host "  $([char]0x2713) " -NoNewline -ForegroundColor Green
                        } else {
                            Write-Host "    " -NoNewline
                        }
                        Write-Host ($p.name.PadRight($nameWidth)) -NoNewline -ForegroundColor White
                        Write-Host "$soundStr sounds" -NoNewline -ForegroundColor DarkGray
                        if ($displayName) {
                            Write-Host "   $displayName" -NoNewline -ForegroundColor DarkGray
                        }
                        Write-Host "  " -NoNewline
                        Write-Host "[$tier]" -ForegroundColor DarkGray
                    }
                    return
                }
                "list" {
                    Write-Host "Available packs:" -ForegroundColor Cyan
                    if ($available.Count -eq 0) {
                        Write-Host "  No packs installed." -ForegroundColor Yellow
                        return
                    }
                    $currentPack = Get-ActivePack $cfg
                    foreach ($packName in $available) {
                        $soundCount = (Get-ChildItem -Path (Join-Path $packsDir "$packName\sounds") -File -ErrorAction SilentlyContinue | Measure-Object).Count
                        $marker = if ($packName -eq $currentPack) { " <-- active" } else { "" }
                        Write-Host "  $packName ($soundCount sounds)$marker"
                    }
                    return
                }
                default {
                    Write-Host "Usage: peon packs <list|use|install|install-local|next|remove|community|search|bind|unbind|bindings|ide-bind|ide-unbind|ide-bindings|exclude>" -ForegroundColor Yellow
                    return
                }
            }
        }
        "^(--)?pack$" {
            $cfg = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
            $packsDir = Join-Path $InstallDir "packs"
            $available = Get-InstalledPackNames -PacksDir $packsDir

            $currentPack = Get-ActivePack $cfg
            if ($available.Count -eq 0) {
                Write-Host "No packs installed." -ForegroundColor Yellow
                return
            }
            if ($Arg1 -eq "use") {
                # "peon pack use <name>" - treat Arg2 as the pack name
                if (-not $Arg2) {
                    Write-Host "Usage: peon pack use <pack-name>" -ForegroundColor Yellow
                    return
                }
                $newPack = $Arg2
            } elseif ($Arg1 -eq "next") {
                # "peon pack next" - cycle to next
                $newPack = Get-NextPackName -Available $available -CurrentPack $currentPack
            } elseif ($Arg1) {
                $newPack = $Arg1
            } else {
                $newPack = Get-NextPackName -Available $available -CurrentPack $currentPack
            }

            if ($newPack -notin $available) {
                Write-Host "Pack '$newPack' not found. Available: $($available -join ', ')" -ForegroundColor Red
                return
            }

            Set-SelectedPack -ConfigPath $ConfigPath -PackName $newPack
            Write-Host "peon-ping: switched to '$newPack'" -ForegroundColor Green
            return
        }
        "^(--)?volume$" {
            if ($Arg1) {
                $vol = [math]::Round([math]::Max(0.0, [math]::Min(1.0, [double]::Parse($Arg1.Trim(), [System.Globalization.CultureInfo]::InvariantCulture))), 2)
                $volStr = $vol.ToString([System.Globalization.CultureInfo]::InvariantCulture)
                $raw = Get-Content $ConfigPath -Raw
                $updated = $raw -replace '"volume"\s*:\s*[\d.]+(,?)', "`"volume`": $volStr`$1"
                if ($updated -ne $raw) { Set-Content $ConfigPath -Value $updated -Encoding UTF8 }
                Write-Host "peon-ping: volume set to $vol" -ForegroundColor Green
            } else {
                $cfg = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
                Write-Host "peon-ping: volume $($cfg.volume)" -ForegroundColor Cyan
            }
            return
        }
        "^debug$" {
            $debugSub = if ($Arg1) { $Arg1 } else { "status" }
            switch ($debugSub) {
                "on" {
                    $cfgObj = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
                    $cfgObj | Add-Member -NotePropertyName 'debug' -NotePropertyValue $true -Force
                    $prevCulture = [System.Threading.Thread]::CurrentThread.CurrentCulture
                    [System.Threading.Thread]::CurrentThread.CurrentCulture = [System.Globalization.CultureInfo]::InvariantCulture
                    $cfgObj | ConvertTo-Json -Depth 10 | Set-Content $ConfigPath -Encoding UTF8
                    [System.Threading.Thread]::CurrentThread.CurrentCulture = $prevCulture
                    $logDir = Join-Path $InstallDir "logs"
                    Write-Host "peon-ping: debug logging enabled -- logs at $logDir" -ForegroundColor Green
                    return
                }
                "off" {
                    $cfgObj = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
                    $cfgObj | Add-Member -NotePropertyName 'debug' -NotePropertyValue $false -Force
                    $prevCulture = [System.Threading.Thread]::CurrentThread.CurrentCulture
                    [System.Threading.Thread]::CurrentThread.CurrentCulture = [System.Globalization.CultureInfo]::InvariantCulture
                    $cfgObj | ConvertTo-Json -Depth 10 | Set-Content $ConfigPath -Encoding UTF8
                    [System.Threading.Thread]::CurrentThread.CurrentCulture = $prevCulture
                    Write-Host "peon-ping: debug logging disabled" -ForegroundColor Yellow
                    return
                }
                "status" {
                    $cfgObj = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
                    $debugEnabled = if ($cfgObj.debug) { $true } else { $false }
                    $state = if ($debugEnabled) { "enabled" } else { "disabled" }
                    $logDir = Join-Path $InstallDir "logs"
                    Write-Host "peon-ping: debug $state" -ForegroundColor Cyan
                    Write-Host "peon-ping: log directory: $logDir" -ForegroundColor Cyan
                    if (Test-Path $logDir) {
                        $logFiles = @(Get-ChildItem -Path $logDir -Filter "peon-ping-*.log" -ErrorAction SilentlyContinue)
                        $totalSize = ($logFiles | Measure-Object -Property Length -Sum).Sum
                        if (-not $totalSize) { $totalSize = 0 }
                        if ($totalSize -ge 1MB) {
                            $sizeStr = "{0:N1} MB" -f ($totalSize / 1MB)
                        } elseif ($totalSize -ge 1KB) {
                            $sizeStr = "{0:N1} KB" -f ($totalSize / 1KB)
                        } else {
                            $sizeStr = "$totalSize bytes"
                        }
                        Write-Host "peon-ping: log files: $($logFiles.Count) ($sizeStr)" -ForegroundColor Cyan
                    } else {
                        Write-Host "peon-ping: log files: 0 (0 bytes)" -ForegroundColor Cyan
                    }
                    return
                }
                default {
                    Write-Host "Usage: peon debug [on|off|status]" -ForegroundColor Yellow
                    return
                }
            }
        }
        "^logs$" {
            $logDir = Join-Path $InstallDir "logs"
            # Parse flags from Arg1, Arg2, ExtraArgs
            $flag = $Arg1
            switch -Regex ($flag) {
                "^--clear$" {
                    if (Test-Path $logDir) {
                        $logFiles = @(Get-ChildItem -Path $logDir -Filter "peon-ping-*.log" -ErrorAction SilentlyContinue)
                        if ($logFiles.Count -gt 0) {
                            foreach ($f in $logFiles) {
                                Remove-Item $f.FullName -Force -ErrorAction SilentlyContinue
                            }
                            Write-Host "peon-ping: cleared $($logFiles.Count) log file(s)" -ForegroundColor Green
                        } else {
                            Write-Host "peon-ping: no log files to clear" -ForegroundColor Yellow
                        }
                    } else {
                        Write-Host "peon-ping: no log files to clear" -ForegroundColor Yellow
                    }
                    return
                }
                "^--last$" {
                    $n = 50
                    if ($Arg2) {
                        $parsed = $Arg2 -as [int]
                        if ($null -eq $parsed -or $parsed -le 0) {
                            Write-Host "Usage: peon logs --last N  (N must be a positive integer)" -ForegroundColor Yellow
                            return
                        }
                        $n = $parsed
                    }
                    if (-not (Test-Path $logDir)) {
                        Write-Host "peon-ping: no log files found" -ForegroundColor Yellow
                        return
                    }
                    $logFiles = @(Get-ChildItem -Path $logDir -Filter "peon-ping-*.log" -ErrorAction SilentlyContinue | Sort-Object Name)
                    if ($logFiles.Count -eq 0) {
                        Write-Host "peon-ping: no log files found" -ForegroundColor Yellow
                        return
                    }
                    $collected = @()
                    foreach ($f in $logFiles) {
                        $lines = @(Get-Content $f.FullName -Encoding UTF8 | Where-Object { $_ -ne '' })
                        $collected += $lines
                    }
                    # Take last N lines (chronological order, oldest first)
                    if ($collected.Count -gt $n) {
                        $collected = $collected[($collected.Count - $n)..($collected.Count - 1)]
                    }
                    foreach ($line in $collected) {
                        Write-Host $line
                    }
                    return
                }
                "^--session$" {
                    $sessionId = $Arg2
                    if (-not $sessionId) {
                        Write-Host "Usage: peon logs --session <ID> [--all]" -ForegroundColor Yellow
                        return
                    }
                    if (-not (Test-Path $logDir)) {
                        Write-Host "peon-ping: no log files found" -ForegroundColor Yellow
                        return
                    }
                    $searchAll = $ExtraArgs -contains "--all"
                    if ($searchAll) {
                        # Search across all log files in chronological order
                        $logFiles = @(Get-ChildItem -Path $logDir -Filter "peon-ping-*.log" -ErrorAction SilentlyContinue | Sort-Object Name)
                        if ($logFiles.Count -eq 0) {
                            Write-Host "peon-ping: no log files found" -ForegroundColor Yellow
                            return
                        }
                        $found = @()
                        foreach ($f in $logFiles) {
                            $lines = @(Get-Content $f.FullName -Encoding UTF8 | Where-Object { $_ -match "session=$sessionId" })
                            $found += $lines
                        }
                        if ($found.Count -eq 0) {
                            Write-Host "peon-ping: no entries for session=$sessionId across all log files" -ForegroundColor Yellow
                            return
                        }
                        foreach ($line in $found) {
                            Write-Host $line
                        }
                        return
                    }
                    $logDate = (Get-Date).ToString('yyyy-MM-dd')
                    $todayLog = Join-Path $logDir "peon-ping-$logDate.log"
                    if (-not (Test-Path $todayLog)) {
                        Write-Host "peon-ping: no log file for today" -ForegroundColor Yellow
                        return
                    }
                    $lines = @(Get-Content $todayLog -Encoding UTF8 | Where-Object { $_ -match "session=$sessionId" })
                    if ($lines.Count -eq 0) {
                        Write-Host "peon-ping: no entries for session $sessionId" -ForegroundColor Yellow
                        return
                    }
                    foreach ($line in $lines) {
                        Write-Host $line
                    }
                    return
                }
                "^--prune$" {
                    # Read retention days from config
                    $cfg = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
                    $retention = if ($cfg.debug_retention_days) { [int]$cfg.debug_retention_days } else { 7 }
                    if (-not (Test-Path $logDir)) {
                        Write-Host "peon-ping: no logs directory found" -ForegroundColor Yellow
                        return
                    }
                    $logFiles = @(Get-ChildItem -Path $logDir -Filter "peon-ping-*.log" -ErrorAction SilentlyContinue)
                    $beforeCount = $logFiles.Count
                    if ($beforeCount -eq 0) {
                        Write-Host "peon-ping: no log files older than $retention days" -ForegroundColor Yellow
                        return
                    }
                    $cutoff = (Get-Date).AddDays(-$retention).ToString('yyyy-MM-dd')
                    foreach ($f in $logFiles) {
                        $datePart = $f.BaseName -replace '^peon-ping-', ''
                        # Validate date format YYYY-MM-DD
                        if ($datePart -match '^\d{4}-\d{2}-\d{2}$' -and $datePart -lt $cutoff) {
                            Remove-Item $f.FullName -Force -ErrorAction SilentlyContinue
                        }
                    }
                    $afterFiles = @(Get-ChildItem -Path $logDir -Filter "peon-ping-*.log" -ErrorAction SilentlyContinue)
                    $removed = $beforeCount - $afterFiles.Count
                    if ($removed -gt 0) {
                        Write-Host "peon-ping: pruned $removed log file(s) older than $retention days" -ForegroundColor Green
                    } else {
                        Write-Host "peon-ping: no log files older than $retention days" -ForegroundColor Yellow
                    }
                    return
                }
                default {
                    # No flag or unrecognized: show last 50 lines of today's log
                    if ($flag -and $flag -match "^--") {
                        Write-Host "Usage: peon logs [--last N] [--session ID [--all]] [--prune] [--clear]" -ForegroundColor Yellow
                        return
                    }
                    if (-not (Test-Path $logDir)) {
                        Write-Host "peon-ping: no log files found. Enable debug logging with: peon debug on" -ForegroundColor Yellow
                        return
                    }
                    $logDate = (Get-Date).ToString('yyyy-MM-dd')
                    $todayLog = Join-Path $logDir "peon-ping-$logDate.log"
                    if (-not (Test-Path $todayLog)) {
                        Write-Host "peon-ping: no log file for today. Enable debug logging with: peon debug on" -ForegroundColor Yellow
                        return
                    }
                    $lines = @(Get-Content $todayLog -Encoding UTF8 | Where-Object { $_ -ne '' })
                    $n = 50
                    if ($lines.Count -gt $n) {
                        $lines = $lines[($lines.Count - $n)..($lines.Count - 1)]
                    }
                    foreach ($line in $lines) {
                        Write-Host $line
                    }
                    return
                }
            }
        }
        "^(--)?update$" {
            Write-Host "Updating peon-ping..." -ForegroundColor Cyan
            # Migrate config keys (active_pack â†’ default_pack, agentskill â†’ session_override)
            $cfgObj = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
            $changed = $false
            if ($cfgObj.PSObject.Properties['active_pack'] -and -not $cfgObj.PSObject.Properties['default_pack']) {
                $cfgObj | Add-Member -NotePropertyName 'default_pack' -NotePropertyValue $cfgObj.active_pack -Force
                $cfgObj.PSObject.Properties.Remove('active_pack')
                $changed = $true
            } elseif ($cfgObj.PSObject.Properties['active_pack']) {
                $cfgObj.PSObject.Properties.Remove('active_pack')
                $changed = $true
            }
            if ($cfgObj.pack_rotation_mode -eq 'agentskill') {
                $cfgObj.pack_rotation_mode = 'session_override'
                $changed = $true
            }
            if (-not $cfgObj.PSObject.Properties['exclude_dirs']) {
                $cfgObj | Add-Member -NotePropertyName 'exclude_dirs' -NotePropertyValue @() -Force
                $changed = $true
            }
            if (-not $cfgObj.PSObject.Properties['ide_rules']) {
                $cfgObj | Add-Member -NotePropertyName 'ide_rules' -NotePropertyValue @() -Force
                $changed = $true
            }
            if (-not $cfgObj.PSObject.Properties['notification_title_ide']) {
                $cfgObj | Add-Member -NotePropertyName 'notification_title_ide' -NotePropertyValue $false -Force
                $changed = $true
            }
            if ($changed) {
                $cfgObj | ConvertTo-Json -Depth 10 | Set-Content $ConfigPath -Encoding UTF8
                Write-Host "peon-ping: config migrated (active_pack -> default_pack, agentskill -> session_override, exclude_dirs, ide_rules, notification_title_ide)" -ForegroundColor Green
            }
            # Re-run install.ps1 from a temp directory. Download install-utils.ps1
            # alongside it so the dot-source resolves correctly via $PSScriptRoot.
            $tempDir = Join-Path $env:TEMP "peon-ping-update"
            $tempScriptsDir = Join-Path $tempDir "scripts"
            New-Item -ItemType Directory -Path $tempScriptsDir -Force | Out-Null
            try {
                $base = "https://raw.githubusercontent.com/PeonPing/peon-ping/main"
                Invoke-WebRequest -Uri "$base/install.ps1" -OutFile (Join-Path $tempDir "install.ps1") -UseBasicParsing -ErrorAction Stop
                Invoke-WebRequest -Uri "$base/scripts/install-utils.ps1" -OutFile (Join-Path $tempScriptsDir "install-utils.ps1") -UseBasicParsing -ErrorAction Stop
                & powershell -NoProfile -File (Join-Path $tempDir "install.ps1")
            } catch {
                Write-Host "Error: Could not download installer. Check your internet connection." -ForegroundColor Red
            } finally {
                Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue
            }
            return
        }
        "^(--)?help$" {
            Write-Host "peon-ping commands:" -ForegroundColor Cyan
            Write-Host "  peon toggle           Toggle enabled/paused"
            Write-Host "  peon pause            Pause sounds"
            Write-Host "  peon resume           Resume sounds"
            Write-Host "  peon mute             Alias for pause"
            Write-Host "  peon unmute           Alias for resume"
            Write-Host "  peon status           Show current status"
            Write-Host "  peon status --verbose Show expanded status details"
            Write-Host "  peon volume           Show current volume"
            Write-Host "  peon volume N         Set volume (0.0-1.0)"
            Write-Host "  peon update           Update peon-ping (migrate config + reinstall)"
            Write-Host "  peon help             Show this help"
            Write-Host ""
            Write-Host "Pack management:" -ForegroundColor Cyan
            Write-Host "  peon packs list              List installed sound packs"
            Write-Host "  peon packs list --registry   List all packs from registry"
            Write-Host "  peon packs use <name>        Switch to pack (auto-installs from registry)"
            Write-Host "  peon packs use --install <name> Install/update then switch"
            Write-Host "  peon packs install <p1,p2>   Install pack(s) from registry"
            Write-Host "  peon packs install --all     Install every registry pack"
            Write-Host "  peon packs install-local <path> Install a local pack directory"
            Write-Host "  peon packs next              Cycle to the next pack"
            Write-Host "  peon packs remove <p1,p2>    Remove installed pack(s)"
            Write-Host "  peon packs community         List all packs from registry"
            Write-Host "  peon packs search <q>        Search registry packs by name"
            Write-Host "  peon packs bind              Bind a pack to current directory"
            Write-Host "  peon packs unbind            Remove a pack binding"
            Write-Host "  peon packs bindings          List all pack bindings"
            Write-Host "  peon packs ide-bind          Bind a pack to an IDE id"
            Write-Host "  peon packs ide-unbind        Remove an IDE binding"
            Write-Host "  peon packs ide-bindings      List all IDE bindings"
            Write-Host "  peon packs exclude           Manage excluded paths for path_rules"
            Write-Host "  peon pack [name]             Switch pack (or cycle)"
            Write-Host ""
            Write-Host "Trainer:" -ForegroundColor Cyan
            Write-Host "  trainer on            Enable trainer mode"
            Write-Host "  trainer off           Disable trainer mode"
            Write-Host "  trainer status        Show today's progress"
            Write-Host "  trainer log <n> <ex>  Log completed reps"
            Write-Host "  trainer goal <n>      Set daily goal for all exercises"
            Write-Host "  trainer goal <ex> <n> Set daily goal for one exercise"
            Write-Host "  trainer help          Show trainer help"
            Write-Host ""
            Write-Host "Notifications:" -ForegroundColor Cyan
            Write-Host "  peon notifications on         Enable desktop notifications"
            Write-Host "  peon notifications off        Disable desktop notifications"
            Write-Host "  peon notifications template               Show all templates"
            Write-Host "  peon notifications template <key> <fmt>  Set a template"
            Write-Host "  peon notifications template --reset      Clear all templates"
            Write-Host "  peon popups on/off            Alias for notifications on/off"
            Write-Host "  --notifications on/off        Legacy alias for peon notifications on/off"
            Write-Host "  --popups on/off               Legacy alias for peon popups on/off"
            Write-Host ""
            Write-Host "Debug & Logs:" -ForegroundColor Cyan
            Write-Host "  debug on              Enable debug logging"
            Write-Host "  debug off             Disable debug logging"
            Write-Host "  debug status          Show debug state and log info"
            Write-Host "  logs                  Show last 50 lines of today's log"
            Write-Host "  logs --last N         Show last N lines across all logs"
            Write-Host "  logs --session ID     Filter today's log by session ID"
            Write-Host "  logs --session ID --all  Search all log files for session ID"
            Write-Host "  logs --prune          Delete logs older than debug_retention_days"
            Write-Host "  logs --clear          Delete all log files"
            Write-Host ""
            Write-Host "Legacy --status/--toggle/--packs/--volume forms still work." -ForegroundColor DarkGray
            return
        }
        "^(--)?(notifications|popups)$" {
            $notifSub = if ($Arg1) { $Arg1 } else { "help" }
            switch ($notifSub) {
                "on" {
                    $cfgObj = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
                    $cfgObj | Add-Member -NotePropertyName 'desktop_notifications' -NotePropertyValue $true -Force
                    Set-PeonConfig $cfgObj $ConfigPath
                    Write-Host "peon-ping: desktop notifications on" -ForegroundColor Green
                    return
                }
                "off" {
                    $cfgObj = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
                    $cfgObj | Add-Member -NotePropertyName 'desktop_notifications' -NotePropertyValue $false -Force
                    Set-PeonConfig $cfgObj $ConfigPath
                    Write-Host "peon-ping: desktop notifications off" -ForegroundColor Yellow
                    return
                }
                "template" {
                    $tplKey = $Arg2
                    $tplVal = if ($ExtraArgs.Count -gt 0) { $ExtraArgs[0] } else { "" }
                    $validKeys = @("stop", "permission", "error", "idle", "question")

                    if (-not $tplKey) {
                        # Show all templates
                        $cfgObj = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
                        $tpls = $cfgObj.notification_templates
                        if (-not $tpls -or ($tpls.PSObject.Properties | Measure-Object).Count -eq 0) {
                            Write-Host "peon-ping: no notification templates configured (using defaults)" -ForegroundColor Cyan
                        } else {
                            foreach ($vk in $validKeys) {
                                $v = $tpls.$vk
                                if ($v) {
                                    Write-Host "peon-ping: template $vk = `"$v`"" -ForegroundColor Cyan
                                }
                            }
                            # Show unknown keys
                            foreach ($prop in $tpls.PSObject.Properties) {
                                if ($prop.Name -notin $validKeys -and $prop.Value) {
                                    Write-Host "peon-ping: template $($prop.Name) = `"$($prop.Value)`" (unknown key)" -ForegroundColor Cyan
                                }
                            }
                        }
                        return
                    }

                    if ($tplKey -eq "--reset") {
                        # Clear all templates
                        $cfgObj = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
                        $members = @($cfgObj.PSObject.Properties | Where-Object { $_.Name -eq 'notification_templates' })
                        if ($members.Count -gt 0) {
                            $cfgObj.PSObject.Properties.Remove('notification_templates')
                        }
                        Set-PeonConfig $cfgObj $ConfigPath
                        Write-Host "peon-ping: notification templates cleared" -ForegroundColor Cyan
                        return
                    }

                    # Validate key
                    if ($tplKey -notin $validKeys) {
                        Write-Host "peon-ping: invalid template key `"$tplKey`" - use one of: $($validKeys -join ', ')" -ForegroundColor Red
                        exit 1
                    }

                    if (-not $tplVal) {
                        # Show single template
                        $cfgObj = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
                        $tpls = $cfgObj.notification_templates
                        $v = if ($tpls) { $tpls.$tplKey } else { $null }
                        if ($v) {
                            Write-Host "peon-ping: template $tplKey = `"$v`"" -ForegroundColor Cyan
                        } else {
                            Write-Host "peon-ping: template $tplKey not set (default: `"{project}`")" -ForegroundColor Cyan
                        }
                        return
                    }

                    # Set template
                    $cfgObj = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
                    $tpls = if ($cfgObj.notification_templates) {
                        $tplHash = @{}
                        foreach ($prop in $cfgObj.notification_templates.PSObject.Properties) {
                            $tplHash[$prop.Name] = $prop.Value
                        }
                        $tplHash
                    } else { @{} }
                    $tpls[$tplKey] = $tplVal
                    $tplObj = [PSCustomObject]@{}
                    foreach ($k in ($tpls.Keys | Sort-Object)) {
                        $tplObj | Add-Member -NotePropertyName $k -NotePropertyValue $tpls[$k]
                    }
                    $cfgObj | Add-Member -NotePropertyName 'notification_templates' -NotePropertyValue $tplObj -Force
                    Set-PeonConfig $cfgObj $ConfigPath
                    Write-Host "peon-ping: template $tplKey set to `"$tplVal`"" -ForegroundColor Green
                    return
                }
                default {
                    Write-Host "Usage: peon --notifications [on|off|template]" -ForegroundColor Cyan
                    Write-Host ""
                    Write-Host "Commands:"
                    Write-Host "  on                            Enable desktop notifications"
                    Write-Host "  off                           Disable desktop notifications"
                    Write-Host "  template                      Show all templates"
                    Write-Host "  template [key] [format]       Set a template"
                    Write-Host "  template [key]                Show a template"
                    Write-Host "  template --reset              Clear all templates"
                    Write-Host ""
                    Write-Host "Template keys: stop, permission, error, idle, question"
                    Write-Host "Template variables: {project}, {summary}, {tool_name}, {status}, {event}"
                    return
                }
            }
        }
        "^(--trainer|trainer)$" {
            $StatePath = Join-Path $InstallDir ".state.json"
            $trainerSub = if ($Arg1) { $Arg1 } else { "help" }
            switch ($trainerSub) {
                "on" {
                    $cfgObj = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
                    if (-not $cfgObj.trainer) {
                        $cfgObj | Add-Member -NotePropertyName 'trainer' -NotePropertyValue ([PSCustomObject]@{
                            enabled = $true
                            exercises = [PSCustomObject]@{ pushups = 300; squats = 300 }
                            reminder_interval_minutes = 20
                            reminder_min_gap_minutes = 5
                        })
                    } else {
                        $cfgObj.trainer.enabled = $true
                        if (-not $cfgObj.trainer.exercises) {
                            $cfgObj.trainer | Add-Member -NotePropertyName 'exercises' -NotePropertyValue ([PSCustomObject]@{ pushups = 300; squats = 300 })
                        }
                        if (-not $cfgObj.trainer.reminder_interval_minutes) {
                            $cfgObj.trainer | Add-Member -NotePropertyName 'reminder_interval_minutes' -NotePropertyValue 20
                        }
                        if (-not $cfgObj.trainer.reminder_min_gap_minutes) {
                            $cfgObj.trainer | Add-Member -NotePropertyName 'reminder_min_gap_minutes' -NotePropertyValue 5
                        }
                    }
                    Set-PeonConfig $cfgObj $ConfigPath
                    Write-Host "peon-ping: trainer enabled" -ForegroundColor Green
                    return
                }
                "off" {
                    $cfgObj = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
                    if ($cfgObj.trainer) {
                        $cfgObj.trainer.enabled = $false
                    } else {
                        $cfgObj | Add-Member -NotePropertyName 'trainer' -NotePropertyValue ([PSCustomObject]@{
                            enabled = $false
                        })
                    }
                    Set-PeonConfig $cfgObj $ConfigPath
                    Write-Host "peon-ping: trainer disabled" -ForegroundColor Yellow
                    return
                }
                "status" {
                    $cfgObj = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
                    $trainerCfg = $cfgObj.trainer
                    if (-not $trainerCfg -or -not $trainerCfg.enabled) {
                        Write-Host "peon-ping: trainer not enabled"
                        Write-Host 'Run "peon trainer on" to enable.'
                        return
                    }
                    $exercises = @{}
                    if ($trainerCfg.exercises) {
                        foreach ($prop in $trainerCfg.exercises.PSObject.Properties) {
                            $exercises[$prop.Name] = [int]$prop.Value
                        }
                    } else {
                        $exercises = @{ pushups = 300; squats = 300 }
                    }

                    $state = Read-StateWithRetry $StatePath
                    $trainerState = $state['trainer']
                    $today = (Get-Date).ToString("yyyy-MM-dd")

                    # Auto-reset if date changed
                    if (-not $trainerState -or $trainerState['date'] -ne $today) {
                        $resetReps = @{}
                        foreach ($ex in $exercises.Keys) { $resetReps[$ex] = 0 }
                        $trainerState = @{ date = $today; reps = $resetReps; last_reminder_ts = 0 }
                        $state['trainer'] = $trainerState
                        Write-StateAtomic -State $state -Path $StatePath
                    }

                    $reps = $trainerState['reps']
                    if (-not $reps) { $reps = @{} }

                    Write-Host "peon-ping: trainer status ($today)"
                    Write-Host ""

                    $barWidth = 16
                    $fullBlock = [char]0x2588
                    $lightShade = [char]0x2591
                    foreach ($ex in ($exercises.Keys | Sort-Object)) {
                        $goal = $exercises[$ex]
                        $done = if ($reps[$ex]) { [int]$reps[$ex] } else { 0 }
                        $pct = if ($goal -gt 0) { [Math]::Min($done / $goal, 1.0) } else { 0 }
                        $filled = [int]($pct * $barWidth)
                        $empty = $barWidth - $filled
                        $bar = ($fullBlock.ToString() * $filled) + ($lightShade.ToString() * $empty)
                        $pctStr = [int]($pct * 100)
                        Write-Host "${ex}:  ${bar}  ${done}/${goal}  (${pctStr}%)"
                    }
                    return
                }
                "log" {
                    $count = $Arg2
                    $exercise = if ($ExtraArgs.Count -gt 0) { $ExtraArgs[0] } else { "" }
                    if (-not $count -or -not $exercise) {
                        Write-Host "Usage: peon trainer log <count> <exercise>" -ForegroundColor Yellow
                        Write-Host "Example: peon trainer log 25 pushups" -ForegroundColor Yellow
                        return
                    }
                    # Validate numeric
                    $countInt = 0
                    if (-not [int]::TryParse($count, [ref]$countInt) -or $countInt -le 0) {
                        Write-Host "peon-ping: count must be a positive number" -ForegroundColor Red
                        return
                    }

                    $cfgObj = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
                    $trainerCfg = $cfgObj.trainer
                    $exercises = @{}
                    if ($trainerCfg -and $trainerCfg.exercises) {
                        foreach ($prop in $trainerCfg.exercises.PSObject.Properties) {
                            $exercises[$prop.Name] = [int]$prop.Value
                        }
                    } else {
                        $exercises = @{ pushups = 300; squats = 300 }
                    }

                    if (-not $exercises.ContainsKey($exercise)) {
                        Write-Host "peon-ping: unknown exercise `"$exercise`"" -ForegroundColor Red
                        if ($exercises.Count -gt 0) {
                            Write-Host "Known exercises: $($exercises.Keys -join ', ')" -ForegroundColor Red
                        }
                        Write-Host "Add it first: peon trainer goal $exercise <daily-goal>" -ForegroundColor Red
                        return
                    }

                    $goal = $exercises[$exercise]
                    $state = Read-StateWithRetry $StatePath
                    $trainerState = $state['trainer']
                    $today = (Get-Date).ToString("yyyy-MM-dd")

                    # Auto-reset if date changed
                    if (-not $trainerState -or $trainerState['date'] -ne $today) {
                        $resetReps = @{}
                        foreach ($ex in $exercises.Keys) { $resetReps[$ex] = 0 }
                        $trainerState = @{ date = $today; reps = $resetReps; last_reminder_ts = 0 }
                    }

                    $reps = $trainerState['reps']
                    if (-not $reps) { $reps = @{} }
                    $reps[$exercise] = ([int]($reps[$exercise])) + $countInt
                    $trainerState['reps'] = $reps
                    $trainerState['date'] = $today
                    $state['trainer'] = $trainerState
                    Write-StateAtomic -State $state -Path $StatePath

                    $done = $reps[$exercise]
                    $pct = if ($goal -gt 0) { [Math]::Min($done / $goal, 1.0) } else { 0 }
                    $barWidth = 16
                    $fullBlock = [char]0x2588
                    $lightShade = [char]0x2591
                    $filled = [int]($pct * $barWidth)
                    $empty = $barWidth - $filled
                    $bar = ($fullBlock.ToString() * $filled) + ($lightShade.ToString() * $empty)
                    $pctStr = [int]($pct * 100)
                    Write-Host "peon-ping: logged $countInt $exercise ($done/$goal)" -ForegroundColor Green
                    Write-Host "  ${bar}  ${pctStr}%"
                    return
                }
                "goal" {
                    $goalArg1 = $Arg2
                    $goalArg2 = if ($ExtraArgs.Count -gt 0) { $ExtraArgs[0] } else { "" }
                    if (-not $goalArg1) {
                        Write-Host "Usage: peon trainer goal <number>           Set all exercises" -ForegroundColor Yellow
                        Write-Host "       peon trainer goal <exercise> <number> Set one exercise" -ForegroundColor Yellow
                        return
                    }

                    $cfgObj = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
                    if (-not $cfgObj.trainer) {
                        $cfgObj | Add-Member -NotePropertyName 'trainer' -NotePropertyValue ([PSCustomObject]@{
                            enabled = $false
                            exercises = [PSCustomObject]@{ pushups = 300; squats = 300 }
                        })
                    }
                    $exercises = @{}
                    if ($cfgObj.trainer.exercises) {
                        foreach ($prop in $cfgObj.trainer.exercises.PSObject.Properties) {
                            $exercises[$prop.Name] = [int]$prop.Value
                        }
                    } else {
                        $exercises = @{ pushups = 300; squats = 300 }
                    }

                    if ($goalArg2) {
                        # goal <exercise> <number>
                        $exerciseName = $goalArg1
                        $goalNum = 0
                        if (-not [int]::TryParse($goalArg2, [ref]$goalNum) -or $goalNum -le 0) {
                            Write-Host "peon-ping: goal must be a positive number" -ForegroundColor Red
                            return
                        }
                        $isNew = -not $exercises.ContainsKey($exerciseName)
                        $exercises[$exerciseName] = $goalNum
                        if ($isNew) {
                            Write-Host "peon-ping: new exercise added - $exerciseName goal set to $goalNum" -ForegroundColor Green
                        } else {
                            Write-Host "peon-ping: $exerciseName goal set to $goalNum" -ForegroundColor Green
                        }
                    } else {
                        # goal <number>
                        $goalNum = 0
                        if (-not [int]::TryParse($goalArg1, [ref]$goalNum) -or $goalNum -le 0) {
                            Write-Host "peon-ping: goal must be a positive number" -ForegroundColor Red
                            return
                        }
                        foreach ($k in @($exercises.Keys)) {
                            $exercises[$k] = $goalNum
                        }
                        Write-Host "peon-ping: all exercise goals set to $goalNum" -ForegroundColor Green
                    }

                    # Write exercises back to config
                    $exercisesObj = [PSCustomObject]@{}
                    foreach ($k in ($exercises.Keys | Sort-Object)) {
                        $exercisesObj | Add-Member -NotePropertyName $k -NotePropertyValue $exercises[$k]
                    }
                    $cfgObj.trainer.exercises = $exercisesObj
                    Set-PeonConfig $cfgObj $ConfigPath
                    return
                }
                default {
                    # "help" or unknown subcommand
                    Write-Host "Usage: peon trainer <command>" -ForegroundColor Cyan
                    Write-Host ""
                    Write-Host "Commands:"
                    Write-Host "  on                   Enable trainer mode"
                    Write-Host "  off                  Disable trainer mode"
                    Write-Host "  status               Show today's progress"
                    Write-Host "  log <count> <exercise>  Log completed reps (e.g. log 25 pushups)"
                    Write-Host "  goal <number>        Set daily goal for all exercises"
                    Write-Host "  goal <exercise> <n>  Set daily goal for one exercise"
                    Write-Host "  help                 Show this help"
                    Write-Host ""
                    Write-Host "Exercises: pushups, squats"
                    return
                }
            }
        }
    }
    return
}

# --- Hook mode (called by Claude Code via stdin JSON) ---
$InstallDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ConfigPath = Join-Path $InstallDir "config.json"
$StatePath = Join-Path $InstallDir ".state.json"
$_peonStart = [System.Diagnostics.Stopwatch]::StartNew()

# Read config (capture error for logging after init)
$_configError = $null
try {
    $config = Get-PeonConfigRaw $ConfigPath | ConvertFrom-Json
} catch {
    $_configError = "$_"
# Fall back to minimal defaults so the hook can still run (logging requires PEON_DEBUG=1 when config is broken)
    $config = [PSCustomObject]@{ enabled = $true; debug = $false; volume = 0.5; debug_retention_days = 7; notification_title_marker = 'â—'; notification_title_ide = $false }
}

# NOTE: enabled check moved below logging init so paused invocations are visible in debug logs

# --- Structured logging infrastructure ---
# Mirrors peon.sh log() closure: key=value format, invocation IDs, daily rotation.
# When debug=false (default): empty scriptblock, zero overhead.
# When debug=true or PEON_DEBUG=1: appends to $PEON_DIR/logs/peon-ping-YYYY-MM-DD.log.
$peonInv = '{0:x4}' -f ([System.Random]::new().Next(0, 65535))
$script:peonLogEnabled = ($config.debug -eq $true) -or ($peonDebug)
$script:peonLogPath = $null

if ($script:peonLogEnabled) {
    $logDir = Join-Path $InstallDir 'logs'
    if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
    $logDate = (Get-Date).ToString('yyyy-MM-dd')
    $script:peonLogPath = Join-Path $logDir "peon-ping-$logDate.log"
    $logIsNew = -not (Test-Path $script:peonLogPath)

    $peonLog = {
        param([string]$Phase, [hashtable]$Fields)
        if (-not $script:peonLogEnabled) { return }
        $ts = (Get-Date).ToString('yyyy-MM-ddTHH:mm:ss.fff')
        $parts = "$ts [$Phase] inv=$peonInv"
        foreach ($kv in $Fields.GetEnumerator()) {
            $v = [string]$kv.Value
            if ($v -match '[ "=]' -or $v -eq '') {
                $v = '"' + ($v -replace '\\','\\' -replace '"','\"') + '"'
            }
            $parts += " $($kv.Key)=$v"
        }
        try { Add-Content -Path $script:peonLogPath -Value $parts -Encoding UTF8 -ErrorAction Stop }
        catch { $script:peonLogEnabled = $false }
    }

    # Prune old logs on first file of the day
    if ($logIsNew) {
        $retention = if ($config.debug_retention_days) { $config.debug_retention_days } else { 7 }
        $cutoff = (Get-Date).AddDays(-$retention).ToString('yyyy-MM-dd')
        Get-ChildItem -Path $logDir -Filter 'peon-ping-*.log' -ErrorAction SilentlyContinue |
            Where-Object { $_.BaseName -replace 'peon-ping-','' -lt $cutoff } |
            Remove-Item -Force -ErrorAction SilentlyContinue
    }
} else {
    $peonLog = { }
}

# Log config error if config load failed
if ($_configError) {
    & $peonLog 'config' @{ error = $_configError; fallback = 'defaults' }
    & $peonLog 'exit' @{ duration_ms = [string]$_peonStart.ElapsedMilliseconds; exit = '0' }
    exit 0
}

# --- Paused check (after logging init so paused invocations are visible) ---
if (-not $config.enabled) {
    $_activePack = Get-ActivePack $config
    & $peonLog 'config' @{ loaded = $ConfigPath; volume = [string]$config.volume; pack = $_activePack; enabled = 'False' }
    & $peonLog 'hook' @{ event = 'unknown'; session = 'unknown'; cwd = ''; paused = 'True' }
    & $peonLog 'exit' @{ duration_ms = [string]$_peonStart.ElapsedMilliseconds; exit = '0'; reason = 'paused' }
    exit 0
}

# Log config phase
$_activePack = Get-ActivePack $config
& $peonLog 'config' @{ loaded = $ConfigPath; volume = [string]$config.volume; pack = $_activePack; enabled = 'True' }

# Read hook input from stdin (StreamReader with UTF-8 auto-strips BOM on Windows)
$hookInput = ""
try {
    if (-not [Console]::IsInputRedirected) { exit 0 }
    $stream = [Console]::OpenStandardInput()
    $reader = New-Object System.IO.StreamReader($stream, [System.Text.Encoding]::UTF8)
    $hookInput = $reader.ReadToEnd()
    $reader.Close()
} catch {
    exit 0
}

if (-not $hookInput) { exit 0 }

try {
    $event = $hookInput | ConvertFrom-Json
} catch {
    exit 0
}

$rawEvent = $event.hook_event_name
# Defensive fallback: GitHub Copilot CLI's permissionRequest event leaks
# camelCase fields ("hookName") even when the hook is registered with the
# PascalCase key that should produce the VS Code-compatible payload. Without
# this fallback, every Copilot CLI permission popup goes silent. See PR
# adding native Copilot CLI support for the upstream-bug repro.
if (-not $rawEvent) { $rawEvent = $event.hookName }
if (-not $rawEvent) { exit 0 }

# Cursor IDE sends camelCase via Third-party skills; Claude Code sends PascalCase.
# Map to PascalCase so the switch below matches.
$cursorMap = @{
    "sessionStart" = "SessionStart"
    "sessionEnd" = "SessionEnd"
    "beforeSubmitPrompt" = "UserPromptSubmit"
    "stop" = "Stop"
    "preToolUse" = "UserPromptSubmit"
    "postToolUse" = "Stop"
    "subagentStop" = "Stop"
    "subagentStart" = "SubagentStart"
    "preCompact" = "PreCompact"
    # Copilot CLI camelCase fallbacks (most events normalize via PascalCase
    # registration; permissionRequest leaks camelCase as of CLI 1.0.48-1).
    "permissionRequest" = "PermissionRequest"
    "notification" = "Notification"
    "agentStop" = "Stop"
    "userPromptSubmitted" = "UserPromptSubmit"
    "postToolUseFailure" = "PostToolUseFailure"
}
$hookEvent = if ($cursorMap.ContainsKey($rawEvent)) { $cursorMap[$rawEvent] } else { $rawEvent }

# Extract session ID (Claude Code: session_id, Cursor: conversation_id, Copilot CLI camelCase leak: sessionId)
$sessionId = if ($event.session_id) { $event.session_id } elseif ($event.conversation_id) { $event.conversation_id } elseif ($event.sessionId) { $event.sessionId } else { "default" }

# Extract cwd from event (used by path_rules for directory-based pack selection)
$cwd = if ($event.cwd) { $event.cwd } else { "" }
$sessionSource = if ($event.source) { [string]$event.source } else { "" }
$sessionIde = Detect-SessionIde -Event $event -SessionId $sessionId -Source $sessionSource

# Derive project name from cwd (used in desktop notification titles)
$project = if ($cwd) { Split-Path $cwd -Leaf } else { "" }
if (-not $project) { $project = "claude" }
$project = $project -replace '[^a-zA-Z0-9 ._-]', ''

# IDE display names (parity with peon.sh IDE_DISPLAY_NAMES)
$ideDisplayNames = @{
    'claude' = 'Claude Code'
    'codex' = 'OpenAI Codex'
    'cursor' = 'Cursor'
    'opencode' = 'OpenCode'
    'kilo' = 'Kilo CLI'
    'kiro' = 'Kiro'
    'gemini' = 'Gemini CLI'
    'copilot' = 'GitHub Copilot'
    'windsurf' = 'Windsurf'
    'kimi' = 'Kimi Code'
    'antigravity' = 'Antigravity'
    'amp' = 'Amp'
    'deepagents' = 'DeepAgents'
    'openclaw' = 'OpenClaw'
    'rovodev' = 'Rovo Dev CLI'
    'qwen' = 'Qwen Code'
    'iflow' = 'iFlow CLI'
    'trae' = 'Trae'
    'kiro-ide' = 'Kiro IDE'
    'eca' = 'ECA'
}
$ideLabel = ''
if ($sessionIde) {
    $ideKey = (Normalize-IdeId $sessionIde)
    if ($ideKey -and $ideDisplayNames.ContainsKey($ideKey)) {
        $ideLabel = $ideDisplayNames[$ideKey]
    } elseif ($ideKey) {
        $ideLabel = (Get-Culture).TextInfo.ToTitleCase(($ideKey -replace '-', ' '))
    }
}
$notificationProject = if ($config.notification_title_ide -and $ideLabel) { "$project - $ideLabel" } else { $project }

# Log hook phase
$_isPaused = if ($config.enabled) { 'False' } else { 'True' }
& $peonLog 'hook' @{ event = $hookEvent; session = $sessionId; cwd = $cwd; paused = $_isPaused }

# Read state
$state = Read-StateWithRetry -Path $StatePath

# Log state phase
$_stateSessions = if ($state.ContainsKey("agent_sessions")) { @($state["agent_sessions"]).Count } else { 0 }
$_stateRotIdx = if ($state.ContainsKey("rotation_index")) { $state["rotation_index"] } else { 0 }
$_stateLastStop = if ($state.ContainsKey("last_stop_time")) { $state["last_stop_time"] } else { 0 }
& $peonLog 'state' @{ sessions = [string]$_stateSessions; rotation_index = [string]$_stateRotIdx; last_stop = [string]$_stateLastStop }

# --- Session cleanup: expire old sessions ---
$now = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
$ttlDays = if ($config.session_ttl_days) { $config.session_ttl_days } else { 7 }
$cutoff = $now - ($ttlDays * 86400)
$sessionPacks = if ($state.ContainsKey("session_packs")) { $state["session_packs"] } else { @{} }
$sessionPacksClean = @{}
foreach ($sid in $sessionPacks.Keys) {
    $packData = $sessionPacks[$sid]
    if ($packData -is [hashtable]) {
        # New format with timestamp
        $lastUsed = if ($packData.ContainsKey("last_used")) { $packData["last_used"] } else { 0 }
        if ($lastUsed -gt $cutoff) {
            if ($sid -eq $sessionId) {
                $packData["last_used"] = $now
            }
            $sessionPacksClean[$sid] = $packData
        }
    } elseif ($sid -eq $sessionId) {
        # Old format, upgrade active session
        $sessionPacksClean[$sid] = @{ pack = $packData; last_used = $now }
    } elseif ($packData -is [string]) {
        # Old format for inactive sessions - keep for now (migration path)
        $sessionPacksClean[$sid] = $packData
    }
}
$state["session_packs"] = $sessionPacksClean
$stateDirty = $false
if ($sessionPacksClean.Count -ne $sessionPacks.Count) {
    $stateDirty = $true
}

$recentIdeSources = if ($state.ContainsKey("recent_ide_sources")) { $state["recent_ide_sources"] } else { @{} }
if (-not $recentIdeSources) { $recentIdeSources = @{} }
$recentIdeSources[$sessionIde] = $now
foreach ($ideKey in @($recentIdeSources.Keys)) {
    if ([double]$recentIdeSources[$ideKey] -lt ($now - (30 * 86400))) {
        $recentIdeSources.Remove($ideKey)
    }
}
$state["recent_ide_sources"] = $recentIdeSources
$stateDirty = $true

# --- Agent detection (delegate mode) ---
$_permMode = if ($event.permission_mode) { $event.permission_mode } else { '' }
$_agentModes = @('delegate')
$_agentSessions = if ($state.ContainsKey("agent_sessions")) { @($state["agent_sessions"]) } else { @() }

if ($_permMode -and $_agentModes -contains $_permMode) {
    $_agentSessions = @($_agentSessions + $sessionId | Select-Object -Unique)
    $state["agent_sessions"] = $_agentSessions
    & $peonLog 'route' @{ category = 'none'; suppressed = 'True'; reason = 'delegate_mode' }
    & $peonLog 'exit' @{ duration_ms = [string]$_peonStart.ElapsedMilliseconds; exit = '0' }
    try { Write-StateAtomic -State $state -Path $StatePath } catch { <# state write best-effort #> }
    exit 0
} elseif ($sessionId -and $_agentSessions -contains $sessionId) {
    & $peonLog 'route' @{ category = 'none'; suppressed = 'True'; reason = 'agent_session' }
    & $peonLog 'exit' @{ duration_ms = [string]$_peonStart.ElapsedMilliseconds; exit = '0' }
    exit 0
}

# --- exclude_dirs: silence sounds & notifications when cwd matches ---
$_excludedDirPattern = $null
if ($cwd -and $config.exclude_dirs) {
    foreach ($_pat in $config.exclude_dirs) {
        if ($_pat -and (Test-PathRuleMatch $cwd $_pat)) {
            $_excludedDirPattern = $_pat
            break
        }
    }
}
if ($_excludedDirPattern) {
    & $peonLog 'route' @{ category = 'none'; suppressed = 'True'; reason = 'excluded_dir'; pattern = $_excludedDirPattern }
    & $peonLog 'exit' @{ duration_ms = [string]$_peonStart.ElapsedMilliseconds; exit = '0' }
    try { if ($stateDirty) { Write-StateAtomic -State $state -Path $StatePath } } catch { <# state write best-effort #> }
    exit 0
}

# --- Map Claude Code hook event -> CESP manifest category ---
$category = $null
$ntype = $event.notification_type
$notify = $false
$notifyColor = ""
$notifyMsg = ""
$notifyStatus = ""

switch ($hookEvent) {
    "SessionStart" {
        $category = "session.start"
        # Debounce rapid SessionStart events (e.g. --continue fires twice, multi-workspace IDE startup)
        $now = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
        $ssCooldown = if ($null -ne $config.session_start_cooldown_seconds) { [int]$config.session_start_cooldown_seconds } else { 30 }
        $lastStart = if ($state.ContainsKey("last_session_start_sound_time")) { $state["last_session_start_sound_time"] } else { 0 }
        if ($ssCooldown -gt 0 -and ($now - $lastStart) -lt $ssCooldown) {
            & $peonLog 'route' @{ category = 'session.start'; suppressed = 'True'; reason = 'session_start_cooldown' }
            $category = $null
        } else {
            $state["last_session_start_sound_time"] = $now
        }
    }
    "Stop" {
        $category = "task.complete"
        # Debounce rapid Stop events (5s cooldown)
        $now = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
        $lastStop = if ($state.ContainsKey("last_stop_time")) { $state["last_stop_time"] } else { 0 }
        if (($now - $lastStop) -lt 5) {
            & $peonLog 'route' @{ category = 'task.complete'; suppressed = 'True'; reason = 'debounce_5s' }
            $category = $null
        } else {
            $notify = $true
            $notifyColor = "blue"
            $notifyStatus = "done"
            $notifyMsg = $notifyStatus
        }
        $state["last_stop_time"] = $now
    }
    "Notification" {
        if ($ntype -eq "permission_prompt") {
            # PermissionRequest event handles the sound, skip here
            $category = $null
        } elseif ($ntype -eq "idle_prompt") {
            # Notification only â€” no sound (matches peon.sh idle_prompt behavior)
            $category = $null
            $notify = $true
            $notifyColor = "yellow"
            $notifyStatus = "done"
            $notifyMsg = $notifyStatus
        } elseif ($ntype -eq "elicitation_dialog") {
            $category = "input.required"
            $notify = $true
            $notifyColor = "blue"
            $notifyStatus = "question"
            $notifyMsg = "$notifyStatus`: Question pending"
        } else {
            # Other notification types (e.g., tool results) map to task.complete
            $category = "task.complete"
        }
    }
    "PermissionRequest" {
        $category = "input.required"
        $notify = $true
        $notifyColor = "red"
        $notifyStatus = "needs approval"
        $_tool = if ($event.tool_name) { [string]$event.tool_name } else { "" }
        $notifyMsg = if ($_tool) { "$notifyStatus`: $_tool" } else { $notifyStatus }
    }
    "PreCompact" {
        $category = "resource.limit"
        $notify = $true
        $notifyColor = "red"
        $notifyStatus = "context limit"
        $notifyMsg = "$notifyStatus`: Context compacting"
    }
    "UserPromptSubmit" {
        # Detect rapid prompts for "annoyed" easter egg
        $now = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
        $annoyedThreshold = if ($config.annoyed_threshold) { $config.annoyed_threshold } else { 3 }
        $annoyedWindow = if ($config.annoyed_window_seconds) { $config.annoyed_window_seconds } else { 10 }

        $allPrompts = if ($state.ContainsKey("prompt_timestamps")) { $state["prompt_timestamps"] } else { @{} }
        $recentPrompts = @()
        if ($allPrompts.ContainsKey($sessionId)) {
            $recentPrompts = @($allPrompts[$sessionId] | Where-Object { ($now - $_) -lt $annoyedWindow })
        }
        $recentPrompts += $now
        $allPrompts[$sessionId] = $recentPrompts
        $state["prompt_timestamps"] = $allPrompts

        if ($recentPrompts.Count -ge $annoyedThreshold) {
            $category = "user.spam"
        }
    }
    "PostToolUseFailure" {
        $category = "task.error"
    }
    "SubagentStart" {
        $category = "task.acknowledge"
    }
}

# Save state
try {
    Write-StateAtomic -State $state -Path $StatePath
} catch {
    if ($peonDebug) { Write-Warning "peon-ping: state write failed: $_" }
}

$skipSound = (-not $category)
if ($skipSound -and -not $notify) {
    # No category and no notification â€” nothing to do (may have already logged route reason like debounce)
    & $peonLog 'exit' @{ duration_ms = [string]$_peonStart.ElapsedMilliseconds; exit = '0' }
    exit 0
}

# Check if category is enabled (only relevant when we have a category to play)
if (-not $skipSound) {
    try {
        $catEnabled = $config.categories.$category
        if ($catEnabled -eq $false -and -not $notify) {
            & $peonLog 'route' @{ category = $category; suppressed = 'True'; reason = 'category_disabled' }
            & $peonLog 'exit' @{ duration_ms = [string]$_peonStart.ElapsedMilliseconds; exit = '0' }
            exit 0
        }
        if ($catEnabled -eq $false) { $skipSound = $true }
    } catch {
        if ($peonDebug) { Write-Warning "peon-ping: category check failed for '$category': $_" }
    }
}

# Log route decision (normal flow â€” not suppressed)
if ($category) {
    & $peonLog 'route' @{ category = $category; suppressed = 'False' }
}

# Pre-resolve notification template for TTS text fallback
$resolvedTemplate = ""
if ($category) {
    $tplCfg0 = $config.notification_templates
    if ($tplCfg0) {
        $tplSum0 = Resolve-TemplateSummary $event
        $tplTool0 = if ($event.tool_name) { [string]$event.tool_name } else { '' }
        $resolvedTemplate = Resolve-NotificationTemplate `
            -Templates $tplCfg0 `
            -Category $category `
            -Event $hookEvent `
            -Ntype $ntype `
            -Project $project `
            -Summary $tplSum0 `
            -ToolName $tplTool0 `
            -Status $notifyStatus `
            -DefaultMsg ""
    }
}

# --- TTS config (read before skipSound gate so trainer TTS can use it) ---
$ttsCfg = if ($config.tts) { $config.tts } else { @{} }
# Note: $paused guard is handled implicitly by the early-exit when $config.enabled = false
# (see top of hook block), rather than explicitly checked here.
$ttsEnabled = ($ttsCfg.enabled -eq $true)
$ttsBackend = if ($ttsCfg.backend) { $ttsCfg.backend } else { "auto" }
$ttsVoice = if ($ttsCfg.voice) { $ttsCfg.voice } else { "default" }
$ttsRate = if ($ttsCfg.rate) { $ttsCfg.rate } else { 1.0 }
$ttsVolume = if ($ttsCfg.volume) { $ttsCfg.volume } else { 0.5 }
$ttsMode = if ($ttsCfg.mode) { $ttsCfg.mode } else { "sound-then-speak" }
$ttsText = ""

if (-not $skipSound) {
# --- Pick a sound ---
$activePack = Get-ActivePack $config

# Support pack rotation
$rotationMode = $config.pack_rotation_mode
if (-not $rotationMode) { $rotationMode = "random" }

# --- Path rules and IDE rules: first matching layer wins ---
# session_override > path_rules > ide_rules > rotation > default_pack
# Note: exclude_dirs is handled earlier as a full silence short-circuit.
$pathRulePack = $null
$pathRules = $config.path_rules
if ($cwd -and $pathRules) {
    foreach ($rule in $pathRules) {
        $pattern = $rule.pattern
        $candidate = $rule.pack
        if ($pattern -and $candidate -and (Test-PathRuleMatch $cwd $pattern)) {
            $candidateDir = Join-Path $InstallDir "packs\$candidate"
            if (Test-Path $candidateDir -PathType Container) {
                $pathRulePack = $candidate
                break
            }
        }
    }
}
$ideRulePack = $null
$ideRules = $config.ide_rules
if ($sessionIde -and $ideRules) {
    foreach ($rule in $ideRules) {
        $ruleIde = Normalize-IdeId $rule.ide
        $candidate = $rule.pack
        if ($ruleIde -and $candidate -and $ruleIde -eq $sessionIde) {
            $candidateDir = Join-Path $InstallDir "packs\$candidate"
            if (Test-Path $candidateDir -PathType Container) {
                $ideRulePack = $candidate
                break
            }
        }
    }
}
$defaultPack = Get-ActivePack $config

if ($rotationMode -eq "agentskill" -or $rotationMode -eq "session_override") {
    # Explicit per-session assignments (from skill)
    $sessionPacks = $state.session_packs
    if (-not $sessionPacks) { $sessionPacks = @{} }
    if ($sessionPacks.ContainsKey($sessionId) -and $sessionPacks[$sessionId]) {
        $packData = $sessionPacks[$sessionId]
        # Handle both old string format and new dict format
        if ($packData -is [hashtable]) {
            $candidate = $packData.pack
        } else {
            $candidate = $packData
        }
        $candidateDir = Join-Path $InstallDir "packs\$candidate"
        if ($candidate -and (Test-Path $candidateDir -PathType Container)) {
            $activePack = $candidate
            # Update timestamp
            $sessionPacks[$sessionId] = @{ pack = $candidate; last_used = [int][double]::Parse((Get-Date -UFormat %s)) }
            $state.session_packs = $sessionPacks
            $stateDirty = $true
        } else {
            # Pack missing, fall through hierarchy: path_rules > ide_rules > default_pack
            $activePack = if ($pathRulePack) { $pathRulePack } elseif ($ideRulePack) { $ideRulePack } else { $defaultPack }
            $sessionPacks.Remove($sessionId)
            $state.session_packs = $sessionPacks
            $stateDirty = $true
        }
    } else {
        # No assignment: check session_packs["default"] (Cursor users without conversation_id)
        $defaultData = $sessionPacks.default
        if ($defaultData) {
            $candidate = if ($defaultData -is [hashtable]) { $defaultData.pack } else { $defaultData }
            $candidateDir = Join-Path $InstallDir "packs\$candidate"
            if ($candidate -and (Test-Path $candidateDir -PathType Container)) {
                $activePack = $candidate
            } else {
                $activePack = if ($pathRulePack) { $pathRulePack } elseif ($ideRulePack) { $ideRulePack } else { $defaultPack }
            }
        } else {
            $activePack = if ($pathRulePack) { $pathRulePack } elseif ($ideRulePack) { $ideRulePack } else { $defaultPack }
        }
    }
} elseif ($pathRulePack) {
    # Path rule wins over IDE rules, rotation, and default
    $activePack = $pathRulePack
} elseif ($ideRulePack) {
    # IDE rule wins over rotation and default when no path rule matched
    $activePack = $ideRulePack
} elseif ($config.pack_rotation -and $config.pack_rotation.Count -gt 0) {
    # Automatic rotation
    $activePack = $config.pack_rotation | Get-Random
}

$packDir = Join-Path $InstallDir "packs\$activePack"
$manifestPath = Join-Path $packDir "openpeon.json"
if (-not (Test-Path $manifestPath)) {
    & $peonLog 'sound' @{ error = 'manifest not found'; pack = $activePack; fallback = 'none' }
    & $peonLog 'exit' @{ duration_ms = [string]$_peonStart.ElapsedMilliseconds; exit = '0' }
    exit 0
}

try {
    $manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
} catch {
    & $peonLog 'sound' @{ error = "$_"; pack = $activePack; fallback = 'none' }
    & $peonLog 'exit' @{ duration_ms = [string]$_peonStart.ElapsedMilliseconds; exit = '0' }
    exit 0
}

# Get sounds for this category
$catSounds = $null
try {
    $catSounds = $manifest.categories.$category.sounds
} catch {
    if ($peonDebug) { Write-Warning "peon-ping: sound lookup failed for category '$category': $_" }
    & $peonLog 'sound' @{ error = "$_"; pack = $activePack; fallback = 'none' }
}
if (-not $catSounds -or $catSounds.Count -eq 0) {
    & $peonLog 'sound' @{ error = 'no sound found'; pack = $activePack; fallback = 'none' }
    & $peonLog 'exit' @{ duration_ms = [string]$_peonStart.ElapsedMilliseconds; exit = '0' }
    exit 0
}

# Filter out individually disabled sounds (config.disabled_sounds[pack][category])
$disabledList = @()
try {
    $_dsPack = $config.disabled_sounds.$activePack
    if ($_dsPack) {
        $_dsCat = $_dsPack.$category
        if ($_dsCat) { $disabledList = @($_dsCat) }
    }
} catch {
    # missing or non-object disabled_sounds; treat as no per-sound disables
}
if ($disabledList.Count -gt 0) {
    $catSounds = @($catSounds | Where-Object { $disabledList -notcontains (Split-Path $_.file -Leaf) })
    if ($catSounds.Count -eq 0) {
        & $peonLog 'sound' @{ error = 'all sounds disabled'; pack = $activePack; category = $category; fallback = 'none' }
        & $peonLog 'exit' @{ duration_ms = [string]$_peonStart.ElapsedMilliseconds; exit = '0' }
        exit 0
    }
}

# Anti-repeat: avoid last played sound
$lastKey = "last_$category"
$lastPlayed = ""
if ($state.ContainsKey($lastKey)) {
    $lastPlayed = $state[$lastKey]
}

$candidates = @($catSounds | Where-Object { (Split-Path $_.file -Leaf) -ne $lastPlayed })
if ($candidates.Count -eq 0) { $candidates = @($catSounds) }

$chosen = $candidates | Get-Random
$soundFile = Split-Path $chosen.file -Leaf
$soundPath = Join-Path $packDir "sounds\$soundFile"

if (-not (Test-Path $soundPath)) {
    & $peonLog 'sound' @{ error = "file not found: $soundFile"; pack = $activePack; fallback = 'none' }
    & $peonLog 'exit' @{ duration_ms = [string]$_peonStart.ElapsedMilliseconds; exit = '0' }
    exit 0
}

# Log sound selection
& $peonLog 'sound' @{ file = $soundFile; pack = $activePack; candidates = [string]$candidates.Count; no_repeat = 'True' }

# Icon resolution chain (CESP Â§5.5)
$iconPath = ""
$iconCandidate = ""
if ($chosen.icon) { $iconCandidate = $chosen.icon }
elseif ($manifest.categories.$category.icon) { $iconCandidate = $manifest.categories.$category.icon }
elseif ($manifest.icon) { $iconCandidate = $manifest.icon }
elseif (Test-Path (Join-Path $packDir "icon.png")) { $iconCandidate = "icon.png" }
if ($iconCandidate) {
    $resolved = [System.IO.Path]::GetFullPath((Join-Path $packDir $iconCandidate))
    $packRoot = [System.IO.Path]::GetFullPath($packDir) + [System.IO.Path]::DirectorySeparatorChar
    if ($resolved.StartsWith($packRoot) -and (Test-Path $resolved -PathType Leaf)) {
        $iconPath = $resolved
    }
}

# Save last played
$state[$lastKey] = $soundFile
try {
    Write-StateAtomic -State $state -Path $StatePath
} catch {
    if ($peonDebug) { Write-Warning "peon-ping: state write failed (last played): $_" }
}

# --- TTS speech text resolution ---
if ($ttsEnabled -and $category) {
    $speechTpl = ""
    if ($chosen -and $chosen.speech_text) {
        $speechTpl = $chosen.speech_text
    } elseif ($resolvedTemplate) {
        $speechTpl = $resolvedTemplate
    } else {
        $speechTpl = "{project} " + [char]0x2014 + " {status}"
    }

    # Build template variables (same set as notification templates).
    # NOTE: This duplicates the variable construction from the notification template
    # rendering block (~lines 1710-1725). Intentional for now to keep TTS text
    # resolution self-contained. If this area is touched again, consolidate into
    # a shared $tplVars hashtable built once and reused by both paths.
    $tplSummary = Resolve-TemplateSummary $event
    $tplToolName = if ($event.tool_name) { [string]$event.tool_name } else { '' }
    $ttsVars = @{
        project   = $project
        summary   = $tplSummary
        tool_name = $tplToolName
        status    = $notifyStatus
        event     = $hookEvent
    }

    $ttsText = $speechTpl
    foreach ($key in $ttsVars.Keys) {
        $ttsText = $ttsText.Replace("{$key}", $ttsVars[$key])
    }
    $ttsText = $ttsText.Trim()
    if ($ttsText -eq [string][char]0x2014 -or -not $ttsText) { $ttsText = "" }
}

# --- Sound and TTS playback with mode sequencing ---
$volume = $config.volume
if (-not $volume) { $volume = 0.5 }

$winPlayScript = Join-Path $InstallDir "scripts\win-play.ps1"

# Helper: play sound file via win-play.ps1
function Play-Sound {
    param([string]$SndPath, [double]$Vol)
    if ((Test-Path $winPlayScript) -and (Test-Path $SndPath)) {
        Start-Process -FilePath "powershell.exe" -ArgumentList "-NoProfile", "-NonInteractive", "-File", "`"$winPlayScript`"", "-path", "`"$SndPath`"", "-vol", $Vol -WindowStyle Hidden
        & $peonLog 'play' @{ backend = 'win-play.ps1'; file = $soundFile; volume = [string]$Vol }
    } else {
        if (-not (Test-Path $winPlayScript)) {
            if ($peonDebug) { Write-Warning "peon-ping: win-play.ps1 not found at '$winPlayScript' - audio skipped" }
            & $peonLog 'play' @{ error = "win-play.ps1 not found"; backend = 'none' }
        } elseif (-not (Test-Path $SndPath)) {
            if ($peonDebug) { Write-Warning "peon-ping: sound file not found at '$SndPath' - audio skipped" }
            & $peonLog 'play' @{ error = "sound file not found"; backend = 'none' }
        }
    }
}

if ($ttsEnabled -and $ttsText) {
    switch ($ttsMode) {
        "sound-then-speak" {
            Play-Sound $soundPath $volume
            Invoke-TtsSpeak -Text $ttsText -Backend $ttsBackend -Voice $ttsVoice -Rate $ttsRate -Volume $ttsVolume
        }
        "speak-only" {
            Invoke-TtsSpeak -Text $ttsText -Backend $ttsBackend -Voice $ttsVoice -Rate $ttsRate -Volume $ttsVolume
        }
        "speak-then-sound" {
            Invoke-TtsSpeak -Text $ttsText -Backend $ttsBackend -Voice $ttsVoice -Rate $ttsRate -Volume $ttsVolume
            Play-Sound $soundPath $volume
        }
    }
} else {
    # No TTS â€” play sound normally
    Play-Sound $soundPath $volume
}

} # end if (-not $skipSound)

# --- Trainer reminder check ---
$trainerSoundPath = ""
$trainerMsg = ""
$trainerCfg = $config.trainer
if ($trainerCfg -and $trainerCfg.enabled) {
    $today = (Get-Date).ToString("yyyy-MM-dd")
    $trainerState = if ($state.ContainsKey("trainer")) { $state["trainer"] } else { @{} }
    if ($trainerState -isnot [hashtable]) { $trainerState = @{} }

    # Default exercises if not configured
    $exercises = @{ pushups = 300; squats = 300 }
    if ($trainerCfg.exercises) {
        $exercises = ConvertTo-Hashtable $trainerCfg.exercises
        if ($exercises -isnot [hashtable]) { $exercises = @{ pushups = 300; squats = 300 } }
    }

    # Date reset: new day resets reps and last_reminder_ts
    if ($trainerState["date"] -ne $today) {
        $freshReps = @{}
        foreach ($ex in $exercises.Keys) { $freshReps[$ex] = 0 }
        $trainerState = @{ date = $today; reps = $freshReps; last_reminder_ts = 0 }
    }

    $reps = if ($trainerState.ContainsKey("reps")) { $trainerState["reps"] } else { @{} }
    if ($reps -isnot [hashtable]) { $reps = @{} }

    # Completion check: skip if all exercises meet or exceed goals
    $allDone = $true
    foreach ($ex in $exercises.Keys) {
        $done = if ($reps.ContainsKey($ex)) { [int]$reps[$ex] } else { 0 }
        $goal = [int]$exercises[$ex]
        if ($done -lt $goal) { $allDone = $false; break }
    }

    if (-not $allDone) {
        $nowTs = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
        $lastTs = if ($trainerState.ContainsKey("last_reminder_ts")) { [long]$trainerState["last_reminder_ts"] } else { 0 }
        $intervalMin = if ($trainerCfg.reminder_interval_minutes) { [int]$trainerCfg.reminder_interval_minutes } else { 20 }
        $minGapMin = if ($trainerCfg.reminder_min_gap_minutes) { [int]$trainerCfg.reminder_min_gap_minutes } else { 5 }
        $elapsed = $nowTs - $lastTs
        $isSessionStart = ($hookEvent -eq "SessionStart")

        if ($isSessionStart -or ($elapsed -ge ($intervalMin * 60) -and $elapsed -ge ($minGapMin * 60))) {
            # Pick trainer sound category
            $trainerDir = Join-Path $InstallDir "trainer"
            $trainerManifestPath = Join-Path $trainerDir "manifest.json"
            if (Test-Path $trainerManifestPath) {
                try {
                    $tm = Get-Content $trainerManifestPath -Raw | ConvertFrom-Json
                    if ($isSessionStart) {
                        $tcat = "trainer.session_start"
                    } else {
                        $hour = (Get-Date).Hour
                        $totalReps = 0; $totalGoal = 0
                        foreach ($ex in $exercises.Keys) {
                            $totalReps += if ($reps.ContainsKey($ex)) { [int]$reps[$ex] } else { 0 }
                            $totalGoal += [int]$exercises[$ex]
                        }
                        $pct = if ($totalGoal -gt 0) { $totalReps / $totalGoal } else { 1.0 }
                        if ($hour -ge 12 -and $pct -lt 0.25) {
                            $tcat = "trainer.slacking"
                        } else {
                            $tcat = "trainer.remind"
                        }
                    }
                    $tSounds = $tm.$tcat
                    if ($tSounds -and $tSounds.Count -gt 0) {
                        $tPick = $tSounds | Get-Random
                        $tFile = Join-Path $trainerDir $tPick.file
                        if (Test-Path $tFile) {
                            $trainerSoundPath = $tFile
                            # Build progress message
                            $parts = @()
                            foreach ($ex in $exercises.Keys) {
                                $done = if ($reps.ContainsKey($ex)) { [int]$reps[$ex] } else { 0 }
                                $goal = [int]$exercises[$ex]
                                $parts += "${ex}: ${done}/${goal}"
                            }
                            $trainerMsg = $parts -join " | "
                        }
                    }
                } catch {
                    if ($peonDebug) { Write-Warning "peon-ping: trainer manifest read failed: $_" }
                }
            }
            # Update last_reminder_ts regardless of sound pick success
            $trainerState["last_reminder_ts"] = $nowTs
        }
    }

    # Persist trainer state
    $state["trainer"] = $trainerState
    try {
        Write-StateAtomic -State $state -Path $StatePath
    } catch {
        if ($peonDebug) { Write-Warning "peon-ping: state write failed (trainer): $_" }
    }

    & $peonLog 'trainer' @{ active = 'True'; reminder = [string][bool]$trainerSoundPath }
} else {
    & $peonLog 'trainer' @{ active = 'False'; reminder = 'False' }
}

# --- Trainer sound sequencing (500ms delay after main sound) ---
if ($trainerSoundPath) {
    $volume = $config.volume
    if (-not $volume) { $volume = 0.5 }
    $winPlayScript = Join-Path $InstallDir "scripts\win-play.ps1"
    if (Test-Path $winPlayScript) {
        $trainerArgs = @("-NoProfile", "-NonInteractive", "-Command",
            "Start-Sleep -Milliseconds 500; & '$winPlayScript' -path '$trainerSoundPath' -vol $volume")
        Start-Process -FilePath "powershell.exe" -ArgumentList $trainerArgs -WindowStyle Hidden
    }
}

# --- Trainer TTS (speak progress after trainer sound) ---
$trainerTtsText = if ($ttsEnabled -and $trainerMsg) { $trainerMsg } else { "" }
if ($trainerTtsText) {
    Invoke-TtsSpeak -Text $trainerTtsText -Backend $ttsBackend -Voice $ttsVoice -Rate $ttsRate -Volume $ttsVolume
}

# --- Trainer desktop notification ---
if ($trainerMsg) {
    $desktopNotif = $config.desktop_notifications
    if ($null -eq $desktopNotif) { $desktopNotif = $true }
    if ($desktopNotif) {
        $winNotifyScript = Join-Path $InstallDir "scripts\win-notify.ps1"
        if (Test-Path $winNotifyScript) {
            $trainerTitle = "Peon Trainer"
            $dismissSecs = if ($config.notification_dismiss_seconds) { $config.notification_dismiss_seconds } else { 4 }
            $parentPid = 0
            try {
                $proc = Get-Process -Id $PID
                if ($proc.Parent) { $parentPid = $proc.Parent.Id }
            } catch { <# PID may not exist; fall through to $parentPid = 0 #> }
            if (-not $parentPid) { $parentPid = 0 }
            $trainerNotifArgs = @("-NoProfile", "-NonInteractive", "-File", "`"$winNotifyScript`"",
                           "-body", "`"$trainerMsg`"", "-title", "`"$trainerTitle`"", "-dismissSeconds", [string]$dismissSecs,
                           "-parentPid", [string]$parentPid)
            Start-Process -FilePath "powershell.exe" -ArgumentList $trainerNotifArgs -WindowStyle Hidden
        }
    }
}

# --- Notification template resolution ---
if ($notify) {
    $tplCfg = $config.notification_templates
    if ($tplCfg) {
        $tplSummary = Resolve-TemplateSummary $event
        $tplToolName = if ($event.tool_name) { [string]$event.tool_name } else { '' }
        $resolved = Resolve-NotificationTemplate `
            -Templates $tplCfg `
            -Category $category `
            -Event $hookEvent `
            -Ntype $ntype `
            -Project $project `
            -Summary $tplSummary `
            -ToolName $tplToolName `
            -Status $notifyStatus `
            -DefaultMsg $notifyMsg
        $notifyMsg = $resolved
    }
}

# --- TTS speech text resolution ---
$ttsCfg = if ($config.tts) { $config.tts } else { @{} }
# Note: $paused guard is handled implicitly by the early-exit when $config.enabled = false
# (see top of hook block), rather than explicitly checked here. See review finding L2.
$ttsEnabled = ($ttsCfg.enabled -eq $true)
$ttsText = ""
$ttsBackend = if ($ttsCfg.backend) { $ttsCfg.backend } else { "auto" }
$ttsVoice = if ($ttsCfg.voice) { $ttsCfg.voice } else { "default" }
$ttsRate = if ($ttsCfg.rate) { $ttsCfg.rate } else { 1.0 }
$ttsVolume = if ($ttsCfg.volume) { $ttsCfg.volume } else { 0.5 }
$ttsMode = if ($ttsCfg.mode) { $ttsCfg.mode } else { "sound-then-speak" }

if ($ttsEnabled -and $category) {
    $speechTpl = ""
    if ($chosen -and $chosen.speech_text) {
        $speechTpl = $chosen.speech_text
    } elseif ($config.notification_templates) {
        # Check for notification template (same key resolution as notification templates)
        $ttsKeyMap = @{ "task.complete" = "stop"; "task.error" = "error" }
        $ttsTplKey = $ttsKeyMap[$category]
        if ($hookEvent -eq "Notification") {
            if ($ntype -eq "idle_prompt") { $ttsTplKey = "idle" }
            elseif ($ntype -eq "elicitation_dialog") { $ttsTplKey = "question" }
        } elseif ($hookEvent -eq "PermissionRequest") {
            $ttsTplKey = "permission"
        }
        if ($ttsTplKey -and $config.notification_templates.$ttsTplKey) {
            $speechTpl = $config.notification_templates.$ttsTplKey
        }
    }
    if (-not $speechTpl) {
        $speechTpl = "{project} `u{2014} {status}"
    }

    # Interpolate template variables (same set as notification templates)
    $ttsVars = @{
        project   = $project
        summary   = Resolve-TemplateSummary $event
        tool_name = if ($event.tool_name) { [string]$event.tool_name } else { '' }
        status    = $notifyStatus
        event     = $hookEvent
    }
    $ttsText = $speechTpl
    foreach ($key in $ttsVars.Keys) {
        $ttsText = $ttsText.Replace("{$key}", $ttsVars[$key])
    }
    $ttsText = $ttsText.Trim()
    if ($ttsText -eq "`u{2014}" -or -not $ttsText) { $ttsText = "" }
}

# TRAINER_TTS_TEXT: trainer progress string when TTS enabled
$trainerTtsText = if ($ttsEnabled -and $trainerMsg) { $trainerMsg } else { "" }

# --- TTS test output (write variables for Pester verification) ---
if ($env:PEON_TEST -eq "1") {
    $ttsLogPath = Join-Path $InstallDir ".tts-vars.json"
    @{
        TTS_ENABLED      = $ttsEnabled
        TTS_TEXT         = $ttsText
        TTS_BACKEND      = $ttsBackend
        TTS_VOICE        = $ttsVoice
        TTS_RATE         = $ttsRate
        TTS_VOLUME       = $ttsVolume
        TTS_MODE         = $ttsMode
        TRAINER_TTS_TEXT = $trainerTtsText
    } | ConvertTo-Json | Set-Content -Path $ttsLogPath -Encoding UTF8
}

# --- Desktop notification dispatch ---
$desktopNotif = $config.desktop_notifications
if ($null -eq $desktopNotif) { $desktopNotif = $true }

if ($notify -and $desktopNotif) {
    $winNotifyScript = Join-Path $InstallDir "scripts\win-notify.ps1"
    if (Test-Path $winNotifyScript) {
$marker = if ($config.notification_title_marker) { $config.notification_title_marker } else { [char]0x25CF }
        $notifTitle = "$marker $notificationProject"
        $dismissSecs = if ($config.notification_dismiss_seconds) { $config.notification_dismiss_seconds } else { 4 }
        # Resolve parent PID (the IDE/terminal that spawned Claude Code) for click-to-focus
        $parentPid = 0
        try {
            $proc = Get-Process -Id $PID
            if ($proc.Parent) { $parentPid = $proc.Parent.Id }
        } catch { <# PID may not exist; fall through to $parentPid = 0 #> }
        if (-not $parentPid) { $parentPid = 0 }
        $notifArgs = @("-NoProfile", "-NonInteractive", "-File", "`"$winNotifyScript`"",
                       "-body", "`"$notifyMsg`"", "-title", "`"$notifTitle`"", "-dismissSeconds", [string]$dismissSecs,
                       "-parentPid", [string]$parentPid)
        if ($iconPath) { $notifArgs += @("-iconPath", "`"$iconPath`"") }
        Start-Process -FilePath "powershell.exe" -ArgumentList $notifArgs -WindowStyle Hidden
    }
}

# Log notify phase
$_mobileService = ''
if ($config.mobile_notify -and $config.mobile_notify.service) { $_mobileService = $config.mobile_notify.service }
& $peonLog 'notify' @{ desktop = [string]($notify -and $desktopNotif); mobile = [string][bool]$_mobileService }

# Log exit phase with duration
& $peonLog 'exit' @{ duration_ms = [string]$_peonStart.ElapsedMilliseconds; exit = '0' }

exit 0
