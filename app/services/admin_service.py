from app.extensions import db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.order_detail import OrderDetail   # ← Importante
from app.models.category import Category
from sqlalchemy import func, extract
from datetime import datetime

def get_dashboard_stats():
    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_sales = db.session.query(func.sum(Order.total)).filter(Order.status == 'completado').scalar() or 0
    users_by_role = db.session.query(User.role, func.count(User.id)).group_by(User.role).all()
    current_year = datetime.now().year
    sales_by_month = db.session.query(
        extract('month', Order.order_date).label('month'),
        func.sum(Order.total).label('total')
    ).filter(
        Order.status == 'completado',
        extract('year', Order.order_date) == current_year
    ).group_by('month').order_by('month').all()
    top_products = db.session.query(
        Product.name,
        func.sum(OrderDetail.quantity).label('total_sold')
    ).join(OrderDetail, Product.id == OrderDetail.product_id)\
     .join(Order, Order.id == OrderDetail.order_id)\
     .filter(Order.status == 'completado')\
     .group_by(Product.id)\
     .order_by(func.sum(OrderDetail.quantity).desc())\
     .limit(5).all()
    return {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_sales': total_sales,
        'users_by_role': dict(users_by_role),
        'sales_by_month': [(int(month), float(total)) for month, total in sales_by_month],
        'top_products': top_products
    }

def get_recent_activities(limit=10):
    recent_users = User.query.order_by(User.created_at.desc()).limit(limit).all()
    recent_orders = Order.query.order_by(Order.order_date.desc()).limit(limit).all()
    activities = []
    for user in recent_users:
        activities.append({'type': 'new_user', 'description': f'Nuevo usuario registrado: {user.email}', 'date': user.created_at})
    for order in recent_orders:
        activities.append({'type': 'new_order', 'description': f'Nuevo pedido #{order.id} por {order.customer.email} - Total {order.total}', 'date': order.order_date})
    activities.sort(key=lambda x: x['date'], reverse=True)
    return activities[:limit]

def get_orders_paginated(page=1, per_page=20, status=None, date_from=None, date_to=None, customer_email=None):
    query = Order.query
    if status:
        query = query.filter(Order.status == status)
    if date_from:
        query = query.filter(Order.order_date >= date_from)
    if date_to:
        query = query.filter(Order.order_date <= date_to)
    if customer_email:
        query = query.join(User).filter(User.email.ilike(f"%{customer_email}%"))
    query = query.order_by(Order.order_date.desc())
    return query.paginate(page=page, per_page=per_page, error_out=False)

def get_all_users_paginated(page=1, per_page=20, role=None, is_active=None):
    query = User.query
    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == (is_active == '1'))
    query = query.order_by(User.id.asc())
    return query.paginate(page=page, per_page=per_page, error_out=False)

def get_all_products_paginated(page=1, per_page=20, category_id=None, user_id=None, min_stock=None):
    query = Product.query
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if user_id:
        query = query.filter(Product.user_id == user_id)
    if min_stock is not None:
        query = query.filter(Product.stock >= min_stock)
    query = query.order_by(Product.name.asc())
    return query.paginate(page=page, per_page=per_page, error_out=False)

def get_all_categories_admin():
    return Category.query.all()

def create_category(name, description=None):
    if not name or not name.strip():
        raise ValueError("El nombre de la categoría es obligatorio.")
    if Category.query.filter_by(name=name.strip()).first():
        raise ValueError("Ya existe una categoría con ese nombre.")
    cat = Category(name=name.strip(), description=description.strip() if description else None)
    db.session.add(cat)
    db.session.commit()
    return cat

def update_category(category_id, name, description=None):
    cat = Category.query.get(category_id)
    if not cat:
        raise ValueError("Categoría no encontrada.")
    if not name or not name.strip():
        raise ValueError("El nombre de la categoría es obligatorio.")
    existing = Category.query.filter(Category.name == name.strip(), Category.id != category_id).first()
    if existing:
        raise ValueError("Ya existe otra categoría con ese nombre.")
    cat.name = name.strip()
    cat.description = description.strip() if description else None
    db.session.commit()
    return True

def delete_category(category_id):
    cat = Category.query.get(category_id)
    if not cat:
        raise ValueError("Categoría no encontrada.")
    if cat.products:
        raise ValueError("No se puede eliminar la categoría porque tiene productos asociados.")
    db.session.delete(cat)
    db.session.commit()
    return True