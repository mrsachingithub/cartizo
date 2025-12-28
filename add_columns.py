from app import create_app, db
from models import Order, ReturnRequest
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Add payment_method to Order
    try:
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE `order` ADD COLUMN payment_method VARCHAR(20) DEFAULT 'PREPAID'"))
            print("Added payment_method to Order table.")
    except Exception as e:
        print(f"Column payment_method might already exist: {e}")

    # Add risk_report to ReturnRequest
    try:
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE return_request ADD COLUMN risk_report TEXT"))
            print("Added risk_report to ReturnRequest table.")
    except Exception as e:
        print(f"Column risk_report might already exist: {e}")

    db.session.commit()
    print("Migration complete.")
