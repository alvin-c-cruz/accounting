from flask import url_for


def test_user_logout(client):
    assert client.get(url_for("user.logout")).status_code == 302
