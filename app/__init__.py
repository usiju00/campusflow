from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    from app.models import Student

    @login_manager.user_loader
    def load_user(user_id):
        return Student.query.get(int(user_id))

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.wallet import bp as wallet_bp
    app.register_blueprint(wallet_bp)
    return app
