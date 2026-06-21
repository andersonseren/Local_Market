from app import db
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.models.product import Product
from app.models.invoice import Invoice
from app.utils.helpers import generate_invoice_number
from decimal import Decimal

def create_order_from_cart(user_id, cart):
    """Crea un pedido a partir del carrito (sesión) y reduce stock."""
    order = Order(user_id=user_id, total=0, status='pendiente')
    db.session.add(order)
    db.session.flush()  # para obtener order.id
    
    total = Decimal('0')
    for product_id_str, item in cart.items():
        product_id = int(product_id_str)
        product = Product.query.get(product_id)
        if not product or product.stock < item['quantity']:
            db.session.rollback()
            return None
        quantity = item['quantity']
        unit_price = Decimal(str(item['price']))
        subtotal = unit_price * quantity
        detail = OrderDetail(
            order_id=order.id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            subtotal=subtotal
        )
        db.session.add(detail)
        total += subtotal
        # Reducir stock
        product.stock -= quantity
    
    order.total = total
    order.status = 'completado'
    db.session.commit()
    
    # Crear factura
    invoice_number = generate_invoice_number()
    invoice = Invoice(invoice_number=invoice_number, order_id=order.id)
    db.session.add(invoice)
    db.session.commit()
    
    return order

def get_user_orders(user_id):
    return Order.query.filter_by(user_id=user_id).order_by(Order.order_date.desc()).all()

def get_orders_for_entrepreneur(user_id):
    """Retorna todos los pedidos que contienen productos del emprendedor."""
    # Subconsulta: pedidos cuyos detalles tengan productos del usuario
    orders = Order.query.join(OrderDetail).join(Product).filter(Product.user_id == user_id).distinct().all()
    return orders