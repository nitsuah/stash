@echo off
rem -----------------------------------------------------------
rem Script: run-log.bat
rem Description: Report Runner Code with Logging
rem Author: AJH
rem Date: 07/10/2017
rem Updated: 10/25/2023
rem -----------------------------------------------------------

rem How to Use:
rem   Run this script with the report generator as a parameter.
rem   Example: run-log.bat SOMEBATFILE.bat

rem Set report generator
set "reportgen=%1"

rem Extract the base name of the report generator without extension
for %%F in ("%reportgen%") do set "reportbase=%%~nF"

rem Generate timestamp for the log file
set "timestamp=%date:~10,13%_%date:~4,2%_%date:~7,2%"

rem START REPORT
call "%reportgen%" > "%reportbase%_%timestamp%.log"
