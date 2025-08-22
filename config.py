import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # База данных - используем SQLite для простоты
    SQLALCHEMY_DATABASE_URI = 'sqlite:///resumai.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Qwen API (DashScope)
    DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY', '')
    
    # Настройки почты (опционально)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')

