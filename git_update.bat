@echo off
echo Обновляем Git репозиторий...
echo.
echo Проверяем статус...
git status
echo.
echo Добавляем все файлы...
git add .
echo.
echo Создаем коммит...
git commit -m "Обновление: замена OpenAI на Qwen, исправление зависимостей, упрощенная версия"
echo.
echo Отправляем изменения на GitHub...
git push origin main
echo.
echo Готово! Репозиторий обновлен.
pause
