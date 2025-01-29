"""This module contains configuration settings for the application."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration settings for the application."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "fallback_secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = "ja"
    BABEL_DEFAULT_TIMEZONE = "Asia/Tokyo"
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
