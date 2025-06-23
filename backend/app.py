from flask import Flask, request, jsonify, redirect, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import openai
import os
from bs4 import BeautifulSoup
import requests
import random
import string
from datetime import datetime, timedelta

# --- Инициализация Flask и базы данных ---
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///resumai.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_envvar('RESUMAI_SETTINGS', silent=True)

# --- Импорт моделей ---
from models import db, User, Resume

# --- Настройка базы ---
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Настройка OpenAI ---
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Настройка почты ---
from mailer import send_otp

with app.app_context():
    db.create_all()

# --- Генерация OTP ---
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

# --- Авторизация ---
@app.route("/login", methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        data = request.json
        email = data.get("email")

        if not email:
            return jsonify({"error": "Email не указан"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email)

        otp = generate_otp()
        user.otp_code = otp
        user.otp_expires_at = datetime.utcnow() + timedelta(minutes=5)
        db.session.add(user)
        db.session.commit()

        send_otp(email, otp)
        return jsonify({"success": True})

    return render_template("auth.html")

@app.route("/verify", methods=["POST"])
def verify_otp():
    data = request.json
    email = data.get("email")
    code = data.get("code")

    user = User.query.filter_by(email=email).first()
    if not user or user.otp_code != code or user.otp_expires_at < datetime.utcnow():
        return jsonify({"success": False, "error": "Неверный или истёкший код"})

    login_user(user)
    return jsonify({"success": True})

# --- Чат и резюме ---
@app.route("/")
@login_required
def home():
    return send_from_directory("frontend", "index.html")

@app.route("/api/chat", methods=["POST"])
@login_required
def chat():
    data = request.json
    message = data.get("message")

    # Если это ссылка на вакансию
    if "hh.ru/vacancy/" in message or "superjob.ru/vakansiya/" in message:
        vacancy_data = parse_hh_vacancy(message)
        prompt = open("backend/resume_prompt.txt", "r", encoding="utf-8").read()
        full_prompt = prompt.replace("{message}", f"""
Вы получили ссылку на вакансию:
Название: {vacancy_data['title']}
Описание: {vacancy_data['description'][:500]}
Требования: {', '.join(vacancy_data['requirements'])}

На основе этого адаптируйте текущее резюме так, чтобы оно соответствовало требованиям.
""")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": full_prompt}]
        )
        reply = response.choices[0].message.content

        new_resume = Resume(user_id=current_user.id, content=reply, vacancy_link=message)
        db.session.add(new_resume)
        db.session.commit()

        return jsonify({"reply": reply})

    # Обычный диалог
    prompt = open("backend/resume_prompt.txt", "r", encoding="utf-8").read()
    full_prompt = prompt.replace("{message}", message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": full_prompt}]
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

# --- Профиль ---
@app.route("/profile")
@login_required
def profile():
    return send_from_directory("frontend", "profile.html")

@app.route("/api/resumes", methods=["GET"])
@login_required
def get_resumes():
    from_date = request.args.get("from")
    to_date = request.args.get("to")
    vacancy = request.args.get("vacancy")

    query = Resume.query.filter_by(user_id=current_user.id)

    if from_date:
        from_dt = datetime.strptime(from_date, "%Y-%m-%d")
        query = query.filter(Resume.created_at >= from_dt)

    if to_date:
        to_dt = datetime.strptime(to_date, "%Y-%m-%d")
        query = query.filter(Resume.created_at <= to_dt)

    if vacancy:
        query = query.filter(Resume.vacancy_link.contains(vacancy))

    resumes = query.all()
    result = [
        {
            "id": r.id,
            "content": r.content,
            "vacancy_link": r.vacancy_link,
            "created_at": r.created_at.isoformat()
        } for r in resumes
    ]
    return jsonify(result)

# --- Парсинг HH.RU ---
def parse_hh_vacancy(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("h1", {"data-qa": "vacancy-title"})
    description = soup.find("div", {"data-qa": "vacancy-description"})
    requirements = [li.text.strip() for li in soup.select(".bloko-tag-list li")]
    return {
        "title": title.text.strip() if title else "",
        "description": description.text.strip() if description else "",
        "requirements": requirements
    }

# --- Выход ---
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)