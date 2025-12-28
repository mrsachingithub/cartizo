from app import create_app, db
from models import User, Order, Product, OrderItem
from datetime import datetime, timedelta
import json

app = create_app()

with app.app_context():
    # Get user
    user = User.query.filter_by(email='alice@example.com').first()
    product = Product.query.first()
    
    if user and product:
        # Create an order from 20 days ago
        old_date = datetime.utcnow() - timedelta(days=20)
        
        order = Order(
            user_id=user.id,
            total_amount=product.price,
            items=json.dumps([]),
            status='delivered',
            order_date=old_date
        )
        db.session.add(order)
        db.session.commit()
        
        # Add item
        item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=1,
            price_at_purchase=product.price
        )
        db.session.add(item)
        db.session.commit()
        
        print(f"Seeded old order #{order.id} from {old_date}")
    else:
        print("User or Product not found.")
