import pytest

import app
import portfolio


def create_test_app(test_data_file_path=None):
    test_app = app.App(portfolio.Portfolio('./test.db'))
    test_app.portfolio.drop_all_tables()
    test_app.portfolio.create_all_tables()

    if test_data_file_path is not None:
        for table_name in test_app.add_to_table:
            test_app.add_from_csv(test_data_file_path + table_name + '.csv', table_name)

    return test_app


@pytest.fixture
def test_app_empty():
    return create_test_app()


@pytest.fixture
def test_app_original():
    return create_test_app('./test_data/')


@pytest.fixture
def test_app_allocations():
    return create_test_app('./test_data_allocations/')


@pytest.fixture
def empty_portfolio(test_app_empty):
    return test_app_empty.portfolio


@pytest.fixture
def test_portfolio(test_app_original):
    return test_app_original.portfolio


@pytest.fixture
def test_portfolio_allocation(test_app_allocations):
    return test_app_allocations.portfolio
