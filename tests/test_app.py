import pytest
from app import User


def test_login(client, db):  # db fixture を追加
    # テストユーザーを作成
    user = User(username="testuser")  # password 引数は不要
    user.set_password("password")  # set_password メソッドを使用してパスワードを設定
    db.session.add(user)
    db.session.commit()

    # ログインを試みる
    rv = client.post("/login", data={"username": "testuser", "password": "password"})

    # ログイン成功をアサート
    assert rv.status_code == 200
    assert "ログインしました。" in rv.data.decode("utf-8")

    # ログイン失敗をアサート
    rv = client.post(
        "/login", data={"username": "testuser", "password": "wrongpassword"}
    )
    assert rv.status_code == 200
    assert "ユーザー名またはパスワードが間違っています。" in rv.data.decode("utf-8")
