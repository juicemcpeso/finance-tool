# test_db.py
# Tests for db.py
# 2024-01-25
# @juicemcpeso

import csv
import db
import sqlite3
import pytest
import tests.test_data as td


@pytest.fixture
def test_db_0(tmp_path):
    db_test = tmp_path / "test.db"
    db.execute_script(db_test, db.create_tables)
    db.execute_script(db_test, db.create_views)
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

# create_table_sequence = {('account', db.create_table_account),
#                          ('account_type', db.create_table_account_type),
#                          ('allocation', db.create_table_allocation),
#                          ('asset', db.create_table_asset),
#                          ('asset_class', db.create_table_asset_class),
#                          ('balance', db.create_table_balance),
#                          ('component', db.create_table_component),
#                          ('institution', db.create_table_institution),
#                          ('location', db.create_table_location),
#                          ('owner', db.create_table_owner),
#                          ('price', db.create_table_price)}


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


def test_create_views(tmp_path):
    db_test = tmp_path / "test.db"
    db.execute_script(database=db_test, cmd=db.create_views)

    sql = """SELECT * FROM sqlite_master WHERE type = 'view'"""

    result_list = db.sql_fetch_all(database=db_test, cmd=sql)

    assert set(line['name'] for line in result_list) == view_names
