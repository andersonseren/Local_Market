import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # ============================================================
    # BASE DE DATOS
    # ============================================================
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        if os.getenv('FLASK_ENV') == 'development':
            SQLALCHEMY_DATABASE_URI = 'sqlite:///local_market.db'
        else:
            raise ValueError("DATABASE_URL no está configurada. Debes establecer esta variable de entorno.")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ============================================================
    # JWT CONFIGURATION
    # ============================================================
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    
    # ============================================================
    # SESSION CONFIGURATION
    # ============================================================
    PERMANENT_SESSION_LIFETIME = 86400  # 24 horas
    SESSION_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'
    REMEMBER_COOKIE_HTTPONLY = True
    
    # ============================================================
    # MAIL CONFIGURATION (para recuperación de contraseña)
    # ============================================================
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
    MAIL_DEBUG = os.getenv('MAIL_DEBUG', 'False') == 'True'
    
    # ============================================================
    # FILE UPLOAD
    # ============================================================
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False  # Permitir HTTP en local


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Seleccionar configuración según el entorno
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Obtiene la configuración según el entorno"""
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, config_by_name['default'])