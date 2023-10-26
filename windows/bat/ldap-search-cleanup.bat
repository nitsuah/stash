@echo off
setlocal enabledelayedexpansion

set "inputFile=C:\users\USERNAME\desktop\ou_search.txt"
set "outputFile=C:\users\USERNAME\desktop\ou_usernames.txt"

for /f "tokens=*" %%A in (%inputFile%) do (
    set "line=%%A"
    set "line=!line:member: uid=!"
    set "line=!line:,ou=users,ou=group,dc=dc=!"
    echo !line! >> %outputFile%
)

echo Script completed.
