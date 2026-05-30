@echo off
setlocal enabledelayedexpansion

set APP_NAME=Wallace's PDFirst
set APP_BUILD_NAME=Wallaces_PDFirst
set ROOT=%~dp0
set VENV=%ROOT%.venv-build
set PYTHON_CMD=

cd /d "%ROOT%"

echo [1/6] Preparing clean build folders...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "%APP_BUILD_NAME%.spec" del "%APP_BUILD_NAME%.spec"
if exist "%APP_NAME%.spec" del "%APP_NAME%.spec"

echo [2/6] Creating/verifying Python virtual environment...
if not "%PYTHON_EXE%"=="" (
  set PYTHON_CMD="%PYTHON_EXE%"
) else (
  py -3.12 -c "import sys" >nul 2>nul
  if not errorlevel 1 set PYTHON_CMD=py -3.12
)
if "%PYTHON_CMD%"=="" (
  py -3.11 -c "import sys" >nul 2>nul
  if not errorlevel 1 set PYTHON_CMD=py -3.11
)
if "%PYTHON_CMD%"=="" (
  python -c "import sys" >nul 2>nul
  if not errorlevel 1 set PYTHON_CMD=python
)
if "%PYTHON_CMD%"=="" (
  echo Python 3.11 or 3.12 is required to build. Set PYTHON_EXE to python.exe if it is not on PATH.
  exit /b 1
)

%PYTHON_CMD% -m venv "%VENV%"
if errorlevel 1 (
  echo Could not create virtual environment. Check that Python includes venv support.
  exit /b 1
)

call "%VENV%\Scripts\python.exe" -m pip install --upgrade pip
call "%VENV%\Scripts\pip.exe" install -r requirements.txt
if errorlevel 1 exit /b 1

echo [3/5] Running automated tests...
call "%VENV%\Scripts\python.exe" -m unittest discover -s app\tests
if errorlevel 1 exit /b 1

echo [4/5] Building portable executable with PyInstaller...
call "%VENV%\Scripts\pyinstaller.exe" ^
  --noconfirm ^
  --clean ^
  --windowed ^
  --name "%APP_BUILD_NAME%" ^
  --add-data "resources;resources" ^
  app\main.py
if errorlevel 1 exit /b 1

echo [5/5] Copying documentation and notices...
if not exist "dist\%APP_NAME%" ren "dist\%APP_BUILD_NAME%" "%APP_NAME%"
if exist "dist\%APP_NAME%\%APP_BUILD_NAME%.exe" ren "dist\%APP_NAME%\%APP_BUILD_NAME%.exe" "%APP_NAME%.exe"
copy README.md "dist\%APP_NAME%\README.md" >nul
if not exist "dist\%APP_NAME%\resources" xcopy /e /i /y resources "dist\%APP_NAME%\resources" >nul
(
  echo Dependency license notices:
  echo - PySide6 / Qt: LGPL/commercial terms, see official Qt for Python notices.
  echo - pypdf: BSD license.
  echo - Pillow: HPND license.
  echo - python-docx: MIT license.
  echo - reportlab: BSD-style license.
  echo - PyInstaller: GPL with bootloader exception.
) > "dist\%APP_NAME%\THIRD_PARTY_NOTICES.txt"

echo.
echo Portable build complete:
echo   dist\%APP_NAME%\%APP_NAME%.exe
echo.
endlocal
