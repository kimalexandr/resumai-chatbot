#!/usr/bin/env python3
"""
Простой тест ResumAI Chatbot без OpenAI API
"""

from flask import Flask, request, jsonify
import os

# Создаем простое тестовое приложение
app = Flask(__name__)
app.secret_key = "test_secret_key"

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ResumAI Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .chat-box { border: 1px solid #ccc; padding: 20px; margin: 20px 0; }
            input[type="text"] { width: 70%; padding: 10px; }
            button { padding: 10px 20px; background: #007bff; color: white; border: none; }
        </style>
    </head>
    <body>
        <h1>🧪 ResumAI Chatbot - Test Mode</h1>
        <p>Это тестовая версия без OpenAI API. Протестируйте интерфейс чата.</p>
        
        <div class="chat-box" id="chat-box">
            <p><strong>AI:</strong> Привет! Я помогу вам создать резюме. Что вы хотите сделать?</p>
        </div>
        
        <div>
            <input type="text" id="user-input" placeholder="Введите сообщение..." />
            <button onclick="sendMessage()">Отправить</button>
        </div>
        
        <script>
            function sendMessage() {
                const input = document.getElementById('user-input');
                const message = input.value.trim();
                if (!message) return;
                
                const chatBox = document.getElementById('chat-box');
                chatBox.innerHTML += '<p><strong>Вы:</strong> ' + message + '</p>';
                
                // Простые ответы для тестирования
                let response = '';
                if (message.toLowerCase().includes('резюме')) {
                    response = 'Отлично! Давайте создадим резюме. Расскажите о вашем опыте работы.';
                } else if (message.toLowerCase().includes('опыт')) {
                    response = 'Сколько лет у вас опыта работы? В какой области?';
                } else if (message.toLowerCase().includes('навыки')) {
                    response = 'Какие у вас технические навыки? Например: Python, JavaScript, SQL?';
                } else {
                    response = 'Понятно! Расскажите больше о том, что вы хотите добавить в резюме.';
                }
                
                chatBox.innerHTML += '<p><strong>AI:</strong> ' + response + '</p>';
                input.value = '';
                chatBox.scrollTop = chatBox.scrollHeight;
            }
            
            // Enter для отправки
            document.getElementById('user-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>
    """

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    
    # Простые ответы для тестирования
    if "резюме" in message.lower():
        reply = "Отлично! Давайте создадим резюме. Расскажите о вашем опыте работы."
    elif "опыт" in message.lower():
        reply = "Сколько лет у вас опыта работы? В какой области?"
    elif "навыки" in message.lower():
        reply = "Какие у вас технические навыки? Например: Python, JavaScript, SQL?"
    else:
        reply = "Понятно! Расскажите больше о том, что вы хотите добавить в резюме."
    
    return jsonify({"reply": reply})

if __name__ == "__main__":
    print("🧪 Запуск тестовой версии ResumAI Chatbot...")
    print("🌐 Приложение доступно по адресу: http://localhost:5000")
    print("📝 Это тестовая версия без OpenAI API")
    print("⏹️  Нажмите Ctrl+C для остановки")
    print("-" * 50)
    
    app.run(debug=True, host="0.0.0.0", port=5000)
