from flask import url_for


def test_user_home(client):
    assert client.get(url_for("user.home")).status_code == 302

