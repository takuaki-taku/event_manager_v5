from flask import url_for


def test_login_success(client):
    response = client.post(
        url_for("auth.login"),
        data={"username": "testuser", "password": "testpassword"},
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_login_failure(client):
    response = client.post(
        url_for("auth.login"),
        data={"username": "wronguser", "password": "wrongpassword"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "ユーザー名またはパスワードが間違っています" in response.data.decode("utf-8")


def test_redirect_if_authenticated(client):
    client.post(
        url_for("auth.login"),
        data={"username": "testuser", "password": "testpassword"},
    )
    response = client.get(url_for("auth.login"), follow_redirects=True)
    assert response.status_code == 200
    assert "あなたは既にログインしています" not in response.data.decode("utf-8")
