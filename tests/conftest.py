import pytest
import portfolio


@pytest.fixture
def test_portfolio():
    return portfolio.Portfolio('./portfolios/test.db')
