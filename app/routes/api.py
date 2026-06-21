from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.models.product import Product
from app.services.product_service import get_all_products, get_product_by_id

api_bp = Blueprint('api', __name__)

@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    role = data.get('role', 'cliente')
    
    if not all([email, password, first_name, last_name]):
        return jsonify({'error': 'Faltan campos obligatorios'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'El email ya está registrado'}), 409
    
    user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        role=role
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Usuario creado exitosamente', 'user_id': user.id}), 201

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Credenciales inválidas'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Usuario desactivado'}), 403
    
    access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role
        }
    }), 200

@api_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '')
    products = get_all_products(category_id=category_id, search_term=search)
    result = []
    for p in products:
        result.append({
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'price': float(p.price),
            'stock': p.stock,
            'image_url': p.image_url,
            'category_id': p.category_id,
            'category_name': p.category.name if p.category else None
        })
    return jsonify(result), 200

@api_bp.route('/products/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({'error': 'Producto no encontrado'}), 404
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': float(product.price),
        'stock': product.stock,
        'image_url': product.image_url,
        'category_id': product.category_id,
        'category_name': product.category.name if product.category else None
    }), 200

@api_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify({
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': user.role,
        'is_active': user.is_active,
        'created_at': user.created_at.isoformat() if user.created_at else None
    }), 200