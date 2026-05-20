@echo off

:: Set expiry date and time (YYYY-MM-DD HH:MM)
SET EXPIRY=2026-05-22 18:00

:: Get current datetime in YYYY-MM-DD HH:MM format
FOR /F "tokens=2 delims==" %%I IN ('wmic os get localdatetime /value') DO SET DATETIME=%%I
SET NOW=%DATETIME:~0,4%-%DATETIME:~4,2%-%DATETIME:~6,2% %DATETIME:~8,2%:%DATETIME:~10,2%

IF "%NOW%" GTR "%EXPIRY%" (
    echo ========================================
    echo  Trial period has expired.
    echo  Expired on: %EXPIRY%
    echo  Please contact support to continue.
    echo ========================================
    pause
    exit /b 1
)

echo Trial valid until: %EXPIRY%
python -m streamlit run app_tally.py
