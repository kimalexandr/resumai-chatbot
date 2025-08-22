@echo off
echo Checking if ResumAI Chatbot is running...
netstat -an | findstr :5000
if %errorlevel% equ 0 (
    echo App is running on port 5000
) else (
    echo App is NOT running on port 5000
)
pause
