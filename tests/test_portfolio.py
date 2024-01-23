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


def test_add_to_table(empty_portfolio, table_name):
    expected = csv_to_numeric_dict_list(data_file_path(table_name))[0]
    empty_portfolio.add_to_table[table_name](kwargs=expected)
    assert [expected] == empty_portfolio[table_name]


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


def test_allocation_deviation(test_portfolio_allocation):
    file_name = 'expected_deviations/add_0.csv'
    expected = csv_to_numeric_dict_list(file_name)

    assert expected == test_portfolio_allocation.allocation_deviation()
