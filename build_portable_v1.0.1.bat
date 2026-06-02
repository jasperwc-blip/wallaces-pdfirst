@echo off
setlocal enabledelayedexpansion

set APP_PUBLIC_NAME=Wallace's PDFirst
set APP_BUILD_NAME=Wallaces_PDFirst
set VERSION_FOLDER=Wallace's_PDFirst_v1.0.1
set ROOT=%~dp0
set VENV=%ROOT%.venv-build
set BUILD_DIR=%ROOT%build-v1.0.1
set DIST_STAGE=%ROOT%dist\_v1.0.1_stage
set FINAL_DIR=%ROOT%dist\%VERSION_FOLDER%
set NO_OCR_FOLDER=Wallace's_PDFirst_v1.0.1_(Excl_OCR)
set NO_OCR_DIR=%ROOT%dist\%NO_OCR_FOLDER%
set PYTHON_CMD=

cd /d "%ROOT%"

echo [1/6] Preparing v1.0.1 build folders...
if exist "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%"
if exist "%DIST_STAGE%" rmdir /s /q "%DIST_STAGE%"
if exist "%FINAL_DIR%" rmdir /s /q "%FINAL_DIR%"
if exist "%NO_OCR_DIR%" rmdir /s /q "%NO_OCR_DIR%"

echo [2/6] Creating/verifying Python virtual environment...
if exist "%VENV%\Scripts\python.exe" (
  set PYTHON_CMD="%VENV%\Scripts\python.exe"
) else if not "%PYTHON_EXE%"=="" (
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

if not exist "%VENV%\Scripts\python.exe" (
  %PYTHON_CMD% -m venv "%VENV%"
  if errorlevel 1 exit /b 1
)

call "%VENV%\Scripts\python.exe" -m pip install --upgrade pip
call "%VENV%\Scripts\pip.exe" install -r requirements.txt
if errorlevel 1 exit /b 1

echo [3/6] Running automated tests...
call "%VENV%\Scripts\python.exe" -m unittest discover -s app\tests
if errorlevel 1 exit /b 1

echo [4/6] Building v1.0.1 executable with PyInstaller...
call "%VENV%\Scripts\pyinstaller.exe" ^
  --noconfirm ^
  --clean ^
  --windowed ^
  --name "%APP_BUILD_NAME%" ^
  --distpath "%DIST_STAGE%" ^
  --workpath "%BUILD_DIR%" ^
  --specpath "%BUILD_DIR%" ^
  --hidden-import pdf2docx ^
  --hidden-import app.pdf2docx_worker ^
  --hidden-import app.services.pdf_to_pptx ^
  --hidden-import fitz ^
  --hidden-import docx ^
  --hidden-import cv2 ^
  --hidden-import numpy ^
  --hidden-import pytesseract ^
  --hidden-import pptx ^
  --add-data "%ROOT%resources;resources" ^
  app\main.py
if errorlevel 1 exit /b 1

echo [5/6] Creating v1.0.1 portable folder...
mkdir "%FINAL_DIR%"
xcopy /e /i /y "%DIST_STAGE%\%APP_BUILD_NAME%" "%FINAL_DIR%" >nul
copy README.md "%FINAL_DIR%\README.md" >nul
call :PruneOcrBundle "%FINAL_DIR%\_internal\resources\ocr\tesseract"
(
  echo Dependency license notices:
  echo - PySide6 / Qt: LGPL/commercial terms, see official Qt for Python notices.
  echo - pypdf: BSD license.
  echo - Pillow: HPND license.
  echo - python-docx: MIT license.
  echo - reportlab: BSD-style license.
  echo - PyMuPDF: AGPL/commercial terms, see official PyMuPDF notices.
  echo - pdf2docx: AGPL/commercial terms, see official pdf2docx notices.
  echo - opencv-python / numpy: see bundled package license notices.
  echo - PyInstaller: GPL with bootloader exception.
) > "%FINAL_DIR%\THIRD_PARTY_NOTICES.txt"

echo [6/6] Verifying v1.0.1 executable...
if not exist "%FINAL_DIR%\%APP_BUILD_NAME%.exe" (
  echo Expected executable missing: "%FINAL_DIR%\%APP_BUILD_NAME%.exe"
  exit /b 1
)

echo Creating no-OCR v1.0.1 portable folder...
xcopy /e /i /y "%FINAL_DIR%" "%NO_OCR_DIR%" >nul
if exist "%NO_OCR_DIR%\_internal\resources\ocr" rmdir /s /q "%NO_OCR_DIR%\_internal\resources\ocr"
(
  echo This portable build intentionally excludes OCR PDF mode and bundled OCR files.
  echo Delete this marker only if OCR resources are restored.
) > "%NO_OCR_DIR%\NO_OCR_PORTABLE"
if not exist "%NO_OCR_DIR%\%APP_BUILD_NAME%.exe" (
  echo Expected no-OCR executable missing: "%NO_OCR_DIR%\%APP_BUILD_NAME%.exe"
  exit /b 1
)

if exist "%DIST_STAGE%" rmdir /s /q "%DIST_STAGE%"

echo.
echo Wallace's PDFirst v1.0.1 portable build complete:
echo   dist\%VERSION_FOLDER%\%APP_BUILD_NAME%.exe
echo   dist\%NO_OCR_FOLDER%\%APP_BUILD_NAME%.exe
echo.
endlocal
exit /b 0

:PruneOcrBundle
set "OCR_ROOT=%~1"
if not exist "%OCR_ROOT%" exit /b 0
if exist "%OCR_ROOT%\doc" rmdir /s /q "%OCR_ROOT%\doc"
del /q "%OCR_ROOT%\*.html" >nul 2>nul
for %%F in ("%OCR_ROOT%\*.exe") do (
  if /I not "%%~nxF"=="tesseract.exe" del /q "%%~fF"
)
if exist "%OCR_ROOT%\tessdata" (
  for /d %%D in ("%OCR_ROOT%\tessdata\*") do rmdir /s /q "%%~fD"
  for %%F in ("%OCR_ROOT%\tessdata\*.traineddata") do (
    if /I not "%%~nxF"=="eng.traineddata" if /I not "%%~nxF"=="chi_sim.traineddata" if /I not "%%~nxF"=="chi_tra.traineddata" del /q "%%~fF"
  )
  for %%F in ("%OCR_ROOT%\tessdata\*") do (
    if /I not "%%~nxF"=="eng.traineddata" if /I not "%%~nxF"=="chi_sim.traineddata" if /I not "%%~nxF"=="chi_tra.traineddata" del /q "%%~fF"
  )
)
exit /b 0
