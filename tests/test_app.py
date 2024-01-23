# test_app.py
# Tests for app.py
# 2024-01-22
# @juicemcpeso

import csv

import pytest

list_of_tables = ['account',
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


# def add_row_to_table_test(app, table_name):
#     expected = csv_to_numeric_dict_list(data_file_path(table_name))[0]
#     app.add_row_to_table(table_name, kwargs=expected)
#
#     return [expected] == app.portfolio[table_name]
#
# def add_id(dict_with_id):
#     dict_with_id.update({'id': 1})
#     return dict_with_id


@pytest.mark.parametrize("table_name", list_of_tables)
def test_add_row_to_table(test_app_empty, table_name):
    expected = csv_to_numeric_dict_list(data_file_path(table_name))[0]
    test_app_empty.add_row_to_table(table_name, kwargs=expected)
    assert [expected] == test_app_empty.portfolio[table_name]


def test_add_from_csv_account(test_app_empty):
    assert add_from_csv_test(test_app_empty, 'account')


def test_add_from_csv_account_type(test_app_empty):
    assert add_from_csv_test(test_app_empty, 'account_type')


def test_add_from_csv_allocation(test_app_empty):
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

#
# def test_add_to_table_account(test_app_empty):
#     expected = {'id': 1, 'name': 'Carlos IRA', 'account_type_id': 2, 'institution_id': 1, 'owner_id': 1}
#     test_app_empty.add_row_to_table('account', kwargs=expected)
#
#     assert [expected] == test_app_empty.portfolio['account']


# def test_add_to_table_account_type(test_app_empty):
#     expected = {'id': 1, 'name': 'Traditional IRA', 'tax_in': 0, 'tax_growth': 0, 'tax_out': 1}
#     test_app_empty.add_row_to_table('account_type', kwargs=expected)
#
#     assert [expected] == test_app_empty.portfolio['account_type']

# def test_add_to_table_account_type(test_app_empty):
#     expected = csv_to_numeric_dict_list(data_file_path('account_type'))[0]
#     test_app_empty.add_row_to_table('account_type', kwargs=expected)
#
#     assert [expected] == test_app_empty.portfolio['account_type']
#
#
# def test_add_to_table_account_type(test_app_empty):
#     assert add_row_to_table_test(test_app_empty, 'account_type')
#
#
# def test_add_to_table_allocation(test_app_empty):
#     expected = csv_to_numeric_dict_list(data_file_path('allocation'))[0]
#     # expected = {'id': 1, 'sssjjjhhkjame': 'Traditional IRA', 'tax_in': 0, 'tax_growth': 0, 'tax_out': 1}
#     test_app_empty.add_row_to_table('allocation', kwargs=expected)
#
#     assert [expected] == test_app_empty.portfolio['allocation']
#
#
# def test_add_row_to_table_account(test_app_empty):
#     assert add_row_to_table_test(test_app_empty, 'account')


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
