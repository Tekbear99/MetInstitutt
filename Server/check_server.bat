@echo off
:start
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL

if "%ERRORLEVEL%"=="0" (
    echo The program is running
    goto start
) ELSE (
    echo The program is not running
    start cmd /k CALL start_server.bat
    goto start
)