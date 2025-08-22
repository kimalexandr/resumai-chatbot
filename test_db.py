#!/usr/bin/env python3
"""
Тестовый скрипт для проверки базы данных и OTP
"""

import sqlite3
import os

def test_database():
    """Проверяем содержимое базы данных"""
    db_path = "resumai.db"
    
    if not os.path.exists(db_path):
        print("❌ База данных не найдена")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Проверка базы данных...")
        print("=" * 50)
        
        # Проверяем таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📋 Таблицы в базе: {[t[0] for t in tables]}")
        
        # Проверяем пользователей
        cursor.execute("SELECT * FROM user;")
        users = cursor.fetchall()
        print(f"\n👥 Пользователи ({len(users)}):")
        for user in users:
            print(f"  ID: {user[0]}, Email: {user[1]}, OTP: {user[2]}, Expires: {user[3]}, Created: {user[4]}")
        
        # Проверяем резюме
        cursor.execute("SELECT * FROM resume;")
        resumes = cursor.fetchall()
        print(f"\n📄 Резюме ({len(resumes)}):")
        for resume in resumes:
            print(f"  ID: {resume[0]}, User ID: {resume[1]}, Content: {resume[2][:50]}..., Link: {resume[3]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка при проверке базы: {e}")

if __name__ == "__main__":
    test_database()
