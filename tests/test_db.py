# test_db.py
# Tests for db.py
# 2024-01-25
# @juicemcpeso

import db
import pytest
import json
import tests.test_lookup as test_lookup
import tests.data.setup as setup
import tests.data.expected as expected
import tests.test_data_constraints as td_constraints

table_names = {'account',
               'account_type',
               'allocation',
               'asset',
               'asset_class',
               'balance',
               'component',
               'constant',
               'institution',
               'location',
               'owner',
               'price'}

view_names = {'account_value_current_by_asset',
              'allocation_deviation',
              'asset_price_newest',
              'asset_quantity_by_account_current',
              'asset_value_current',
              'asset_class_value_by_location',
              'component_value',
              'decimal',
              'net_worth'}


@pytest.mark.parametrize('table_name, column_names',
                         [('account', {'name', 'id', 'institution_id', 'owner_id', 'account_type_id'}),
                          ('account_type', {'name', 'id', 'tax_in', 'tax_growth', 'tax_out'}),
                          ('allocation', {'percentage', 'location_id', 'asset_class_id', 'id'}),
                          ('asset', {'name', 'symbol', 'id'}),
                          ('asset_class', {'name', 'id'}),
                          ('balance', {'balance_date', 'asset_id', 'account_id', 'id', 'quantity'}),
                          ('component', {'percentage', 'location_id', 'asset_id', 'asset_class_id', 'id'}),
                          ('constant', {'name', 'amount', 'id'}),
                          ('institution', {'name', 'id'}),
                          ('location', {'name', 'id'}),
                          ('owner', {'name', 'birthday', 'id'}),
                          ('price', {'asset_id', 'price_date', 'amount', 'id'})])
def test_create_table_columns(test_db_0, table_name, column_names):
    sql = f"SELECT * FROM {table_name}"

    assert set(db.column_names(database=test_db_0, cmd=sql)) == column_names


def test_create_tables(test_db_0):
    sql = """SELECT * FROM sqlite_master WHERE type = 'table'"""

    result_list = db.fetch_all(database=test_db_0, cmd=sql)

    assert set(line['name'] for line in result_list) == table_names


def test_create_views(test_db_0):
    sql = """SELECT * FROM sqlite_master WHERE type = 'view'"""

    result_list = db.fetch_all(database=test_db_0, cmd=sql)

    assert set(line['name'] for line in result_list) == view_names


# Test - insert
insert_list = [('account', db.insert_account),
               ('account_type', db.insert_account_type),
               ('allocation', db.insert_allocation),
               ('asset', db.insert_asset),
               ('asset_class', db.insert_asset_class),
               ('balance', db.insert_balance),
               ('component', db.insert_component),
               ('constant', db.insert_constant),
               ('institution', db.insert_institution),
               ('location', db.insert_location),
               ('owner', db.insert_owner),
               ('price', db.insert_price)]

insert_entry = {'account': [{'id': 1, 'name': 'Work 401k', 'account_type_id': 1, 'institution_id': 1, 'owner_id': 1}],
                'account_type': [{'id': 1, 'name': '401k', 'tax_in': 0, 'tax_growth': 0, 'tax_out': 1}],
                'allocation': [{'id': 1, 'asset_class_id': 1, 'location_id': 1, 'percentage': .4000}],
                'asset': [{'id': 1, 'name': 'Rearguard Total Stock Market Index Fund', 'symbol': 'RSUSA'}],
                'asset_class': [{'id': 1, 'name': 'stocks'}],
                'balance': [{'id': 1, 'account_id': 1, 'asset_id': 1, 'balance_date': '2021-01-01', 'quantity': 34000}],
                'component': [{'id': 1, 'asset_id': 1, 'asset_class_id': 1, 'location_id': 1, 'percentage': 1.0000}],
                'constant': [{'id': 1, 'name': 'decimal', 'amount': 10000}],
                'institution': [{'id': 1, 'name': 'Rearguard Investments'}],
                'location': [{'id': 1, 'name': 'USA'}],
                'owner': [{'id': 1, 'name': 'Bob', 'birthday': '1992-10-31'}],
                'price': [{'id': 1, 'asset_id': 1, 'price_date': '2020-01-01', 'amount': 1}]}

insert_expected = {
    'account': [{'id': 1, 'name': 'Work 401k', 'account_type_id': 1, 'institution_id': 1, 'owner_id': 1}],
    'account_type': [{'id': 1, 'name': '401k', 'tax_in': 0, 'tax_growth': 0, 'tax_out': 1}],
    'allocation': [{'id': 1, 'asset_class_id': 1, 'location_id': 1, 'percentage': 4000}],
    'asset': [{'id': 1, 'name': 'Rearguard Total Stock Market Index Fund', 'symbol': 'RSUSA'}],
    'asset_class': [{'id': 1, 'name': 'stocks'}],
    'balance': [{'id': 1, 'account_id': 1, 'asset_id': 1, 'balance_date': '2021-01-01', 'quantity': 340000000}],
    'component': [{'id': 1, 'asset_id': 1, 'asset_class_id': 1, 'location_id': 1, 'percentage': 10000}],
    'constant': [{'id': 1, 'name': 'decimal', 'amount': 10000}],
    'institution': [{'id': 1, 'name': 'Rearguard Investments'}],
    'location': [{'id': 1, 'name': 'USA'}],
    'owner': [{'id': 1, 'name': 'Bob', 'birthday': '1992-10-31'}],
    'price': [{'id': 1, 'asset_id': 1, 'price_date': '2020-01-01', 'amount': 10000}]}


@pytest.mark.parametrize('table_name, command', insert_list)
def test_insert(test_db_0, table_name, command):
    sql = f"""SELECT * FROM {table_name}"""

    db.execute_many(database=test_db_0, cmd=command, data_sequence=insert_entry[table_name])
    assert db.fetch_all(database=test_db_0, cmd=sql) == insert_expected[table_name]


insert_entry_no_id = {
    'account': [{'id': None, 'name': 'Work 401k', 'account_type_id': 1, 'institution_id': 1, 'owner_id': 1}],
    'account_type': [{'id': None, 'name': '401k', 'tax_in': 0, 'tax_growth': 0, 'tax_out': 1}],
    'allocation': [{'id': None, 'asset_class_id': 1, 'location_id': 1, 'percentage': .4000}],
    'asset': [{'id': None, 'name': 'Rearguard Total Stock Market Index Fund', 'symbol': 'RSUSA'}],
    'asset_class': [{'id': None, 'name': 'stocks'}],
    'balance': [{'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': '2021-01-01', 'quantity': 34000}],
    'component': [{'id': None, 'asset_id': 1, 'asset_class_id': 1, 'location_id': 1, 'percentage': 1.0000}],
    'constant': [{'id': None, 'name': 'decimal', 'amount': 10000}],
    'institution': [{'id': None, 'name': 'Rearguard Investments'}],
    'location': [{'id': None, 'name': 'USA'}],
    'owner': [{'id': None, 'name': 'Bob', 'birthday': '1992-10-31'}],
    'price': [{'id': None, 'asset_id': 1, 'price_date': '2020-01-01', 'amount': 1}]}


@pytest.mark.parametrize('table_name, command', insert_list)
def test_insert_no_id(test_db_0, table_name, command):
    sql = f"""SELECT * FROM {table_name}"""
    db.execute_many(database=test_db_0, cmd=command, data_sequence=insert_entry_no_id[table_name])
    assert db.fetch_all(database=test_db_0, cmd=sql) == insert_expected[table_name]


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
    assert db.fetch_all(database=test_db_0, cmd=f"SELECT * FROM {table_name}") == []


def test_deviation_levels(test_db_1):
    assert expected.deviation_levels == db.fetch_all(database=test_db_1, cmd=db.deviation_levels)


def test_allocation_deviation_with_next_level(test_db_1):
    assert expected.allocation_deviation_with_next_level == db.fetch_all(database=test_db_1,
                                                                         cmd=db.allocation_deviation_with_next_level)


def test_value_at_each_deviation_level(test_db_1):
    assert expected.value_at_each_deviation_level == db.fetch_all(database=test_db_1,
                                                                  cmd=db.value_at_each_deviation_level)


def test_value_difference_at_each_deviation_level(test_db_1):
    assert expected.value_difference_deviation_level == db.fetch_all(database=test_db_1,
                                                                     cmd=db.value_difference_at_each_deviation_level)


def test_sum_value_difference_at_each_deviation_level(test_db_1):
    assert expected.sum_value_difference_at_each_deviation_level == db.fetch_all(database=test_db_1,
                                                                                 cmd=db.sum_value_difference_at_each_deviation_level)
