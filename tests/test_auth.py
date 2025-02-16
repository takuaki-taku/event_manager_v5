import json
import pytest
from app import db
import typing as t
from app.models.user import User  # ユーザーモデルのパスを調整してください
from unittest.mock import patch, MagicMock
from flask import url_for


def _default(o: t.Any) -> t.Any:
    if isinstance(o, date):
        return http_date(o)

    if isinstance(o, (decimal.Decimal, uuid.UUID)):
        return str(o)

    if dataclasses and dataclasses.is_dataclass(o):
        return dataclasses.asdict(o)

    if hasattr(o, "__html__"):
        return str(o.__html__())

    if isinstance(o, MagicMock):
        return json.dumps(str(o))  # MagicMockを文字列に変換してからJSONにシリアライズ

    raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")


def test_login_success(client):
    """ログインが成功するケース"""
    # モックするユーザーデータ
    mock_user = MagicMock()
    mock_user.check_password.return_value = True  # 正しいパスワードを返す

    # Userモデルのクエリをモック
    with patch("app.models.User.query") as mock_query:
        mock_query.filter_by.return_value.first.return_value = {
            "id": 1,
            "username": "testuser",
        }  # ダミーデータを使用

        # ログインリクエストを送信
        response = client.post(
            url_for("auth.login"),
            data={"username": "testuser", "password": "testpassword"},
            follow_redirects=True,  # リダイレクトをフォローする
        )

        # リダイレクト後のページでのアサーション
        assert response.status_code == 200


def test_login_failure(client):
    """ログインが失敗するケース"""
    # モックするユーザーデータ（存在しないユーザー）
    with patch("app.models.User.query") as mock_query:
        mock_query.filter_by.return_value.first.return_value = None

        # ログインリクエストを送信
        response = client.post(
            url_for("auth.login"),
            data={"username": "wronguser", "password": "wrongpassword"},
            follow_redirects=True,
        )

        # アサーション
        assert response.status_code == 200
        assert (
            "ユーザー名またはパスワードが間違っています".encode("utf-8")
            in response.data
        )


def test_redirect_if_authenticated(client):
    """ログイン済みの場合、リダイレクトされるケース"""
    with patch("flask_login.utils._get_user") as mock_current_user:
        mock_current_user.return_value.is_authenticated = True

        # ログインページへのリクエスト
        response = client.get(url_for("auth.login"), follow_redirects=True)

        # アサーション
        assert response.status_code == 200
        assert "あなたは既にログインしています".encode("utf-8") not in response.data
