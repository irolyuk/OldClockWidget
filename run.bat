@echo off
cd /d "%~dp0"

py -c "import PySide6" >nul 2>&1

if errorlevel 1 (
    echo PySide6 not found. Installing...
    py -m pip install PySide6
    if errorlevel 1 (
        echo Failed to install PySide6.
        pause
        exit /b 1
    )
)

py main.py
if errorlevel 1 pause
