@echo off
title StockSense Launcher

:: Set expiry date and time (YYYY-MM-DD HH:MM)
SET EXPIRY=2026-05-22 18:00

:: Get current datetime using PowerShell (works on all Windows versions)
FOR /F "usebackq" %%I IN (`powershell -NoProfile -Command "Get-Date -Format 'yyyy-MM-dd HH:mm'"`) DO SET NOW=%%I

echo Current time : %NOW%
echo Trial expiry : %EXPIRY%
echo.

IF "%NOW%" GTR "%EXPIRY%" (
    echo ========================================
    echo  Trial period has expired.
    echo  Expired on: %EXPIRY%
    echo  Please contact support to continue.
    echo ========================================
    pause
    exit /b 1
)

echo Trial is valid. Starting StockSense...
echo.
python -m streamlit run app_tally.py
pause
