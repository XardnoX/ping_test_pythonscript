@echo off
:: Check for administrative privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :admin
) else (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%0' -Verb RunAs"
    exit
)

:admin
:: Change to the directory where the batch file is located
cd /d %~dp0/ping_test

:: Run the first Python script
python ping_and_write.py

:: After the first script completes, run the second Python script
python ping_graph.py

pause