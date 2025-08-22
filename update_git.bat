@echo off
echo Updating Git repository...
echo.
echo Checking status...
git status
echo.
echo Adding all files...
git add .
echo.
echo Creating commit...
git commit -m "Update: OpenAI to Qwen, fix dependencies, simplified version"
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo Done! Repository updated.
pause
