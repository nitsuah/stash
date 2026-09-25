---
up: "[[repos/stash]]"
source: https://github.com/nitsuah/stash/blob/main/windows/README.md
kind: repo-doc
repo: stash
---

# Windows

Scripts for Windows automation, Active Directory, and log management.

## Batch (`bat/`)

| Script | Description |
|--------|-------------|
| [`ldap-search-users.bat`](https://github.com/nitsuah/stash/blob/main/windows/bat/ldap-search-users.bat) | LDAP user search — by email, username, group, disabled accounts, stale logins |
| [`ldap-search-cleanup.bat`](https://github.com/nitsuah/stash/blob/main/windows/bat/ldap-search-cleanup.bat) | Strip LDAP member attribute prefixes from OU export → clean username list |
| [`run-logger.bat`](https://github.com/nitsuah/stash/blob/main/windows/bat/run-logger.bat) | Wrap any batch script with timestamped log output |

**Usage — ldap-search-cleanup:**
```bat
rem Default paths (Desktop):
ldap-search-cleanup.bat

rem Custom paths:
ldap-search-cleanup.bat C:\exports\ou_search.txt C:\exports\usernames.txt
```

## PowerShell (`pwsh/`)

See [`pwsh/README.md`](pwsh/README.md) for full details.

| Script | Description |
|--------|-------------|
| [`compress-logs-v02a.ps1`](https://github.com/nitsuah/stash/blob/main/windows/pwsh/compress-logs-v02a.ps1) | Log file compression with JBoss server detection and retention policies |
| [`ConvertCSV-ToExcel.ps1`](https://github.com/nitsuah/stash/blob/main/windows/pwsh/ConvertCSV-ToExcel.ps1) | Batch CSV → Excel with auto-formatting and COM lifecycle management |
| [`detect-server-v03d.ps1`](https://github.com/nitsuah/stash/blob/main/windows/pwsh/detect-server-v03d.ps1) | JVM server type detection, environment mapping, config validation |

## VBA (`vba/`)

| Script | Description |
|--------|-------------|
| [`ldap-search-cleanup.vb`](https://github.com/nitsuah/stash/blob/main/windows/vba/ldap-search-cleanup.vb) | LDAP search result processing and formatting for Office |
