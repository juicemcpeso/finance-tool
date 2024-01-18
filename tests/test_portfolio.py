# test_portfolio.py
# Tests for portfolio.py
# 2024-01-16
# @juicemcpeso

import csv


# Get csv files
def data_file_path(table_name):
    return './test_data/' + table_name + '.csv'


def add_test_data_from_csv(portfolio_to_test, table_name):
    portfolio_to_test.add_from_csv(data_file_path(table_name), table_name)


def add_from_csv_test(portfolio_to_test, table_name):
    add_test_data_from_csv(portfolio_to_test, table_name)

    return numeric_test_data(table_name) == portfolio_to_test[table_name]


# Helper functions
def csv_to_numeric_dict_list(file_name):
    entry = list(csv.DictReader(open(file_name)))
    convert_dict_list_to_numeric(entry)
    return entry


def numeric_test_data(table_name):
    return csv_to_numeric_dict_list(data_file_path(table_name))


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


def sum_to_amount(test_function, key_to_sum, expected_amount):
    total = 0
    for item in test_function():
        total += item[key_to_sum]

    return total == expected_amount


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
    assert add_from_csv_test(empty_portfolio, 'accounts')


def test_add_from_csv_account_type(empty_portfolio):
    assert add_from_csv_test(empty_portfolio, 'account_types')


def test_add_from_csv_allocation_plan(empty_portfolio):
    assert add_from_csv_test(empty_portfolio, 'allocations')


def test_add_from_csv_asset(empty_portfolio):
    assert add_from_csv_test(empty_portfolio, 'assets')


def test_add_from_csv_balance(empty_portfolio):
    assert add_from_csv_test(empty_portfolio, 'balances')


def test_add_from_csv_institution(empty_portfolio):
    assert add_from_csv_test(empty_portfolio, 'institutions')


def test_add_from_csv_location(empty_portfolio):
    assert add_from_csv_test(empty_portfolio, 'locations')


def test_add_from_csv_owner(empty_portfolio):
    assert add_from_csv_test(empty_portfolio, 'owners')


def test_add_from_csv_price(empty_portfolio):
    assert add_from_csv_test(empty_portfolio, 'prices')


# Calculations
def test_asset_price_newest(test_portfolio):
    expected = [{'asset_id': 1, 'price_date': '1776-07-04', 'amount': 10000},
                {'asset_id': 2, 'price_date': '2022-01-01', 'amount': 28100},
                {'asset_id': 3, 'price_date': '2022-12-01', 'amount': 113900},
                {'asset_id': 4, 'price_date': '2022-01-01', 'amount': 478900},
                {'asset_id': 5, 'price_date': '2021-12-15', 'amount': 10000}]

    assert expected == test_portfolio.asset_price_newest()


def test_account_asset_quantity_current(test_portfolio):
    expected = [{'account_id': 1, 'asset_id': 4, 'balance_date': '2022-01-01', 'quantity': 100000},
                {'account_id': 2, 'asset_id': 3, 'balance_date': '2022-01-01', 'quantity': 75000},
                {'account_id': 3, 'asset_id': 5, 'balance_date': '2021-12-15', 'quantity': 100000000},
                {'account_id': 4, 'asset_id': 2, 'balance_date': '2022-01-01', 'quantity': 80000},
                {'account_id': 4, 'asset_id': 3, 'balance_date': '2021-01-01', 'quantity': 60000},
                {'account_id': 5, 'asset_id': 1, 'balance_date': '2022-01-01', 'quantity': 60000000}]

    assert expected == test_portfolio.account_asset_quantity_current()


def test_account_value_current_by_asset(test_portfolio):
    expected = [{'account_id': 1, 'asset_id': 4, 'balance_date': '2022-01-01', 'current_value': 4789000},
                {'account_id': 2, 'asset_id': 3, 'balance_date': '2022-01-01', 'current_value': 854250},
                {'account_id': 3, 'asset_id': 5, 'balance_date': '2021-12-15', 'current_value': 100000000},
                {'account_id': 4, 'asset_id': 2, 'balance_date': '2022-01-01', 'current_value': 224800},
                {'account_id': 4, 'asset_id': 3, 'balance_date': '2021-01-01', 'current_value': 683400},
                {'account_id': 5, 'asset_id': 1, 'balance_date': '2022-01-01', 'current_value': 60000000}]

    assert expected == test_portfolio.account_value_current_by_asset()


def test_account_value_current_by_asset_sum(test_portfolio):
    assert sum_to_amount(test_portfolio.account_value_current_by_asset, 'current_value', 166551450)


def test_net_worth(test_portfolio):
    expected = 166551450
    assert expected == test_portfolio.net_worth()


def test_asset_class_percentage(test_portfolio):
    expected = [{'asset_class_id': 1, 'percentage': 100.0 * 5593650 / 166551450},
                {'asset_class_id': 2, 'percentage': 100.0 * 100718350 / 166551450},
                {'asset_class_id': 3, 'percentage': 100.0 * 60000000 / 166551450},
                {'asset_class_id': 4, 'percentage': 100.0 * 239450 / 166551450}]

    assert expected == test_portfolio.asset_class_percentage()


def test_asset_class_percentage_sum(test_portfolio):
    assert sum_to_amount(test_portfolio.asset_class_percentage, 'percentage', 100.0)


def test_asset_class_percentage_by_location(test_portfolio):
    expected = [{'asset_class_id': 1, 'location_id': 1, 'percentage': 100.0 * 4171600 / 166551450},
                {'asset_class_id': 1, 'location_id': 2, 'percentage': 100.0 * 1422050 / 166551450},
                {'asset_class_id': 2, 'location_id': 1, 'percentage': 100.0 * 100478900 / 166551450},
                {'asset_class_id': 2, 'location_id': 2, 'percentage': 100.0 * 239450 / 166551450},
                {'asset_class_id': 3, 'location_id': 1, 'percentage': 100.0 * 60000000 / 166551450},
                {'asset_class_id': 4, 'location_id': 'NULL', 'percentage': 100.0 * 239450 / 166551450}]

    assert expected == test_portfolio.asset_class_percentage_by_location()


def test_asset_class_percentage_by_location_sum(test_portfolio):
    assert sum_to_amount(test_portfolio.asset_class_percentage_by_location, 'percentage', 100.0)


def test_asset_class_value(test_portfolio):
    expected = [{'asset_class_id': 1, 'current_value': 5593650},
                {'asset_class_id': 2, 'current_value': 100718350},
                {'asset_class_id': 3, 'current_value': 60000000},
                {'asset_class_id': 4, 'current_value': 239450}]

    assert expected == test_portfolio.asset_class_value()


def test_asset_class_value_sum(test_portfolio):
    assert sum_to_amount(test_portfolio.asset_class_value, 'current_value', 166551450)


def test_asset_class_value_by_location(test_portfolio):
    expected = [{'asset_class_id': 1, 'location_id': 1, 'current_value': 4171600},
                {'asset_class_id': 1, 'location_id': 2, 'current_value': 1422050},
                {'asset_class_id': 2, 'location_id': 1, 'current_value': 100478900},
                {'asset_class_id': 2, 'location_id': 2, 'current_value': 239450},
                {'asset_class_id': 3, 'location_id': 1, 'current_value': 60000000},
                {'asset_class_id': 4, 'location_id': 'NULL', 'current_value': 239450}]

    assert expected == test_portfolio.asset_class_value_by_location()


def test_asset_class_value_by_location_sum(test_portfolio):
    assert sum_to_amount(test_portfolio.asset_class_value_by_location, 'current_value', 166551450)


def test_asset_quantity(test_portfolio):
    expected = [{'asset_id': 1, 'quantity': 60000000},
                {'asset_id': 2, 'quantity': 80000},
                {'asset_id': 3, 'quantity': 135000},
                {'asset_id': 4, 'quantity': 100000},
                {'asset_id': 5, 'quantity': 100000000}]

    assert expected == test_portfolio.asset_quantity()


def test_asset_value_current(test_portfolio):
    expected = [{'asset_id': 1, 'current_value': 60000000},
                {'asset_id': 2, 'current_value': 224800},
                {'asset_id': 3, 'current_value': 1537650},
                {'asset_id': 4, 'current_value': 4789000},
                {'asset_id': 5, 'current_value': 100000000}]

    assert expected == test_portfolio.asset_value_current()


def test_asset_value_current_sum(test_portfolio):
    assert sum_to_amount(test_portfolio.asset_value_current, 'current_value', 166551450)


# def test_allocation_difference(test_portfolio):
#     file_name = 'expected/expected_allocation_difference.csv'
#     expected = csv_to_numeric_dict_list(file_name)
#
#     assert expected == test_portfolio.allocation_difference()
#
#
# def test_allocation_difference_after_adding(test_portfolio):
#     file_name = 'expected/expected_allocation_difference_after_adding.csv'
#     expected = csv_to_numeric_dict_list(file_name)
#
#     assert expected == test_portfolio.allocation_difference_after_addition(10000000)


# TODO - remove following 3 tests once confirmed redundant
# def test_value_by_asset_type_in_plan(test_portfolio):
#     expected = [{'asset_class_id': 1, 'location_id': 1, 'current_value': 4171600},
#                 {'asset_class_id': 1, 'location_id': 2, 'current_value': 1422050},
#                 {'asset_class_id': 2, 'location_id': 1, 'current_value': 100478900},
#                 {'asset_class_id': 2, 'location_id': 2, 'current_value': 239450},
#                 {'asset_class_id': 3, 'location_id': 1, 'current_value': 60000000}]
#
#     assert expected == test_portfolio.value_by_asset_type_in_plan()
#
#
# def test_value_by_asset_type_in_plan_future_value(test_portfolio):
#     expected = [{'asset_class_id': 1, 'location_id': 1, 'desired': 4000, 'no_buy': 236, 'yes_buy': 802},
#                 {'asset_class_id': 1, 'location_id': 2, 'desired': 2000, 'no_buy': 80, 'yes_buy': 646},
#                 {'asset_class_id': 2, 'location_id': 1, 'desired': 2500, 'no_buy': 5691, 'yes_buy': 6257},
#                 {'asset_class_id': 2, 'location_id': 2, 'desired': 500, 'no_buy': 13, 'yes_buy': 579},
#                 {'asset_class_id': 3, 'location_id': 1, 'desired': 1000, 'no_buy': 3398, 'yes_buy': 3964}]
#
#     assert expected == test_portfolio.value_by_asset_type_in_plan_future_value(10000000)
#
#
# def test_which_asset_to_buy(test_portfolio):
#     expected = [{'asset_class_id': 1, 'location_id': 1}]
#
#     assert expected == test_portfolio.which_asset_to_buy(10000000)
# TODO - end remove

# def test_allocation_deviation(test_portfolio):
#     file_name = 'expected/expected_allocation_deviation.csv'
#     expected = csv_to_numeric_dict_list(file_name)
#
#     assert expected == test_portfolio.allocation_deviation()
#
#
# def test_allocation_deviation_10000000(test_portfolio):
#     file_name = 'expected/expected_allocation_deviation_10000000.csv'
#     expected = csv_to_numeric_dict_list(file_name)
#
#     assert expected == test_portfolio.allocation_deviation(10000000)

def test_where_to_contribute_0(test_portfolio_allocation):
    expected = []

    assert expected == test_portfolio_allocation.where_to_contribute(0)


def test_where_to_contribute_1000(test_portfolio_allocation):
    expected = [{'asset_class_id': 1, 'location_id': 2, 'contribution': 10000000}]

    assert expected == test_portfolio_allocation.where_to_contribute(10000000)


# def test_where_to_contribute_10000000(test_portfolio):
#     expected = [
#
#     assert expected == test_portfolio.where_to_contribute(10000000)


def test_allocation_deviation(test_portfolio_allocation):
    file_name = 'expected_deviations/add_0.csv'
    expected = csv_to_numeric_dict_list(file_name)

    assert expected == test_portfolio_allocation.allocation_deviation()


# TODO - delete following tests as redundant
#
#
# def test_allocation_deviation_add_1000(test_portfolio_allocation):
#     file_name = 'expected_deviations/add_1000.csv'
#     expected = csv_to_numeric_dict_list(file_name)
#
#     assert expected == test_portfolio_allocation.allocation_deviation(10000000)

# def test_allocation_deviation_add_10000(test_portfolio_allocation):
#     file_name = 'expected_deviations/add_10000.csv'
#     expected = csv_to_numeric_dict_list(file_name)
#
#     assert expected == test_portfolio_allocation.allocation_deviation(100000000)
#
#
# def test_allocation_deviation_add_20000(test_portfolio_allocation):
#     file_name = 'expected_deviations/add_20000.csv'
#     expected = csv_to_numeric_dict_list(file_name)
#
#     assert expected == test_portfolio_allocation.allocation_deviation(200000000)
#
#
# def test_allocation_deviation_add_100000(test_portfolio_allocation):
#     file_name = 'expected_deviations/add_100000.csv'
#     expected = csv_to_numeric_dict_list(file_name)
#
#     assert expected == test_portfolio_allocation.allocation_deviation(1000000000)
