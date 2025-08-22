@echo off
title ResumAI Chatbot Launcher
color 0A

echo.
echo ========================================
echo    RESUMAI CHATBOT LAUNCHER
echo ========================================
echo.

echo Checking Python installation...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found! Installing dependencies...
py -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    echo.
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.
echo Starting ResumAI Chatbot...
echo The application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the application
echo.
echo ========================================
echo.

py run.py

echo.
echo Application stopped.
pause
