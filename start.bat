@echo off
title StockSense Launcher
cd /d "%~dp0"

:: ── Set expiry date and time (YYYY-MM-DD HH:MM) ──────────────────────
SET EXPIRY=2026-05-24 18:00
:: ─────────────────────────────────────────────────────────────────────

echo ========================================
echo  StockSense - Smart Inventory Dashboard
echo ========================================
echo.

:: Check expiry using PowerShell
FOR /F "usebackq" %%I IN (`powershell -NoProfile -Command "Get-Date -Format 'yyyy-MM-dd HH:mm'"`) DO SET NOW=%%I

echo Current time : %NOW%
echo Trial expiry : %EXPIRY%
echo.

IF "%NOW%" GTR "%EXPIRY%" (
    echo ========================================
    echo  Trial period has expired.
    echo  Expired on : %EXPIRY%
    echo  Contact support to continue.
    echo ========================================
    pause
    exit /b 1
)

:: Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate
)

:: Install dependencies if streamlit is missing
python -m streamlit --version >nul 2>&1
if errorlevel 1 (
    echo Streamlit not found. Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies.
        echo Make sure Python and pip are installed.
        pause
        exit /b 1
    )
)

echo Trial valid. Starting StockSense...
echo Open browser at: http://localhost:8501
echo Press Ctrl+C to stop.
echo.

python -m streamlit run app_tally.py

pause
