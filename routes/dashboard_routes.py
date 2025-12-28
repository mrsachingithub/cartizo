from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Order, ReturnRequest, User
from risk_engine import RiskEngine
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)
risk_engine = RiskEngine()

@dashboard_bp.route('/customer/dashboard')
@login_required
def customer_dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('dashboard.admin_dashboard'))
        
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.order_date.desc()).all()
    returns = ReturnRequest.query.filter_by(user_id=current_user.id).order_by(ReturnRequest.request_date.desc()).all()
    return render_template('customer/dashboard.html', orders=orders, returns=returns, user=current_user)

@dashboard_bp.route('/customer/order/<int:order_id>')
@login_required
def order_details(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and current_user.role != 'admin':
        flash('Unauthorized', 'error')
        return redirect(url_for('dashboard.customer_dashboard'))
    
    expected_delivery = order.order_date + timedelta(days=7)
    return render_template('customer/order_details.html', order=order, expected_delivery=expected_delivery)

@dashboard_bp.route('/customer/return/<int:order_id>', methods=['GET', 'POST'])
@login_required
def request_return(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('dashboard.customer_dashboard'))

    # Check for existing return
    existing_return = ReturnRequest.query.filter_by(order_id=order_id).first()
    if existing_return:
        flash('Return already requested for this order', 'info')
        return redirect(url_for('dashboard.customer_dashboard'))

    # CHECK: 10-day return policy
    delta = datetime.utcnow() - order.order_date
    if delta.days > 10:
        flash('Return period expired (10 days policy).', 'error')
        return redirect(url_for('dashboard.customer_dashboard'))

    if request.method == 'POST':
        reason = request.form.get('reason')
        description = request.form.get('description')
        
        new_return = ReturnRequest(
            user_id=current_user.id,
            order_id=order_id,
            reason=reason,
            description=description,
            refund_amount=order.total_amount
        )
        db.session.add(new_return)
        
        # Risk Engine Calculation
        analysis = risk_engine.analyze_return_risk(current_user, new_return)
        
        # Update User Stats
        score_change = analysis['score'] # Simplified: Use the score itself or delta?
        # Logic: If returning score 0-100, we might want to just set the user's latest score OR add to it?
        # User.risk_score is usually a cumulative metric or current status. 
        # Let's say user.risk_score represents "Current Risk Level" (0-100).
        current_user.risk_score = analysis['score'] 
        
        new_return.risk_report = analysis['report']

        if analysis['level'] == 'High Risk':
            current_user.is_flagged = True
            current_user.is_blocked = True
            flash(f"Return Flagged & Account Blocked: {analysis['report'].splitlines()[3]}", 'error') # Show Reason

        
        db.session.commit()
        flash('Return request submitted successfully', 'success')
        return redirect(url_for('dashboard.customer_dashboard'))
        
    return render_template('customer/request_return.html', order=order)

@dashboard_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard.customer_dashboard'))

    high_risk_users = User.query.filter(User.risk_score > 50).order_by(User.risk_score.desc()).all()
    pending_returns = ReturnRequest.query.filter_by(status='pending').all()
    
    return render_template('admin/dashboard.html', high_risk_users=high_risk_users, pending_returns=pending_returns)

@dashboard_bp.route('/admin/return/<int:request_id>/<action>', methods=['POST'])
@login_required
def process_return(request_id, action):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard.customer_dashboard'))
        
    ret_req = ReturnRequest.query.get_or_404(request_id)
    
    if action == 'approve':
        ret_req.status = 'approved'
        flash('Return approved', 'success')
    elif action == 'reject':
        ret_req.status = 'rejected'
        flash('Return rejected', 'info')
    else:
        flash('Invalid action', 'error')
        return redirect(url_for('dashboard.admin_dashboard'))

    db.session.commit()
    flash('Return approved', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))

@dashboard_bp.route('/admin/user/<int:user_id>/block/<action>', methods=['POST'])
@login_required
def toggle_block_user(user_id, action):
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard.customer_dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    if action == 'block':
        user.is_blocked = True
        flash(f'User {user.username} has been blocked.', 'success')
    elif action == 'unblock':
        user.is_blocked = False
        flash(f'User {user.username} has been unblocked.', 'success')
    else:
        flash('Invalid action', 'error')
        
    db.session.commit()
    return redirect(url_for('dashboard.admin_dashboard'))
