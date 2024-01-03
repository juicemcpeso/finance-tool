import pytest

import app
import portfolio


@pytest.fixture
def test_portfolio():
    test_portfolio = portfolio.Portfolio('./test.db')
    test_portfolio.populate_test_portfolio()

    return test_portfolio


@pytest.fixture
def test_app(test_portfolio):
    test_app = app.App
    test_app.portfolio = test_portfolio

    return test_app
