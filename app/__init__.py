import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel
from flask_session import Session

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
babel = Babel()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.config["SECRET_KEY"] = "your_secret_key"  # 必ず適切な秘密鍵に置き換えてください
    app.config["SESSION_TYPE"] = (
        "filesystem"  # 開発用。本番環境では'redis'か'memcached'に変更
    )
    app.config["SESSION_PERMANENT"] = False
    app.config["STATIC_FOLDER"] = os.path.join(app.root_path, "static")

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    babel.init_app(app)
    Session(app)  # Flask-Session を初期化

    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.admin import bp as admin_bp

    app.register_blueprint(admin_bp)

    return app
