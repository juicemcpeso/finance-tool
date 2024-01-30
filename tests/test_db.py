# test_db.py
# Tests for db.py
# 2024-01-25
# @juicemcpeso

import csv
import db
import sqlite3
import pytest
import tests.test_data as td

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


@pytest.fixture
def test_db_0(tmp_path):
    db_test = tmp_path / "test.db"
    db.execute_script(db_test, db.create_tables)
    db.execute_script(db_test, db.create_views)
    return db_test


@pytest.fixture
def test_db_2(tmp_path):
    db_test = tmp_path / "test.db"
    db.execute_script(db_test, db.create_tables)
    db.execute_script(db_test, db.create_views)
    for table_name in insert_dict:
        db.execute_many(database=db_test, cmd=insert_dict[table_name], data_sequence=td.db_2[table_name])
    return db_test


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

first_lines = {table_name: td.db_1[table_name][0] for table_name in td.db_1}


@pytest.mark.parametrize('table_name, command', create_table_sequence)
def test_create_table(tmp_path, table_name, command):
    db_test = tmp_path / "test.db"
    db.execute(database=db_test, cmd=command)

    sql = """SELECT * FROM sqlite_master WHERE type = 'table'"""

    assert db.sql_fetch_all(database=db_test, cmd=sql)[0]['name'] == table_name
    assert len(db.sql_fetch_all(database=db_test, cmd=sql)) == 1


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

    result_list = db.sql_fetch_all(database=db_test, cmd=sql)

    assert set(line['name'] for line in result_list) == table_names


def test_create_tables_test_db_0(test_db_0):
    sql = """SELECT * FROM sqlite_master WHERE type = 'table'"""

    result_list = db.sql_fetch_all(database=test_db_0, cmd=sql)

    assert set(line['name'] for line in result_list) == table_names


@pytest.mark.parametrize('view_name, command', create_view_sequence)
def test_create_view(tmp_path, view_name, command):
    db_test = tmp_path / "test.db"
    db.execute(database=db_test, cmd=command)

    sql = """SELECT * FROM sqlite_master WHERE type = 'view'"""

    assert db.sql_fetch_all(database=db_test, cmd=sql)[0]['name'] == view_name
    assert len(db.sql_fetch_all(database=db_test, cmd=sql)) == 1


def test_create_views(tmp_path):
    db_test = tmp_path / "test.db"
    db.execute_script(database=db_test, cmd=db.create_views)

    sql = """SELECT * FROM sqlite_master WHERE type = 'view'"""

    result_list = db.sql_fetch_all(database=db_test, cmd=sql)

    assert set(line['name'] for line in result_list) == view_names


def test_create_views_test_db_0(test_db_0):
    sql = """SELECT * FROM sqlite_master WHERE type = 'view'"""

    result_list = db.sql_fetch_all(database=test_db_0, cmd=sql)

    assert set(line['name'] for line in result_list) == view_names


@pytest.mark.parametrize('table_name, command', insert_sequence)
def test_insert(test_db_0, table_name, command):
    sql = f"""SELECT * FROM {table_name}"""
    test_data = first_lines[table_name]
    db.execute(database=test_db_0, cmd=command, params=test_data)
    assert db.sql_fetch_one(database=test_db_0, cmd=sql) == test_data


@pytest.mark.parametrize('table_name, command', insert_sequence)
def test_insert_no_id(test_db_0, table_name, command):
    sql = f"""SELECT * FROM {table_name}"""
    test_data = first_lines[table_name]
    test_data.update({'id': None})
    db.execute(database=test_db_0, cmd=command, params=test_data)
    test_data.update({'id': 1})
    assert db.sql_fetch_one(database=test_db_0, cmd=sql) == test_data


@pytest.mark.parametrize('table_name, command', insert_sequence)
def test_insert_id_2(test_db_0, table_name, command):
    sql = f"""SELECT * FROM {table_name}"""
    test_data = first_lines[table_name]
    test_data.update({'id': 2})
    db.execute(database=test_db_0, cmd=command, params=test_data)
    assert db.sql_fetch_one(database=test_db_0, cmd=sql) == test_data


# Test views
def test_view_asset_value_current():
    pass


def test_net_worth(test_db_2):
    assert db.sql_fetch_one(database=test_db_2, cmd=db.net_worth) == {'net_worth': 500000000}
