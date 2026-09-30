@echo off
setlocal

rem Always build from the directory containing this script and main.py.
cd /d "%~dp0"

set "PYTHON=.venv\Scripts\python.exe"
if not exist "%PYTHON%" (
  echo The project virtual environment was not found.
  echo Run setup.bat before build.bat.
  exit /b 1
)

"%PYTHON%" -c "import PySide6, PyInstaller" >nul 2>nul
if errorlevel 1 (
  echo PySide6 or PyInstaller is not installed in .venv.
  echo Run setup.bat before build.bat.
  exit /b 1
)

"%PYTHON%" -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --windowed ^
  --onedir ^
  --name CoCTracker ^
  main.py

if errorlevel 1 (
  echo.
  echo Build failed.
  exit /b 1
)

echo.
echo Build complete: "%~dp0dist\CoCTracker\CoCTracker.exe"
endlocal
