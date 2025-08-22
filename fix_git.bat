@echo off
echo Fixing Git issues...
echo.
echo Setting up Git user...
git config --global user.email "kimalexandr@gmail.com"
git config --global user.name "kimalexandr"
echo.
echo Checking current branch...
git branch
echo.
echo Creating main branch if it doesn't exist...
git checkout -b main
echo.
echo Adding all files...
git add .
echo.
echo Creating commit...
git commit -m "Update: OpenAI to Qwen, fix dependencies, simplified version"
echo.
echo Pushing to GitHub...
git push -u origin main
echo.
echo Done! Git issues fixed.
pause
