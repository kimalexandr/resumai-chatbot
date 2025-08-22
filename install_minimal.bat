@echo off
echo Устанавливаем минимальные зависимости для ResumAI...
echo.
echo Удаляем все старые пакеты...
pip uninstall -y flask flask-login flask-sqlalchemy sqlalchemy werkzeug openai dashscope
echo.
echo Устанавливаем только необходимые пакеты...
pip install Flask==2.2.5
pip install dashscope==1.14.0
pip install python-dotenv==1.0.0
pip install requests==2.31.0
echo.
echo Готово! Теперь можно запускать упрощенную версию.
pause
