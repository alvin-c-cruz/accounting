import pytest
from accounting import create_app


@pytest.fixture(scope="session")
def app():
    return create_app(test_config="test_config.py")
