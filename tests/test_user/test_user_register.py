from flask import url_for


def test_user_model(user_model, admin_user):
    test_user = user_model(
        name=admin_user['name'],
        email=admin_user['email'],
        password=admin_user['password']
    )
    assert test_user.name == "Alvin"
    assert test_user.email == "alvinccruz12@gmail.com"
    assert test_user.password == "s1mplep@ssword"


def test_user_register(client):
    assert client.get(url_for("user.register")).status_code == 200


def test_user_register_has_name_control(client):
    response = client.get(url_for("user.register"))
    assert "Name" in response.text


def test_user_register_has_email_control(client):
    response = client.get(url_for("user.register"))
    assert "Email" in response.text


def test_user_register_has_password_control(client):
    response = client.get(url_for("user.register"))
    assert "Password" in response.text


def test_user_register_has_confirm_password_control(client):
    response = client.get(url_for("user.register"))
    assert "Confirm Password" in response.text


def test_user_register_has_submit_button(client):
    response = client.get(url_for("user.register"))
    assert "" in response.text
