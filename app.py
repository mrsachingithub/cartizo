from flask import Flask, redirect, url_for, render_template
from models import db, User
from flask_login import LoginManager
import os

def create_app():
    from dotenv import load_dotenv
    load_dotenv()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from routes.auth_routes import auth_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.api_routes import api_bp
    from routes.shop_routes import shop_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(shop_bp)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
