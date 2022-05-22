import pytest


@pytest.mark.user
class TestUserLogin:
    @pytest.mark.smoke
    @pytest.mark.user_logged_out
    def test_user_login_page(self, login_html):
        assert login_html.status_code == 200

    @pytest.mark.user_logged_out
    def test_user_login_has_email_control(self, login_soup):
        assert login_soup.find("label", {"for": "email"})
        assert login_soup.find("input", {"name": "email"})

    @pytest.mark.user_logged_out
    def test_user_login_has_password_control(self, login_soup):
        assert login_soup.find("label", {"for": "password"})
        assert login_soup.find("input", {"name": "password"})

    @pytest.mark.user_logged_out
    def test_user_login_has_login_button(self, login_soup):
        assert login_soup.find("input", {"value": "Log In"})

    @pytest.mark.smoke
    @pytest.mark.user_logged_out
    def test_user_login(self, test_client, admin_user):
        data = {
            "email": admin_user.email,
            "password": admin_user.password,
            "follow_redirects": True,
        }
        response = test_client.post('/user/login', data=data)

        assert response.status_code == 200
