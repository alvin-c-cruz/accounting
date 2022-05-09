import pytest
from accounting import create_app


@pytest.fixture
def app():
    app = create_app(test_config="test_config.py")
    return app
