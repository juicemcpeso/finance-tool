# test_db.py
# Tests for db.py
# 2024-01-25
# @juicemcpeso

import db
import pytest

import tests.test_lookup as test_lookup
import tests.data.setup as setup
import tests.data.expected as expected
import tests.test_data_constraints as td_constraints


# TODO: make this test more clear (it checks to see if the columns in a table are correct)
@pytest.mark.parametrize('table_name', test_lookup.table_names)
def test_create_table_columns(test_db_0, table_name):
    sql = f"SELECT * FROM {table_name}"

    assert db.column_names(database=test_db_0, cmd=sql) == list(setup.db_1[table_name][0].keys())


def test_create_tables(test_db_0):
    sql = """SELECT * FROM sqlite_master WHERE type = 'table'"""

    result_list = db.fetch_all(database=test_db_0, cmd=sql)

    assert set(line['name'] for line in result_list) == test_lookup.table_names


def test_create_views(test_db_0):
    sql = """SELECT * FROM sqlite_master WHERE type = 'view'"""

    result_list = db.fetch_all(database=test_db_0, cmd=sql)

    assert set(line['name'] for line in result_list) == test_lookup.view_names


# Test - insert
@pytest.mark.parametrize('table_name, command', test_lookup.insert_sequence)
def test_insert(test_db_0, table_name, command):
    sql = f"""SELECT * FROM {table_name}"""
    test_data = setup.first_lines[table_name][0]
    db.execute(database=test_db_0, cmd=command, params=test_data)
    assert db.fetch_one(database=test_db_0, cmd=sql) == expected.first_lines[table_name][0]


@pytest.mark.parametrize('table_name, command', test_lookup.insert_sequence)
def test_insert_no_id(test_db_0, table_name, command):
    sql = f"""SELECT * FROM {table_name}"""
    test_data = setup.first_lines[table_name][0]
    test_data.update({'id': None})
    db.execute(database=test_db_0, cmd=command, params=test_data)
    test_data.update({'id': 1})
    assert db.fetch_one(database=test_db_0, cmd=sql) == expected.first_lines[table_name][0]


@pytest.mark.parametrize('table_name, command', test_lookup.insert_sequence)
def test_insert_id_2(test_db_0, table_name, command):
    sql = f"""SELECT * FROM {table_name}"""
    test_data = setup.first_lines[table_name][0]
    test_data.update({'id': 2})
    db.execute(database=test_db_0, cmd=command, params=test_data)
    response = expected.first_lines[table_name][0]
    response.update({'id': 2})
    assert db.fetch_one(database=test_db_0, cmd=sql) == response


# Test select
@pytest.mark.parametrize('table_name, command', test_lookup.select_sequence)
def test_select(test_db_2, table_name, command):
    assert expected.db_2[table_name] == db.fetch_all(database=test_db_2, cmd=command)


# Test views
def test_view_account_value_current_by_asset(test_db_2):
    expected = [{'account_id': 1, 'asset_id': 4, 'balance_date': '2022-01-01', 'current_value': 40000000},
                {'account_id': 2, 'asset_id': 3, 'balance_date': '2022-01-01', 'current_value': 40000000},
                {'account_id': 3, 'asset_id': 5, 'balance_date': '2021-12-15', 'current_value': 100000000},
                {'account_id': 4, 'asset_id': 2, 'balance_date': '2022-01-01', 'current_value': 100000000},
                {'account_id': 4, 'asset_id': 3, 'balance_date': '2021-01-01', 'current_value': 20000000},
                {'account_id': 5, 'asset_id': 1, 'balance_date': '2022-01-01', 'current_value': 200000000}]

    command = "SELECT * FROM account_value_current_by_asset"

    assert expected == db.fetch_all(database=test_db_2, cmd=command)


def test_view_allocation_deviation(test_db_1):
    command = "SELECT * FROM allocation_deviation"

    assert expected.allocation == db.fetch_all(database=test_db_1, cmd=command)


def test_view_asset_value_current(test_db_2):
    expected = [{'asset_id': 1, 'current_value': 200000000},
                {'asset_id': 2, 'current_value': 100000000},
                {'asset_id': 3, 'current_value': 60000000},
                {'asset_id': 4, 'current_value': 40000000},
                {'asset_id': 5, 'current_value': 100000000}]

    command = "SELECT * FROM asset_value_current"

    assert expected == db.fetch_all(database=test_db_2, cmd=command)


def test_view_asset_price_newest(test_db_2):
    expected = [{'asset_id': 1, 'price_date': '1776-07-04', 'amount': 10000},
                {'asset_id': 2, 'price_date': '2022-01-01', 'amount': 20000},
                {'asset_id': 3, 'price_date': '2022-12-01', 'amount': 400000},
                {'asset_id': 4, 'price_date': '2022-01-01', 'amount': 800000},
                {'asset_id': 5, 'price_date': '2021-12-15', 'amount': 10000}]

    command = "SELECT * FROM asset_price_newest"

    assert expected == db.fetch_all(database=test_db_2, cmd=command)


def test_view_asset_quantity_by_account_current(test_db_2):
    expected = [{'account_id': 1, 'asset_id': 4, 'balance_date': '2022-01-01', 'quantity': 500000},
                {'account_id': 2, 'asset_id': 3, 'balance_date': '2022-01-01', 'quantity': 1000000},
                {'account_id': 3, 'asset_id': 5, 'balance_date': '2021-12-15', 'quantity': 100000000},
                {'account_id': 4, 'asset_id': 2, 'balance_date': '2022-01-01', 'quantity': 50000000},
                {'account_id': 4, 'asset_id': 3, 'balance_date': '2021-01-01', 'quantity': 500000},
                {'account_id': 5, 'asset_id': 1, 'balance_date': '2022-01-01', 'quantity': 200000000}]

    command = "SELECT * FROM asset_quantity_by_account_current"

    assert expected == db.fetch_all(database=test_db_2, cmd=command)


def test_view_asset_class_value_by_location(test_db_2):
    expected = [{'asset_class_id': 1, 'location_id': 1, 'current_value': 82000000},
                {'asset_class_id': 1, 'location_id': 2, 'current_value': 110000000},
                {'asset_class_id': 2, 'location_id': 1, 'current_value': 104000000},
                {'asset_class_id': 2, 'location_id': 2, 'current_value': 2000000},
                {'asset_class_id': 3, 'location_id': 1, 'current_value': 200000000},
                {'asset_class_id': 4, 'location_id': None, 'current_value': 2000000}]

    command = "SELECT * FROM asset_class_value_by_location"

    assert expected == db.fetch_all(database=test_db_2, cmd=command)


def test_view_component_value(test_db_2):
    expected = [{'asset_id': 1, 'asset_class_id': 3, 'location_id': 1, 'current_value': 200000000},
                {'asset_id': 2, 'asset_class_id': 1, 'location_id': 2, 'current_value': 100000000},
                {'asset_id': 3, 'asset_class_id': 1, 'location_id': 1, 'current_value': 60000000},
                {'asset_id': 4, 'asset_class_id': 1, 'location_id': 1, 'current_value': 22000000},
                {'asset_id': 4, 'asset_class_id': 1, 'location_id': 2, 'current_value': 10000000},
                {'asset_id': 4, 'asset_class_id': 2, 'location_id': 1, 'current_value': 4000000},
                {'asset_id': 4, 'asset_class_id': 2, 'location_id': 2, 'current_value': 2000000},
                {'asset_id': 4, 'asset_class_id': 4, 'location_id': None, 'current_value': 2000000},
                {'asset_id': 5, 'asset_class_id': 2, 'location_id': 1, 'current_value': 100000000}]

    command = "SELECT * FROM component_value"

    assert expected == db.fetch_all(database=test_db_2, cmd=command)


def test_view_decimal(test_db_2):
    expected = {'constant': 10000}

    command = "SELECT * FROM decimal"

    assert expected == db.fetch_one(database=test_db_2, cmd=command)


def test_view_net_worth(test_db_2):
    expected = {'net_worth': 500000000}

    command = "SELECT * FROM net_worth"

    assert expected == db.fetch_one(database=test_db_2, cmd=command)


# Test calculations
def test_net_worth_formatted(test_db_2):
    assert db.fetch_one(database=test_db_2, cmd=db.net_worth_formatted) == {'net_worth': 50000.0}


@pytest.mark.parametrize('table_name, expected', td_constraints.formatted_expected)
def test_constraints(test_db_0, table_name, expected):
    db.execute(database=test_db_0, cmd=test_lookup.insert_dict[table_name], params=expected)

    assert db.fetch_all(database=test_db_0, cmd=test_lookup.select_dict[table_name]) == []


def test_deviation_levels(test_db_1):
    assert expected.deviation_levels == db.fetch_all(database=test_db_1, cmd=db.deviation_levels)


def test_allocation_deviation_with_next_level(test_db_1):
    assert expected.allocation_deviation_with_next_level == db.fetch_all(database=test_db_1, cmd=db.allocation_deviation_with_next_level)


def test_value_at_each_deviation_level(test_db_1):
    assert expected.value_at_each_deviation_level == db.fetch_all(database=test_db_1, cmd=db.value_at_each_deviation_level)


def test_value_difference_at_each_deviation_level(test_db_1):
    assert expected.value_difference_deviation_level == db.fetch_all(database=test_db_1, cmd=db.value_difference_at_each_deviation_level)


def test_sum_value_difference_at_each_deviation_level(test_db_1):
    assert expected.sum_value_difference_at_each_deviation_level == db.fetch_all(database=test_db_1, cmd=db.sum_value_difference_at_each_deviation_level)