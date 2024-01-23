# test_app.py
# Tests for app.py
# 2024-01-22
# @juicemcpeso

import csv

import pytest


def data_file_path(table_name):
    return './test_data/' + table_name + '.csv'


def csv_to_numeric_dict_list(file_name):
    entry = list(csv.DictReader(open(file_name.replace(' ', '_'))))
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


def test_add_row_to_table(test_app_empty, app_table_name):
    expected = csv_to_numeric_dict_list(data_file_path(app_table_name))[0]
    test_app_empty.add_row_to_table(app_table_name, kwargs=expected)
    assert [expected] == test_app_empty.portfolio[app_table_name.replace(' ', '_')]


@pytest.mark.parametrize('amount', [1000, 10000, 100000])
def test_where_to_contribute(test_app_allocation, amount):
    file_name = 'expected_deviations/add_' + str(amount) + '.csv'
    expected = csv_to_numeric_dict_list(file_name)

    assert expected == test_app_allocation.where_to_contribute(amount * test_app_allocation.decimal)


@pytest.mark.skip(reason="Functionality does not currently support allocating $0")
def test_where_to_contribute_0(test_app_allocation):
    file_name = 'expected_deviations/add_' + str(0) + '.csv'
    expected = csv_to_numeric_dict_list(file_name)

    assert expected == test_app_allocation.where_to_contribute(0 * test_app_allocation.decimal)
