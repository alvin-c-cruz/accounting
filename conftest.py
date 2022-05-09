import pytest
from accounting import create_app


@pytest.fixture(scope="session")
def client():
    app = create_app(test_config="test_config.py")
    return app.test_client()
