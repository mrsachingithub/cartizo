from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Add mobile to User
    try:
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE user ADD COLUMN mobile VARCHAR(15)"))
            print("Added mobile to User table.")
    except Exception as e:
        print(f"Column mobile might already exist: {e}")

    # Add is_blocked to User
    try:
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE user ADD COLUMN is_blocked BOOLEAN DEFAULT 0"))
            print("Added is_blocked to User table.")
    except Exception as e:
        print(f"Column is_blocked might already exist: {e}")

    db.session.commit()
    print("User table migration complete.")
