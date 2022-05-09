import pytest
from accounting.blueprints import user


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
