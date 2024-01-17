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
    add_all_test_data_from_csv('./test_data/test_', test_portfolio)

    # test_portfolio.add_from_csv('./test_data/test_accounts.csv', 'accounts')
    # test_portfolio.add_from_csv('./test_data/test_account_types.csv', 'account_types')
    # test_portfolio.add_from_csv('./test_data/test_allocation_plan.csv', 'allocation_plan')
    # test_portfolio.add_from_csv('./test_data/test_assets.csv', 'assets')
    # test_portfolio.add_from_csv('./test_data/test_asset_classes.csv', 'asset_classes')
    # test_portfolio.add_from_csv('./test_data/test_balances.csv', 'balances')
    # test_portfolio.add_from_csv('./test_data/test_components.csv', 'components')
    # test_portfolio.add_from_csv('./test_data/test_institutions.csv', 'institutions')
    # test_portfolio.add_from_csv('./test_data/test_locations.csv', 'locations')
    # test_portfolio.add_from_csv('./test_data/test_owners.csv', 'owners')
    # test_portfolio.add_from_csv('./test_data/test_prices.csv', 'prices')

    return test_portfolio


@pytest.fixture
def test_app(test_portfolio):
    test_app = app.App
    test_app.portfolio = test_portfolio

    return test_app


def add_all_test_data_from_csv(file_path, test_portfolio):
    for table in test_portfolio.add_to_table:
        full_file_path = file_path + table + '.csv'
        test_portfolio.add_from_csv(full_file_path, table)
