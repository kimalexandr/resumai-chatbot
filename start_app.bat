@echo off
echo Starting ResumAI Chatbot...
echo.

REM Проверяем наличие Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Trying py command...
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Python is not installed or not in PATH.
        echo Please install Python from https://www.python.org/downloads/
        pause
        exit /b 1
    ) else (
        echo Python found. Installing dependencies...
        py -m pip install -r requirements.txt
        echo.
        echo Starting application...
        py run.py
    )
) else (
    echo Python found. Installing dependencies...
    python -m pip install -r requirements.txt
    echo.
    echo Starting application...
    python run.py
)

pause
