from app.extensions import db

class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(20), unique=True, nullable=False)
    issue_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    pdf_path = db.Column(db.String(255), nullable=True)
    
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, unique=True)