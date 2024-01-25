import pytest

import app
import portfolio
import sql_database
import text_ui


# Test portfolios
@pytest.fixture
def empty_portfolio():
    test_portfolio = portfolio.Portfolio('./test.db')
    test_portfolio.drop_all_tables()
    test_portfolio.create_all_tables()
    return test_portfolio


@pytest.fixture
def test_portfolio(empty_portfolio):
    for table_name in empty_portfolio:
        empty_portfolio.add_from_csv('./test_data/' + table_name + '.csv', table_name)
    return empty_portfolio


@pytest.fixture
def test_portfolio_allocation(empty_portfolio):
    for table_name in empty_portfolio:
        empty_portfolio.add_from_csv('./test_data_allocations/' + table_name + '.csv', table_name)
    return empty_portfolio


@pytest.fixture
def test_database():
    return sql_database.Database('test.db')


# Test apps
@pytest.fixture
def test_app_empty(empty_portfolio):
    return app.App(empty_portfolio)


@pytest.fixture
def test_app(test_portfolio):
    return app.App(test_portfolio)


@pytest.fixture
def test_app_allocation(test_portfolio_allocation):
    return app.App(test_portfolio_allocation)


# Test Text UIs
@pytest.fixture
def test_ui(test_app):
    return text_ui.TextUI(test_app)


@pytest.fixture
def test_ui_empty(test_app_empty):
    return text_ui.TextUI(test_app_empty)


table_names = ['account',
               'account_type',
               'allocation',
               'asset',
               'asset_class',
               'balance',
               'component',
               'institution',
               'location',
               'owner',
               'price']


@pytest.fixture(params=table_names)
def portfolio_table_name(request):
    return request.param


@pytest.fixture(params=table_names)
def app_table_name(request):
    return request.param.replace('_', ' ')
