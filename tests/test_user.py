from flask import url_for


class TestUserHome:
    def test_user_home(self, client):
        assert client.get(url_for("user.home")).status_code == 302


class TestUserRegister:
    def test_user_register(self, client):
        assert client.get(url_for("user.register")).status_code == 200

    def test_user_register_has_name_control(self, client):
        response = client.get(url_for("user.register"))
        assert "Name" in response.text

    def test_user_register_has_email_control(self, client):
        response = client.get(url_for("user.register"))
        assert "Email" in response.text

    def test_user_register_has_password_control(self, client):
        response = client.get(url_for("user.register"))
        assert "Password" in response.text

    def test_user_register_has_confirm_password_control(self, client):
        response = client.get(url_for("user.register"))
        assert "Confirm Password" in response.text

    def test_user_register_has_submit_button(self, client):
        response = client.get(url_for("user.register"))
        assert "" in response.text


def test_user_login(client):
    assert client.get(url_for("user.login")).status_code == 200


def test_user_logout(client):
    assert client.get(url_for("user.logout")).status_code == 302
