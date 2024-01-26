# test_db.py
# Tests for db.py
# 2024-01-25
# @juicemcpeso

import db
import sqlite3
import pytest

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
