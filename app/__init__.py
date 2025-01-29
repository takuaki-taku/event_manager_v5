import os
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel
from app.config import Config


db = SQLAlchemy()

login_manager = LoginManager()
migrate = Migrate()
babel = Babel()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)
    app.db = db
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # ログインページのエンドポイントを指定
    login_manager.login_message = (
        "ログインが必要です。"  # ログインメッセージをカスタマイズ
    )

    babel.init_app(app, locale_selector=get_locale)

    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.admin import bp as admin_bp

    app.register_blueprint(admin_bp)

    return app


def get_locale():
    """
    Determine the preferred language for the user.
    """
    return session.get("lang", request.accept_languages.best_match(["en", "ja"]))
