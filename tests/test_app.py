# test_app.py
# Tests for app.py
# 2024-01-22
# @juicemcpeso

import app
import db
import pytest
import tests.test_lookup as test_lookup
import tests.test_data as td
import tests.test_data_deviation as td_deviation

# select_sequence = {('account', db.select_account),
#                    ('account_type', db.select_account_type),
#                    ('allocation', db.select_allocation),
#                    ('asset', db.select_asset),
#                    ('asset_class', db.select_asset_class),
#                    ('balance', db.select_balance),
#                    ('component', db.select_component),
#                    ('institution', db.select_institution),
#                    ('location', db.select_location),
#                    ('owner', db.select_owner),
#                    ('price', db.select_price)}
# select_dict = {'account': db.select_account,
#                'account_type': db.select_account_type,
#                'allocation': db.select_allocation,
#                'asset': db.select_asset,
#                'asset_class': db.select_asset_class,
#                'balance': db.select_balance,
#                'component': db.select_component,
#                'institution': db.select_institution,
#                'location': db.select_location,
#                'owner': db.select_owner,
#                'price': db.select_price}
#
# select_sequence = {(table_name, select_statement) for table_name, select_statement in select_dict.items()}


@pytest.mark.parametrize('table_name, select_statement', test_lookup.select_sequence)
def test_insert_from_csv_file(test_app_db_0, table_name, select_statement):
    test_app_db_0.insert_from_csv_file(file_path='./test_csv_data/' + table_name + '.csv', table_name=table_name)
    assert db.fetch_all(database=test_app_db_0.db, cmd=select_statement) == td.db_1_response[table_name]


def test_insert_from_csv_directory(test_app_db_0):
    test_app_db_0.insert_from_csv_directory('./test_csv_data/')
    results_dict = {}

    for table_name in test_app_db_0['select']:
        result = db.fetch_all(database=test_app_db_0.db, cmd=test_app_db_0['select'][table_name])
        results_dict.update({table_name: result})
    assert results_dict == td.db_1_response


@pytest.mark.parametrize('amount', [0, 1000, 10000, 100000])
def test_where_to_contribute(test_app_db_1, amount):
    expected = td_deviation.expected[amount]
    assert expected == test_app_db_1.where_to_contribute(amount * test_app_db_1.decimal)
