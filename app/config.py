"""This module contains configuration settings for the application."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration settings for the application."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "fallback_secret_key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = "ja"
    BABEL_DEFAULT_TIMEZONE = "Asia/Tokyo"
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DEV_DATABASE_URL") or "sqlite:///dev.db"
    )  # 開発用DBを指定


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:test_password@localhost:5432/test_db"  # インメモリDBを使用
    WTF_CSRF_ENABLED = False  # CSRFを無効化（テスト時）
    # SESSION_TYPE = None # テスト時はセッションを無効化することも検討


class ProductionConfig(Config):
    """Production configuration."""

    # 本番環境用の設定。必要に応じてオーバーライド
    SESSION_TYPE = "redis"  # 本番環境ではredisなどを使用
    # REDIS_URL = os.environ.get("REDIS_URL")
    SQLALCHEMY_DATABASE_URI = os.environ.get("PROD_DATABASE_URL")
