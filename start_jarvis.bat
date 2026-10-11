
@echo off
cd /d "%~dp0"

if exist "venv\Scripts\python.exe" (
    "venv\Scripts\python.exe" "main.py"
) else (
    py -3 "main.py"
)

echo.
echo JARVIS has stopped or encountered an error.
pause