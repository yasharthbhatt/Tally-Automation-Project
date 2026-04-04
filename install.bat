@echo off
REM Quick Installation Script for Windows

echo ========================================
echo  Inventory Intelligence System
echo  Installation Wizard
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.9 or higher from python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Install compatible altair
echo Installing compatible Altair version...
pip install altair==4.2.2

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
)

REM Create data directories
if not exist "data\" mkdir data
if not exist "logs\" mkdir logs

echo.
echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo To start the dashboard, double-click:
echo   run_dashboard.bat
echo.
echo Or run from command line:
echo   .venv\Scripts\activate
echo   streamlit run app_tally.py
echo.
pause
