import pytest
from app import create_app  # create_appをインポート
from app import db


@pytest.fixture(scope="session")
def app():
    app = create_app(config_name="testing")  # config_nameを指定
    app.config["SERVER_NAME"] = "localhost"  # SERVER_NAME を設定
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
