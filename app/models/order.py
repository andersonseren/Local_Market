from app.extensions import db

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.Enum('pendiente', 'completado', 'cancelado', name='order_status'), default='pendiente')
    total = db.Column(db.Numeric(10, 2), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    details = db.relationship('OrderDetail', backref='order', lazy=True, cascade='all, delete-orphan')
    invoice = db.relationship('Invoice', backref='order', uselist=False, lazy=True)