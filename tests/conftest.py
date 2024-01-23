import pytest

import app
import portfolio
#
#
# def test_data_csv(directory_name, table_name):
#     return directory_name + table_name + '.csv'
#


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
    # empty_portfolio = portfolio.Portfolio('./test.db')
    # empty_portfolio.drop_all_tables()
    # empty_portfolio.create_all_tables()
    return test_app_empty.portfolio


@pytest.fixture
def test_portfolio(test_app_original):
    # test_portfolio = portfolio.Portfolio('./test.db')
    # test_portfolio.drop_all_tables()
    # test_portfolio.create_all_tables()
    # add_all_test_data_from_csv(test_portfolio, './test_data/')
    #
    # return test_portfolio
    #
    # test_portfolio = portfolio.Portfolio('./test.db')
    # test_portfolio.drop_all_tables()
    # test_portfolio.create_all_tables()
    # add_all_test_data_from_csv(test_portfolio, './test_data/')

    return test_app_original.portfolio


@pytest.fixture
def test_portfolio_allocation(test_app_allocations):
    # test_portfolio = portfolio.Portfolio('./test_allocation.db')
    # test_portfolio.drop_all_tables()
    # test_portfolio.create_all_tables()
    # add_all_test_data_from_csv(test_portfolio, './test_data_allocations/')

    return test_app_allocations.portfolio


# @pytest.fixture
# def test_app(test_portfolio):
#     test_app = app.App
#     test_app.portfolio = test_portfolio
#
#     return test_app

#
# def add_all_test_data_from_csv(test_app, directory_name):
#     for table_name in test_app.add_to_table:
#         add_test_data_from_csv(test_app, directory_name, table_name)
#
#
# def add_test_data_from_csv(test_app, directory_name, table_name):
#     test_app.add_from_csv(test_data_csv(directory_name, table_name), table_name)
