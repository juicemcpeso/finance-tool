import pytest
import portfolio
import csv


def test_add_account(empty_portfolio):
    entry = {'name': 'Carlos IRA', 'account_type_id': 2, 'institution_id': 1, 'owner_id': 1}
    empty_portfolio.add_account(args=entry)

    sql = """
    SELECT name, account_type_id, institution_id, owner_id FROM account WHERE id = 1
    """

    assert entry == empty_portfolio.sql_fetch_one(sql)


def test_add_account_type(empty_portfolio):
    entry = {'name': 'Traditional IRA', 'tax_in': 0, 'tax_growth': 0, 'tax_out': 1}
    empty_portfolio.add_account_type(args=entry)

    sql = """
    SELECT name, tax_in, tax_growth, tax_out FROM account_type WHERE id = 1
    """

    assert entry == empty_portfolio.sql_fetch_one(sql)


def test_add_asset(empty_portfolio):
    entry = {'name': 'Test Index Fund', 'symbol': 'TEST'}
    empty_portfolio.add_asset(args=entry)

    sql = """
    SELECT name, symbol FROM asset WHERE id = 1
    """

    assert entry == empty_portfolio.sql_fetch_one(sql)


def test_add_balance(empty_portfolio):
    entry = {'account_id': 1, 'asset_id': 4, 'balance_date': '2023-01-01', 'quantity': 12}
    empty_portfolio.add_balance(args=entry)

    sql = """
    SELECT account_id, asset_id, balance_date, quantity FROM balance WHERE id = 1
    """

    assert entry == empty_portfolio.sql_fetch_one(sql)


def test_add_owner(empty_portfolio):
    entry = {'name': 'Carlos', 'birthday': '2000-01-01'}
    empty_portfolio.add_owner(args=entry)

    sql = """
    SELECT name, birthday FROM owner WHERE id = 1
    """

    assert entry == empty_portfolio.sql_fetch_one(sql)


def test_add_price(empty_portfolio):
    entry = {'asset_id': 2, 'price_date': '2023-01-01', 'amount': 3.61}
    empty_portfolio.add_price(args=entry)

    sql = """
    SELECT asset_id, price_date, amount FROM price WHERE id = 1
    """

    assert entry == empty_portfolio.sql_fetch_one(sql)


def test_add_from_csv_owner(empty_portfolio):
    file_name = './test_data/test_owners.csv'
    empty_portfolio.add_from_csv_owner(file_name)

    entry = list(csv.DictReader(open(file_name)))
    for row in entry:
        row['id'] = int(row['id'])

    sql = """SELECT * FROM owner"""

    assert entry == empty_portfolio.sql_fetch_all_dict(sql)


def test_add_from_csv_account(empty_portfolio):
    file_name = './test_data/test_accounts.csv'
    empty_portfolio.add_from_csv_account(file_name)

    entry = list(csv.DictReader(open(file_name)))
    for row in entry:
        row['id'] = int(row['id'])
        row['account_type_id'] = int(row['account_type_id'])
        row['institution_id'] = int(row['institution_id'])
        row['owner_id'] = int(row['owner_id'])

    sql = """SELECT * FROM account"""

    assert entry == empty_portfolio.sql_fetch_all_dict(sql)


def test_add_from_csv_account_type(empty_portfolio):
    file_name = './test_data/test_account_types.csv'
    empty_portfolio.add_from_csv_account_type(file_name)

    entry = list(csv.DictReader(open(file_name)))
    for row in entry:
        row['id'] = int(row['id'])
        row['tax_in'] = int(row['tax_in'])
        row['tax_growth'] = int(row['tax_growth'])
        row['tax_out'] = int(row['tax_out'])

    sql = """SELECT * FROM account_type"""

    assert entry == empty_portfolio.sql_fetch_all_dict(sql)
