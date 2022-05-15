import pytest


@pytest.mark.user
class TestUser:
    @pytest.mark.smoke
    @pytest.mark.user_logged_out
    def test_user_register(self, register_html):
        assert register_html.status_code == 200

    @pytest.mark.user_logged_out
    def test_user_register_has_name_control(self, register_soup):
        assert register_soup.find('label', {"for": "name"})
        assert register_soup.find('input', {"name": "name"})

    @pytest.mark.user_logged_out
    def test_user_register_has_email_control(self, register_soup):
        assert register_soup.find('label', {"for": "email"})
        assert register_soup.find('input', {"name": "email"})

    @pytest.mark.user_logged_out
    def test_user_register_has_password_control(self, register_soup):
        assert register_soup.find('label', {"for": "password"})
        assert register_soup.find('input', {"name": "password"})

    @pytest.mark.user_logged_out
    def test_user_register_has_confirm_password_control(self, register_soup):
        assert register_soup.find('label', {"for": "confirm_password"})
        assert register_soup.find('input', {"name": "confirm_password"})

    @pytest.mark.user_logged_out
    def test_user_register_has_submit_button(self, register_soup):
        assert register_soup.find('input', {"type": "submit"})

    @pytest.mark.user_logged_out
    def test_user_create_new_user(self, client, new_user):
        data = {
            "name": new_user['name'],
            "email": new_user['email'],
            "password": new_user['password'],
            "confirm_password": new_user['password'],
            "follow_redirects": True,
        }
        response = client.post('/user/register', data=data)

        assert response.status_code == 200

    @pytest.mark.smoke
    @pytest.mark.user_logged_out
    def test_user_login(self, client, new_user):
        data = {
            "email": new_user['email'],
            "password": new_user['password'],
            "follow_redirects": True,
        }
        response = client.post('/user/login', data=data)

        assert response.status_code == 200