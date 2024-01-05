import pytest
import portfolio
import csv


# Helper functions
def csv_to_numeric_dict_list(file_name):
    entry = list(csv.DictReader(open(file_name)))
    convert_dict_list_to_numeric(entry)
    return entry


def convert_dict_list_to_numeric(dict_list):
    for row in dict_list:
        for key in row:
            row.update({key: convert_to_numeric(row[key])})


def convert_to_numeric(item):
    numeric_output = item
    try:
        numeric_output = float(item)
    except ValueError:
        pass
    else:
        if isinstance(numeric_output, int):
            numeric_output = int(item)

    return numeric_output


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


def test_add_from_csv_account(empty_portfolio):
    file_name = './test_data/test_accounts.csv'
    empty_portfolio.add_from_csv_account(file_name)
    entry = csv_to_numeric_dict_list(file_name)

    sql = """SELECT * FROM account"""

    assert entry == empty_portfolio.sql_fetch_all_dict(sql)


def test_add_from_csv_account_type(empty_portfolio):
    file_name = './test_data/test_account_types.csv'
    empty_portfolio.add_from_csv_account_type(file_name)
    entry = csv_to_numeric_dict_list(file_name)

    sql = """SELECT * FROM account_type"""

    assert entry == empty_portfolio.sql_fetch_all_dict(sql)


def test_add_from_csv_asset(empty_portfolio):
    file_name = './test_data/test_assets.csv'
    empty_portfolio.add_from_csv_asset(file_name)
    entry = csv_to_numeric_dict_list(file_name)

    sql = """SELECT * FROM asset"""

    assert entry == empty_portfolio.sql_fetch_all_dict(sql)


def test_add_from_csv_balance(empty_portfolio):
    file_name = './test_data/test_balances.csv'
    empty_portfolio.add_from_csv_balance(file_name)
    entry = csv_to_numeric_dict_list(file_name)

    sql = """SELECT * FROM balance"""

    assert entry == empty_portfolio.sql_fetch_all_dict(sql)


def test_add_from_csv_institution(empty_portfolio):
    file_name = './test_data/test_institutions.csv'
    empty_portfolio.add_from_csv_institution(file_name)
    entry = csv_to_numeric_dict_list(file_name)

    sql = """SELECT * FROM institution"""

    assert entry == empty_portfolio.sql_fetch_all_dict(sql)


def test_add_from_csv_location(empty_portfolio):
    file_name = './test_data/test_locations.csv'
    empty_portfolio.add_from_csv_location(file_name)
    entry = csv_to_numeric_dict_list(file_name)

    sql = """SELECT * FROM location"""

    assert entry == empty_portfolio.sql_fetch_all_dict(sql)


def test_add_from_csv_owner(empty_portfolio):
    file_name = './test_data/test_owners.csv'
    empty_portfolio.add_from_csv_owner(file_name)
    entry = csv_to_numeric_dict_list(file_name)

    sql = """SELECT * FROM owner"""

    assert entry == empty_portfolio.sql_fetch_all_dict(sql)


def test_add_from_csv_price(empty_portfolio):
    file_name = './test_data/test_prices.csv'
    empty_portfolio.add_from_csv_price(file_name)
    entry = csv_to_numeric_dict_list(file_name)

    sql = """SELECT * FROM price"""

    assert entry == empty_portfolio.sql_fetch_all_dict(sql)


def test_portfolio_owners(test_portfolio):
    file_name = './test_data/test_owners.csv'
    entry = csv_to_numeric_dict_list(file_name)

    assert entry == test_portfolio['owners']


# Calculations
def test_newest_prices(test_portfolio):
    expected = [{'asset_id': 1, 'price_date': '1776-07-04', 'amount': 10000},
                {'asset_id': 2, 'price_date': '2022-01-01', 'amount': 28100},
                {'asset_id': 3, 'price_date': '2022-12-01', 'amount': 113900},
                {'asset_id': 4, 'price_date': '2022-01-01', 'amount': 478900},
                {'asset_id': 5, 'price_date': '2021-12-15', 'amount': 10000}]

    assert expected == test_portfolio.newest_prices()


def test_current_balances(test_portfolio):
    expected = [{'account_id': 1, 'asset_id': 4, 'balance_date': '2022-01-01', 'quantity': 100000},
                {'account_id': 2, 'asset_id': 3, 'balance_date': '2022-01-01', 'quantity': 75000},
                {'account_id': 3, 'asset_id': 5, 'balance_date': '2021-12-15', 'quantity': 100000000},
                {'account_id': 4, 'asset_id': 2, 'balance_date': '2022-01-01', 'quantity': 80000},
                {'account_id': 4, 'asset_id': 3, 'balance_date': '2021-01-01', 'quantity': 60000},
                {'account_id': 5, 'asset_id': 1, 'balance_date': '2022-01-01', 'quantity': 60000000}]

    assert expected == test_portfolio.current_balances()


def test_value_of_balances(test_portfolio):
    expected = [{'account_id': 1, 'asset_id': 4, 'balance_date': '2022-01-01', 'current_value': 4789000},
                {'account_id': 2, 'asset_id': 3, 'balance_date': '2022-01-01', 'current_value': 854250},
                {'account_id': 3, 'asset_id': 5, 'balance_date': '2021-12-15', 'current_value': 100000000},
                {'account_id': 4, 'asset_id': 2, 'balance_date': '2022-01-01', 'current_value': 224800},
                {'account_id': 4, 'asset_id': 3, 'balance_date': '2021-01-01', 'current_value': 683400},
                {'account_id': 5, 'asset_id': 1, 'balance_date': '2022-01-01', 'current_value': 60000000}]

    assert expected == test_portfolio.value_of_balances()


def test_net_worth(test_portfolio):
    expected = [{'net_worth': 166551450}]
    assert expected == test_portfolio.net_worth()
