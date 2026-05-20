@echo off
title StockSense Launcher
cd /d "%~dp0"

:: ── Set expiry date and time (YYYY-MM-DD HH:MM) ──────────────────────
SET EXPIRY=2026-05-22 18:00
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

:: Activate virtual environment
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate
) else (
    echo WARNING: No .venv found, using system Python
)

echo Trial valid. Starting StockSense...
echo Open browser at: http://localhost:8501
echo Press Ctrl+C to stop.
echo.

streamlit run app_tally.py

pause
