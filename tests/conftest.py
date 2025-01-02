import pytest
from .app import create_app, db
import os

TEST_DATABASE_URI = os.environ.get("TEST_DATABASE_URI", "sqlite:///:memory:")


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = TEST_DATABASE_URI
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def db(app):
    with app.app_context():
        yield db
