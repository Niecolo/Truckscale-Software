@echo off
REM ============================================================================
REM Weighing Scale Application - Single Build Script
REM ============================================================================
REM This batch file creates an executable from the Python application using PyInstaller
REM with comprehensive prerequisite checks and post-build operations.
REM ============================================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"

REM ============================================================================
REM Set Counters and Flags
REM ============================================================================
set CHECKS_TOTAL=0
set CHECKS_PASSED=0
set CHECKS_FAILED=0
set BUILD_FAILED=0

echo.
echo ============================================================================
echo Weighing Scale Application - Build Process Started
echo ============================================================================
echo.

REM ============================================================================
REM Check Python Installation
REM ============================================================================
set /a CHECKS_TOTAL+=1
echo [!CHECKS_TOTAL!/X] Checking Python installation...
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [FAIL] Python is not installed or not in PATH
    set /a CHECKS_FAILED+=1
    set BUILD_FAILED=1
) else (
    echo [PASS] Python is available
    set /a CHECKS_PASSED+=1
)

REM ============================================================================
REM Check PyInstaller Installation
REM ============================================================================
set /a CHECKS_TOTAL+=1
echo [!CHECKS_TOTAL!/X] Checking PyInstaller installation...
pip show pyinstaller >nul 2>&1
if !errorlevel! neq 0 (
    echo [FAIL] PyInstaller is not installed
    echo Installing PyInstaller...
    pip install pyinstaller
    if !errorlevel! neq 0 (
        echo [FAIL] Failed to install PyInstaller
        set /a CHECKS_FAILED+=1
        set BUILD_FAILED=1
    ) else (
        echo [PASS] PyInstaller installed successfully
        set /a CHECKS_PASSED+=1
    )
) else (
    echo [PASS] PyInstaller is available
    set /a CHECKS_PASSED+=1
)

REM ============================================================================
REM Check Required Python Packages
REM ============================================================================
set /a CHECKS_TOTAL+=1
echo [!CHECKS_TOTAL!/X] Checking required Python packages...

REM Check for reportlab (for PDF generation)
python -c "import reportlab" >nul 2>&1
if !errorlevel! neq 0 (
    echo [WARN] reportlab not found - Installing...
    pip install reportlab
    if !errorlevel! neq 0 (
        echo [WARN] Failed to install reportlab - PDF generation disabled
    ) else (
        echo [PASS] reportlab installed successfully
    )
) else (
    echo [PASS] reportlab is available
)

REM Check for pyserial (for serial communication)
python -c "import serial" >nul 2>&1
if !errorlevel! neq 0 (
    echo [WARN] pyserial not found - Installing...
    pip install pyserial
    if !errorlevel! neq 0 (
        echo [WARN] Failed to install pyserial - serial communication disabled
    ) else (
        echo [PASS] pyserial installed successfully
    )
) else (
    echo [PASS] pyserial is available
)

REM Check for pywin32 (for Windows-specific features)
python -c "import win32print, win32api, win32con" >nul 2>&1
if !errorlevel! neq 0 (
    echo [WARN] pywin32 not found - Installing...
    pip install pywin32
    if !errorlevel! neq 0 (
        echo [WARN] Failed to install pywin32 - some features may be limited
    ) else (
        echo [PASS] pywin32 installed successfully
    )
) else (
    echo [PASS] pywin32 is available
)

REM Check for opencv-python (for camera functionality)
python -c "import cv2" >nul 2>&1
if !errorlevel! neq 0 (
    echo [WARN] opencv-python not found - Installing...
    pip install opencv-python
    if !errorlevel! neq 0 (
        echo [WARN] Failed to install opencv-python - camera functionality disabled
    ) else (
        echo [PASS] opencv-python installed successfully
    )
) else (
    echo [PASS] opencv-python is available
)

REM Check for pillow (for image handling)
python -c "import PIL" >nul 2>&1
if !errorlevel! neq 0 (
    echo [WARN] pillow not found - Installing...
    pip install pillow
    if !errorlevel! neq 0 (
        echo [WARN] Failed to install pillow - image handling may be limited
    ) else (
        echo [PASS] pillow installed successfully
    )
) else (
    echo [PASS] pillow is available
)

REM Check for numpy (for numerical operations)
python -c "import numpy" >nul 2>&1
if !errorlevel! neq 0 (
    echo [WARN] numpy not found - Installing...
    pip install numpy
    if !errorlevel! neq 0 (
        echo [WARN] Failed to install numpy - some functionality may be limited
    ) else (
        echo [PASS] numpy installed successfully
    )
) else (
    echo [PASS] numpy is available
)

REM Check for additional dependencies that might be needed
python -c "import tkinter" >nul 2>&1
if !errorlevel! neq 0 (
    echo [WARN] tkinter not found - This should be included with Python
) else (
    echo [PASS] tkinter is available
)

python -c "import ttk" >nul 2>&1
if !errorlevel! neq 0 (
    echo [WARN] ttk not found - This should be included with Python
) else (
    echo [PASS] ttk is available
)

REM Install any additional dependencies from requirements.txt if it exists in parent directory
if exist "..\requirements.txt" (
    echo [BUILD] Installing additional dependencies from requirements.txt...
    pip install -r "..\requirements.txt"
    if !errorlevel! neq 0 (
        echo [WARN] Some additional dependencies failed to install
    ) else (
        echo [PASS] Additional dependencies installed successfully
    )
)

echo [PASS] Required packages check completed
set /a CHECKS_PASSED+=1

REM ============================================================================
REM Check Application Files
REM ============================================================================
set /a CHECKS_TOTAL+=1
echo [!CHECKS_TOTAL!/X] Checking application files...

REM Check for essential application files (minimum required for build)
set MISSING_FILES=0

if not exist "main.py" (
    echo [FAIL] main.py not found
    set /a MISSING_FILES+=1
)
if not exist "weighing_scale_app.py" (
    echo [FAIL] weighing_scale_app.py not found
    set /a MISSING_FILES+=1
)

echo DEBUG: Essential files missing: %MISSING_FILES%

if %MISSING_FILES% gtr 0 (
    echo [FAIL] Missing essential application files
    set /a CHECKS_FAILED+=1
    set BUILD_FAILED=1
) else (
    echo [PASS] Essential application files found
    set /a CHECKS_PASSED+=1
    
    REM Check for optional refactored files (warn if missing but don't fail build)
    set OPTIONAL_MISSING=0
    if not exist "constants.py" (
        echo [WARN] constants.py not found (refactored version will not be built)
        set /a OPTIONAL_MISSING+=1
    )
    if not exist "config_manager.py" (
        echo [WARN] config_manager.py not found (refactored version will not be built)
        set /a OPTIONAL_MISSING+=1
    )
    if not exist "database_manager.py" (
        echo [WARN] database_manager.py not found (refactored version will not be built)
        set /a OPTIONAL_MISSING+=1
    )
    if not exist "ui_manager.py" (
        echo [WARN] ui_manager.py not found (refactored version will not be built)
        set /a OPTIONAL_MISSING+=1
    )
    if not exist "tab_manager.py" (
        echo [WARN] tab_manager.py not found (refactored version will not be built)
        set /a OPTIONAL_MISSING+=1
    )
    if not exist "error_handler.py" (
        echo [WARN] error_handler.py not found (refactored version will not be built)
        set /a OPTIONAL_MISSING+=1
    )
    if not exist "refactored_app.py" (
        echo [WARN] refactored_app.py not found (refactored version will not be built)
        set /a OPTIONAL_MISSING+=1
    )
    
    if %OPTIONAL_MISSING% gtr 0 (
        echo [INFO] %OPTIONAL_MISSING% optional files missing - only original version will be built
    ) else (
        echo [INFO] All refactored files found - both versions will be built
    )
)

REM ============================================================================
REM Check Assets Directory and Icon
REM ============================================================================
set /a CHECKS_TOTAL+=1
echo [!CHECKS_TOTAL!/X] Checking assets directory and icon...

if not exist "assets" (
    echo [WARN] assets directory not found, creating it...
    mkdir assets
    echo [INFO] Created assets directory
) else (
    echo [PASS] assets directory found
)

set ICON_FOUND=0
set ICON_PATH=assets\app_icon.ico

if not exist "%ICON_PATH%" (
    echo [WARN] app_icon.ico not found in assets folder
    echo [INFO] Looking for alternative icon files...
    
    REM Check for other common icon formats
    if exist "assets\icon.ico" (
        set ICON_PATH=assets\icon.ico
        echo [PASS] Found alternative icon: icon.ico
        set ICON_FOUND=1
    ) else if exist "assets\app.ico" (
        set ICON_PATH=assets\app.ico
        echo [PASS] Found alternative icon: app.ico
        set ICON_FOUND=1
    ) else if exist "assets\*.png" (
        echo [WARN] Found PNG files but need ICO format for Windows executable
        echo [INFO] Consider converting PNG to ICO format for better compatibility
        set ICON_FOUND=0
    ) else (
        echo [WARN] No icon files found in assets folder
        echo [INFO] Application will be built without custom icon
        set ICON_FOUND=0
    )
) else (
    echo [PASS] app_icon.ico found in assets folder
    echo [INFO] Icon file size verification:
    for %%F in ("%ICON_PATH%") do (
        set ICON_SIZE=%%~zF
        echo [INFO] Icon size: %%~zF bytes
    )
    set ICON_FOUND=1
)

if %ICON_FOUND% equ 1 (
    echo [PASS] Icon file available: %ICON_PATH%
    echo [INFO] This icon will be used for the executable and application window
) else (
    echo [WARN] No suitable icon found - building with default Windows icon
    set ICON_PATH=
)

set /a CHECKS_PASSED+=1

REM ============================================================================
REM Summary of Pre-build Checks
REM ============================================================================
echo.
echo ============================================================================
echo Pre-build Checks Summary
echo ============================================================================
echo Total Checks: !CHECKS_TOTAL!
echo Passed: !CHECKS_PASSED!
echo Failed: !CHECKS_FAILED!
echo.

if %BUILD_FAILED% equ 1 (
    echo [FAIL] Some critical checks failed. Build process aborted.
    echo Please resolve the issues above and run this script again.
    pause
    exit /b 1
)

echo [PASS] All critical checks passed. Proceeding with build...
echo.

REM ============================================================================
REM Clean Previous Build
REM ============================================================================
echo [BUILD] Cleaning previous build files...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"
echo [BUILD] Previous build files cleaned

REM ============================================================================
REM Create PyInstaller Command
REM ============================================================================
REM Install all dependencies from requirements.txt if it exists
if exist "..\requirements.txt" (
    echo [BUILD] Installing dependencies from requirements.txt...
    pip install -r "..\requirements.txt"
    if !errorlevel! neq 0 (
        echo [WARN] Some dependencies from requirements.txt failed to install
    ) else (
        echo [PASS] Dependencies from requirements.txt installed successfully
    )
)

REM Create PyInstaller Command
echo [BUILD] Creating PyInstaller command...

set APP_NAME=WeighingScaleApp
set MAIN_SCRIPT=main.py

set PYINSTALLER_CMD=pyinstaller --name=%APP_NAME% --onefile --windowed --clean

REM Add icon if available
if defined ICON_PATH (
    if exist "%ICON_PATH%" (
        set PYINSTALLER_CMD=%PYINSTALLER_CMD% --icon="%ICON_PATH%"
        echo [BUILD] Using icon: %ICON_PATH%
        echo [INFO] This icon will be used for:
        echo   - Executable file icon
        echo   - Application window title bar
        echo   - Taskbar icon
        echo   - Alt+Tab switcher
    ) else (
        echo [BUILD] Icon path defined but file not found: %ICON_PATH%
        echo [BUILD] Building without custom icon
    )
) else (
    echo [BUILD] No icon found, building with default Windows icon
)

REM Add data files including assets folder
set PYINSTALLER_CMD=%PYINSTALLER_CMD% --add-data="assets;assets"

REM Add all Python modules to ensure complete packaging
set PYINSTALLER_CMD=%PYINSTALLER_CMD% --add-data="*.py;."

REM Add comprehensive hidden imports for all modules
set PYINSTALLER_CMD=%PYINSTALLER_CMD% --hidden-import=tkinter --hidden-import=ttk --hidden-import=sqlite3 --hidden-import=serial --hidden-import=serial.tools.list_ports --hidden-import=reportlab --hidden-import=win32print --hidden-import=win32api --hidden-import=win32con --hidden-import=cv2 --hidden-import=PIL --hidden-import=numpy --hidden-import=queue --hidden-import=threading --hidden-import=datetime --hidden-import=json --hidden-import=csv --hidden-import=os --hidden-import=sys --hidden-import=hashlib --hidden-import=getpass --hidden-import=atexit --hidden-import=base64 --hidden-import=secrets --hidden-import=io --hidden-import=tempfile --hidden-import=subprocess --hidden-import=re --hidden-import=shutil --hidden-import=logging --hidden-import=functools --hidden-import=contextlib --hidden-import=typing --hidden-import=enum --hidden-import=time --hidden-import=decimal --hidden-import=uuid --hidden-import=inspect --hidden-import=importlib --hidden-import=traceback --hidden-import=math --hidden-import=statistics

REM Add hidden imports for refactored modules
set PYINSTALLER_CMD=%PYINSTALLER_CMD% --hidden-import=constants --hidden-import=config_manager --hidden-import=database_manager --hidden-import=ui_manager --hidden-import=tab_manager --hidden-import=error_handler --hidden-import=refactored_app --hidden-import=camera_manager --hidden-import=serial_manager --hidden-import=messagebox --hidden-import=pdf_print_manager --hidden-import=ui_components --hidden-import=config --hidden-import=database

REM Add hidden imports for specific components that might be missed
set PYINSTALLER_CMD=%PYINSTALLER_CMD% --hidden-import=tkinter.messagebox --hidden-import=tkinter.filedialog --hidden-import=tkinter.simpledialog --hidden-import=tkinter.scrolledtext --hidden-import=tkinter.ttk --hidden-import=tkinter.font --hidden-import=tkinter.colorchooser --hidden-import=PIL.Image --hidden-import=PIL.ImageTk --hidden-import=PIL.ImageDraw --hidden-import=PIL.ImageFont --hidden-import=cv2.VideoCapture --hidden-import=cv2.destroyAllWindows --hidden-import=cv2.waitKey --hidden-import=cv2.imshow --hidden-import=serial.Serial --hidden-import=serial.tools.list_ports.comports --hidden-import=serial.SerialException --hidden-import=reportlab.pdfgen --hidden-import=reportlab.lib.pagesizes --hidden-import=reportlab.lib.units --hidden-import=reportlab.platypus --hidden-import=reportlab.lib.styles --hidden-import=reportlab.pdfbase --hidden-import=reportlab.pdfbase.ttfonts --hidden-import=reportlab.lib.enums --hidden-import=win32print.GetDefaultPrinter --hidden-import=win32api.GetProfileString --hidden-import=win32con.CW_USEDEFAULT --hidden-import=win32print.OpenPrinter --hidden-import=win32print.StartDocPrinter --hidden-import=win32print.StartPagePrinter --hidden-import=win32print.EndPagePrinter --hidden-import=win32print.EndDocPrinter --hidden-import=win32print.ClosePrinter

REM Exclude unnecessary modules to reduce size
set PYINSTALLER_CMD=%PYINSTALLER_CMD% --exclude-module=matplotlib --exclude-module=pandas --exclude-module=scipy --exclude-module=jupyter --exclude-module=IPython --exclude-module=sphinx --exclude-module=pytest --exclude-module=setuptools --exclude-module=pip --exclude-module=wheel --exclude-module=distutils --exclude-module=ensurepip --exclude-module=venv --exclude-module=pipenv --exclude-module=conda --exclude-module=anaconda

REM Collect all data from subdirectories for complete packaging
set PYINSTALLER_CMD=%PYINSTALLER_CMD% --collect-all=cv2 --collect-all=PIL --collect-all=numpy --collect-all=reportlab --collect-all=serial

REM Runtime hooks are automatically handled by PyInstaller

set PYINSTALLER_CMD=%PYINSTALLER_CMD% %MAIN_SCRIPT%

echo [BUILD] Final PyInstaller command configured
echo [INFO] Build will include:
echo   - All required dependencies
echo   - Assets folder with icon and resources
echo   - Complete Python module collection
echo   - Windows-specific components
echo   - Camera and serial communication support
echo   - PDF generation capabilities

echo [BUILD] Command: %PYINSTALLER_CMD%

REM ============================================================================
REM Build Executable
REM ============================================================================
echo.
echo [BUILD] Starting PyInstaller build process...
echo This may take several minutes...
echo.

%PYINSTALLER_CMD%

if !errorlevel! neq 0 (
    echo.
    echo [FAIL] PyInstaller build failed
    set BUILD_FAILED=1
) else (
    echo.
    echo [PASS] PyInstaller build completed successfully
)

REM ============================================================================
REM Build Refactored Version (Optional)
REM ============================================================================
if %BUILD_FAILED% equ 0 (
    if exist "refactored_app.py" (
        if exist "constants.py" (
            echo.
            echo [BUILD] Building refactored version as alternative...
            
            REM Clean previous build for refactored version (but keep main executable)
            if exist "build" rmdir /s /q "build"
            
            REM Backup main executable if it exists
            if exist "dist\%APP_NAME%.exe" (
                copy "dist\%APP_NAME%.exe" "dist\%APP_NAME%_backup.exe" >nul
            )
            
            REM Create PyInstaller command for refactored version
            set REFACTORED_CMD=pyinstaller --name=%APP_NAME%_Refactored --onefile --windowed --clean
            
            if defined ICON_PATH (
                if exist "%ICON_PATH%" (
                    set REFACTORED_CMD=%REFACTORED_CMD% --icon="%ICON_PATH%"
                    echo [BUILD] Using icon for refactored version: %ICON_PATH%
                ) else (
                    echo [BUILD] Icon path defined but file not found for refactored version
                )
            )
            
            set REFACTORED_CMD=%REFACTORED_CMD% --add-data="assets;assets" --add-data="*.py;."
            
            REM Add all hidden imports for refactored version (same as main version)
            set REFACTORED_CMD=%REFACTORED_CMD% --hidden-import=tkinter --hidden-import=ttk --hidden-import=sqlite3 --hidden-import=serial --hidden-import=serial.tools.list_ports --hidden-import=reportlab --hidden-import=win32print --hidden-import=win32api --hidden-import=win32con --hidden-import=cv2 --hidden-import=PIL --hidden-import=numpy --hidden-import=queue --hidden-import=threading --hidden-import=datetime --hidden-import=json --hidden-import=csv --hidden-import=os --hidden-import=sys --hidden-import=hashlib --hidden-import=getpass --hidden-import=atexit --hidden-import=base64 --hidden-import=secrets --hidden-import=io --hidden-import=tempfile --hidden-import=subprocess --hidden-import=re --hidden-import=shutil --hidden-import=logging --hidden-import=functools --hidden-import=contextlib --hidden-import=typing --hidden-import=enum --hidden-import=time --hidden-import=decimal --hidden-import=uuid --hidden-import=inspect --hidden-import=importlib --hidden-import=traceback --hidden-import=math --hidden-import=statistics --hidden-import=constants --hidden-import=config_manager --hidden-import=database_manager --hidden-import=ui_manager --hidden-import=tab_manager --hidden-import=error_handler --hidden-import=refactored_app --hidden-import=camera_manager --hidden-import=serial_manager --hidden-import=messagebox --hidden-import=pdf_print_manager --hidden-import=ui_components --hidden-import=config --hidden-import=database --hidden-import=tkinter.messagebox --hidden-import=tkinter.filedialog --hidden-import=tkinter.simpledialog --hidden-import=tkinter.scrolledtext --hidden-import=tkinter.ttk --hidden-import=tkinter.font --hidden-import=tkinter.colorchooser --hidden-import=PIL.Image --hidden-import=PIL.ImageTk --hidden-import=PIL.ImageDraw --hidden-import=PIL.ImageFont --hidden-import=cv2.VideoCapture --hidden-import=cv2.destroyAllWindows --hidden-import=cv2.waitKey --hidden-import=cv2.imshow --hidden-import=serial.Serial --hidden-import=serial.tools.list_ports.comports --hidden-import=serial.SerialException --hidden-import=reportlab.pdfgen --hidden-import=reportlab.lib.pagesizes --hidden-import=reportlab.lib.units --hidden-import=reportlab.platypus --hidden-import=reportlab.lib.styles --hidden-import=reportlab.pdfbase --hidden-import=reportlab.pdfbase.ttfonts --hidden-import=reportlab.lib.enums --hidden-import=win32print.GetDefaultPrinter --hidden-import=win32api.GetProfileString --hidden-import=win32con.CW_USEDEFAULT --hidden-import=win32print.OpenPrinter --hidden-import=win32print.StartDocPrinter --hidden-import=win32print.StartPagePrinter --hidden-import=win32print.EndPagePrinter --hidden-import=win32print.EndDocPrinter --hidden-import=win32print.ClosePrinter
            
            set REFACTORED_CMD=%REFACTORED_CMD% --exclude-module=matplotlib --exclude-module=pandas --exclude-module=scipy --exclude-module=jupyter --exclude-module=IPython --exclude-module=sphinx --exclude-module=pytest --exclude-module=setuptools --exclude-module=pip --exclude-module=wheel --exclude-module=distutils --exclude-module=ensurepip --exclude-module=venv --exclude-module=pipenv --exclude-module=conda --exclude-module=anaconda --collect-all=cv2 --collect-all=PIL --collect-all=numpy --collect-all=reportlab --collect-all=serial --runtime-hook=pyi_rth_tkinter.py --runtime-hook=pyi_rth_pkgres.py
            
            set REFACTORED_CMD=%REFACTORED_CMD% main_refactored.py
            
            echo [BUILD] Building refactored version...
            
            pyinstaller !REFACTORED_CMD!
            
            if !errorlevel! neq 0 (
                echo [WARN] Refactored version build failed, but main build succeeded
                REM Restore main executable if refactored build failed
                if exist "dist\%APP_NAME%_backup.exe" (
                    move "dist\%APP_NAME%_backup.exe" "dist\%APP_NAME%.exe" >nul
                )
            ) else (
                echo [PASS] Refactored version build completed successfully
                REM Restore main executable after successful refactored build
                if exist "dist\%APP_NAME%_backup.exe" (
                    move "dist\%APP_NAME%_backup.exe" "dist\%APP_NAME%.exe" >nul
                )
            )
        ) else (
            echo [SKIP] Refactored version build skipped - constants.py not found
        )
    ) else (
        echo [SKIP] Refactored version build skipped - refactored_app.py not found
    )
)

REM ============================================================================
REM Post-build Operations
REM ============================================================================
if %BUILD_FAILED% equ 0 (
    echo.
    echo [BUILD] Performing post-build operations...
    
    REM Create distribution directory
    if not exist "distribution" mkdir "distribution"
    
    REM Check and copy main executable
    if exist "dist\%APP_NAME%.exe" (
        echo [PASS] Main executable created: dist\%APP_NAME%.exe
        
        REM Get file size
        for %%F in ("dist\%APP_NAME%.exe") do set FILE_SIZE=%%~zF
        set /a FILE_SIZE_MB=!FILE_SIZE!/1048576
        echo [INFO] Main executable size: !FILE_SIZE_MB! MB
        
        REM Copy main executable to distribution directory
        copy "dist\%APP_NAME%.exe" "distribution\" >nul
        echo [PASS] Main executable copied to distribution directory
        
        REM Create version info file
        echo Weighing Scale Application - Original Version > "distribution\VERSION_ORIGINAL.txt"
        echo Build Date: %date% %time% >> "distribution\VERSION_ORIGINAL.txt"
        echo Executable: %APP_NAME%.exe >> "distribution\VERSION_ORIGINAL.txt"
        echo Size: !FILE_SIZE_MB! MB >> "distribution\VERSION_ORIGINAL.txt"
        echo. >> "distribution\VERSION_ORIGINAL.txt"
        echo This is the original monolithic version. >> "distribution\VERSION_ORIGINAL.txt"
        echo. >> "distribution\VERSION_ORIGINAL.txt"
        echo Features: >> "distribution\VERSION_ORIGINAL.txt"
        echo - Complete functionality >> "distribution\VERSION_ORIGINAL.txt"
        echo - All original features preserved >> "distribution\VERSION_ORIGINAL.txt"
        echo - Single executable file >> "distribution\VERSION_ORIGINAL.txt"
        
    ) else (
        echo [FAIL] Main executable not found in dist directory
    )
    
    REM Check and copy refactored executable
    if exist "dist\main_refactored\main_refactored.exe" (
        echo [PASS] Refactored executable created: dist\main_refactored\main_refactored.exe
        
        REM Get file size for refactored version
        for %%F in ("dist\main_refactored\main_refactored.exe") do set REFACTORED_SIZE=%%~zF
        set /a REFACTORED_SIZE_MB=!REFACTORED_SIZE!/1048576
        echo [INFO] Refactored executable size: !REFACTORED_SIZE_MB! MB
        
        REM Copy refactored executable to distribution directory
        copy "dist\main_refactored\main_refactored.exe" "distribution\%APP_NAME%_Refactored.exe" >nul
        echo [PASS] Refactored executable copied to distribution directory
        
        REM Create version info file for refactored version
        echo Weighing Scale Application - Refactored Version > "distribution\VERSION_REFACTORED.txt"
        echo Build Date: %date% %time% >> "distribution\VERSION_REFACTORED.txt"
        echo Executable: %APP_NAME%_Refactored.exe >> "distribution\VERSION_REFACTORED.txt"
        echo Size: !REFACTORED_SIZE_MB! MB >> "distribution\VERSION_REFACTORED.txt"
        echo. >> "distribution\VERSION_REFACTORED.txt"
        echo This is the new refactored modular version. >> "distribution\VERSION_REFACTORED.txt"
        echo. >> "distribution\VERSION_REFACTORED.txt"
        echo Improvements: >> "distribution\VERSION_REFACTORED.txt"
        echo - Clean modular architecture >> "distribution\VERSION_REFACTORED.txt"
        echo - Separated concerns >> "distribution\VERSION_REFACTORED.txt"
        echo - Better error handling >> "distribution\VERSION_REFACTORED.txt"
        echo - Type-safe configuration >> "distribution\VERSION_REFACTORED.txt"
        echo - Comprehensive logging >> "distribution\VERSION_REFACTORED.txt"
        echo - Easier to maintain and extend >> "distribution\VERSION_REFACTORED.txt"
        echo. >> "distribution\VERSION_REFACTORED.txt"
        echo Architecture: >> "distribution\VERSION_REFACTORED.txt"
        echo - constants.py - Centralized constants and enums >> "distribution\VERSION_REFACTORED.txt"
        echo - config_manager.py - Configuration management >> "distribution\VERSION_REFACTORED.txt"
        echo - database_manager.py - Database operations >> "distribution\VERSION_REFACTORED.txt"
        echo - ui_manager.py - UI components >> "distribution\VERSION_REFACTORED.txt"
        echo - tab_manager.py - Tab functionality >> "distribution\VERSION_REFACTORED.txt"
        echo - error_handler.py - Error handling and logging >> "distribution\VERSION_REFACTORED.txt"
        echo - refactored_app.py - Main application >> "distribution\VERSION_REFACTORED.txt"
        
    ) else (
        echo [WARN] Refactored executable not found (this is optional)
    )
    
    REM Copy assets if they exist
    if exist "assets" (
        xcopy "assets" "distribution\assets\" /e /i /y >nul
        echo [PASS] Assets copied to distribution directory
    )
    
    REM Copy documentation if it exists
    if exist "REFACTORING_README.md" (
        copy "REFACTORING_README.md" "distribution\" >nul
        echo [PASS] Refactoring documentation copied
    )
    
    REM Create comprehensive README file
    echo Weighing Scale Application - Complete Distribution Package > "distribution\README.txt"
    echo ========================================================== >> "distribution\README.txt"
    echo. >> "distribution\README.txt"
    echo Build Date: %date% %time% >> "distribution\README.txt"
    echo. >> "distribution\README.txt"
    echo AVAILABLE VERSIONS: >> "distribution\README.txt"
    echo ------------------- >> "distribution\README.txt"
    echo. >> "distribution\README.txt"
    
    if exist "distribution\%APP_NAME%.exe" (
        echo 1. ORIGINAL VERSION (%APP_NAME%.exe) >> "distribution\README.txt"
        echo    - Traditional monolithic architecture >> "distribution\README.txt"
        echo    - All original features preserved >> "distribution\README.txt"
        echo    - Size: !FILE_SIZE_MB! MB >> "distribution\README.txt"
        echo    - Use this version if you want the proven stable version >> "distribution\README.txt"
        echo. >> "distribution\README.txt"
    )
    
    if exist "distribution\%APP_NAME%_Refactored.exe" (
        echo 2. REFACTORED VERSION (%APP_NAME%_Refactored.exe) >> "distribution\README.txt"
        echo    - New modular architecture >> "distribution\README.txt"
        echo    - Clean separation of concerns >> "distribution\README.txt"
        echo    - Better error handling and logging >> "distribution\README.txt"
        echo    - Size: !REFACTORED_SIZE_MB! MB >> "distribution\README.txt"
        echo    - Use this version for development and future enhancements >> "distribution\README.txt"
        echo. >> "distribution\README.txt"
    )
    
    echo INSTALLATION INSTRUCTIONS: >> "distribution\README.txt"
    echo -------------------------- >> "distribution\README.txt"
    echo 1. Choose which version to run (see descriptions above) >> "distribution\README.txt"
    echo 2. Run the executable file (.exe) >> "distribution\README.txt"
    echo 3. The application will create necessary directories and files automatically >> "distribution\README.txt"
    echo 4. First run will require authentication (default admin credentials) >> "distribution\README.txt"
    echo. >> "distribution\README.txt"
    echo SYSTEM REQUIREMENTS: >> "distribution\README.txt"
    echo -------------------- >> "distribution\README.txt"
    echo - Windows 7 or later >> "distribution\README.txt"
    echo - 2GB RAM minimum (4GB recommended) >> "distribution\README.txt"
    echo - 100MB free disk space >> "distribution\README.txt"
    echo - Administrator privileges for first run >> "distribution\README.txt"
    echo. >> "distribution\README.txt"
    echo HARDWARE REQUIREMENTS: >> "distribution\README.txt"
    echo --------------------- >> "distribution\README.txt"
    echo - Compatible weighing scale with serial output >> "distribution\README.txt"
    echo - USB or Serial port connection >> "distribution\README.txt"
    echo - Optional: USB camera for photo capture >> "distribution\README.txt"
    echo - Optional: Big display for weight visualization >> "distribution\README.txt"
    echo. >> "distribution\README.txt"
    echo IMPORTANT NOTES: >> "distribution\README.txt"
    echo ---------------- >> "distribution\README.txt"
    echo - Ensure the scale is connected to the correct COM port >> "distribution\README.txt"
    echo - Configure the scale settings in the application >> "distribution\README.txt"
    echo - The application data is stored in: C:\ProgramData\Truck Scale >> "distribution\README.txt"
    echo - Database file: transactions.db >> "distribution\README.txt"
    echo - Configuration file: config.json >> "distribution\README.txt"
    echo - Log files: logs\app.log and logs\app_errors.log >> "distribution\README.txt"
    echo. >> "distribution\README.txt"
    echo TROUBLESHOOTING: >> "distribution\README.txt"
    echo --------------- >> "distribution\README.txt"
    echo - If the application doesn't start, run as Administrator >> "distribution\README.txt"
    echo - Check Windows Event Viewer for error details >> "distribution\README.txt"
    echo - Ensure all required Windows components are installed >> "distribution\README.txt"
    echo - Contact technical support for persistent issues >> "distribution\README.txt"
    echo. >> "distribution\README.txt"
    echo TECHNICAL SUPPORT: >> "distribution\README.txt"
    echo ------------------ >> "distribution\README.txt"
    echo Email: advantechnique@gmail.com >> "distribution\README.txt"
    echo Phone: [Your Phone Number] >> "distribution\README.txt"
    echo. >> "distribution\README.txt"
    echo VERSION INFORMATION: >> "distribution\README.txt"
    echo ------------------- >> "distribution\README.txt"
    echo Build Date: %date% %time% >> "distribution\README.txt"
    echo Builder: Automated Build Script >> "distribution\README.txt"
    echo Python Version: Built with Python 3.11 >> "distribution\README.txt"
    echo Dependencies: All dependencies bundled in executable >> "distribution\README.txt"
    
    echo [PASS] Comprehensive README.txt created
    
    REM Create installation batch file
    echo @echo off > "distribution\INSTALL.bat"
    echo echo Weighing Scale Application - Installation >> "distribution\INSTALL.bat"
    echo echo ========================================== >> "distribution\INSTALL.bat"
    echo echo. >> "distribution\INSTALL.bat"
    echo echo This will create necessary directories and set up the application. >> "distribution\INSTALL.bat"
    echo echo. >> "distribution\INSTALL.bat"
    echo pause >> "distribution\INSTALL.bat"
    echo echo Creating application data directory... >> "distribution\INSTALL.bat"
    echo if not exist "C:\ProgramData\Truck Scale" mkdir "C:\ProgramData\Truck Scale" >> "distribution\INSTALL.bat"
    echo echo Application data directory created successfully. >> "distribution\INSTALL.bat"
    echo echo. >> "distribution\INSTALL.bat"
    echo echo Installation complete! You can now run the application. >> "distribution\INSTALL.bat"
    echo echo. >> "distribution\INSTALL.bat"
    echo pause >> "distribution\INSTALL.bat"
    
    echo [PASS] Installation batch file created
    
    REM Create launcher batch files for each version
    if exist "distribution\%APP_NAME%.exe" (
        echo @echo off > "distribution\Run_Original.bat"
        echo echo Starting Weighing Scale Application (Original Version)... >> "distribution\Run_Original.bat"
        echo start "" "%APP_NAME%.exe" >> "distribution\Run_Original.bat"
        echo [PASS] Original version launcher created
    )
    
    if exist "distribution\%APP_NAME%_Refactored.exe" (
        echo @echo off > "distribution\Run_Refactored.bat"
        echo echo Starting Weighing Scale Application (Refactored Version)... >> "distribution\Run_Refactored.bat"
        echo start "" "%APP_NAME%_Refactored.exe" >> "distribution\Run_Refactored.bat"
        echo [PASS] Refactored version launcher created
    )
    
) else (
    echo [FAIL] Build failed, skipping post-build operations
)

REM ============================================================================
REM Final Summary
REM ============================================================================
echo.
echo ============================================================================ 
echo Build Process Summary
echo ============================================================================ 
echo Total Checks: !CHECKS_TOTAL!
echo Passed: !CHECKS_PASSED!
echo Failed: !CHECKS_FAILED!

if !BUILD_FAILED! equ 0 (
    echo.
    echo [SUCCESS] Build completed successfully!
    echo.
    echo DISTRIBUTION PACKAGE CREATED:
    echo ============================
    echo.
    echo Location: distribution\
    echo.
    echo EXECUTABLES:
    if exist "distribution\%APP_NAME%.exe" echo   - %APP_NAME%.exe ^(Original Version^)
    if exist "distribution\%APP_NAME%_Refactored.exe" echo   - %APP_NAME%_Refactored.exe ^(Refactored Version^)
    echo.
    echo LAUNCHERS:
    if exist "distribution\Run_Original.bat" echo   - Run_Original.bat ^(Launch Original Version^)
    if exist "distribution\Run_Refactored.bat" echo   - Run_Refactored.bat ^(Launch Refactored Version^)
    echo.
    echo DOCUMENTATION:
    if exist "distribution\README.txt" echo   - README.txt ^(Complete Installation Guide^)
    if exist "distribution\VERSION_ORIGINAL.txt" echo   - VERSION_ORIGINAL.txt ^(Original Version Info^)
    if exist "distribution\VERSION_REFACTORED.txt" echo   - VERSION_REFACTORED.txt ^(Refactored Version Info^)
    if exist "distribution\REFACTORING_README.md" echo   - REFACTORING_README.md ^(Architecture Documentation^)
    echo.
    echo UTILITIES:
    if exist "distribution\INSTALL.bat" echo   - INSTALL.bat ^(Setup Utility^)
    echo.
    echo ASSETS:
    if exist "distribution\assets" echo   - assets\ ^(Application Resources^)
    echo.
    echo PACKAGE SIZE:
    echo   - Check distribution folder size manually
    echo.
    echo READY FOR DISTRIBUTION!
    echo ========================
    echo.
    echo The complete distribution package is ready in the 'distribution' folder.
    echo This package contains:
    echo - Both versions of the application (Original and Refactored)
    echo - Complete documentation and installation guides
    echo - Launcher scripts for easy execution
    echo - All necessary assets and resources
    echo - Installation utilities
    echo.
    echo You can now distribute the entire 'distribution' folder to users.
    echo.
    echo NEXT STEPS:
    echo 1. Test both executables to ensure they work correctly
    echo 2. Verify all features are functioning as expected
    echo 3. Create installer package if desired (using tools like Inno Setup)
    echo 4. Distribute to end users
    echo.
) else (
    echo.
    echo [FAIL] Build process failed
    echo Please check the error messages above and resolve any issues
    echo Common issues:
    echo - Missing Python dependencies
    echo - Missing application files
    echo - Insufficient disk space
    echo - Antivirus software blocking the build
    echo.
    echo Troubleshooting:
    echo 1. Ensure all required Python packages are installed
    echo 2. Check that all application files are present
    echo 3. Run the script as Administrator
    echo 4. Temporarily disable antivirus software during build
    echo.
)

echo.
echo ============================================================================ 
echo Build Process Completed
echo ============================================================================ 

if !BUILD_FAILED! equ 0 (
    echo.
    echo [SUCCESS] Build completed successfully! Check the 'distribution' folder.
    echo.
    echo Quick Test Commands:
    if exist "distribution\Run_Original.bat" echo   - Test Original: distribution\Run_Original.bat
    if exist "distribution\Run_Refactored.bat" echo   - Test Refactored: distribution\Run_Refactored.bat
    echo.
)

pause
exit /b !BUILD_FAILED!
<arg_value><arg_key>EmptyFile</arg_key>
<arg_value>false
