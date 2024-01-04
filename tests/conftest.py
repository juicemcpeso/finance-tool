import pytest

import app
import portfolio


@pytest.fixture
def empty_portfolio():
    empty_portfolio = portfolio.Portfolio('./test.db')
    empty_portfolio.drop_all_tables()
    empty_portfolio.create_all_tables()
    return empty_portfolio


@pytest.fixture
def test_portfolio():
    test_portfolio = portfolio.Portfolio('./test.db')
    test_portfolio.drop_all_tables()
    test_portfolio.create_all_tables()
    test_portfolio.add_from_csv_account('./test_data/test_accounts.csv')
    test_portfolio.add_from_csv_account_type('./test_data/test_account_types.csv')
    test_portfolio.add_from_csv_asset('./test_data/test_assets.csv')
    test_portfolio.add_from_csv_balance('./test_data/test_balances.csv')
    test_portfolio.add_from_csv_institution('./test_data/test_institutions.csv')
    test_portfolio.add_from_csv_owner('./test_data/test_owners.csv')
    test_portfolio.add_from_csv_price('./test_data/test_prices.csv')

    return test_portfolio


@pytest.fixture
def test_app(test_portfolio):
    test_app = app.App
    test_app.portfolio = test_portfolio

    return test_app
