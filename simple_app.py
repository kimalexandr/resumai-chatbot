from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, 
            template_folder='frontend',
            static_folder='static')

# Простая конфигурация
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['DASHSCOPE_API_KEY'] = os.getenv('DASHSCOPE_API_KEY', '')

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
        
        # Простой ответ без AI
        if message_type == 'vacancy':
            reply = f"Анализирую вакансию: {message}\n\nЭто тестовый ответ. Для полного анализа нужен DASHSCOPE_API_KEY."
        elif message_type == 'resume':
            reply = f"Анализирую резюме: {message[:100]}...\n\nЭто тестовый ответ. Для полного анализа нужен DASHSCOPE_API_KEY."
        else:
            reply = f"Получено сообщение: {message}\n\nЭто тестовый ответ. Для полного анализа нужен DASHSCOPE_API_KEY."
        
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
