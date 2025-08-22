#!/usr/bin/env python3
"""
Простой скрипт для тестирования ResumAI Chatbot
"""

import requests
import json
import time

def test_app():
    base_url = "http://localhost:5000"
    
    print("🧪 Тестирование ResumAI Chatbot...")
    print("=" * 50)
    
    # Тест 1: Проверка доступности главной страницы
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Главная страница доступна")
        else:
            print(f"❌ Главная страница недоступна: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к серверу")
        print("   Убедитесь, что приложение запущено: python run.py")
        return
    
    # Тест 2: Проверка страницы авторизации
    try:
        response = requests.get(f"{base_url}/login")
        if response.status_code == 200:
            print("✅ Страница авторизации доступна")
        else:
            print(f"❌ Страница авторизации недоступна: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка при проверке авторизации: {e}")
    
    # Тест 3: Проверка API чата (должен требовать авторизацию)
    try:
        response = requests.post(f"{base_url}/api/chat", 
                               json={"message": "Тестовое сообщение"})
        if response.status_code == 401 or response.status_code == 302:
            print("✅ API чата защищен авторизацией")
        else:
            print(f"⚠️  API чата вернул неожиданный статус: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка при проверке API чата: {e}")
    
    # Тест 4: Проверка профиля
    try:
        response = requests.get(f"{base_url}/profile")
        if response.status_code == 401 or response.status_code == 302:
            print("✅ Профиль защищен авторизацией")
        else:
            print(f"⚠️  Профиль вернул неожиданный статус: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка при проверке профиля: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Для полного тестирования:")
    print("1. Откройте http://localhost:5000 в браузере")
    print("2. Войдите с любым email")
    print("3. Протестируйте чат и создание резюме")
    print("4. Попробуйте вставить ссылку на вакансию с HH.ru")

if __name__ == "__main__":
    test_app()

