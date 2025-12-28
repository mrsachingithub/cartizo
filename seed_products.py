from app import create_app, db
from models import User, Order, Product, OrderItem
from werkzeug.security import generate_password_hash
from datetime import datetime

app = create_app()

with app.app_context():
    db.create_all()
    
    # 1. Create Products
    products = [
        {"name": "Wireless Noise-Canceling Headphones", "price": 299.99, "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60", "desc": "Premium sound quality with active noise cancellation."},
        {"name": "Smart Fitness Watch", "price": 199.50, "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=60", "desc": "Track your health and fitness goals with precision."},
        {"name": "Designer Leather Handbag", "price": 450.00, "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=500&auto=format&fit=crop&q=60", "desc": "Handcrafted Italian leather bag for everyday elegance."},
        {"name": "Mechanical Gaming Keyboard", "price": 129.99, "image": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=500&auto=format&fit=crop&q=60", "desc": "Tactile switches with RGB lighting for the ultimate gaming experience."},
        {"name": "Organic Cotton T-Shirt", "price": 25.00, "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&auto=format&fit=crop&q=60", "desc": "Soft, breathable, and eco-friendly cotton tee."},
        {"name": "UV Protection Sunglasses", "price": 85.00, "image": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500&auto=format&fit=crop&q=60", "desc": "Stylish shades to protect your eyes from harmful rays."},
    ]

    for p_data in products:
        if not Product.query.filter_by(name=p_data['name']).first():
            product = Product(
                name=p_data['name'],
                price=p_data['price'],
                image_url=p_data['image'],
                description=p_data['desc']
            )
            db.session.add(product)
    
    db.session.commit()
    print("Products seeded.")

    # Check if admin exists
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        admin_password = os.getenv('ADMIN_PASSWORD')
        if not admin_password:
             raise ValueError("ADMIN_PASSWORD not set in environment")

        admin = User(
            username='admin',
            email='admin@refundguard.com',
            password_hash=generate_password_hash(admin_password),
            role='admin'
        )
        db.session.add(admin)

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
        db.session.commit()

    db.session.commit()
    print("Database seeded with Products, Admin and Test User!")
