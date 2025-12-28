from models import User, Order, ReturnRequest, RefundParams
from datetime import datetime, timedelta

class RiskEngine:
    def __init__(self):
        pass

    def analyze_return_risk(self, user, return_request):
        # 1. Gather Data
        score = 0
        reasons_list = []
        action = "Allow return"
        risk_level = "Low Risk"

        # Account Age
        account_age_days = (datetime.utcnow() - user.created_at).days
        if account_age_days < 30:
            score += 20
            reasons_list.append("New Account (< 30 days)")

        # Order Stats
        total_orders = Order.query.filter_by(user_id=user.id).count()
        total_returns = ReturnRequest.query.filter_by(user_id=user.id).count() # Includes this one if committed, or check logic
        
        # Adjust for current request not being in DB yet usually, but passed as object
        # Since we haven't committed this return request yet in most flows calling this, add 1 to effective returns if logic requires
        # However, for this calculation let's assume 'total_returns' is historical + current
        effective_returns = total_returns + 1 
        
        return_rate = (effective_returns / (total_orders if total_orders > 0 else 1)) * 100
        
        if return_rate > 80:
            score += 40
            reasons_list.append(f"High Return Rate ({int(return_rate)}%)")
        elif return_rate > 50:
            score += 20
            reasons_list.append(f"Moderate Return Rate ({int(return_rate)}%)")

        # Returns in last 30 days
        last_30_days = datetime.utcnow() - timedelta(days=30)
        returns_30_days = ReturnRequest.query.filter(
            ReturnRequest.user_id == user.id,
            ReturnRequest.request_date >= last_30_days
        ).count()
        
        if returns_30_days >= 3:
            score += 30
            reasons_list.append(f"Frequent Returns ({returns_30_days} in 30 days)")

        # Payment Method Check (Current Order)
        current_order = Order.query.get(return_request.order_id)
        payment_method = current_order.payment_method if current_order else "UNKNOWN"
        if payment_method == 'COD':
            score += 15
            reasons_list.append("COD Payment Method")

        # Return Reason
        if return_request.reason in ['Defective', 'Not as Described']:
            score += 10 # Slight risk increase for subjective/claims
        
        if return_request.reason == 'Wore once (Test Wardrobing)':
             score += 50
             reasons_list.append("Wardrobing Admitted")

        # High Value
        if return_request.refund_amount > 5000:
            score += 10
            reasons_list.append("High Value Return")

        # Cap Score
        score = min(score, 100)

        # Classification
        if score >= 70:
            risk_level = "High Risk"
            action = "Block return" if score > 85 else "Manual review"
        elif score >= 40:
            risk_level = "Medium Risk"
            action = "Extra verification"
        
        # Most common return reason (Historical)
        # Simplified: Just taking the current one for now as 'Most common' proxy if history is low
        common_reason = return_request.reason 

        # Formatted Output
        avg_return_val = 0 # Placeholder for complex avg calc
        
        report = f"""
Risk Level: {risk_level}
Risk Score (0–100): {score}
Reason: {', '.join(reasons_list) if reasons_list else 'Standard Return'}
Recommended Action: {action}
"""
        return {
            "score": score,
            "level": risk_level,
            "report": report
        }

    # Deprecated/Wrapper for backward compatibility if needed, or remove
    def calculate_risk_score(self, user, return_request):
        analysis = self.analyze_return_risk(user, return_request)
        return 10 if analysis['score'] > 50 else 0 # Simple delta for legacy

