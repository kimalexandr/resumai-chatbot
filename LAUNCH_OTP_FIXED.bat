@echo off
title ResumAI Chatbot - OTP Fixed
color 0A

echo.
echo ========================================
echo    RESUMAI CHATBOT LAUNCHER
echo    (OTP Fixed - 30 minutes validity)
echo ========================================
echo.

echo Starting ResumAI Chatbot...
echo The application will be available at: http://localhost:5000
echo.
echo OTP IMPROVEMENTS:
echo - Code valid for 30 minutes (was 5 minutes)
echo - Better error messages
echo - Code displayed on page
echo - New code button
echo.
echo Press Ctrl+C to stop the application
echo ========================================
echo.

py run.py

echo.
echo Application stopped.
pause
