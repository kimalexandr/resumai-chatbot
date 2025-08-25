from flask import Flask, render_template, request, jsonify
import os
import openai

app = Flask(__name__, 
            template_folder='frontend',
            static_folder='static')

# Простая конфигурация
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['DEEPSEEK_API_KEY'] = os.getenv('DEEPSEEK_API_KEY', '')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        message_type = data.get('type', 'chat')
        
        print(f"Получено сообщение: {message} (тип: {message_type})")
        
        # Проверяем наличие API ключа
        if not app.config['DEEPSEEK_API_KEY'] or app.config['DEEPSEEK_API_KEY'] == 'your_deepseek_api_key_here':
            reply = f"Анализирую: {message}\n\nЭто тестовый ответ. Для полного анализа нужен DEEPSEEK_API_KEY в файле .env"
        else:
            # Используем DeepSeek API
            try:
                client = openai.OpenAI(
                    api_key=app.config['DEEPSEEK_API_KEY'],
                    base_url="https://api.deepseek.com/v1"
                )
                
                if message_type == 'vacancy':
                    system_prompt = "Ты - эксперт по анализу вакансий. Проанализируй вакансию и дай рекомендации по адаптации резюме."
                elif message_type == 'resume':
                    system_prompt = "Ты - эксперт по составлению резюме. Проанализируй резюме и дай рекомендации по улучшению."
                else:
                    system_prompt = "Ты - помощник по карьере и резюме. Отвечай на вопросы пользователей."
                
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': message}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                
                reply = response.choices[0].message.content
                
            except Exception as e:
                error_msg = str(e)
                if "Insufficient Balance" in error_msg or "402" in error_msg:
                    reply = f"Анализирую: {message}\n\n⚠️ Недостаточно баланса на DeepSeek аккаунте.\n\nЭто тестовый ответ. Для полного анализа:\n1. Пополните баланс на https://platform.deepseek.com/\n2. Или используйте тестовый режим"
                else:
                    reply = f"Ошибка при обращении к DeepSeek API: {error_msg}"
        
        return jsonify({
            'success': True,
            'reply': reply
        })
        
    except Exception as e:
        print(f"Ошибка в чате: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'Файл не найден'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Файл не выбран'}), 400
        
        print(f"Загружен файл: {file.filename}")
        
        # Простой ответ без AI
        reply = f"Файл {file.filename} успешно загружен!\n\nЭто тестовый ответ. Для полного анализа нужен DASHSCOPE_API_KEY."
        
        return jsonify({
            'success': True,
            'reply': reply
        })
        
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/resumes')
def get_resumes():
    # Простые тестовые данные
    resumes = [
        {
            'id': 1,
            'title': 'Тестовое резюме 1',
            'content': 'Это тестовое резюме для демонстрации',
            'created_at': '2024-01-01',
            'vacancy': 'Тестовая вакансия'
        },
        {
            'id': 2,
            'title': 'Тестовое резюме 2',
            'content': 'Еще одно тестовое резюме',
            'created_at': '2024-01-02',
            'vacancy': 'Другая вакансия'
        }
    ]
    
    return jsonify({
        'success': True,
        'resumes': resumes
    })

if __name__ == '__main__':
    print("Запускаем упрощенную версию ResumAI...")
    print("Приложение будет доступно по адресу: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
