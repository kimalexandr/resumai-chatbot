@echo off
echo Устанавливаем зависимости для DeepSeek...
echo.
echo Удаляем старые пакеты...
pip uninstall dashscope openai httpx -y
echo.
echo Устанавливаем совместимые версии...
pip install httpx==0.24.1
pip install openai==1.3.0
pip install -r requirements.txt
echo.
echo Готово! Теперь можно запускать приложение с DeepSeek.
echo.
echo Не забудьте настроить DEEPSEEK_API_KEY в файле .env
pause
