@echo off
:: ============================================================
:: Truck Scale Weighing System - Portable Setup Script
:: This script creates a portable version that can run on any
:: Windows computer without installing Python or dependencies.
:: ============================================================

setlocal enabledelayedexpansion
title Truck Scale Weighing System - Portable Setup

echo.
echo ========================================================
echo    TRUCK SCALE WEIGHING SYSTEM - PORTABLE SETUP
echo ========================================================
echo.
echo This script will create a portable version of the
echo application that can run on any Windows computer.
echo.
echo Options:
echo   1. Build Standalone EXE (Recommended - Single file)
echo   2. Create Portable Folder (For development/testing)
echo   3. Exit
echo.
set /p choice="Enter your choice (1/2/3): "

if "%choice%"=="1" goto BUILD_EXE
if "%choice%"=="2" goto PORTABLE_FOLDER
if "%choice%"=="3" goto END
echo Invalid choice. Exiting.
goto END

:BUILD_EXE
echo.
echo ========================================================
echo    BUILDING STANDALONE EXECUTABLE
echo ========================================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    goto END
)

:: Install PyInstaller if not present
echo Checking PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

:: Install required dependencies
echo.
echo Installing required dependencies...
pip install pillow opencv-python pyserial reportlab pywin32

:: Build the executable
echo.
echo Building standalone executable...
echo This may take a few minutes...
echo.

pyinstaller --noconfirm --onefile --windowed ^
    --name "TruckScaleApp" ^
    --icon "assets\app_icon.ico" ^
    --add-data "assets;assets" ^
    --add-data "config.json;." ^
    --hidden-import "PIL._tkinter_finder" ^
    --hidden-import "cv2" ^
    --hidden-import "serial" ^
    --hidden-import "reportlab" ^
    --hidden-import "win32print" ^
    --hidden-import "win32api" ^
    --collect-all "reportlab" ^
    main.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    echo Check the error messages above.
    pause
    goto END
)

echo.
echo ========================================================
echo    BUILD SUCCESSFUL!
echo ========================================================
echo.
echo The standalone executable has been created at:
echo   dist\TruckScaleApp.exe
echo.
echo You can copy this file to any Windows computer.
echo The application will create necessary folders on first run.
echo.

:: Create a simple launcher info
echo Creating distribution package...

:: Create dist folder with necessary files
if not exist "dist\assets" mkdir "dist\assets"
if exist "assets\app_icon.ico" copy "assets\app_icon.ico" "dist\assets\" >nul

:: Create a readme in dist
echo Truck Scale Weighing System > "dist\README.txt"
echo. >> "dist\README.txt"
echo This is a standalone application. >> "dist\README.txt"
echo No installation required. >> "dist\README.txt"
echo. >> "dist\README.txt"
echo Simply run TruckScaleApp.exe to start the application. >> "dist\README.txt"
echo. >> "dist\README.txt"
echo The application will create the following folders: >> "dist\README.txt"
echo - logs\ (application logs) >> "dist\README.txt"
echo - exports\ (exported data) >> "dist\README.txt"

echo.
echo Distribution package created in 'dist' folder.
echo You can copy the 'dist' folder to any Windows computer.
echo.
pause
goto END

:PORTABLE_FOLDER
echo.
echo ========================================================
echo    CREATING PORTABLE FOLDER
echo ========================================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    goto END
)

:: Create portable folder structure
set "PORTABLE_DIR=TruckScale_Portable"
if exist "%PORTABLE_DIR%" (
    echo Removing existing portable folder...
    rmdir /s /q "%PORTABLE_DIR%"
)

echo Creating portable folder structure...
mkdir "%PORTABLE_DIR%"
mkdir "%PORTABLE_DIR%\app"
mkdir "%PORTABLE_DIR%\app\assets"
mkdir "%PORTABLE_DIR%\app\logs"
mkdir "%PORTABLE_DIR%\app\exports"
mkdir "%PORTABLE_DIR%\python"

:: Copy application files
echo Copying application files...
copy "main.py" "%PORTABLE_DIR%\app\" >nul
copy "weighing_scale_app.py" "%PORTABLE_DIR%\app\" >nul
copy "config.py" "%PORTABLE_DIR%\app\" >nul
copy "config.json" "%PORTABLE_DIR%\app\" >nul 2>nul
copy "database.py" "%PORTABLE_DIR%\app\" >nul
copy "serial_manager.py" "%PORTABLE_DIR%\app\" >nul
copy "camera_manager.py" "%PORTABLE_DIR%\app\" >nul
copy "messagebox.py" "%PORTABLE_DIR%\app\" >nul
copy "ui_components.py" "%PORTABLE_DIR%\app\" >nul
copy "pdf_print_manager.py" "%PORTABLE_DIR%\app\" >nul
copy "setup_database.py" "%PORTABLE_DIR%\app\" >nul
copy "requirements.txt" "%PORTABLE_DIR%\app\" >nul
copy "transactions.db" "%PORTABLE_DIR%\app\" >nul 2>nul
xcopy "assets" "%PORTABLE_DIR%\app\assets\" /E /I /Y >nul 2>nul
xcopy "hooks" "%PORTABLE_DIR%\app\hooks\" /E /I /Y >nul 2>nul

:: Create launcher batch file
echo Creating launcher...
(
echo @echo off
echo title Truck Scale Weighing System
echo cd /d "%%~dp0app"
echo.
echo :: Check if venv exists
echo if not exist "..\python\Scripts\python.exe" (
echo     echo First run - Setting up Python environment...
echo     echo This may take a few minutes...
echo     echo.
echo     
echo     :: Download embedded Python if not present
echo     if not exist "..\python\python.exe" (
echo         echo Downloading Python...
echo         powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-embed-amd64.zip' -OutFile '..\python.zip'}"
echo         echo Extracting Python...
echo         powershell -Command "& {Expand-Archive -Path '..\python.zip' -DestinationPath '..\python' -Force}"
echo         del "..\python.zip"
echo         
echo         :: Configure embedded Python for pip
echo         echo import site ^>^> "..\python\python311._pth"
echo     )
echo     
echo     :: Install pip
echo     echo Installing pip...
echo     powershell -Command "& {Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile '..\python\get-pip.py'}"
echo     ..\python\python.exe ..\python\get-pip.py
echo     
echo     :: Install dependencies
echo     echo Installing dependencies...
echo     ..\python\Scripts\pip.exe install pillow opencv-python pyserial reportlab pywin32
echo     
echo     echo.
echo     echo Setup complete! Starting application...
echo     echo.
echo )
echo.
echo :: Run the application
echo ..\python\python.exe main.py
echo if errorlevel 1 (
echo     echo.
echo     echo Application closed with an error.
echo     pause
echo )
) > "%PORTABLE_DIR%\RUN_TRUCKSCALE.bat"

:: Create a simple run script for systems with Python already installed
(
echo @echo off
echo title Truck Scale Weighing System
echo cd /d "%%~dp0app"
echo python main.py
echo if errorlevel 1 (
echo     echo.
echo     echo Application closed with an error.
echo     pause
echo )
) > "%PORTABLE_DIR%\RUN_WITH_PYTHON.bat"

:: Create README
(
echo Truck Scale Weighing System - Portable Edition
echo ===============================================
echo.
echo HOW TO RUN:
echo.
echo Option 1: If Python is NOT installed on the computer
echo   - Double-click RUN_TRUCKSCALE.bat
echo   - First run will download Python and dependencies
echo   - This may take several minutes on first run
echo.
echo Option 2: If Python IS already installed
echo   - Double-click RUN_WITH_PYTHON.bat
echo   - Requires Python 3.8+ with pip
echo.
echo SYSTEM REQUIREMENTS:
echo   - Windows 10/11 (64-bit)
echo   - Internet connection (first run only)
echo   - USB camera (optional)
echo   - Serial port for scale (optional)
echo.
echo FOLDERS:
echo   app\        - Application files
echo   python\     - Embedded Python (created on first run)
echo.
echo The application stores data in:
echo   app\logs\       - Application logs
echo   app\exports\    - Exported reports
echo   app\transactions.db - Database
echo.
echo For support: advantechnique@gmail.com
) > "%PORTABLE_DIR%\README.txt"

echo.
echo ========================================================
echo    PORTABLE FOLDER CREATED!
echo ========================================================
echo.
echo The portable folder has been created: %PORTABLE_DIR%\
echo.
echo Contents:
echo   - RUN_TRUCKSCALE.bat  (Auto-setup and run)
echo   - RUN_WITH_PYTHON.bat (Run if Python installed)
echo   - README.txt          (Instructions)
echo   - app\                (Application files)
echo.
echo You can copy the entire '%PORTABLE_DIR%' folder to a USB
echo drive and run it on any Windows computer.
echo.
pause
goto END

:END
endlocal