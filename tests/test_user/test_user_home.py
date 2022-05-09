def test_user_home(user_home_html):
    assert user_home_html.status_code == 308

