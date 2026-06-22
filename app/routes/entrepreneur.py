from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.utils.decorators import role_required
from app.services.product_service import get_products_by_user_paginated, create_product, update_product, delete_product, get_all_categories
from app.services.entrepreneur_service import (
    get_entrepreneur_orders_paginated, get_entrepreneur_sales_by_month,
    get_low_stock_products, update_entrepreneur_profile
)
from app.extensions import db
from app.models.product import Product
from collections import Counter
from datetime import datetime
from sqlalchemy import func

entrepreneur_bp = Blueprint('entrepreneur', __name__)


# ============================================================
# DASHBOARD
# ============================================================
@entrepreneur_bp.route('/dashboard')
@login_required
@role_required('emprendedor')
def dashboard():
    products = Product.query.filter_by(user_id=current_user.id).all()
    orders = get_entrepreneur_orders_paginated(current_user.id, page=1, per_page=100)
    total_ventas = sum(order.total for order in orders.items if order.status == 'completado')
    num_pedidos = orders.total
    product_counter = Counter()
    for order in orders.items:
        for detail in order.details:
            if detail.product.user_id == current_user.id:
                product_counter[detail.product.name] += detail.quantity
    top_products = product_counter.most_common(5)
    sales_by_month = get_entrepreneur_sales_by_month(current_user.id)
    low_stock = get_low_stock_products(current_user.id)
    return render_template('entrepreneur/dashboard.html',
                           products=products,
                           total_ventas=total_ventas,
                           num_pedidos=num_pedidos,
                           top_products=top_products,
                           sales_by_month=sales_by_month,
                           low_stock=low_stock)


# ============================================================
# LISTAR PRODUCTOS
# ============================================================
@entrepreneur_bp.route('/productos')
@login_required
@role_required('emprendedor')
def list_products():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    low_stock = str(request.args.get('low_stock', 'false')).lower() in ('1', 'true', 'yes')
    pagination = get_products_by_user_paginated(current_user.id, page=page, per_page=10,
                                                category_id=category_id, low_stock=low_stock)
    products = pagination.items
    categories = get_all_categories()
    return render_template('entrepreneur/products.html',
                           products=products,
                           pagination=pagination,
                           categories=categories,
                           selected_category=category_id,
                           low_stock=low_stock)


# ============================================================
# CREAR PRODUCTO
# ============================================================
@entrepreneur_bp.route('/producto/nuevo', methods=['GET', 'POST'])
@login_required
@role_required('emprendedor')
def create_product_view():
    categories = get_all_categories()
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            description = request.form.get('description')
            price = float(request.form.get('price'))
            stock = int(request.form.get('stock'))
            image_url = request.form.get('image_url')
            category_id = request.form.get('category_id')
            category_id = int(category_id) if category_id else None
            product = create_product(name, description, price, stock, current_user.id, category_id, image_url)
            flash('Producto creado exitosamente.', 'success')
            return redirect(url_for('entrepreneur.list_products'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('entrepreneur/product_form.html', product=None, categories=categories)


# ============================================================
# EDITAR PRODUCTO
# ============================================================
@entrepreneur_bp.route('/producto/editar/<int:product_id>', methods=['GET', 'POST'])
@login_required
@role_required('emprendedor')
def edit_product_view(product_id):
    product = Product.query.filter_by(id=product_id, user_id=current_user.id).first_or_404()
    categories = get_all_categories()
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            description = request.form.get('description')
            price = float(request.form.get('price'))
            stock = int(request.form.get('stock'))
            image_url = request.form.get('image_url')
            category_id = request.form.get('category_id')
            category_id = int(category_id) if category_id else None
            if update_product(product.id, name, description, price, stock, category_id, image_url):
                flash('Producto actualizado.', 'success')
                return redirect(url_for('entrepreneur.list_products'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('entrepreneur/product_form.html', product=product, categories=categories)


# ============================================================
# ELIMINAR PRODUCTO
# ============================================================
@entrepreneur_bp.route('/producto/eliminar/<int:product_id>')
@login_required
@role_required('emprendedor')
def delete_product_view(product_id):
    try:
        product = Product.query.filter_by(id=product_id, user_id=current_user.id).first_or_404()
        if delete_product(product.id):
            flash('Producto eliminado.', 'success')
        else:
            flash('No se pudo eliminar.', 'danger')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('entrepreneur.list_products'))


# ============================================================
# PEDIDOS RECIBIDOS
# ============================================================
@entrepreneur_bp.route('/pedidos')
@login_required
@role_required('emprendedor')
def orders():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    pagination = get_entrepreneur_orders_paginated(current_user.id, page=page, per_page=10,
                                                   status=status if status else None,
                                                   date_from=date_from if date_from else None,
                                                   date_to=date_to if date_to else None)
    orders = pagination.items
    return render_template('entrepreneur/orders.html',
                           orders=orders,
                           pagination=pagination,
                           current_status=status,
                           date_from=date_from,
                           date_to=date_to)


# ============================================================
# PERFIL DEL EMPRENDEDOR
# ============================================================
@entrepreneur_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
@role_required('emprendedor')
def profile():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        success, message = update_entrepreneur_profile(current_user, first_name, last_name, email, new_password)
        flash(message, 'success' if success else 'danger')
        if success:
            return redirect(url_for('entrepreneur.profile'))
    return render_template('entrepreneur/profile.html', user=current_user)


# ============================================================
# ESTADÍSTICAS (MEJORADO CON current_date)
# ============================================================
@entrepreneur_bp.route('/estadisticas')
@login_required
@role_required('emprendedor')
def statistics():
    orders_data = get_entrepreneur_orders_paginated(current_user.id, page=1, per_page=1000)
    orders = orders_data.items
    
    # Métricas básicas (convertir Decimal a float)
    total_ventas = float(sum(order.total for order in orders if order.status == 'completado'))
    num_pedidos = len([o for o in orders if o.status == 'completado'])
    ticket_promedio = float(total_ventas / num_pedidos) if num_pedidos > 0 else 0.0
    
    # Productos vendidos (contador)
    product_counter = Counter()
    product_revenue = {}
    for order in orders:
        if order.status == 'completado':
            for detail in order.details:
                if detail.product.user_id == current_user.id:
                    product_counter[detail.product.name] += detail.quantity
                    product_revenue[detail.product.name] = product_revenue.get(detail.product.name, 0.0) + float(detail.subtotal)
    
    total_productos_vendidos = sum(product_counter.values())
    
    # Productos más vendidos (top 10)
    top_products = product_counter.most_common(10)
    
    # Preparar datos para tabla de productos (todos los productos con ventas)
    product_table = []
    for name, qty in product_counter.items():
        product_table.append({
            'name': name,
            'quantity': qty,
            'revenue': product_revenue.get(name, 0.0)
        })
    product_table.sort(key=lambda x: x['quantity'], reverse=True)
    
    # Ventas mensuales (convertir Decimal a float)
    sales_by_month = [(mes, float(monto)) for mes, monto in get_entrepreneur_sales_by_month(current_user.id)]
    
    # Calcular crecimiento (comparativa mes actual vs mes anterior)
    growth = 0.0
    if len(sales_by_month) >= 2:
        current_month = sales_by_month[-1][1] if sales_by_month else 0.0
        previous_month = sales_by_month[-2][1] if len(sales_by_month) >= 2 else 0.0
        if previous_month > 0:
            growth = ((current_month - previous_month) / previous_month) * 100
    
    current_date = datetime.now()
    
    return render_template('entrepreneur/statistics.html',
                           total_ventas=total_ventas,
                           num_pedidos=num_pedidos,
                           ticket_promedio=ticket_promedio,
                           total_productos_vendidos=total_productos_vendidos,
                           top_products=top_products,
                           product_table=product_table,
                           sales_by_month=sales_by_month,
                           growth=growth,
                           current_date=current_date)