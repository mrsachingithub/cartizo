from app import create_app, db
from models import User, Order
from werkzeug.security import generate_password_hash
from datetime import datetime
import os


app = create_app()

with app.app_context():
    db.create_all()
    
    # Check if admin exists
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@refundguard.com',
            password_hash=generate_password_hash(os.getenv('ADMIN_PASSWORD', 'admin123')),

            role='admin'
        )
        db.session.add(admin)
        print("Admin user created.")

    # Create a test customer
    customer = User.query.filter_by(email='alice@example.com').first()
    if not customer:
        customer = User(
            username='alice',
            email='alice@example.com',
            password_hash=generate_password_hash('password'),
            role='customer'
        )
        db.session.add(customer)
        db.session.commit() # Commit to get ID
        
        # Create some dummy orders for Alice
        order1 = Order(
            user_id=customer.id,
            total_amount=120.50,
            items='[{"name": "Fancy Dress", "price": 120.50}]',
            status='delivered'
        )
        order2 = Order(
            user_id=customer.id,
            total_amount=600.00,
            items='[{"name": "Luxury Watch", "price": 600.00}]',
            status='delivered'
        )
        db.session.add(order1)
        db.session.add(order2)
        print("Test customer and orders created.")
    
    db.session.commit()
    print("Database seeded successfully!")
