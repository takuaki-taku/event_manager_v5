import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Pooler 側のアイドル接続切断で stale connection になるのを防ぐ
    # PostgreSQL のみ。SQLite(テスト) は pool_timeout などを受け付けない
    SQLALCHEMY_ENGINE_OPTIONS = (
        {
            "pool_pre_ping": True,
            "pool_recycle": 180,
            "pool_timeout": 30,
        }
        if SQLALCHEMY_DATABASE_URI.startswith(("postgresql://", "postgres://"))
        else {}
    )
    BABEL_DEFAULT_LOCALE = "ja"

    # --- session / cookie hardening ---
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
