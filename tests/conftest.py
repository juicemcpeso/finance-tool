import pytest
import app
import db
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
    db.execute_script(database=db_test, cmd=db.create_triggers)
    return db_test


# Use for simplified allocation data
@pytest.fixture
def test_db_1(tmp_path):
    db_test = tmp_path / "test_1.db"
    db.execute_script(db_test, db.create_tables)
    db.execute_script(db_test, db.create_views)
    db.execute_script(database=db_test, cmd=db.create_triggers)
    for table_name in insert_dict:
        db.execute_many(database=db_test, cmd=insert_dict[table_name], data_sequence=td.db_1_entry[table_name])

    return db_test


# Use for general testing (has multiple of each item)
@pytest.fixture
def test_db_2(tmp_path):
    db_test = tmp_path / "test_2.db"
    db.execute_script(db_test, db.create_tables)
    db.execute_script(db_test, db.create_views)
    db.execute_script(database=db_test, cmd=db.create_triggers)
    for table_name in insert_dict:
        db.execute_many(database=db_test, cmd=insert_dict[table_name], data_sequence=td.db_2_entry[table_name])
    return db_test


@pytest.fixture
def test_app_db_1(test_db_1):
    return app.App(test_db_1)


@pytest.fixture
def test_app_db_2(test_db_2):
    return app.App(test_db_2)
