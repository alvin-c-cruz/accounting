from flask import url_for


def test_user_login(client):
    assert client.get(url_for("user.login")).status_code == 200
