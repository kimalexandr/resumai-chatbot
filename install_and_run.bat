@echo off
echo Installing dependencies...
py -m pip install -r requirements.txt
echo.
echo Starting ResumAI Chatbot...
py run.py
pause
