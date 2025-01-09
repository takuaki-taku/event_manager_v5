import os
import pytest
from wsgi import application
from app import db


@pytest.fixture(scope="session")
def app():
    application.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": os.environ.get("TEST_DATABASE_URL"),
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "SERVER_NAME": "localhost",
        }
    )
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
