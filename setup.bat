@echo off
setlocal

rem Create an isolated Windows environment beside the application source.
cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
  echo Python Launcher was not found.
  echo Install Python from https://www.python.org/downloads/windows/
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo Creating .venv...
  py -3 -m venv .venv
  if errorlevel 1 exit /b 1
)

echo Updating pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :network_error

echo Installing application and build dependencies...
".venv\Scripts\python.exe" -m pip install --requirement requirements.txt
if errorlevel 1 goto :network_error

echo Verifying installed packages...
".venv\Scripts\python.exe" -c "import PySide6, PyInstaller; print('PySide6', PySide6.__version__); print('PyInstaller', PyInstaller.__version__)"
if errorlevel 1 exit /b 1

echo.
echo Setup complete. Run the app with:
echo   .venv\Scripts\python.exe main.py
exit /b 0

:network_error
echo.
echo Package installation failed. If the output contains HTTP 403, the
echo configured network proxy or package index is refusing access; this is
echo not an application error. See README.md under "HTTP 403 troubleshooting".
exit /b 1
