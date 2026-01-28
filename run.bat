@echo off
REM ========================================
REM HCI Application - Quick Run Script
REM ========================================

echo Starting HCI Controller...

REM Check for executable first
if exist "dist\HCI_Controller.exe" (
    echo Running from executable...
    start "" "dist\HCI_Controller.exe"
    exit /b 0
)

REM Fall back to Python
if exist "venv\Scripts\python.exe" (
    echo Running from Python...
    call venv\Scripts\activate.bat
    python launcher.py
) else (
    echo ERROR: Neither executable nor virtual environment found!
    echo.
    echo Options:
    echo   1. Run build.bat to create executable
    echo   2. Run: python -m venv venv ^&^& venv\Scripts\pip install -r requirements.txt
    pause
)
