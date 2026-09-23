@echo off
cd /d "%~dp0"

py -m pip install PySide6 pyinstaller
if errorlevel 1 goto error

py -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --windowed ^
  --onefile ^
  --name OldClockWidget ^
  --add-data "clock_font.json;." ^
  main.py

if errorlevel 1 goto error

echo.
echo DONE: dist\OldClockWidget.exe
pause
exit /b 0

:error
echo.
echo BUILD FAILED
pause
exit /b 1
