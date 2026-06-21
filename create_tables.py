from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.models.invoice import Invoice

app = create_app()
with app.app_context():
    # 1. Crear todas las tablas
    db.create_all()
    print("Tablas creadas exitosamente.")

    # 2. Insertar categorías iniciales si no existen
    categorias_iniciales = [
        ('Electrónica', 'Productos electrónicos como celulares, computadoras, etc.'),
        ('Ropa', 'Prendas de vestir para hombre, mujer y niños'),
        ('Hogar', 'Muebles, decoración y artículos para el hogar'),
        ('Deportes', 'Equipamiento deportivo y accesorios'),
        ('Cocina', 'Utensilios, electrodomésticos y accesorios de cocina'),
        ('Juguetes', 'Juguetes y juegos para niños')
    ]

    categorias_creadas = 0
    for nombre, descripcion in categorias_iniciales:
        if not Category.query.filter_by(name=nombre).first():
            db.session.add(Category(name=nombre, description=descripcion))
            categorias_creadas += 1

    db.session.commit()
    print(f"{categorias_creadas} categorías insertadas.")

    # 3. Opcional: Crear un usuario administrador por defecto si no existe
    admin_email = "admin@localmarket.com"
    if not User.query.filter_by(email=admin_email).first():
        admin = User(
            email=admin_email,
            first_name="Admin",
            last_name="Local",
            role="admin",
            is_active=True
        )
        admin.set_password("admin123")  # Contraseña por defecto, cámbiala después
        db.session.add(admin)
        db.session.commit()
        print("Usuario administrador creado (email: admin@localmarket.com / pass: admin123).")
    else:
        print("El usuario administrador ya existe.")

    print("\n Base de datos lista para usar.")