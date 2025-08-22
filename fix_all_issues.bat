@echo off
echo Исправляем все проблемы с зависимостями...
echo.
echo Удаляем проблемные пакеты...
pip uninstall flask flask-login flask-sqlalchemy sqlalchemy werkzeug openai -y
echo.
echo Устанавливаем совместимые версии для Python 3.13...
pip install Flask==2.2.5
pip install Flask-Login==0.6.2
pip install Flask-SQLAlchemy==3.0.2
pip install SQLAlchemy==1.4.53
pip install Werkzeug==2.2.3
pip install dashscope==1.14.0
pip install python-dotenv==1.0.0
pip install requests==2.31.0
pip install beautifulsoup4==4.12.2
pip install python-docx==0.8.11
pip install PyPDF2==3.0.1
echo.
echo Готово! Теперь можно запускать приложение.
pause
