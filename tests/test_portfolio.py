import pytest
import portfolio
import csv


def test_add_account(test_portfolio):
    entry = {'name': 'Carlos IRA', 'account_type_id': 2, 'institution_id': 1, 'owner_id': 3}
    test_portfolio.add_account(args=entry)

    sql = """
    SELECT name, account_type_id, institution_id, owner_id FROM account WHERE id = 6
    """

    assert entry == test_portfolio.sql_fetch_one(sql)


def test_add_asset(test_portfolio):
    entry = {'name': 'Test Index Fund', 'symbol': 'TEST'}
    test_portfolio.add_asset(args=entry)

    sql = """
    SELECT name, symbol FROM asset WHERE id = 6
    """

    assert entry == test_portfolio.sql_fetch_one(sql)


def test_add_balance(test_portfolio):
    entry = {'account_id': 1, 'asset_id': 4, 'balance_date': '2023-01-01', 'quantity': 12}
    test_portfolio.add_balance(args=entry)

    sql = """
    SELECT account_id, asset_id, balance_date, quantity FROM balance WHERE id = 11
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


def test_add_from_csv_owner(test_portfolio):
    entry = list(csv.DictReader(open('./test_data/test_owners.csv')))
    for row in entry:
        row['id'] = int(row['id'])

    sql = """SELECT * FROM owner"""

    assert entry == test_portfolio.sql_fetch_all_dict(sql)


def test_add_from_csv_account(test_portfolio):
    entry = list(csv.DictReader(open('./test_data/test_accounts.csv')))
    for row in entry:
        row['id'] = int(row['id'])
        row['account_type_id'] = int(row['account_type_id'])
        row['institution_id'] = int(row['institution_id'])
        row['owner_id'] = int(row['owner_id'])

    sql = """SELECT * FROM account"""

    assert entry == test_portfolio.sql_fetch_all_dict(sql)
