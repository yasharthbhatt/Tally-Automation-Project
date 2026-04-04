@echo off
REM Inventory Intelligence Dashboard Launcher for Windows
REM Double-click this file to start the dashboard

echo ========================================
echo  Inventory Intelligence Dashboard
echo  Starting...
echo ========================================
echo.

REM Get the directory where this script is located
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run installation first.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate

REM Check if streamlit is installed
streamlit --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Streamlit not installed!
    echo Installing dependencies...
    pip install -r requirements.txt
    pip install altair==4.2.2
)

REM Start the dashboard
echo.
echo Dashboard starting...
echo Open your browser and go to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the dashboard
echo.

streamlit run app_tally.py

pause
