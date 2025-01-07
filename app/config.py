"""This module contains configuration settings for the application."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration settings for the application."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "fallback_secret_key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = "ja"
    SESSION_TYPE = "filesystem"  # 開発用。本番環境では'redis'か'memcached'に変更)

    BABEL_DEFAULT_TIMEZONE = "Asia/Tokyo"  # タイムゾーンを設定
    SESSION_PERMANENT = False
