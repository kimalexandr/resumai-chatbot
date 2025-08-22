@echo off
echo Устанавливаем зависимости для Qwen...
echo.
echo Удаляем старые пакеты...
pip uninstall openai -y
echo.
echo Устанавливаем новые пакеты...
pip install dashscope==1.14.0
pip install -r requirements.txt
echo.
echo Готово! Теперь можно запускать приложение с Qwen.
pause
