#!/usr/bin/env python3
"""
Скрипт для установки зависимостей и запуска ResumAI Chatbot
"""

import subprocess
import sys
import os

def run_command(command):
    """Выполняет команду и выводит результат"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {command}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при выполнении: {command}")
        if e.stderr:
            print(f"Ошибка: {e.stderr}")
        return False

def main():
    print("🚀 Установка и запуск ResumAI Chatbot")
    print("=" * 50)
    
    # Проверяем наличие pip
    print("📦 Проверка pip...")
    if not run_command("py -m pip --version"):
        print("❌ pip не найден. Установите Python с pip.")
        return
    
    # Устанавливаем зависимости
    print("\n📥 Установка зависимостей...")
    if not run_command("py -m pip install -r requirements.txt"):
        print("❌ Ошибка при установке зависимостей.")
        return
    
    print("\n✅ Зависимости установлены!")
    
    # Запускаем приложение
    print("\n🚀 Запуск приложения...")
    print("Приложение будет доступно по адресу: http://localhost:5000")
    print("Нажмите Ctrl+C для остановки")
    print("-" * 50)
    
    try:
        subprocess.run(["py", "run.py"], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Приложение остановлено пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка при запуске: {e}")

if __name__ == "__main__":
    main()
