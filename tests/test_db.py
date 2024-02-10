import json
import pytest
import sqlite3


def create_test_db_from_json(tmp_path, data_file_name=None):
    db_test = tmp_path / "test.db"
    execute_file(db_test, '../db.sql')

    if data_file_name is not None:
        json_data = json_loader(data_file_name)

        for table_name in json_data:
            keys = ', '.join(json_data[table_name][0].keys())
            q_marks = ', '.join(['?' for _ in json_data[table_name][0]])
            command = f"INSERT INTO {table_name} ({keys}) VALUES ({q_marks})"
            values = [tuple(line.values()) for line in json_data[table_name]]
            execute_many(db_test, cmd=command, data_sequence=values)

    return db_test


def json_loader(file_name):
    with open(file_name, "r") as read_file:
        return json.load(read_file)


@pytest.fixture
def test_db_0(tmp_path):
    return create_test_db_from_json(tmp_path)


# Use for simplified allocation data
@pytest.fixture
def test_db_1(tmp_path):
    return create_test_db_from_json(tmp_path, '../tests/data/test_db_1.json')


# Use for general testing (has multiple of each item)
@pytest.fixture
def test_db_2(tmp_path):
    return create_test_db_from_json(tmp_path, '../tests/data/test_db_2.json')


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
              'allocation_deviation_all_levels',
              'asset_price_newest',
              'asset_quantity_by_account_current',
              'asset_value_current',
              'asset_class_value_by_location',
              'component_value',
              'decimal',
              'deviation_level',
              'deviation_level_value',
              'net_worth',
              'net_worth_formatted'}


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def execute_file(database, file_name):
    with open(file_name, 'r') as sql_file:
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.executescript(sql_file.read())
        con.commit()
        con.close()


def execute_many(database, cmd, data_sequence):
    con = sqlite3.connect(database)
    cur = con.cursor()
    try:
        cur.executemany(cmd, data_sequence)
    except sqlite3.IntegrityError:
        pass
    con.commit()
    con.close()


def fetch_one(database, cmd, params=None):
    con = sqlite3.connect(database)
    con.row_factory = dict_factory
    cur = con.cursor()
    result = cur.execute(cmd, params).fetchone() if params is not None else cur.execute(cmd).fetchone()
    con.commit()
    con.close()
    return result


def fetch_all(database, cmd, params=None):
    con = sqlite3.connect(database)
    con.row_factory = dict_factory
    cur = con.cursor()
    result = cur.execute(cmd, params).fetchall() if params is not None else cur.execute(cmd).fetchall()
    con.commit()
    con.close()
    return result


def column_names(database, cmd):
    con = sqlite3.connect(database)
    cur = con.execute(cmd)
    result = [description[0] for description in cur.description]
    con.commit()
    con.close()
    return result


@pytest.mark.parametrize('table_name, column_name',
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
def test_create_table_columns(test_db_0, table_name, column_name):
    assert set(column_names(database=test_db_0, cmd=f"SELECT * FROM {table_name}")) == column_name


def test_create_tables(test_db_0):
    result_list = fetch_all(database=test_db_0, cmd="SELECT * FROM sqlite_master WHERE type = 'table'")

    assert set(line['name'] for line in result_list) == table_names


def test_create_views(test_db_0):
    result_list = fetch_all(database=test_db_0, cmd="SELECT * FROM sqlite_master WHERE type = 'view'")

    assert set(line['name'] for line in result_list) == view_names


def test_view_account_value_current_by_asset(test_db_2):
    expected = [{'account_id': 1, 'asset_id': 4, 'balance_date': '2022-01-01', 'current_value': 40000000},
                {'account_id': 2, 'asset_id': 3, 'balance_date': '2022-01-01', 'current_value': 40000000},
                {'account_id': 3, 'asset_id': 5, 'balance_date': '2021-12-15', 'current_value': 100000000},
                {'account_id': 4, 'asset_id': 2, 'balance_date': '2022-01-01', 'current_value': 100000000},
                {'account_id': 4, 'asset_id': 3, 'balance_date': '2021-01-01', 'current_value': 20000000},
                {'account_id': 5, 'asset_id': 1, 'balance_date': '2022-01-01', 'current_value': 200000000}]

    assert fetch_all(database=test_db_2, cmd="SELECT * FROM account_value_current_by_asset") == expected


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

    assert fetch_all(database=test_db_1, cmd="SELECT * FROM allocation_deviation") == expected


def test_view_allocation_deviation_all_levels(test_db_1):
    expected = [{'asset_class_id': 1,
                 'location_id': 2,
                 'current_value': 140000000,
                 'plan_percent': 2000,
                 'plan_value': 200000000,
                 'deviation': -3000,
                 'value_at_next_deviation': 140000000,
                 'value_difference': 0,
                 'next_deviation': -3000},
                {'asset_class_id': 1,
                 'location_id': 2,
                 'current_value': 140000000,
                 'plan_percent': 2000,
                 'plan_value': 200000000,
                 'deviation': -3000,
                 'value_at_next_deviation': 160000000,
                 'value_difference': 20000000,
                 'next_deviation': -2000},
                {'asset_class_id': 1,
                 'location_id': 2,
                 'current_value': 140000000,
                 'plan_percent': 2000,
                 'plan_value': 200000000,
                 'deviation': -3000,
                 'value_at_next_deviation': 170000000,
                 'value_difference': 30000000,
                 'next_deviation': -1500},
                {'asset_class_id': 1,
                 'location_id': 2,
                 'current_value': 140000000,
                 'plan_percent': 2000,
                 'plan_value': 200000000,
                 'deviation': -3000,
                 'value_at_next_deviation': 272000000,
                 'value_difference': 132000000,
                 'next_deviation': 3600},
                {'asset_class_id': 1,
                 'location_id': 2,
                 'current_value': 140000000,
                 'plan_percent': 2000,
                 'plan_value': 200000000,
                 'deviation': -3000,
                 'value_at_next_deviation': 280000000,
                 'value_difference': 140000000,
                 'next_deviation': 4000},
                {'asset_class_id': 2,
                 'location_id': 2,
                 'current_value': 40000000,
                 'plan_percent': 500,
                 'plan_value': 50000000,
                 'deviation': -2000,
                 'value_at_next_deviation': 40000000,
                 'value_difference': 0,
                 'next_deviation': -2000},
                {'asset_class_id': 2,
                 'location_id': 2,
                 'current_value': 40000000,
                 'plan_percent': 500,
                 'plan_value': 50000000,
                 'deviation': -2000,
                 'value_at_next_deviation': 42500000,
                 'value_difference': 2500000,
                 'next_deviation': -1500},
                {'asset_class_id': 2,
                 'location_id': 2,
                 'current_value': 40000000,
                 'plan_percent': 500,
                 'plan_value': 50000000,
                 'deviation': -2000,
                 'value_at_next_deviation': 68000000,
                 'value_difference': 28000000,
                 'next_deviation': 3600},
                {'asset_class_id': 2,
                 'location_id': 2,
                 'current_value': 40000000,
                 'plan_percent': 500,
                 'plan_value': 50000000,
                 'deviation': -2000,
                 'value_at_next_deviation': 70000000,
                 'value_difference': 30000000,
                 'next_deviation': 4000},
                {'asset_class_id': 1,
                 'location_id': 1,
                 'current_value': 340000000,
                 'plan_percent': 4000,
                 'plan_value': 400000000,
                 'deviation': -1500,
                 'value_at_next_deviation': 340000000,
                 'value_difference': 0,
                 'next_deviation': -1500},
                {'asset_class_id': 1,
                 'location_id': 1,
                 'current_value': 340000000,
                 'plan_percent': 4000,
                 'plan_value': 400000000,
                 'deviation': -1500,
                 'value_at_next_deviation': 544000000,
                 'value_difference': 204000000,
                 'next_deviation': 3600},
                {'asset_class_id': 1,
                 'location_id': 1,
                 'current_value': 340000000,
                 'plan_percent': 4000,
                 'plan_value': 400000000,
                 'deviation': -1500,
                 'value_at_next_deviation': 560000000,
                 'value_difference': 220000000,
                 'next_deviation': 4000},
                {'asset_class_id': 2,
                 'location_id': 1,
                 'current_value': 340000000,
                 'plan_percent': 2500,
                 'plan_value': 250000000,
                 'deviation': 3600,
                 'value_at_next_deviation': 340000000,
                 'value_difference': 0,
                 'next_deviation': 3600},
                {'asset_class_id': 2,
                 'location_id': 1,
                 'current_value': 340000000,
                 'plan_percent': 2500,
                 'plan_value': 250000000,
                 'deviation': 3600,
                 'value_at_next_deviation': 350000000,
                 'value_difference': 10000000,
                 'next_deviation': 4000},
                {'asset_class_id': 3,
                 'location_id': 1,
                 'current_value': 140000000,
                 'plan_percent': 1000,
                 'plan_value': 100000000,
                 'deviation': 4000,
                 'value_at_next_deviation': 140000000,
                 'value_difference': 0,
                 'next_deviation': 4000}]

    assert fetch_all(database=test_db_1, cmd="SELECT * FROM allocation_deviation_all_levels") == expected


def test_view_asset_value_current(test_db_2):
    expected = [{'asset_id': 1, 'current_value': 200000000},
                {'asset_id': 2, 'current_value': 100000000},
                {'asset_id': 3, 'current_value': 60000000},
                {'asset_id': 4, 'current_value': 40000000},
                {'asset_id': 5, 'current_value': 100000000}]

    assert fetch_all(database=test_db_2, cmd="SELECT * FROM asset_value_current") == expected


def test_view_asset_price_newest(test_db_2):
    expected = [{'asset_id': 1, 'price_date': '1776-07-04', 'amount': 10000},
                {'asset_id': 2, 'price_date': '2022-01-01', 'amount': 20000},
                {'asset_id': 3, 'price_date': '2022-12-01', 'amount': 400000},
                {'asset_id': 4, 'price_date': '2022-01-01', 'amount': 800000},
                {'asset_id': 5, 'price_date': '2021-12-15', 'amount': 10000}]

    assert fetch_all(database=test_db_2, cmd="SELECT * FROM asset_price_newest") == expected


def test_view_asset_quantity_by_account_current(test_db_2):
    expected = [{'account_id': 1, 'asset_id': 4, 'balance_date': '2022-01-01', 'quantity': 500000},
                {'account_id': 2, 'asset_id': 3, 'balance_date': '2022-01-01', 'quantity': 1000000},
                {'account_id': 3, 'asset_id': 5, 'balance_date': '2021-12-15', 'quantity': 100000000},
                {'account_id': 4, 'asset_id': 2, 'balance_date': '2022-01-01', 'quantity': 50000000},
                {'account_id': 4, 'asset_id': 3, 'balance_date': '2021-01-01', 'quantity': 500000},
                {'account_id': 5, 'asset_id': 1, 'balance_date': '2022-01-01', 'quantity': 200000000}]

    assert fetch_all(database=test_db_2, cmd="SELECT * FROM asset_quantity_by_account_current") == expected


def test_view_asset_class_value_by_location(test_db_2):
    expected = [{'asset_class_id': 1, 'location_id': 1, 'current_value': 82000000},
                {'asset_class_id': 1, 'location_id': 2, 'current_value': 110000000},
                {'asset_class_id': 2, 'location_id': 1, 'current_value': 104000000},
                {'asset_class_id': 2, 'location_id': 2, 'current_value': 2000000},
                {'asset_class_id': 3, 'location_id': 1, 'current_value': 200000000},
                {'asset_class_id': 4, 'location_id': None, 'current_value': 2000000}]

    assert fetch_all(database=test_db_2, cmd="SELECT * FROM asset_class_value_by_location") == expected


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

    assert fetch_all(database=test_db_2, cmd="SELECT * FROM component_value") == expected


def test_view_decimal(test_db_2):
    assert fetch_one(database=test_db_2, cmd="SELECT * FROM decimal") == {'constant': 10000}


def test_view_deviation_level(test_db_1):
    expected = [{'deviation': -3000},
                {'deviation': -2000},
                {'deviation': -1500},
                {'deviation': 3600},
                {'deviation': 4000}]

    assert fetch_all(database=test_db_1, cmd="SELECT * FROM deviation_level") == expected


def test_view_deviation_level_value(test_db_1):
    expected = [{'deviation': -3000, 'level_value': 0},
                {'deviation': -2000, 'level_value': 20000000},
                {'deviation': -1500, 'level_value': 32500000},
                {'deviation': 3600, 'level_value': 364000000},
                {'deviation': 4000, 'level_value': 400000000}]

    assert fetch_all(database=test_db_1, cmd="SELECT * FROM deviation_level_value") == expected


def test_view_net_worth(test_db_2):
    assert fetch_one(database=test_db_2, cmd="SELECT * FROM net_worth") == {'net_worth': 500000000}


# Test calculations
def test_net_worth_formatted(test_db_2):
    assert fetch_one(database=test_db_2, cmd="SELECT * FROM net_worth_formatted") == {'net_worth': 50000.00}
