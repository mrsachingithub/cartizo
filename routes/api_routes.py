from flask import Blueprint, jsonify
from models import User
from flask_login import login_required, current_user

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/risk_score/<int:user_id>')
@login_required
def get_risk_score(user_id):
    if current_user.role != 'admin' and current_user.id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    user = User.query.get_or_404(user_id)
    return jsonify({
        'user_id': user.id,
        'risk_score': user.risk_score,
        'is_flagged': user.is_flagged
    })
