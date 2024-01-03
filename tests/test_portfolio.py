import pytest
import portfolio


#
#
# @pytest.fixture
# def test_portfolio():
#     test_portfolio = portfolio.Portfolio('./portfolios/test.db')
#     test_portfolio.populate_test_portfolio()
#
#     return test_portfolio


def test_add_account(test_portfolio):
    entry = {'name': 'Carlos IRA', 'account_type_id': 2, 'institution_id': 1, 'owner_id': 3}
    test_portfolio.add_account(args=entry)
    sql = """
    SELECT name, account_type_id, institution_id, owner_id FROM account WHERE id = 6
    """

    assert entry == test_portfolio.sql_fetch_one(sql)


def test_add_owner(test_portfolio):
    entry = {'name': 'Carlos', 'birthday': '2000-01-01'}
    test_portfolio.add_owner(args=entry)

    sql = """
    SELECT name, birthday FROM owner WHERE id = 3
    """

    assert entry == test_portfolio.sql_fetch_one(sql)


def test_add_price(test_portfolio):
    entry = {'asset_id': 2, 'price_date': '2023-01-01', 'amount': 3.61}
    test_portfolio.add_price(args=entry)
    sql = """
    SELECT asset_id, price_date, amount FROM price WHERE id = 10
    """

    assert entry == test_portfolio.sql_fetch_one(sql)
