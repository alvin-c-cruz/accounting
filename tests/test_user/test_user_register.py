import pytest


@pytest.mark.user
class TestUser:
    @pytest.mark.smoke
    @pytest.mark.user_logged_out
    def test_user_register(self, register_html):
        assert register_html.status_code == 200

    @pytest.mark.smoke
    @pytest.mark.user_logged_out
    def test_user_register_has_name_control(self, register_soup):
        assert register_soup.find('label', {"for": "name"})
        assert register_soup.find('input', {"name": "name"})


def test_user_register_has_email_control(register_soup):
    assert register_soup.find('label', {"for": "email"})
    assert register_soup.find('input', {"name": "email"})


def test_user_register_has_password_control(register_soup):
    assert register_soup.find('label', {"for": "password"})
    assert register_soup.find('input', {"name": "password"})


def test_user_register_has_confirm_password_control(register_soup):
    assert register_soup.find('label', {"for": "confirm_password"})
    assert register_soup.find('input', {"name": "confirm_password"})


def test_user_register_has_submit_button(register_soup):
    assert register_soup.find('input', {"type": "submit"})


def test_user_create_new_admin_user(client, admin_user):
    data = admin_user
    data["confirm_password"] = admin_user['password']
    response = client.post('/user/register', json=data)
    assert response.status_code == 201
