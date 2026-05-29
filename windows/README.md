# Windows

Scripts for Windows automation, Active Directory, and log management.

## Batch (`bat/`)

| Script | Description |
|--------|-------------|
| [`ldap-search-users.bat`](bat/ldap-search-users.bat) | LDAP user search — by email, username, group, disabled accounts, stale logins |
| [`ldap-search-cleanup.bat`](bat/ldap-search-cleanup.bat) | Strip LDAP member attribute prefixes from OU export → clean username list |
| [`run-logger.bat`](bat/run-logger.bat) | Wrap any batch script with timestamped log output |

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
| [`compress-logs-v02a.ps1`](pwsh/compress-logs-v02a.ps1) | Log file compression with JBoss server detection and retention policies |
| [`ConvertCSV-ToExcel.ps1`](pwsh/ConvertCSV-ToExcel.ps1) | Batch CSV → Excel with auto-formatting and COM lifecycle management |
| [`detect-server-v03d.ps1`](pwsh/detect-server-v03d.ps1) | JVM server type detection, environment mapping, config validation |

## VBA (`vba/`)

| Script | Description |
|--------|-------------|
| [`ldap-search-cleanup.vb`](vba/ldap-search-cleanup.vb) | LDAP search result processing and formatting for Office |
