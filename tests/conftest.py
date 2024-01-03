import pytest
import portfolio


@pytest.fixture
def test_portfolio():
    test_portfolio = portfolio.Portfolio('./test.db')
    test_portfolio.populate_test_portfolio()

    return test_portfolio
