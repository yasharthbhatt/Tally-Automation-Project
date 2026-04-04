@echo off
REM Deployment Package Preparation Script for Windows
REM Creates a clean package ready for client deployment

echo ========================================
echo  StockSense - Deployment Package Creator
echo ========================================
echo.

REM Get version (default to 1.0 if not provided)
set VERSION=%1
if "%VERSION%"=="" set VERSION=1.0

REM Get current date
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set DATE=%datetime:~0,8%
set PACKAGE_NAME=StockSense_v%VERSION%_%DATE%
set DEPLOY_DIR=..\%PACKAGE_NAME%

echo Creating deployment package: %PACKAGE_NAME%
echo.

REM Create deployment directory
if exist "%DEPLOY_DIR%" (
    echo Warning: Deployment directory already exists. Removing...
    rmdir /s /q "%DEPLOY_DIR%"
)

mkdir "%DEPLOY_DIR%"

echo Step 1: Copying essential files...

REM Copy directories
xcopy ai_engine "%DEPLOY_DIR%\ai_engine\" /E /I /Q
xcopy automation "%DEPLOY_DIR%\automation\" /E /I /Q
xcopy config "%DEPLOY_DIR%\config\" /E /I /Q
xcopy dashboard "%DEPLOY_DIR%\dashboard\" /E /I /Q
xcopy data_ingestion "%DEPLOY_DIR%\data_ingestion\" /E /I /Q
xcopy insights "%DEPLOY_DIR%\insights\" /E /I /Q
xcopy models "%DEPLOY_DIR%\models\" /E /I /Q
xcopy subscription "%DEPLOY_DIR%\subscription\" /E /I /Q
xcopy utils "%DEPLOY_DIR%\utils\" /E /I /Q

REM Copy main application file
copy app_tally.py "%DEPLOY_DIR%\"

REM Copy installation and run scripts
copy install.sh "%DEPLOY_DIR%\"
copy install.bat "%DEPLOY_DIR%\"
copy run_dashboard.sh "%DEPLOY_DIR%\"
copy run_dashboard.bat "%DEPLOY_DIR%\"

REM Copy requirements
copy requirements.txt "%DEPLOY_DIR%\"

REM Copy environment example (NOT .env with real keys!)
copy .env.example "%DEPLOY_DIR%\"

REM Copy documentation
copy README.md "%DEPLOY_DIR%\"
copy CLIENT_INSTALL_GUIDE.md "%DEPLOY_DIR%\"
copy INSTALLATION.md "%DEPLOY_DIR%\"
copy QUICK_START.md "%DEPLOY_DIR%\"
copy DEPLOYMENT_CHECKLIST.md "%DEPLOY_DIR%\"
copy FEATURES_IMPLEMENTED.md "%DEPLOY_DIR%\"
if exist SUBSCRIPTION_SETUP.md copy SUBSCRIPTION_SETUP.md "%DEPLOY_DIR%\"
if exist PACKAGES_GUIDE.md copy PACKAGES_GUIDE.md "%DEPLOY_DIR%\"

echo Step 2: Creating empty directories...

REM Create empty directories for data and logs
mkdir "%DEPLOY_DIR%\data"
mkdir "%DEPLOY_DIR%\logs"

echo Step 3: Cleaning up unnecessary files...

REM Remove Python cache files
for /d /r "%DEPLOY_DIR%" %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
del /s /q "%DEPLOY_DIR%\*.pyc" 2>nul
del /s /q "%DEPLOY_DIR%\*.pyo" 2>nul

echo Step 4: Creating README for deployment...

(
echo ========================================
echo   StockSense - AI Inventory Intelligence
echo ========================================
echo.
echo QUICK START:
echo.
echo 1. INSTALL:
echo    Windows: Double-click "install.bat"
echo    Mac/Linux: Run "./install.sh" in Terminal
echo.
echo 2. RUN:
echo    Windows: Double-click "run_dashboard.bat"
echo    Mac/Linux: Run "./run_dashboard.sh"
echo.
echo 3. ACCESS:
echo    Open browser to: http://localhost:8501
echo.
echo DOCUMENTATION:
echo - CLIENT_INSTALL_GUIDE.md - Simple installation guide
echo - INSTALLATION.md - Detailed installation instructions
echo - README.md - Application overview
echo - QUICK_START.md - How to use the application
echo.
echo REQUIREMENTS:
echo - Python 3.9 or higher
echo - 500 MB disk space
echo - Internet connection ^(for installation only^)
echo.
echo SUPPORT:
echo Check documentation files for troubleshooting.
echo.
echo ========================================
) > "%DEPLOY_DIR%\START_HERE.txt"

echo Step 5: Creating version info...

(
echo StockSense Deployment Package
echo Version: %VERSION%
echo Build Date: %DATE%
echo Package: %PACKAGE_NAME%
echo.
echo Included Components:
echo - Core application ^(app_tally.py^)
echo - AI Engine modules
echo - Data ingestion tools
echo - Dashboard interface
echo - Subscription management
echo - Documentation
echo.
echo Installation: See CLIENT_INSTALL_GUIDE.md
echo Support: See documentation files
) > "%DEPLOY_DIR%\VERSION.txt"

echo Step 6: Creating deployment package...

REM Check if PowerShell is available for compression
where powershell >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    powershell -Command "Compress-Archive -Path '%DEPLOY_DIR%' -DestinationPath '..\%PACKAGE_NAME%.zip' -Force"
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ========================================
        echo  Package Created Successfully!
        echo ========================================
        echo.
        echo Package Location: ..\%PACKAGE_NAME%.zip
        echo.
        echo Package Contents:
        echo   - Source code and modules
        echo   - Installation scripts
        echo   - Documentation
        echo   - Empty data and logs directories
        echo.
        echo IMPORTANT:
        echo   [✓] Virtual environment ^(.venv^) excluded
        echo   [✓] Cache files excluded
        echo   [✓] .env file excluded ^(only .env.example included^)
        echo   [✓] Test data excluded
        echo.
        echo Next Steps:
        echo   1. Copy %PACKAGE_NAME%.zip to USB or send to client
        echo   2. Client extracts the ZIP file
        echo   3. Client runs install.bat
        echo   4. Follow DEPLOYMENT_CHECKLIST.md
        echo.

        set /p CLEANUP="Remove unzipped deployment folder? (y/n): "
        if /i "%CLEANUP%"=="y" (
            rmdir /s /q "%DEPLOY_DIR%"
            echo Unzipped folder removed. ZIP file preserved.
        ) else (
            echo Both ZIP and unzipped folder preserved.
        )
    ) else (
        echo ERROR: Failed to create ZIP package
        exit /b 1
    )
) else (
    echo WARNING: PowerShell not available for creating ZIP
    echo Please manually zip the folder: %DEPLOY_DIR%
)

echo.
echo Deployment package ready! 🚀
echo.
pause
