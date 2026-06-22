from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.user import User
from app.models.password_reset_token import PasswordResetToken
from app.services.mail_service import send_reset_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('client.catalog'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        role = request.form.get('role', 'cliente')
        if role not in ('cliente', 'emprendedor'):
            role = 'cliente'
        
        # Validaciones básicas
        if User.query.filter_by(email=email).first():
            flash('El correo ya está registrado.', 'danger')
            return redirect(url_for('auth.register'))
        
        user = User(email=email, first_name=first_name, last_name=last_name, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Redirigir según rol
        if current_user.role == 'cliente':
            return redirect(url_for('client.catalog'))
        elif current_user.role == 'emprendedor':
            return redirect(url_for('entrepreneur.dashboard'))
        else:
            return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Tu cuenta está desactivada. Contacta al administrador.', 'danger')
                return redirect(url_for('auth.login'))
            login_user(user)
            # Redirigir según rol
            if user.role == 'cliente':
                return redirect(url_for('client.catalog'))
            elif user.role == 'emprendedor':
                return redirect(url_for('entrepreneur.dashboard'))
            else:
                return redirect(url_for('admin.dashboard'))
        else:
            flash('Credenciales incorrectas.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('auth.login'))


# ============================================================
# RECUPERACIÓN DE CONTRASEÑA (NUEVAS RUTAS)
# ============================================================

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Formulario para solicitar recuperación de contraseña."""
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generar token y enviar correo
            token = PasswordResetToken.create_token(user)
            send_reset_email(user, token)
            flash('Te hemos enviado un enlace de recuperación a tu correo.', 'success')
        else:
            # Por seguridad, no revelamos si el email existe o no
            flash('Si el email está registrado, recibirás un enlace de recuperación.', 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html')


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Formulario para nueva contraseña con token."""
    # Validar token
    reset_token = PasswordResetToken.validate_token(token)
    if not reset_token:
        flash('El enlace de recuperación es inválido o ha expirado.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    
    user = reset_token.user
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not password or len(password) < 4:
            flash('La contraseña debe tener al menos 4 caracteres.', 'danger')
        elif password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
        else:
            # Actualizar contraseña y marcar token como usado
            user.set_password(password)
            reset_token.mark_used()
            db.session.commit()
            
            flash('Contraseña actualizada exitosamente. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', token=token)