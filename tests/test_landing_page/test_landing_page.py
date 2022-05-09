import pytest


@pytest.mark.landing_page
class TestLandingPage:
    @pytest.mark.smoke
    @pytest.mark.user_logged_out
    def test_landing_page_home(self, landing_page_html):
        assert landing_page_html.status_code == 200

    @pytest.mark.user_logged_out
    def test_landing_page_home_has_register_link(self, landing_page_soup):
        assert landing_page_soup.find("a", string="Register")
        assert landing_page_soup.find("a", {"href": "/user/register"})

    @pytest.mark.user_logged_out
    def test_landing_page_home_has_login_link(self, landing_page_soup):
        assert landing_page_soup.find("a", string="Log In")
        assert landing_page_soup.find("a", {"href": "/user/login"})
