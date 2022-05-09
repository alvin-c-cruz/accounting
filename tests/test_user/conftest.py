import pytest
from bs4 import BeautifulSoup

from accounting.blueprints import user


@pytest.fixture
def user_home_html(client):
    return client.get("/user")


@pytest.fixture
def user_home_soup(user_home_html):
    return BeautifulSoup(user_home_html.text, 'html.parser')


@pytest.fixture
def register_html(client):
    return client.get("/user/register")


@pytest.fixture
def register_soup(register_html):
    return BeautifulSoup(register_html.text, 'html.parser')


@pytest.fixture
def admin_user():
    data = {
        "name": "Alvin",
        "email": "alvinccruz12@gmail.com",
        "password": "s1mplep@ssword"
    }
    return data


@pytest.fixture
def user_model():
    return user.User
