import pytest


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument('headless')
    chrome_options.add_argument('--window-size=1920,1080')
    return chrome_options
