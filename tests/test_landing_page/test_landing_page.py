from flask import url_for


def test_landing_page_home(client):
    assert client.get(url_for("landing_page.home")).status_code == 200


def test_landing_page_home_has_register_text(client):
    response = client.get(url_for("landing_page.home"))
    assert "Register" in response.text


def test_landing_page_home_has_register_link(client):
    response = client.get(url_for("landing_page.home"))
    assert url_for("user.register") in response.text


def test_landing_page_home_has_login_text(client):
    response = client.get(url_for("landing_page.home"))
    assert "Log In" in response.text


def test_landing_page_home_has_login_link(client):
    response = client.get(url_for("landing_page.home"))
    assert url_for("user.login") in response.text
