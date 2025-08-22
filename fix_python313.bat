@echo off
echo Исправляем проблемы совместимости с Python 3.13...
echo.
echo Удаляем проблемные пакеты...
pip uninstall sqlalchemy flask-sqlalchemy -y
echo.
echo Устанавливаем совместимые версии...
pip install sqlalchemy==2.0.23
pip install flask-sqlalchemy==3.0.5
echo.
echo Готово! Теперь можно запускать приложение.
pause
