import pytest

import app
import portfolio


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

    return test_portfolio


@pytest.fixture
def test_app(test_portfolio):
    test_app = app.App
    test_app.portfolio = test_portfolio

    return test_app


def add_all_test_data_from_csv(test_portfolio):
    for table_name in test_portfolio.add_to_table:
        add_test_data_from_csv(test_portfolio, table_name)


def add_test_data_from_csv(test_portfolio, table_name):
    test_portfolio.add_from_csv(test_data_csv(table_name), table_name)
