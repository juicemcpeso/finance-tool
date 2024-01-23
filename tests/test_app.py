# test_app.py
# Tests for app.py
# 2024-01-22
# @juicemcpeso

import csv


def data_file_path(table_name):
    return './test_data/' + table_name + '.csv'


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


def add_from_csv_test(app, table_name):
    file_name = data_file_path(table_name)
    app.add_from_csv(file_name, table_name)
    return csv_to_numeric_dict_list(file_name) == app.portfolio[table_name]


def test_add_from_csv_account(test_app_empty):
    assert add_from_csv_test(test_app_empty, 'account')


def test_add_from_csv_account_type(test_app_empty):
    assert add_from_csv_test(test_app_empty, 'account_type')


def test_add_from_csv_allocation_plan(test_app_empty):
    assert add_from_csv_test(test_app_empty, 'allocation')


def test_add_from_csv_asset(test_app_empty):
    assert add_from_csv_test(test_app_empty, 'asset')


def test_add_from_csv_balance(test_app_empty):
    assert add_from_csv_test(test_app_empty, 'balance')


def test_add_from_csv_institution(test_app_empty):
    assert add_from_csv_test(test_app_empty, 'institution')


def test_add_from_csv_location(test_app_empty):
    assert add_from_csv_test(test_app_empty, 'location')


def test_add_from_csv_owner(test_app_empty):
    assert add_from_csv_test(test_app_empty, 'owner')


def test_add_from_csv_price(test_app_empty):
    assert add_from_csv_test(test_app_empty, 'price')


def test_where_to_contribute_1000(test_app_allocation):
    file_name = 'expected_deviations/add_1000.csv'
    expected = csv_to_numeric_dict_list(file_name)

    assert expected == test_app_allocation.where_to_contribute(10000000)


def test_where_to_contribute_10000(test_app_allocation):
    file_name = 'expected_deviations/add_10000.csv'
    expected = csv_to_numeric_dict_list(file_name)

    assert expected == test_app_allocation.where_to_contribute(100000000)


def test_where_to_contribute_100000(test_app_allocation):
    file_name = 'expected_deviations/add_100000.csv'
    expected = csv_to_numeric_dict_list(file_name)

    assert expected == test_app_allocation.where_to_contribute(1000000000)
