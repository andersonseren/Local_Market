from flask import Flask, redirect, url_for, render_template
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config import get_config
from app.extensions import db, login_manager
import os

# Inicializar extensiones a nivel de módulo
mail = Mail()  # <-- Objeto global

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(get_config())
    
    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    mail.init_app(app)  # <-- Inicializar Flask-Mail
    
    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.client import client_bp
    from app.routes.entrepreneur import entrepreneur_bp
    from app.routes.admin import admin_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(client_bp, url_prefix='/cliente')
    app.register_blueprint(entrepreneur_bp, url_prefix='/emprendedor')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp)

    # Filtro currency
    @app.template_filter('currency')
    def currency_filter(value):
        try:
            amount = float(value)
            return f"${amount:,.0f}".replace(",", ".")
        except (ValueError, TypeError):
            return f"${value}"

    # Context processor para carrito
    @app.context_processor
    def inject_cart_count():
        from flask import session
        cart = session.get('cart', {})
        total_items = sum(item.get('quantity', 0) for item in cart.values())
        return dict(cart_total_items=total_items)

    # ============================================================ #
    #  HOME PAGE ROUTE                                              #
    # ============================================================ #
    @app.route('/home')
    def home():
        from app.models.category import Category
        from app.models.product import Product
        from app.models.user import User
        from app.services.product_service import get_all_products
        
        categories = Category.query.all()
        featured_products = get_all_products()[:8]
        featured_entrepreneurs = User.query.filter_by(role='emprendedor').limit(4).all()
        
        # Colores para categorías (gradientes)
        category_colors = {
            'Electrónica': '#122474',
            'Ropa': '#e11d48',
            'Hogar': '#0d9488',
            'Deportes': '#f97316',
            'Libros': '#7c3aed',
            'Juguetes': '#f43f5e',
            'Cocina': '#f59e0b',
            'Belleza': '#db2777',
        }
        
        # Emojis para categorías (reemplazo de íconos problemáticos)
        category_emoji = {
            'Electrónica': '📱',
            'Ropa': '👕',
            'Hogar': '🏠',
            'Deportes': '⚽',
            'Libros': '📚',
            'Juguetes': '🎲',
            'Cocina': '🍳',
            'Belleza': '💄',
        }
        
        return render_template('home.html',
                               categories=categories,
                               featured_products=featured_products,
                               featured_entrepreneurs=featured_entrepreneurs,
                               category_colors=category_colors,
                               category_emoji=category_emoji)

    # Ruta raíz
    @app.route('/')
    def index():
        from flask_login import current_user
        if current_user.is_authenticated:
            if current_user.role == 'cliente':
                return redirect(url_for('client.catalog'))
            elif current_user.role == 'emprendedor':
                return redirect(url_for('entrepreneur.dashboard'))
            elif current_user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
        return redirect(url_for('home'))

    @app.route('/health')
    def health():
        return {'status': 'ok'}, 200

    @app.errorhandler(404)
    def page_not_found(e):
        return "Página no encontrada", 404

    @app.errorhandler(403)
    def forbidden(e):
        return "Acceso prohibido", 403

    return app

# Importar modelos y user_loader (deben estar después de la definición de create_app)
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.models.invoice import Invoice
from app.models.password_reset_token import PasswordResetToken

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))