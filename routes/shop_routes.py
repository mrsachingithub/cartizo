from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Product, Order, OrderItem
from flask_login import login_required, current_user
import json
from datetime import datetime, timedelta

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/shop')
def index():
    query = request.args.get('q')
    max_price = request.args.get('max_price')
    
    products_query = Product.query
    
    if query:
        products_query = products_query.filter(Product.name.ilike(f'%{query}%'))
        
    if max_price:
        try:
            products_query = products_query.filter(Product.price <= float(max_price))
        except ValueError:
            pass
            
    products = products_query.all()
    
    # Initialize cart if not exists
    if 'cart' not in session:
        session['cart'] = {}
    return render_template('shop/index.html', products=products)

@shop_bp.route('/shop/product/<int:product_id>')
def product_details(product_id):
    product = Product.query.get_or_404(product_id)
    expected_delivery = datetime.now() + timedelta(days=5)
    return render_template('shop/product_details.html', product=product, expected_delivery=expected_delivery)

@shop_bp.route('/shop/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    str_id = str(product_id)
    
    if str_id in cart:
        cart[str_id] += 1
    else:
        cart[str_id] = 1
    
    session.modified = True
    flash('Item added to cart', 'success')
    return redirect(url_for('shop.index'))

@shop_bp.route('/shop/cart')
def cart():
    if 'cart' not in session:
        session['cart'] = {}
        
    cart_items = []
    total_price = 0
    
    for p_id, qty in session['cart'].items():
        product = Product.query.get(int(p_id))
        if product:
            total = product.price * qty
            total_price += total
            cart_items.append({
                'product': product,
                'quantity': qty,
                'total': total
            })
            
    return render_template('shop/cart.html', cart_items=cart_items, total_price=total_price)

@shop_bp.route('/shop/clear_cart')
def clear_cart():
    session['cart'] = {}
    session.modified = True
    return redirect(url_for('shop.cart'))

@shop_bp.route('/shop/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if not session.get('cart'):
        flash('Your cart is empty', 'warning')
        return redirect(url_for('shop.index'))
        
    if request.method == 'POST':
        # Create Order
        total_price = 0
        items_json = []
        
        # Calculate total and prepare data
        for p_id, qty in session['cart'].items():
            product = Product.query.get(int(p_id))
            if product:
                total_price += product.price * qty
                items_json.append({
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "qty": qty
                })
        
        new_order = Order(
            user_id=current_user.id,
            total_amount=total_price,
            items=json.dumps(items_json), # Deprecated but kept for compatibility
            status='delivered' # Auto-delivered for simulation
        )
        db.session.add(new_order)
        db.session.commit() # Commit to get order ID
        
        # Create OrderItems
        for p_id, qty in session['cart'].items():
            product = Product.query.get(int(p_id))
            if product:
                order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=product.id,
                    quantity=qty,
                    price_at_purchase=product.price
                )
                db.session.add(order_item)
        
        db.session.commit()
        
        # Clear cart
        session['cart'] = {}
        session.modified = True
        
        flash(f'Order #{new_order.id} placed successfully!', 'success')
        return redirect(url_for('dashboard.customer_dashboard'))
        
    # GET request - Show summary
    cart_items = []
    total_price = 0
    for p_id, qty in session['cart'].items():
        product = Product.query.get(int(p_id))
        if product:
            total_price += product.price * qty
            cart_items.append({'product': product, 'qty': qty})
            
    return render_template('shop/checkout.html', cart_items=cart_items, total_price=total_price)
