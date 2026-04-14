@echo off
REM AVAnA Setup Script - Android Vulnerability Analysis Framework
REM This script sets up the environment and starts the application on Windows

cls
echo.
echo ============================================================
echo   Android Vulnerability Static Analysis Framework (AVAnA)
echo                    Setup Script v1.0
echo ============================================================
echo.

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3 is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    pause
    exit /b 1
)

echo [✓] Python found

REM Check if venv exists
if not exist "venv" (
    echo [•] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [✗] Error creating virtual environment
        pause
        exit /b 1
    )
    echo [✓] Virtual environment created
) else (
    echo [✓] Virtual environment already exists
)

REM Activate venv
echo [•] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [✗] Error activating virtual environment
    pause
    exit /b 1
)
echo [✓] Virtual environment activated

REM Update pip
echo [•] Updating pip...
python -m pip install --upgrade pip >nul 2>&1
echo [✓] pip updated

REM Install requirements
echo [•] Installing dependencies from requirements.txt...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [✗] Error installing dependencies
        pause
        exit /b 1
    )
    echo [✓] All dependencies installed successfully
) else (
    echo [✗] requirements.txt not found
    pause
    exit /b 1
)

REM Create necessary directories
echo [•] Creating necessary directories...
if not exist "uploads" mkdir uploads
if not exist "logs" mkdir logs
echo [✓] Directories created

echo.
echo ============================================================
echo                  Setup Complete! [OK]
echo ============================================================
echo.
echo Next steps:
echo   1. Run the application: python run.py
echo   2. Open browser: http://localhost:5000
echo   3. Upload your APK to analyze
echo.
echo For more information, see:
echo   * README.md - Full documentation
echo   * QUICKSTART.md - Quick start guide
echo.

REM Optional: Start the application automatically
set /p answer="Would you like to start the application now? (y/n): "
if /i "%answer%"=="y" (
    echo Starting AVAnA...
    python run.py
) else (
    echo You can start the application later with: python run.py
    echo Remember to activate the virtual environment first:
    echo   call venv\Scripts\activate.bat
    pause
)
