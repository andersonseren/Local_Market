from flask import Blueprint, render_template, redirect, url_for, flash, request, session, send_file, jsonify
from flask_login import login_required, current_user
from app.utils.decorators import role_required
from app.services.product_service import get_products_paginated, get_product_by_id, get_all_categories
from app.services.order_service import create_order_from_cart, get_user_orders
from app.services.pdf_service import generate_invoice_pdf
from app.extensions import db
from app.models.order import Order

client_bp = Blueprint('client', __name__)

def get_cart():
    return session.get('cart', {})

def save_cart(cart):
    session['cart'] = cart

@client_bp.route('/catalogo')
@login_required
@role_required('cliente')
def catalog():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search_term = request.args.get('search', '')
    pagination = get_products_paginated(page=page, per_page=12, category_id=category_id, search_term=search_term)
    products = pagination.items
    categories = get_all_categories()
    return render_template('client/catalog.html', products=products, pagination=pagination,
                           categories=categories, selected_category=category_id, search_term=search_term)

@client_bp.route('/producto/<int:product_id>')
@login_required
@role_required('cliente')
def product_detail(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('client.catalog'))
    return render_template('client/product_detail.html', product=product)

@client_bp.route('/agregar-carrito/<int:product_id>', methods=['POST'])
@login_required
@role_required('cliente')
def add_to_cart(product_id):
    product = get_product_by_id(product_id)
    if not product or product.stock <= 0:
        flash('Producto no disponible.', 'danger')
        return redirect(url_for('client.catalog'))
    quantity = int(request.form.get('quantity', 1))
    cart = get_cart()
    cart_item = cart.get(str(product_id))
    if cart_item:
        cart_item['quantity'] += quantity
    else:
        cart[str(product_id)] = {'name': product.name, 'price': float(product.price), 'quantity': quantity}
    save_cart(cart)
    flash('Producto agregado al carrito.', 'success')
    return redirect(url_for('client.catalog'))

@client_bp.route('/agregar-carrito-ajax/<int:product_id>', methods=['POST'])
@login_required
@role_required('cliente')
def add_to_cart_ajax(product_id):
    product = get_product_by_id(product_id)
    if not product or product.stock <= 0:
        return jsonify({'success': False, 'message': 'Producto no disponible.'})
    quantity = int(request.form.get('quantity', 1))
    cart = get_cart()
    cart_item = cart.get(str(product_id))
    if cart_item:
        cart_item['quantity'] += quantity
    else:
        cart[str(product_id)] = {'name': product.name, 'price': float(product.price), 'quantity': quantity}
    save_cart(cart)
    total_items = sum(item['quantity'] for item in cart.values())
    return jsonify({'success': True, 'message': 'Producto agregado al carrito.', 'total_items': total_items})

@client_bp.route('/carrito')
@login_required
@role_required('cliente')
def view_cart():
    cart = get_cart()
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('client/cart.html', cart=cart, total=total)

@client_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
@role_required('cliente')
def checkout():
    cart = get_cart()
    if not cart:
        flash('El carrito está vacío.', 'warning')
        return redirect(url_for('client.catalog'))
    if request.method == 'POST':
        try:
            order = create_order_from_cart(current_user.id, cart)
            if order:
                session.pop('cart', None)
                generate_invoice_pdf(order.id)
                flash('Compra realizada con éxito. Factura generada.', 'success')
                return redirect(url_for('client.order_detail', order_id=order.id))
            else:
                flash('Error al procesar la compra. Verifique stock.', 'danger')
                return redirect(url_for('client.view_cart'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error inesperado: {str(e)}', 'danger')
            return redirect(url_for('client.view_cart'))
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('client/checkout_form.html', cart=cart, total=total)

@client_bp.route('/pedido/<int:order_id>')
@login_required
@role_required('cliente')
def order_detail(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('client/order_detail.html', order=order)

@client_bp.route('/perfil')
@login_required
@role_required('cliente')
def profile():
    orders = get_user_orders(current_user.id)
    total_compras = sum(order.total for order in orders if order.status == 'completado')
    return render_template('client/profile.html', orders=orders, total_compras=total_compras)

@client_bp.route('/descargar-factura/<int:order_id>')
@login_required
@role_required('cliente')
def download_invoice(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    if not order.invoice or not order.invoice.pdf_path:
        flash('Factura no disponible.', 'danger')
        return redirect(url_for('client.order_detail', order_id=order.id))
    return send_file(order.invoice.pdf_path, as_attachment=True)