@echo off
rem =============================================================================
rem ldap-search-cleanup.bat
rem =============================================================================
rem Strips LDAP member attribute prefixes from an OU search export, leaving
rem clean usernames one-per-line in an output file.
rem
rem Usage:
rem   ldap-search-cleanup.bat [INPUT_FILE] [OUTPUT_FILE]
rem
rem   INPUT_FILE  Path to raw LDAP search output (default: %USERPROFILE%\Desktop\ou_search.txt)
rem   OUTPUT_FILE Path for cleaned username list  (default: %USERPROFILE%\Desktop\ou_usernames.txt)
rem
rem Input format expected (one entry per line):
rem   member: uid=jsmith,ou=users,ou=group,dc=domain,dc=com
rem
rem Output format:
rem   jsmith
rem =============================================================================

setlocal enabledelayedexpansion

set "inputFile=%~1"
set "outputFile=%~2"

if "%inputFile%"=="" set "inputFile=%USERPROFILE%\Desktop\ou_search.txt"
if "%outputFile%"=="" set "outputFile=%USERPROFILE%\Desktop\ou_usernames.txt"

if not exist "%inputFile%" (
    echo ERROR: Input file not found: %inputFile%
    exit /b 1
)

if exist "%outputFile%" del "%outputFile%"

for /f "tokens=*" %%A in (%inputFile%) do (
    set "line=%%A"
    set "line=!line:member: uid=!"
    for /f "delims=," %%B in ("!line!") do (
        echo %%B >> "%outputFile%"
    )
)

echo Done. Output written to: %outputFile%
