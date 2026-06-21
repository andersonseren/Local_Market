from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

def role_required(*roles):
    """Decorador para restringir acceso por roles."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Debes iniciar sesión para acceder.', 'warning')
                return redirect(url_for('auth.login'))
            if current_user.role not in roles:
                abort(403)  # Prohibido
            return f(*args, **kwargs)
        return decorated_function
    return decorator