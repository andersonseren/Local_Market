from app.extensions import db
from app.models.product import Product
from app.models.category import Category
from decimal import Decimal
from sqlalchemy import or_

def get_all_products(category_id=None, search_term=None):
    query = Product.query.filter(Product.stock > 0)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if search_term:
        query = query.filter(
            or_(
                Product.name.ilike(f'%{search_term}%'),
                Product.description.ilike(f'%{search_term}%')
            )
        )
    query = query.order_by(Product.name.asc())
    return query.all()

def get_products_paginated(page=1, per_page=12, category_id=None, search_term=None):
    query = Product.query.filter(Product.stock > 0)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if search_term:
        query = query.filter(
            or_(
                Product.name.ilike(f'%{search_term}%'),
                Product.description.ilike(f'%{search_term}%')
            )
        )
    query = query.order_by(Product.name.asc())
    return query.paginate(page=page, per_page=per_page, error_out=False)

def get_product_by_id(product_id):
    return Product.query.get(product_id)


def get_all_categories():
    return Category.query.all()

def create_product(name, description, price, stock, user_id, category_id=None, image_url=None):
    try:
        # Validaciones
        if not name or not name.strip():
            raise ValueError("El nombre del producto es obligatorio.")
        if price is None or price < 0:
            raise ValueError("El precio debe ser un número positivo.")
        if stock is None or stock < 0:
            raise ValueError("El stock debe ser un número positivo o cero.")
        product = Product(
            name=name.strip(),
            description=description.strip() if description else None,
            price=Decimal(str(price)),
            stock=stock,
            user_id=user_id,
            category_id=category_id,
            image_url=image_url
        )
        db.session.add(product)
        db.session.commit()
        return product
    except Exception as e:
        db.session.rollback()
        raise e

def update_product(product_id, name, description, price, stock, category_id=None, image_url=None):
    try:
        product = Product.query.get(product_id)
        if not product:
            raise ValueError("Producto no encontrado.")
        if not name or not name.strip():
            raise ValueError("El nombre del producto es obligatorio.")
        if price is None or price < 0:
            raise ValueError("El precio debe ser un número positivo.")
        if stock is None or stock < 0:
            raise ValueError("El stock debe ser un número positivo o cero.")
        product.name = name.strip()
        product.description = description.strip() if description else None
        product.price = Decimal(str(price))
        product.stock = stock
        product.category_id = category_id
        product.image_url = image_url
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e

def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        if product.order_details:
            raise ValueError("No se puede eliminar el producto porque tiene pedidos asociados.")
        db.session.delete(product)
        db.session.commit()
        return True
    return False

def get_products_by_user_paginated(user_id, page=1, per_page=10, category_id=None, low_stock=False):
    query = Product.query.filter_by(user_id=user_id)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if low_stock:
        query = query.filter(Product.stock < 5)
    query = query.order_by(Product.name.asc())
    return query.paginate(page=page, per_page=per_page, error_out=False)