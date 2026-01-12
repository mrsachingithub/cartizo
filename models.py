from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'refundguard_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))

    role = db.Column(db.String(20), default='customer')  # 'admin' or 'customer'
    risk_score = db.Column(db.Integer, default=0)
    is_blocked = db.Column(db.Boolean, default=False)
    mobile = db.Column(db.String(15))
    is_flagged = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship('Order', backref='user', lazy=True)
    return_requests = db.relationship('ReturnRequest', backref='user', lazy=True)

class Product(db.Model):
    __tablename__ = 'refundguard_product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), default='https://via.placeholder.com/300')
    description = db.Column(db.Text)

class Order(db.Model):
    __tablename__ = 'refundguard_order'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('refundguard_user.id'), nullable=False)

    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False)
    # Keeping items for backward compatibility if needed, but we will use order_items relationship
    items = db.Column(db.Text, nullable=True) 
    status = db.Column(db.String(20), default='delivered') # delivered, returned, partially_returned
    payment_method = db.Column(db.String(20), default='PREPAID')

    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    return_requests = db.relationship('ReturnRequest', backref='order', lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'refundguard_order_item'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('refundguard_order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('refundguard_product.id'), nullable=False)

    quantity = db.Column(db.Integer, default=1)
    price_at_purchase = db.Column(db.Float, nullable=False)

    product = db.relationship('Product')

class ReturnRequest(db.Model):
    __tablename__ = 'refundguard_return_request'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('refundguard_user.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('refundguard_order.id'), nullable=False)

    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending') # pending, approved, rejected
    reason = db.Column(db.String(200))
    description = db.Column(db.Text) # New field for detailed problem description
    refund_amount = db.Column(db.Float, nullable=False)
    risk_report = db.Column(db.Text) # JSON or formatted string report

class RefundParams(db.Model):
    __tablename__ = 'refundguard_refund_params'

    id = db.Column(db.Integer, primary_key=True)
    param_name = db.Column(db.String(50), unique=True, nullable=False)
    param_value = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))

# Default Risk Parameters (can be seeded)
# MAX_RETURNS_PER_MONTH = 3
# HIGH_VALUE_THRESHOLD = 500
