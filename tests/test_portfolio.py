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


def test_add_owner(test_portfolio):
    entry = {'name': 'Carlos', 'birthday': '2000-01-01'}
    test_portfolio.add_owner(args=entry)

    sql = """
    SELECT name, birthday FROM owner WHERE id = 3
    """

    assert entry == test_portfolio.sql_fetch_one(sql)
