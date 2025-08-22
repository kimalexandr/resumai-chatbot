@echo off
echo Переустанавливаем все зависимости...
echo.
echo Удаляем старые пакеты...
pip uninstall -r requirements.txt -y
echo.
echo Устанавливаем новые пакеты...
pip install -r requirements.txt
echo.
echo Готово! Теперь можно запускать приложение.
pause
