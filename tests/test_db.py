# test_db.py
# Tests for db.py
# 2024-01-25
# @juicemcpeso

import db
import pytest

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
insert_dict = {'account': db.insert_account,
               'account_type': db.insert_account_type,
               'allocation': db.insert_allocation,
               'asset': db.insert_asset,
               'asset_class': db.insert_asset_class,
               'balance': db.insert_balance,
               'component': db.insert_component,
               'constant': db.insert_constant,
               'institution': db.insert_institution,
               'location': db.insert_location,
               'owner': db.insert_owner,
               'price': db.insert_price}

insert_sequence = {(table_name, sql) for table_name, sql in insert_dict.items()}
#
# insert_list = [('account', db.insert_account),
#                ('account_type', db.insert_account_type),
#                ('allocation', db.insert_allocation),
#                ('asset', db.insert_asset),
#                ('asset_class', db.insert_asset_class),
#                ('balance', db.insert_balance),
#                ('component', db.insert_component),
#                ('constant', db.insert_constant),
#                ('institution', db.insert_institution),
#                ('location', db.insert_location),
#                ('owner', db.insert_owner),
#                ('price', db.insert_price)]

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


@pytest.mark.parametrize('table_name, command', insert_sequence)
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


@pytest.mark.parametrize('table_name, command', insert_sequence)
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
    expected = [{'asset_class_id': 1,
                 'location_id': 2,
                 'current_value': 140000000,
                 'plan_percent': 2000,
                 'plan_value': 200000000,
                 'deviation': -3000},
                {'asset_class_id': 2,
                 'location_id': 2,
                 'current_value': 40000000,
                 'plan_percent': 500,
                 'plan_value': 50000000,
                 'deviation': -2000},
                {'asset_class_id': 1,
                 'location_id': 1,
                 'current_value': 340000000,
                 'plan_percent': 4000,
                 'plan_value': 400000000,
                 'deviation': -1500},
                {'asset_class_id': 2,
                 'location_id': 1,
                 'current_value': 340000000,
                 'plan_percent': 2500,
                 'plan_value': 250000000,
                 'deviation': 3600},
                {'asset_class_id': 3,
                 'location_id': 1,
                 'current_value': 140000000,
                 'plan_percent': 1000,
                 'plan_value': 100000000,
                 'deviation': 4000}]

    command = "SELECT * FROM allocation_deviation"

    assert db.fetch_all(database=test_db_1, cmd=command) == expected


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


# Test constraints
expected_constraints = [{'table': 'account',
                         'expected': {'id': None, 'name': None, 'account_type_id': 0, 'institution_id': 0,
                                      'owner_id': 0}},
                        {'table': 'account_type',
                         'expected': {'id': None, 'name': 'test', 'tax_in': 1, 'tax_growth': 4, 'tax_out': 0}},
                        {'table': 'account_type',
                         'expected': {'id': None, 'name': None, 'tax_in': 1, 'tax_growth': 0, 'tax_out': 0}},
                        {'table': 'allocation',
                         'expected': {'id': None, 'asset_class_id': 1, 'location_id': 1, 'percentage': 3}},
                        {'table': 'allocation',
                         'expected': {'id': None, 'asset_class_id': 1, 'location_id': 1, 'percentage': 'test'}},
                        {'table': 'allocation',
                         'expected': {'id': None, 'asset_class_id': 1, 'location_id': 1, 'percentage': None}},
                        {'table': 'asset',
                         'expected': {'id': None, 'name': 'test', 'symbol': None}},
                        {'table': 'asset',
                         'expected': {'id': None, 'name': None, 'symbol': 'TEST'}},
                        {'table': 'asset_class',
                         'expected': {'id': None, 'name': None}},
                        {'table': 'balance',
                         'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': 6, 'quantity': 1}},
                        {'table': 'balance',
                         'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': 'test',
                                      'quantity': 1}},
                        {'table': 'balance',
                         'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': 'April 16, 2023',
                                      'quantity': 1}},
                        {'table': 'balance',
                         'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': '2024-15-43',
                                      'quantity': 1}},
                        {'table': 'balance',
                         'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': None, 'quantity': 1}},
                        {'table': 'balance',
                         'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': '2022-01-01',
                                      'quantity': None}},
                        {'table': 'balance',
                         'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': '2022-01-01',
                                      'quantity': 'test'}},
                        {'table': 'balance',
                         'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': '2022-01-01',
                                      'quantity': ''}},
                        {'table': 'balance',
                         'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': '2022-01-01',
                                      'quantity': -123}},
                        {'table': 'component',
                         'expected': {'id': None, 'asset_id': 1, 'asset_class_id': 1, 'location_id': 1,
                                      'percentage': 1.01}},
                        {'table': 'component',
                         'expected': {'id': None, 'asset_id': 1, 'asset_class_id': 1, 'location_id': 1,
                                      'percentage': -0.01}},
                        {'table': 'institution',
                         'expected': {'id': None, 'name': None}},
                        {'table': 'location',
                         'expected': {'id': None, 'name': None}},
                        {'table': 'owner',
                         'expected': {'id': None, 'name': None, 'birthday': '2021-01-01'}},
                        {'table': 'owner',
                         'expected': {'id': None, 'name': 'test', 'birthday': 'test'}},
                        {'table': 'owner',
                         'expected': {'id': None, 'name': 'test', 'birthday': ''}},
                        {'table': 'owner',
                         'expected': {'id': None, 'name': 'test', 'birthday': '2024-15-43'}},
                        {'table': 'owner',
                         'expected': {'id': None, 'name': 'test', 'birthday': 'April 16, 2023'}},
                        {'table': 'owner',
                         'expected': {'id': None, 'name': 'test', 'birthday': None}},
                        {'table': 'owner',
                         'expected': {'id': None, 'name': 'test', 'birthday': 6}},
                        {'table': 'price',
                         'expected': {'id': None, 'asset_id': 1, 'price_date': '2022-01-01', 'amount': ''}},
                        {'table': 'price',
                         'expected': {'id': None, 'asset_id': 1, 'price_date': '2022-01-01', 'amount': None}},
                        {'table': 'price',
                         'expected': {'id': None, 'asset_id': 1, 'price_date': '2022-01-01', 'amount': 'six'}},
                        {'table': 'price',
                         'expected': {'id': None, 'asset_id': 1, 'price_date': '2024-51-51', 'amount': 1}},
                        {'table': 'price',
                         'expected': {'id': None, 'asset_id': 1, 'price_date': 'test', 'amount': 1}},
                        {'table': 'price',
                         'expected': {'id': None, 'asset_id': 1, 'price_date': None, 'amount': 1}},
                        {'table': 'price',
                         'expected': {'id': None, 'asset_id': 1, 'price_date': 'April 16, 2023', 'amount': 1}},
                        {'table': 'price',
                         'expected': {'id': None, 'asset_id': 1, 'price_date': 6, 'amount': 1}},
                        {'table': 'price',
                         'expected': {'id': None, 'asset_id': 1, 'price_date': '', 'amount': 1}}]

formatted_expected_constraints = [(line['table'], line['expected']) for line in expected_constraints]


@pytest.mark.parametrize('table_name, expected', formatted_expected_constraints)
def test_constraints(test_db_0, table_name, expected):
    db.execute(database=test_db_0, cmd=insert_dict[table_name], params=expected)
    assert db.fetch_all(database=test_db_0, cmd=f"SELECT * FROM {table_name}") == []


def test_deviation_levels(test_db_1):
    expected = [{'deviation': -3000},
                {'deviation': -2000},
                {'deviation': -1500},
                {'deviation': 3600},
                {'deviation': 4000}]
    assert db.fetch_all(database=test_db_1, cmd=db.deviation_levels) == expected


def test_allocation_deviation_with_next_level(test_db_1):
    expected = [{'asset_class_id': 1,
                 'location_id': 2,
                 'current_value': 140000000,
                 'plan_percent': 2000,
                 'plan_value': 200000000,
                 'deviation': -3000,
                 'next_deviation': -2000},
                {'asset_class_id': 1,
                 'location_id': 2,
                 'current_value': 140000000,
                 'plan_percent': 2000,
                 'plan_value': 200000000,
                 'deviation': -3000,
                 'next_deviation': -1500},
                {'asset_class_id': 1,
                 'location_id': 2,
                 'current_value': 140000000,
                 'plan_percent': 2000,
                 'plan_value': 200000000,
                 'deviation': -3000,
                 'next_deviation': 3600},
                {'asset_class_id': 1,
                 'location_id': 2,
                 'current_value': 140000000,
                 'plan_percent': 2000,
                 'plan_value': 200000000,
                 'deviation': -3000,
                 'next_deviation': 4000},
                {'asset_class_id': 2,
                 'location_id': 2,
                 'current_value': 40000000,
                 'plan_percent': 500,
                 'plan_value': 50000000,
                 'deviation': -2000,
                 'next_deviation': -1500},
                {'asset_class_id': 2,
                 'location_id': 2,
                 'current_value': 40000000,
                 'plan_percent': 500,
                 'plan_value': 50000000,
                 'deviation': -2000,
                 'next_deviation': 3600},
                {'asset_class_id': 2,
                 'location_id': 2,
                 'current_value': 40000000,
                 'plan_percent': 500,
                 'plan_value': 50000000,
                 'deviation': -2000,
                 'next_deviation': 4000},
                {'asset_class_id': 1,
                 'location_id': 1,
                 'current_value': 340000000,
                 'plan_percent': 4000,
                 'plan_value': 400000000,
                 'deviation': -1500,
                 'next_deviation': 3600},
                {'asset_class_id': 1,
                 'location_id': 1,
                 'current_value': 340000000,
                 'plan_percent': 4000,
                 'plan_value': 400000000,
                 'deviation': -1500,
                 'next_deviation': 4000},
                {'asset_class_id': 2,
                 'location_id': 1,
                 'current_value': 340000000,
                 'plan_percent': 2500,
                 'plan_value': 250000000,
                 'deviation': 3600,
                 'next_deviation': 4000}]

    assert expected == db.fetch_all(database=test_db_1, cmd=db.allocation_deviation_with_next_level)


def test_value_at_each_deviation_level(test_db_1):
    expected = [{'asset_class_id': 1,
                 'location_id': 2,
                 'current_value': 140000000,
                 'plan_percent': 2000,
                 'plan_value': 200000000,
                 'deviation': -3000,
                 'level_value': 160000000,
                 'next_deviation': -2000},
                {'asset_class_id': 1,
                 'location_id': 2,
                 'current_value': 140000000,
                 'plan_percent': 2000,
                 'plan_value': 200000000,
                 'deviation': -3000,
                 'level_value': 170000000,
                 'next_deviation': -1500},
                {'asset_class_id': 1,
                 'location_id': 2,
                 'current_value': 140000000,
                 'plan_percent': 2000,
                 'plan_value': 200000000,
                 'deviation': -3000,
                 'level_value': 272000000,
                 'next_deviation': 3600},
                {'asset_class_id': 1,
                 'location_id': 2,
                 'current_value': 140000000,
                 'plan_percent': 2000,
                 'plan_value': 200000000,
                 'deviation': -3000,
                 'level_value': 280000000,
                 'next_deviation': 4000},
                {'asset_class_id': 2,
                 'location_id': 2,
                 'current_value': 40000000,
                 'plan_percent': 500,
                 'plan_value': 50000000,
                 'deviation': -2000,
                 'level_value': 42500000,
                 'next_deviation': -1500},
                {'asset_class_id': 2,
                 'location_id': 2,
                 'current_value': 40000000,
                 'plan_percent': 500,
                 'plan_value': 50000000,
                 'deviation': -2000,
                 'level_value': 68000000,
                 'next_deviation': 3600},
                {'asset_class_id': 2,
                 'location_id': 2,
                 'current_value': 40000000,
                 'plan_percent': 500,
                 'plan_value': 50000000,
                 'deviation': -2000,
                 'level_value': 70000000,
                 'next_deviation': 4000},
                {'asset_class_id': 1,
                 'location_id': 1,
                 'current_value': 340000000,
                 'plan_percent': 4000,
                 'plan_value': 400000000,
                 'deviation': -1500,
                 'level_value': 544000000,
                 'next_deviation': 3600},
                {'asset_class_id': 1,
                 'location_id': 1,
                 'current_value': 340000000,
                 'plan_percent': 4000,
                 'plan_value': 400000000,
                 'deviation': -1500,
                 'level_value': 560000000,
                 'next_deviation': 4000},
                {'asset_class_id': 2,
                 'location_id': 1,
                 'current_value': 340000000,
                 'plan_percent': 2500,
                 'plan_value': 250000000,
                 'deviation': 3600,
                 'level_value': 350000000,
                 'next_deviation': 4000}]

    assert expected == db.fetch_all(database=test_db_1, cmd=db.value_at_each_deviation_level)


def test_value_difference_at_each_deviation_level(test_db_1):
    expected = [{'asset_class_id': 1,
                 'location_id': 2,
                 'current_value': 140000000,
                 'plan_percent': 2000,
                 'plan_value': 200000000,
                 'deviation': -3000,
                 'level_value': 160000000,
                 'value_difference': 20000000,
                 'next_deviation': -2000},
                {'asset_class_id': 1,
                 'location_id': 2,
                 'current_value': 140000000,
                 'plan_percent': 2000,
                 'plan_value': 200000000,
                 'deviation': -3000,
                 'level_value': 170000000,
                 'value_difference': 30000000,
                 'next_deviation': -1500},
                {'asset_class_id': 1,
                 'location_id': 2,
                 'current_value': 140000000,
                 'plan_percent': 2000,
                 'plan_value': 200000000,
                 'deviation': -3000,
                 'level_value': 272000000,
                 'value_difference': 132000000,
                 'next_deviation': 3600},
                {'asset_class_id': 1,
                 'location_id': 2,
                 'current_value': 140000000,
                 'plan_percent': 2000,
                 'plan_value': 200000000,
                 'deviation': -3000,
                 'level_value': 280000000,
                 'value_difference': 140000000,
                 'next_deviation': 4000},
                {'asset_class_id': 2,
                 'location_id': 2,
                 'current_value': 40000000,
                 'plan_percent': 500,
                 'plan_value': 50000000,
                 'deviation': -2000,
                 'level_value': 42500000,
                 'value_difference': 2500000,
                 'next_deviation': -1500},
                {'asset_class_id': 2,
                 'location_id': 2,
                 'current_value': 40000000,
                 'plan_percent': 500,
                 'plan_value': 50000000,
                 'deviation': -2000,
                 'level_value': 68000000,
                 'value_difference': 28000000,
                 'next_deviation': 3600},
                {'asset_class_id': 2,
                 'location_id': 2,
                 'current_value': 40000000,
                 'plan_percent': 500,
                 'plan_value': 50000000,
                 'deviation': -2000,
                 'level_value': 70000000,
                 'value_difference': 30000000,
                 'next_deviation': 4000},
                {'asset_class_id': 1,
                 'location_id': 1,
                 'current_value': 340000000,
                 'plan_percent': 4000,
                 'plan_value': 400000000,
                 'deviation': -1500,
                 'level_value': 544000000,
                 'value_difference': 204000000,
                 'next_deviation': 3600},
                {'asset_class_id': 1,
                 'location_id': 1,
                 'current_value': 340000000,
                 'plan_percent': 4000,
                 'plan_value': 400000000,
                 'deviation': -1500,
                 'level_value': 560000000,
                 'value_difference': 220000000,
                 'next_deviation': 4000},
                {'asset_class_id': 2,
                 'location_id': 1,
                 'current_value': 340000000,
                 'plan_percent': 2500,
                 'plan_value': 250000000,
                 'deviation': 3600,
                 'level_value': 350000000,
                 'value_difference': 10000000,
                 'next_deviation': 4000}]

    assert expected == db.fetch_all(database=test_db_1, cmd=db.value_difference_at_each_deviation_level)


def test_sum_value_difference_at_each_deviation_level(test_db_1):
    expected = [{'deviation': -3000, 'total_difference': 0},
                {'deviation': -2000, 'total_difference': 20000000},
                {'deviation': -1500, 'total_difference': 32500000},
                {'deviation': 3600, 'total_difference': 364000000},
                {'deviation': 4000, 'total_difference': 400000000}]

    assert expected == db.fetch_all(database=test_db_1, cmd=db.sum_value_difference_at_each_deviation_level)


@pytest.mark.parametrize('contribution, expected', [(0, {'deviation': -3000}),
                                                    (1000, {'deviation': -3000}),
                                                    (10000, {'deviation': -1500}),
                                                    (100000, {'deviation': 4000})])
def test_which_deviation_level(test_db_1, contribution, expected):
    assert expected == db.fetch_one(database=test_db_1, cmd=db.which_deviation_level,
                                    params={'contribution': contribution})


@pytest.mark.parametrize('contribution, expected', [(0, []),
                                                    (1000, []),
                                                    (10000, [{'asset_class_id': 1,
                                                              'location_id': 2,
                                                              'contribution': 30000000},
                                                             {'asset_class_id': 2,
                                                              'location_id': 2,
                                                              'contribution': 2500000}]),
                                                    (100000, [{'asset_class_id': 1,
                                                               'location_id': 1,
                                                               'contribution': 220000000},
                                                              {'asset_class_id': 1,
                                                               'location_id': 2,
                                                               'contribution': 140000000},
                                                              {'asset_class_id': 2,
                                                               'location_id': 2,
                                                               'contribution': 30000000},
                                                              {'asset_class_id': 2,
                                                               'location_id': 1,
                                                               'contribution': 10000000}])])
def test_fill_full_amounts(test_db_1, contribution, expected):
    assert expected == db.fetch_all(database=test_db_1, cmd=db.fill_full_amounts,
                                    params={'contribution': contribution})


@pytest.mark.parametrize('contribution, expected', [(0, []),
                                                    (1000, [{'asset_class_id': 1,
                                                             'location_id': 2,
                                                             'contribution': 0}]),
                                                    (10000, [{'asset_class_id': 1,
                                                              'location_id': 2,
                                                              'contribution': 30000000},
                                                             {'asset_class_id': 2,
                                                              'location_id': 2,
                                                              'contribution': 2500000},
                                                             {'asset_class_id': 1,
                                                              'location_id': 1,
                                                              'contribution': 0}]),
                                                    (100000, [{'asset_class_id': 1,
                                                               'location_id': 1,
                                                               'contribution': 220000000},
                                                              {'asset_class_id': 1,
                                                               'location_id': 2,
                                                               'contribution': 140000000},
                                                              {'asset_class_id': 2,
                                                               'location_id': 2,
                                                               'contribution': 30000000},
                                                              {'asset_class_id': 2,
                                                               'location_id': 1,
                                                               'contribution': 10000000},
                                                              {'asset_class_id': 3,
                                                               'location_id': 1,
                                                               'contribution': 0}])])
def test_fill_full_amounts_inclusive(test_db_1, contribution, expected):
    assert expected == db.fetch_all(database=test_db_1, cmd=db.fill_full_amounts_inclusive,
                                    params={'contribution': contribution})


@pytest.mark.parametrize('contribution, expected', [(0, []),
                                                    (1000, [{'asset_class_id': 1,
                                                             'location_id': 2}]),
                                                    (10000, [{'asset_class_id': 1,
                                                              'location_id': 1},
                                                             {'asset_class_id': 1,
                                                              'location_id': 2},
                                                             {'asset_class_id': 2,
                                                              'location_id': 2}]),
                                                    (100000, [{'asset_class_id': 1,
                                                               'location_id': 1},
                                                              {'asset_class_id': 1,
                                                               'location_id': 2},
                                                              {'asset_class_id': 2,
                                                               'location_id': 1},
                                                              {'asset_class_id': 2,
                                                               'location_id': 2},
                                                              {'asset_class_id': 3,
                                                               'location_id': 1}])])
def test_which_accounts_receive_funds(test_db_1, contribution, expected):
    assert expected == db.fetch_all(database=test_db_1, cmd=db.which_accounts_receive_funds,
                                    params={'contribution': contribution})


@pytest.mark.parametrize('contribution, expected', [(0, {'remainder': 0}),
                                                    (1000, {'remainder': 10000000}),
                                                    (10000, {'remainder': 67500000}),
                                                    (100000, {'remainder': 600000000})])
def test_remaining_amount(test_db_1, contribution, expected):
    assert expected == db.fetch_one(database=test_db_1, cmd=db.remaining_amount,
                                    params={'contribution': contribution})


@pytest.mark.parametrize('contribution, expected', [(0, []),
                                                    (1000, [{'asset_class_id': 1,
                                                             'location_id': 2,
                                                             'contribution': 10000000}]),
                                                    (10000, [{'asset_class_id': 1,
                                                              'location_id': 1,
                                                              'contribution': 41538461},
                                                             {'asset_class_id': 1,
                                                              'location_id': 2,
                                                              'contribution': 20769230},
                                                             {'asset_class_id': 2,
                                                              'location_id': 2,
                                                              'contribution': 5192307}]),
                                                    (100000, [{'asset_class_id': 1,
                                                               'location_id': 1,
                                                               'contribution': 240000000},
                                                              {'asset_class_id': 1,
                                                               'location_id': 2,
                                                               'contribution': 120000000},
                                                              {'asset_class_id': 2,
                                                               'location_id': 1,
                                                               'contribution': 150000000},
                                                              {'asset_class_id': 2,
                                                               'location_id': 2,
                                                               'contribution': 30000000},
                                                              {'asset_class_id': 3,
                                                               'location_id': 1,
                                                               'contribution': 60000000}])])
def test_assign_remainder_proportionally(test_db_1, contribution, expected):
    assert expected == db.fetch_all(database=test_db_1, cmd=db.assign_remainder_proportionally,
                                    params={'contribution': contribution})


@pytest.mark.parametrize('contribution, expected', [(0, []),
                                                    (1000, [{'asset_class_id': 1,
                                                             'location_id': 2,
                                                             'contribution': 10000000}]),
                                                    (10000, [{'asset_class_id': 1,
                                                              'location_id': 1,
                                                              'contribution': 41538461},
                                                             {'asset_class_id': 1,
                                                              'location_id': 2,
                                                              'contribution': 50769230},
                                                             {'asset_class_id': 2,
                                                              'location_id': 2,
                                                              'contribution': 7692307}]),
                                                    (100000, [{'asset_class_id': 1,
                                                               'location_id': 1,
                                                               'contribution': 460000000},
                                                              {'asset_class_id': 1,
                                                               'location_id': 2,
                                                               'contribution': 260000000},
                                                              {'asset_class_id': 2,
                                                               'location_id': 1,
                                                               'contribution': 160000000},
                                                              {'asset_class_id': 2,
                                                               'location_id': 2,
                                                               'contribution': 60000000},
                                                              {'asset_class_id': 3,
                                                               'location_id': 1,
                                                               'contribution': 60000000}])])
def test_where_to_contribute(test_db_1, contribution, expected):
    assert expected == db.fetch_all(database=test_db_1, cmd=db.where_to_contribute,
                                    params={'contribution': contribution})
