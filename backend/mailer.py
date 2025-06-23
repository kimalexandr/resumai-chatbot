import smtplib
from email.mime.text import MIMEText
from flask import current_app

def send_otp(email, code):
    msg = MIMEText(f"Ваш код для входа в ResumAI: {code}")
    msg['Subject'] = "Код входа в ResumAI"
    msg['From'] = current_app.config['MAIL_USERNAME']
    msg['To'] = email

    with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
        server.starttls()
        server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
        server.sendmail(msg['From'], [msg['To']], msg.as_string())