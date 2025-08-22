@echo off
title ResumAI Chatbot - Debug Mode
color 0E

echo.
echo ========================================
echo    RESUMAI CHATBOT LAUNCHER
echo    (Debug Mode - OTP Issues Fixed)
echo ========================================
echo.

echo Starting ResumAI Chatbot in DEBUG mode...
echo The application will be available at: http://localhost:5000
echo.
echo DEBUG FEATURES:
echo - OTP generation logging
echo - Verification logging
echo - Better error messages
echo - Console logging in browser
echo.
echo Press Ctrl+C to stop the application
echo ========================================
echo.

py run.py

echo.
echo Application stopped.
pause
