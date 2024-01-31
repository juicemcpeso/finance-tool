# test_db.py
# Tests for db.py
# 2024-01-25
# @juicemcpeso

import db
import pytest
import sqlite3

import tests.test_data as td
import tests.test_data_deviation as td_deviation
import tests.test_data_constraints as td_constraints

# TODO - remove once no longer needed
# def csv_to_dict(directory):
#     test_dict = {}
#     for table_name_tuple in create_table_sequence:
#         table_name = table_name_tuple[0]
#         file_path = directory + table_name + '.csv'
#         test_dict.update({table_name: list(csv.DictReader(open(file_path)))})
#     return test_dict
#
#
# def print_csv_as_dict(directory):
#     test_dict = csv_to_dict(directory)
#     for key in sorted(test_dict):
#         print(f"\'{key}\': {test_dict[key]},")
#     assert True
#
#
# def test_print_csv():
#     print_csv_as_dict('./old_test_data/')


table_names = {'account',
               'account_type',
               'allocation',
               'asset',
               'asset_class',
               'balance',
               'component',
               'institution',
               'location',
               'owner',
               'price'}

view_names = {'account_value_current_by_asset',
              'asset_price_newest',
              'asset_quantity_by_account_current',
              'asset_value_current',
              'asset_class_value_by_location',
              'component_value'}

create_view_sequence = {('account_value_current_by_asset', db.create_view_account_value_current_by_asset),
                        ('asset_price_newest', db.create_view_asset_price_newest),
                        ('asset_quantity_by_account_current', db.create_view_asset_quantity_by_account_current),
                        ('asset_value_current', db.create_view_asset_value_current),
                        ('asset_class_value_by_location', db.create_view_asset_class_value_by_location),
                        ('component_value', db.create_view_component_value)}

create_table_sequence = {('account', db.create_table_account),
                         ('account_type', db.create_table_account_type),
                         ('allocation', db.create_table_allocation),
                         ('asset', db.create_table_asset),
                         ('asset_class', db.create_table_asset_class),
                         ('balance', db.create_table_balance),
                         ('component', db.create_table_component),
                         ('institution', db.create_table_institution),
                         ('location', db.create_table_location),
                         ('owner', db.create_table_owner),
                         ('price', db.create_table_price)}

insert_sequence = {('account', db.insert_account),
                   ('account_type', db.insert_account_type),
                   ('allocation', db.insert_allocation),
                   ('asset', db.insert_asset),
                   ('asset_class', db.insert_asset_class),
                   ('balance', db.insert_balance),
                   ('component', db.insert_component),
                   ('institution', db.insert_institution),
                   ('location', db.insert_location),
                   ('owner', db.insert_owner),
                   ('price', db.insert_price)}

select_sequence = {('account', db.select_account),
                   ('account_type', db.select_account_type),
                   ('allocation', db.select_allocation),
                   ('asset', db.select_asset),
                   ('asset_class', db.select_asset_class),
                   ('balance', db.select_balance),
                   ('component', db.select_component),
                   ('institution', db.select_institution),
                   ('location', db.select_location),
                   ('owner', db.select_owner),
                   ('price', db.select_price)}

insert_dict = {'account': db.insert_account,
               'account_type': db.insert_account_type,
               'allocation': db.insert_allocation,
               'asset': db.insert_asset,
               'asset_class': db.insert_asset_class,
               'balance': db.insert_balance,
               'component': db.insert_component,
               'institution': db.insert_institution,
               'location': db.insert_location,
               'owner': db.insert_owner,
               'price': db.insert_price}


select_dict = {'account': db.select_account,
               'account_type': db.select_account_type,
               'allocation': db.select_allocation,
               'asset': db.select_asset,
               'asset_class': db.select_asset_class,
               'balance': db.select_balance,
               'component': db.select_component,
               'institution': db.select_institution,
               'location': db.select_location,
               'owner': db.select_owner,
               'price': db.select_price}


@pytest.mark.parametrize('table_name, command', create_table_sequence)
def test_create_table(tmp_path, table_name, command):
    db_test = tmp_path / "test.db"
    db.execute(database=db_test, cmd=command)

    sql = """SELECT * FROM sqlite_master WHERE type = 'table'"""

    assert db.fetch_all(database=db_test, cmd=sql)[0]['name'] == table_name
    assert len(db.fetch_all(database=db_test, cmd=sql)) == 1


@pytest.mark.parametrize('table_name, command', create_table_sequence)
def test_create_table_columns(tmp_path, table_name, command):
    db_test = tmp_path / "test.db"
    db.execute(database=db_test, cmd=command)

    sql = f"SELECT * FROM {table_name}"

    assert db.column_names(database=db_test, cmd=sql) == list(td.db_1[table_name][0].keys())


def test_create_tables(tmp_path):
    db_test = tmp_path / "test.db"
    db.execute_script(database=db_test, cmd=db.create_tables)

    sql = """SELECT * FROM sqlite_master WHERE type = 'table'"""

    result_list = db.fetch_all(database=db_test, cmd=sql)

    assert set(line['name'] for line in result_list) == table_names


def test_create_tables_test_db_0(test_db_0):
    sql = """SELECT * FROM sqlite_master WHERE type = 'table'"""

    result_list = db.fetch_all(database=test_db_0, cmd=sql)

    assert set(line['name'] for line in result_list) == table_names


@pytest.mark.parametrize('view_name, command', create_view_sequence)
def test_create_view(tmp_path, view_name, command):
    db_test = tmp_path / "test.db"
    db.execute(database=db_test, cmd=command)

    sql = """SELECT * FROM sqlite_master WHERE type = 'view'"""

    assert db.fetch_all(database=db_test, cmd=sql)[0]['name'] == view_name
    assert len(db.fetch_all(database=db_test, cmd=sql)) == 1


def test_create_views(tmp_path):
    db_test = tmp_path / "test.db"
    db.execute_script(database=db_test, cmd=db.create_views)

    sql = """SELECT * FROM sqlite_master WHERE type = 'view'"""

    result_list = db.fetch_all(database=db_test, cmd=sql)

    assert set(line['name'] for line in result_list) == view_names


def test_create_views_test_db_0(test_db_0):
    sql = """SELECT * FROM sqlite_master WHERE type = 'view'"""

    result_list = db.fetch_all(database=test_db_0, cmd=sql)

    assert set(line['name'] for line in result_list) == view_names


# Test - insert
@pytest.mark.parametrize('table_name, command', insert_sequence)
def test_insert(test_db_0, table_name, command):
    sql = f"""SELECT * FROM {table_name}"""
    test_data = td.first_lines[table_name][0]
    db.execute(database=test_db_0, cmd=command, params=test_data)
    assert db.fetch_one(database=test_db_0, cmd=sql) == test_data


@pytest.mark.parametrize('table_name, command', insert_sequence)
def test_insert_no_id(test_db_0, table_name, command):
    sql = f"""SELECT * FROM {table_name}"""
    test_data = td.first_lines[table_name][0]
    test_data.update({'id': None})
    db.execute(database=test_db_0, cmd=command, params=test_data)
    test_data.update({'id': 1})
    assert db.fetch_one(database=test_db_0, cmd=sql) == test_data


@pytest.mark.parametrize('table_name, command', insert_sequence)
def test_insert_id_2(test_db_0, table_name, command):
    sql = f"""SELECT * FROM {table_name}"""
    test_data = td.first_lines[table_name][0]
    test_data.update({'id': 2})
    db.execute(database=test_db_0, cmd=command, params=test_data)
    assert db.fetch_one(database=test_db_0, cmd=sql) == test_data


# Test select
@pytest.mark.parametrize('table_name, command', select_sequence)
def test_select(test_db_2, table_name, command):
    expected = td.db_2[table_name]
    assert expected == db.fetch_all(database=test_db_2, cmd=command)


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


def test_allocation_deviation(test_db_1):
    expected = td_deviation.expected[0]

    assert expected == db.fetch_all(database=test_db_1,
                                    cmd=db.allocation_deviation,
                                    params={'net_worth': 1000000000})


@pytest.mark.parametrize('contribution', [0, 1000, 10000, 100000])
def test_allocation_deviation(test_db_1, contribution):
    expected = td_deviation.expected[contribution]
    for line in expected:
        line.update({'contribution': 0})

    assert expected == db.fetch_all(database=test_db_1,
                                    cmd=db.allocation_deviation,
                                    params={'net_worth': (1000000000 + contribution * 10000)})


# Test calculations
def test_net_worth(test_db_2):
    assert db.fetch_one(database=test_db_2, cmd=db.net_worth) == {'net_worth': 500000000}


@pytest.mark.parametrize('table_name, expected', td_constraints.formatted_expected)
def test_constraints(test_db_0, table_name, expected):
    db.execute(database=test_db_0, cmd=insert_dict[table_name], params=expected)

    assert db.fetch_all(database=test_db_0, cmd=select_dict[table_name]) == []
