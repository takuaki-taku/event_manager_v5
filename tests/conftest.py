import pytest
from wsgi import application  # Flaskアプリをインポート
from app.models.user import User  # ユーザーモデルのパスを調整してください
from app import db  # アプリケーションのデータベース


@pytest.fixture
def app():
    """テスト用のアプリケーション設定"""
    application.config["TESTING"] = True  # テストモードを有効化
    application.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///./test.db"  # テスト用SQLiteデータベース
    )
    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    with application.app_context():
        db.create_all()  # テスト用データベースを作成
        yield application
        db.session.remove()
        db.drop_all()  # テスト終了後にデータベースを削除


@pytest.fixture
def client(app):
    """テストクライアントをセットアップ"""
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_user():
    """テスト用のモックユーザーを作成"""
    user = User(username="testuser", email="test@example.com")
    user.set_password("testpassword")  # 適切なメソッドでハッシュ化
    db.session.add(user)
    db.session.commit()
    return user
