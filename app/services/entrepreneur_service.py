from app.extensions import db
from app.models.user import User
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.models.product import Product
from sqlalchemy import func, extract
from datetime import datetime

def get_entrepreneur_orders_paginated(user_id, page=1, per_page=10, status=None, date_from=None, date_to=None):
    query = Order.query.join(OrderDetail).join(Product).filter(Product.user_id == user_id).distinct()
    if status:
        query = query.filter(Order.status == status)
    if date_from:
        query = query.filter(Order.order_date >= date_from)
    if date_to:
        query = query.filter(Order.order_date <= date_to)
    query = query.order_by(Order.order_date.desc())
    return query.paginate(page=page, per_page=per_page, error_out=False)

def get_entrepreneur_sales_by_month(user_id):
    current_year = datetime.now().year
    sales = db.session.query(
        extract('month', Order.order_date).label('month'),
        func.sum(OrderDetail.quantity * OrderDetail.unit_price).label('total')
    ).join(OrderDetail, Order.id == OrderDetail.order_id)\
     .join(Product, Product.id == OrderDetail.product_id)\
     .filter(Product.user_id == user_id, Order.status == 'completado',
             extract('year', Order.order_date) == current_year)\
     .group_by('month').order_by('month').all()
    return [(int(month), float(total)) for month, total in sales]

def get_low_stock_products(user_id, threshold=5):
    return Product.query.filter(Product.user_id == user_id, Product.stock < threshold).all()

def update_entrepreneur_profile(user, first_name, last_name, email, new_password=None):
    try:
        if not first_name or not first_name.strip():
            raise ValueError("El nombre es obligatorio.")
        if not last_name or not last_name.strip():
            raise ValueError("El apellido es obligatorio.")
        if not email or not email.strip():
            raise ValueError("El email es obligatorio.")
        user.first_name = first_name.strip()
        user.last_name = last_name.strip()
        if user.email != email:
            existing = User.query.filter_by(email=email).first()
            if existing and existing.id != user.id:
                raise ValueError("El email ya está en uso.")
            user.email = email.strip()
        if new_password:
            if len(new_password) < 4:
                raise ValueError("La contraseña debe tener al menos 4 caracteres.")
            user.set_password(new_password)
        db.session.commit()
        return True, "Perfil actualizado correctamente."
    except Exception as e:
        db.session.rollback()
        return False, str(e)