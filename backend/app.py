from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import secrets
import re
from .models import db, User, Resume
from .mailer import send_otp_email
from dashscope import Generation

app = Flask(__name__, 
            template_folder='../frontend',
            static_folder='../static')
app.config.from_object('config.Config')

# Инициализация расширений
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Создание таблиц
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"success": True, "message": "Вы успешно вышли из системы"})

@app.route('/api/send-otp', methods=['POST'])
def send_otp():
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({"success": False, "error": "Email не указан"}), 400
        
        # Проверяем, существует ли пользователь
        user = User.query.filter_by(email=email).first()
        if not user:
            # Создаем нового пользователя
            user = User(email=email)
            db.session.add(user)
        
        # Генерируем OTP
        otp = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
        user.otp = otp
        user.otp_expires_at = datetime.now() + timedelta(days=36500)  # 100 лет для тестирования
        db.session.commit()
        
        # Отправляем OTP по email или возвращаем для тестирования
        if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
            send_otp_email(email, otp)
            return jsonify({"success": True, "message": "OTP отправлен на ваш email"})
        else:
            return jsonify({"success": True, "message": "OTP отправлен на ваш email", "otp": otp})
            
    except Exception as e:
        print(f"Ошибка отправки OTP: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/verify-otp', methods=['POST'])
def verify_otp():
    try:
        data = request.get_json()
        email = data.get('email')
        otp = data.get('otp')
        
        print(f"Проверяем OTP для {email}: {otp}")
        
        if not email or not otp:
            return jsonify({"success": False, "error": "Email и OTP обязательны"}), 400
        
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f"Пользователь не найден: {email}")
            return jsonify({"success": False, "error": "Пользователь не найден"}), 404
        
        print(f"Найден пользователь: {user.email}, OTP в БД: {user.otp}")
        
        # Проверяем OTP
        if str(user.otp).strip() == str(otp).strip():
            print("OTP совпадает!")
            # Закомментировано для "вечного" OTP
            # if user.otp_expires_at and datetime.now() > user.otp_expires_at:
            #     return jsonify({"success": False, "error": "OTP истек"}), 400
            
            login_user(user)
            return jsonify({"success": True, "message": "Успешная авторизация"})
        else:
            print(f"OTP не совпадает: '{user.otp}' != '{otp}'")
            return jsonify({"success": False, "error": "Неверный OTP"}), 400
            
    except Exception as e:
        print(f"Ошибка проверки OTP: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

def generate_ai_response(prompt, message_type="chat"):
    """Генерирует ответ с помощью Qwen"""
    try:
        if not app.config.get('DASHSCOPE_API_KEY'):
            print("DASHSCOPE_API_KEY не настроен")
            return "API ключ для Qwen не настроен. Пожалуйста, настройте DASHSCOPE_API_KEY в переменных окружения."
        
        # Настраиваем API ключ
        os.environ['DASHSCOPE_API_KEY'] = app.config['DASHSCOPE_API_KEY']
        
        # Формируем промпт в зависимости от типа сообщения
        if message_type == "vacancy":
            system_prompt = "Ты - эксперт по анализу вакансий. Проанализируй вакансию и дай рекомендации по адаптации резюме."
        elif message_type == "resume":
            system_prompt = "Ты - эксперт по составлению резюме. Проанализируй резюме и дай рекомендации по улучшению."
        else:
            system_prompt = "Ты - помощник по карьере и резюме. Отвечай на вопросы пользователей."
        
        # Вызываем Qwen API
        response = Generation.call(
            model='qwen-turbo',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ],
            result_format='message',
            max_tokens=1500,
            temperature=0.7
        )
        
        if response.status_code == 200:
            return response.output.choices[0].message.content
        else:
            print(f"Ошибка Qwen API: {response.message}")
            return f"Ошибка при обращении к AI: {response.message}"
            
    except Exception as e:
        print(f"Ошибка при генерации ответа: {e}")
        return f"Произошла ошибка при обработке запроса: {str(e)}"

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        message_type = data.get('type', 'chat')
        
        print(f"Получено сообщение: {message} (тип: {message_type})")
        
        if not message:
            return jsonify({"success": False, "error": "Сообщение не может быть пустым"}), 400
        
        # Генерируем ответ с помощью AI
        ai_reply = generate_ai_response(message, message_type)
        
        # Сохраняем в базу данных, если пользователь авторизован
        if current_user.is_authenticated and message_type in ['vacancy', 'resume']:
            try:
                resume = Resume(
                    user_id=current_user.id,
                    content=message[:500],  # Первые 500 символов
                    vacancy_link=message if message_type == 'vacancy' else None,
                    created_at=datetime.now()
                )
                db.session.add(resume)
                db.session.commit()
                print(f"Резюме сохранено в БД, ID: {resume.id}")
            except Exception as e:
                print(f"Ошибка сохранения в БД: {e}")
                db.session.rollback()
        
        return jsonify({
            "success": True,
            "reply": ai_reply
        })
        
    except Exception as e:
        print(f"Ошибка в чате: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "Файл не найден"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "Файл не выбран"}), 400
        
        print(f"Загружен файл: {file.filename}")
        
        # Читаем содержимое файла
        content = ""
        if file.filename.endswith('.txt'):
            content = file.read().decode('utf-8')
        elif file.filename.endswith('.docx'):
            # Для docx файлов возвращаем заглушку
            content = f"[Содержимое файла {file.filename} - для полного анализа нужен python-docx]"
        elif file.filename.endswith('.pdf'):
            # Для pdf файлов возвращаем заглушку
            content = f"[Содержимое файла {file.filename} - для полного анализа нужен PyPDF2]"
        
        print(f"Содержимое файла: {content[:100]}...")
        
        # Анализируем содержимое с помощью AI
        ai_reply = generate_ai_response(content, "resume")
        
        # Сохраняем в базу данных, если пользователь авторизован
        if current_user.is_authenticated:
            try:
                resume = Resume(
                    user_id=current_user.id,
                    content=content[:500],  # Первые 500 символов
                    vacancy_link=None,
                    created_at=datetime.now()
                )
                db.session.add(resume)
                db.session.commit()
                print(f"Резюме из файла сохранено в БД, ID: {resume.id}")
            except Exception as e:
                print(f"Ошибка сохранения файла в БД: {e}")
                db.session.rollback()
        
        return jsonify({
            "success": True,
            "reply": ai_reply
        })
        
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/resumes')
@login_required
def get_resumes():
    try:
        resumes = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.created_at.desc()).all()
        resume_list = []
        
        for resume in resumes:
            resume_list.append({
                'id': resume.id,
                'content': resume.content,
                'vacancy_link': resume.vacancy_link,
                'created_at': resume.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({
            "success": True,
            "resumes": resume_list
        })
        
    except Exception as e:
        print(f"Ошибка получения резюме: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/api/resumes/<int:resume_id>", methods=["DELETE"])
@login_required
def delete_resume(resume_id):
    try:
        resume = Resume.query.filter_by(id=resume_id, user_id=current_user.id).first()
        if not resume:
            return jsonify({"success": False, "error": "Резюме не найдено"}), 404
        db.session.delete(resume)
        db.session.commit()
        return jsonify({"success": True, "message": "Резюме успешно удалено"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": f"Ошибка удаления: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)