import os
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel


db = SQLAlchemy()

login_manager = LoginManager()
migrate = Migrate()
babel = Babel()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.config["SECRET_KEY"] = "your_secret_key"  # 必ず適切な秘密鍵に置き換えてください
    app.config["SESSION_TYPE"] = (
        "filesystem"  # 開発用。本番環境では'redis'か'memcached'に変更
    )
    app.config["BABEL_DEFAULT_LOCALE"] = "ja"  # デフォルトのロケールを日本語に設定
    app.config["BABEL_DEFAULT_TIMEZONE"] = "Asia/Tokyo"  # タイムゾーンを設定
    app.config["SESSION_PERMANENT"] = False
    app.config["STATIC_FOLDER"] = os.path.join(app.root_path, "static")

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
