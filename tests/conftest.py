import pytest
import app
import db
import pytest
import tests.test_data as td

insert_dict = {'account': db.insert_account,
               'account_type': db.insert_account_type,
               'allocation': db.insert_allocation,
               'asset': db.insert_asset,
               'asset_class': db.insert_asset_class,
               'balance': db.insert_balance,
               'component': db.insert_component,
               'institution': db.insert_institution,
               'location': db.insert_location,
               'owner': db.insert_owner,
               'price': db.insert_price}


@pytest.fixture
def test_db_0(tmp_path):
    db_test = tmp_path / "test.db"
    db.execute_script(db_test, db.create_tables)
    db.execute_script(db_test, db.create_views)
    return db_test


# Use for simplified allocation data
@pytest.fixture
def test_db_1(tmp_path):
    db_test = tmp_path / "test_1.db"
    db.execute_script(db_test, db.create_tables)
    db.execute_script(db_test, db.create_views)
    for table_name in insert_dict:
        db.execute_many(database=db_test, cmd=insert_dict[table_name], data_sequence=td.db_1[table_name])
    return db_test


# Use for general testing (has multiple of each item)
@pytest.fixture
def test_db_2(tmp_path):
    db_test = tmp_path / "test_2.db"
    db.execute_script(db_test, db.create_tables)
    db.execute_script(db_test, db.create_views)
    for table_name in insert_dict:
        db.execute_many(database=db_test, cmd=insert_dict[table_name], data_sequence=td.db_2[table_name])
    return db_test


@pytest.fixture
def test_app_db_1(test_db_1):
    return app.App(test_db_1)


@pytest.fixture
def test_app_db_2(test_db_2):
    return app.App(test_db_2)

# import app
# import portfolio
# import sql_database
# import text_ui
#
#
# # Test portfolios
# @pytest.fixture
# def empty_portfolio():
#     test_portfolio = portfolio.Portfolio('./test.db')
#     test_portfolio.drop_all_tables()
#     test_portfolio.create_all_tables()
#     return test_portfolio
#
#
# @pytest.fixture
# def test_portfolio(empty_portfolio):
#     for table_name in empty_portfolio:
#         empty_portfolio.add_from_csv('./old_test_data/' + table_name + '.csv', table_name)
#     return empty_portfolio
#
#
# @pytest.fixture
# def test_portfolio_allocation(empty_portfolio):
#     for table_name in empty_portfolio:
#         empty_portfolio.add_from_csv('./test_data_allocations/' + table_name + '.csv', table_name)
#     return empty_portfolio
#
#
# @pytest.fixture
# def test_database():
#     return sql_database.Database('test.db')
#
#
# # Test apps
# @pytest.fixture
# def test_app_empty(empty_portfolio):
#     return app.App(empty_portfolio)
#
#
# @pytest.fixture
# def test_app(test_portfolio):
#     return app.App(test_portfolio)
#
#
# @pytest.fixture
# def test_app_allocation(test_portfolio_allocation):
#     return app.App(test_portfolio_allocation)
#
#
# # Test Text UIs
# @pytest.fixture
# def test_ui(test_app):
#     return text_ui.TextUI(test_app)
#
#
# @pytest.fixture
# def test_ui_empty(test_app_empty):
#     return text_ui.TextUI(test_app_empty)
#
#
# table_names = ['account',
#                'account_type',
#                'allocation',
#                'asset',
#                'asset_class',
#                'balance',
#                'component',
#                'institution',
#                'location',
#                'owner',
#                'price']
#
#
# @pytest.fixture(params=table_names)
# def portfolio_table_name(request):
#     return request.param
#
#
# @pytest.fixture(params=table_names)
# def app_table_name(request):
#     return request.param.replace('_', ' ')
