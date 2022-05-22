import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def landing_page_html(test_client):
    return test_client.get("/")


@pytest.fixture
def landing_page_soup(landing_page_html):
    return BeautifulSoup(landing_page_html.text, 'html.parser')

