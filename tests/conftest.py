import pytest
import portfolio


@pytest.fixture
def portfolio():
    test_portfolio = portfolio.Portfolio('./portfolios/test.db')
    test_portfolio.populate_test_portfolio()

    return test_portfolio
