@echo off
echo Полная переустановка всех зависимостей для Python 3.13...
echo.
echo Удаляем все старые пакеты...
pip uninstall -r requirements.txt -y
pip uninstall flask flask-login flask-sqlalchemy sqlalchemy werkzeug -y
echo.
echo Устанавливаем совместимые версии...
pip install -r requirements.txt
echo.
echo Готово! Теперь можно запускать приложение.
pause
