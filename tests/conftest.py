import pytest

import app
import portfolio
#
#
# @pytest.fixture
# def test_data_directory():
#     return './test_data/'
#
#
# @pytest.fixture
# def test_database_path():
#     return './test.db'


def test_data_csv(table_name):
    return './test_data/' + table_name + '.csv'


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
    add_all_test_data_from_csv(test_portfolio)

    # test_portfolio.add_from_csv('./test_data/accounts.csv', 'accounts')
    # test_portfolio.add_from_csv('./test_data/account_types.csv', 'account_types')
    # test_portfolio.add_from_csv('./test_data/allocation_plan.csv', 'allocation_plan')
    # test_portfolio.add_from_csv('./test_data/assets.csv', 'assets')
    # test_portfolio.add_from_csv('./test_data/asset_classes.csv', 'asset_classes')
    # test_portfolio.add_from_csv('./test_data/balances.csv', 'balances')
    # test_portfolio.add_from_csv('./test_data/components.csv', 'components')
    # test_portfolio.add_from_csv('./test_data/institutions.csv', 'institutions')
    # test_portfolio.add_from_csv('./test_data/locations.csv', 'locations')
    # test_portfolio.add_from_csv('./test_data/owners.csv', 'owners')
    # test_portfolio.add_from_csv('./test_data/prices.csv', 'prices')

    return test_portfolio


@pytest.fixture
def test_app(test_portfolio):
    test_app = app.App
    test_app.portfolio = test_portfolio

    return test_app


def add_all_test_data_from_csv(test_portfolio):
    for table_name in test_portfolio.add_to_table:
        add_test_data_from_csv(test_portfolio, table_name)
        # full_file_path = file_path + table + '.csv'
        # test_portfolio.add_from_csv(full_file_path, table)


def add_test_data_from_csv(test_portfolio, table_name):
    # full_file_path = test_data_directory + table_name + '.csv'
    test_portfolio.add_from_csv(test_data_csv(table_name), table_name)
