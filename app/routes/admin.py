from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, Response
from flask_login import login_required, current_user
from app.utils.decorators import role_required
from app.extensions import db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.category import Category
from app.services.admin_service import (
    get_dashboard_stats, get_recent_activities,
    get_all_categories_admin, create_category, update_category, delete_category,
    get_orders_paginated, get_all_users_paginated, get_all_products_paginated
)
from app.services.report_service import (
    get_entrepreneurs_report_data, get_clients_report_data,
    export_to_csv, export_to_pdf
)
import csv
from io import StringIO
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

# ==================== DASHBOARD ====================
@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    stats = get_dashboard_stats()
    activities = get_recent_activities()
    return render_template('admin/dashboard.html', stats=stats, activities=activities)

# ==================== USUARIOS ====================
@admin_bp.route('/usuarios')
@login_required
@role_required('admin')
def users():
    page = request.args.get('page', 1, type=int)
    role_filter = request.args.get('role', '')
    active_filter = request.args.get('active', '')
    pagination = get_all_users_paginated(page=page, per_page=20,
                                         role=role_filter if role_filter else None,
                                         is_active=active_filter if active_filter else None)
    users = pagination.items
    return render_template('admin/users.html', users=users, pagination=pagination,
                           role_filter=role_filter, active_filter=active_filter)

@admin_bp.route('/usuario/editar/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        try:
            user.first_name = request.form.get('first_name').strip()
            user.last_name = request.form.get('last_name').strip()
            new_email = request.form.get('email').strip()
            if not new_email:
                raise ValueError("El email es obligatorio.")
            if user.email != new_email:
                if User.query.filter_by(email=new_email).first():
                    raise ValueError("El email ya está en uso.")
                user.email = new_email
            user.role = request.form.get('role')
            if request.form.get('password'):
                if len(request.form.get('password')) < 4:
                    raise ValueError("La contraseña debe tener al menos 4 caracteres.")
                user.set_password(request.form.get('password'))
            db.session.commit()
            flash('Usuario actualizado correctamente.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'danger')
        return redirect(url_for('admin.users'))
    return render_template('admin/user_form.html', user=user)

@admin_bp.route('/usuario/eliminar/<int:user_id>')
@login_required
@role_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('No puedes eliminarte a ti mismo.', 'danger')
        return redirect(url_for('admin.users'))
    if user.orders or user.products:
        flash('No se puede eliminar: el usuario tiene pedidos o productos asociados.', 'danger')
        return redirect(url_for('admin.users'))
    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/usuario/toggle/<int:user_id>')
@login_required
@role_required('admin')
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('No puedes desactivarte a ti mismo.', 'danger')
        return redirect(url_for('admin.users'))
    user.is_active = not user.is_active
    db.session.commit()
    status = 'activado' if user.is_active else 'desactivado'
    flash(f'Usuario {user.email} {status}.', 'success')
    return redirect(url_for('admin.users'))

# ==================== PRODUCTOS ====================
@admin_bp.route('/productos')
@login_required
@role_required('admin')
def products():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    user_id = request.args.get('user_id', type=int)
    min_stock = request.args.get('min_stock', type=int)
    pagination = get_all_products_paginated(page=page, per_page=20,
                                            category_id=category_id, user_id=user_id, min_stock=min_stock)
    products = pagination.items
    categories = Category.query.all()
    entrepreneurs = User.query.filter_by(role='emprendedor').all()
    return render_template('admin/products.html', products=products, pagination=pagination,
                           categories=categories, entrepreneurs=entrepreneurs,
                           selected_category=category_id, selected_user=user_id, min_stock=min_stock)

@admin_bp.route('/producto/editar/<int:product_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    categories = Category.query.all()
    if request.method == 'POST':
        try:
            product.name = request.form.get('name').strip()
            product.description = request.form.get('description').strip() if request.form.get('description') else None
            price = float(request.form.get('price'))
            if price < 0:
                raise ValueError("El precio no puede ser negativo.")
            product.price = price
            stock = int(request.form.get('stock'))
            if stock < 0:
                raise ValueError("El stock no puede ser negativo.")
            product.stock = stock
            product.image_url = request.form.get('image_url')
            category_id = request.form.get('category_id')
            product.category_id = int(category_id) if category_id else None
            db.session.commit()
            flash('Producto actualizado.', 'success')
            return redirect(url_for('admin.products'))
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'danger')
    return render_template('admin/product_form.html', product=product, categories=categories)

@admin_bp.route('/producto/eliminar/<int:product_id>')
@login_required
@role_required('admin')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        db.session.delete(product)
        db.session.commit()
        flash('Producto eliminado.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'danger')
    return redirect(url_for('admin.products'))

# ==================== PEDIDOS ====================
@admin_bp.route('/pedidos')
@login_required
@role_required('admin')
def orders():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    customer_email = request.args.get('customer_email', '')
    pagination = get_orders_paginated(page=page, per_page=20,
                                      status=status if status else None,
                                      date_from=date_from if date_from else None,
                                      date_to=date_to if date_to else None,
                                      customer_email=customer_email if customer_email else None)
    orders = pagination.items
    return render_template('admin/orders.html', orders=orders, pagination=pagination,
                           current_status=status, date_from=date_from, date_to=date_to, customer_email=customer_email)

@admin_bp.route('/pedido/cambiar-estado/<int:order_id>', methods=['POST'])
@login_required
@role_required('admin')
def change_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    if new_status in ['pendiente', 'completado', 'cancelado']:
        order.status = new_status
        db.session.commit()
        flash(f'Estado del pedido #{order.id} cambiado a {new_status}.', 'success')
    else:
        flash('Estado inválido.', 'danger')
    return redirect(url_for('admin.orders'))

# ==================== CATEGORÍAS ====================
@admin_bp.route('/categorias')
@login_required
@role_required('admin')
def categories():
    categories = get_all_categories_admin()
    return render_template('admin/categories.html', categories=categories)

@admin_bp.route('/categoria/nueva', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def create_category_view():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        try:
            cat = create_category(name, description)
            flash('Categoría creada exitosamente.', 'success')
            return redirect(url_for('admin.categories'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('admin/category_form.html', category=None)

@admin_bp.route('/categoria/editar/<int:category_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_category_view(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        try:
            update_category(category.id, name, description)
            flash('Categoría actualizada.', 'success')
            return redirect(url_for('admin.categories'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('admin/category_form.html', category=category)

@admin_bp.route('/categoria/eliminar/<int:category_id>')
@login_required
@role_required('admin')
def delete_category_view(category_id):
    try:
        delete_category(category_id)
        flash('Categoría eliminada.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('admin.categories'))

# ==================== REPORTES ====================
@admin_bp.route('/reportes/emprendedores')
@login_required
@role_required('admin')
def report_entrepreneurs():
    data = get_entrepreneurs_report_data()
    return render_template('admin/report_entrepreneurs.html', data=data)

@admin_bp.route('/reportes/clientes')
@login_required
@role_required('admin')
def report_clients():
    data = get_clients_report_data()
    return render_template('admin/report_clients.html', data=data)

@admin_bp.route('/reportes/exportar/<tipo>/<formato>')
@login_required
@role_required('admin')
def export_report(tipo, formato):
    if tipo == 'emprendedores':
        data = get_entrepreneurs_report_data()
        headers = ['id', 'email', 'full_name', 'created_at', 'total_products', 'total_sales', 'top_product']
        title = "Reporte de Emprendedores"
        filename = f"emprendedores_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    elif tipo == 'clientes':
        data = get_clients_report_data()
        headers = ['id', 'email', 'full_name', 'created_at', 'total_purchases', 'total_spent']
        title = "Reporte de Clientes"
        filename = f"clientes_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    else:
        flash('Tipo de reporte inválido.', 'danger')
        return redirect(url_for('admin.dashboard'))
    if formato == 'csv':
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        for row in data:
            row_copy = {k: v.strftime('%Y-%m-%d %H:%M') if hasattr(v, 'strftime') else v for k, v in row.items()}
            writer.writerow(row_copy)
        response = Response(output.getvalue(), mimetype='text/csv')
        response.headers['Content-Disposition'] = f'attachment; filename={filename}.csv'
        return response
    elif formato == 'pdf':
        pdf_data = []
        for row in data:
            row_copy = {k: v.strftime('%Y-%m-%d') if hasattr(v, 'strftime') else v for k, v in row.items()}
            pdf_data.append(row_copy)
        filepath = export_to_pdf(pdf_data, headers, title, f"{filename}.pdf")
        return send_file(filepath, as_attachment=True)
    else:
        flash('Formato no soportado.', 'danger')
        return redirect(url_for('admin.dashboard'))