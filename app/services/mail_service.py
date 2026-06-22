from flask import render_template, url_for
from flask_mail import Message
from app import mail
from app.models.user import User
from app.models.password_reset_token import PasswordResetToken
from flask import current_app

def send_reset_email(user, token):
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    msg = Message(
        subject='Recuperación de contraseña - Local Market',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email],
        html=render_template('email/reset_password.html', user=user, reset_url=reset_url)
    )
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error enviando correo: {e}")
        return False