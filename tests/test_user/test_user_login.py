from flask import url_for


def test_user_login(register_html):
    assert register_html.status_code == 200
