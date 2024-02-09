import app
import db
import pytest
import tests.test_lookup as test_lookup
import json


def json_loader(file_name):
    with open(file_name, "r") as read_file:
        return json.load(read_file)


@pytest.fixture
def test_db_0(tmp_path):
    db_test = tmp_path / "test.db"
    db.execute_file(db_test, '../db_sql.sql')
    return db_test


# Use for simplified allocation data
@pytest.fixture
def test_db_1(tmp_path):
    db_test = tmp_path / "test_1.db"
    db.execute_file(db_test, '../db_sql.sql')
    data = json_loader('../tests/data/test_db_1.json')
    for table_name in data:
        db.execute_many(database=db_test, cmd=test_lookup.insert_dict[table_name], data_sequence=data[table_name])

    return db_test


# Use for general testing (has multiple of each item)
@pytest.fixture
def test_db_2(tmp_path):
    db_test = tmp_path / "test_2.db"
    db.execute_file(db_test, '../db_sql.sql')
    data = json_loader('../tests/data/test_db_2.json')
    for table_name in data:
        db.execute_many(database=db_test, cmd=test_lookup.insert_dict[table_name], data_sequence=data[table_name])

    return db_test


@pytest.fixture
def test_app_db_0(test_db_0):
    return app.App(test_db_0)


@pytest.fixture
def test_app_db_1(test_db_1):
    return app.App(test_db_1)


@pytest.fixture
def test_app_db_2(test_db_2):
    return app.App(test_db_2)
