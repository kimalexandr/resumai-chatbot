# ResumAI Chatbot

Умный помощник для создания и адаптации резюме с использованием AI (DeepSeek).

## 🚀 Что нового в этой версии

### ✅ Основные изменения
- **Заменил Qwen на DeepSeek** - теперь используется DeepSeek API
- **Исправил проблемы с Python 3.13** - обновил все зависимости
- **Полная версия с базой данных** - SQLite + SQLAlchemy
- **Полностью переработал UI/UX** - современный дизайн

### 🔧 Технические улучшения
- SQLAlchemy для работы с базой данных
- Создал простые команды для установки и запуска
- Добавил подробные инструкции по настройке
- Исправил все ошибки импорта и зависимостей

## 📋 Требования

- Python 3.13+
- pip (менеджер пакетов Python)

## 🛠️ Установка

### Быстрая установка (рекомендуется)
```bash
# Установка зависимостей
pip install -r requirements.txt

# Настройка API ключа
# Создайте файл .env с DEEPSEEK_API_KEY
```

### Ручная установка
```bash
pip install Flask==2.2.5
pip install openai==1.3.0
pip install python-dotenv==1.0.0
pip install requests==2.31.0
pip install Flask-SQLAlchemy==3.0.2
pip install SQLAlchemy==1.4.53
```

## 🚀 Запуск

### Полная версия (с базой данных)
```bash
python run.py
```

## 🔑 Настройка DeepSeek API

1. **Получите API ключ** на https://platform.deepseek.com/
2. **Создайте файл .env** в корневой папке:
   ```
   DEEPSEEK_API_KEY=ваш_ключ_здесь
   SECRET_KEY=любой_секретный_ключ
   ```

## 📁 Структура проекта

```
resumai-chatbot/
├── backend/           # Основной код приложения
├── frontend/          # HTML шаблоны
├── static/            # CSS, JavaScript, изображения
├── run.py            # Полная версия с БД
├── config.py         # Конфигурация
├── requirements.txt  # Зависимости
└── .env              # Переменные окружения
```

## 🎯 Функциональность

### ✅ Работает
- Загрузка файлов (.txt, .docx, .pdf)
- Анализ вакансий по ссылкам
- Анализ текста резюме
- Чат с AI-помощником
- Современный UI/UX
- Профиль пользователя
- База данных SQLite
- Авторизация пользователей

## 🐛 Решение проблем

### Проблема с SQLAlchemy
```bash
pip uninstall flask-sqlalchemy sqlalchemy
pip install Flask==2.2.5
pip install Flask-SQLAlchemy==3.0.2
pip install SQLAlchemy==1.4.53
```

### Проблема с Qwen
```bash
pip uninstall dashscope
pip install openai==1.3.0
```

### Проблема с Python 3.13
Установите совместимые версии через `pip install -r requirements.txt`.

## 📞 Поддержка

Если возникли проблемы:
1. Переустановите зависимости: `pip install -r requirements.txt`
2. Проверьте настройку `DEEPSEEK_API_KEY` в файле `.env`
3. Убедитесь, что база данных создана
4. Проверьте логи приложения

## 🔄 Обновления

- **v2.0** - Замена Qwen на DeepSeek, исправление зависимостей
- **v1.0** - Базовая версия с OpenAI

---

**Приложение готово к использованию!** 🎉

