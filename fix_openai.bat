@echo off
echo Исправляем проблему с OpenAI...
echo.
echo Удаляем старую версию...
pip uninstall openai -y
echo.
echo Устанавливаем новую версию...
pip install openai --upgrade
echo.
echo Готово! Теперь можно запускать приложение.
pause
