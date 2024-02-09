# test_app.py
# Tests for app.py
# 2024-01-22
# @juicemcpeso

import db
import pytest

csv_expected = {'account': [{'id': 1, 'name': 'Work 401k', 'account_type_id': 1, 'institution_id': 1, 'owner_id': 1}],
                'account_type': [{'id': 1, 'name': '401k', 'tax_in': 0, 'tax_growth': 0, 'tax_out': 1}],
                'allocation': [{'id': 1, 'asset_class_id': 1, 'location_id': 1, 'percentage': 4000},
                               {'id': 2, 'asset_class_id': 1, 'location_id': 2, 'percentage': 2000},
                               {'id': 3, 'asset_class_id': 2, 'location_id': 1, 'percentage': 2500},
                               {'id': 4, 'asset_class_id': 2, 'location_id': 2, 'percentage': 500},
                               {'id': 5, 'asset_class_id': 3, 'location_id': 1, 'percentage': 1000}],
                'asset': [{'id': 1, 'name': 'Rearguard Total Stock Market Index Fund', 'symbol': 'RSUSA'},
                          {'id': 2, 'name': 'Rearguard Total International Stock Index Fund', 'symbol': 'RSINT'},
                          {'id': 3, 'name': 'Rearguard Total Bond Market Index Fund', 'symbol': 'RBUSA'},
                          {'id': 4, 'name': 'Rearguard Total International Bond Index Fund', 'symbol': 'RBINT'},
                          {'id': 5, 'name': 'US Dollars', 'symbol': 'USD'}],
                'asset_class': [{'id': 1, 'name': 'stocks'},
                                {'id': 2, 'name': 'bonds'},
                                {'id': 3, 'name': 'cash'},
                                {'id': 4, 'name': 'other'}],
                'balance': [{'id': 1, 'account_id': 1, 'asset_id': 1, 'balance_date': '2021-01-01', 'quantity': 340000000},
                            {'id': 2, 'account_id': 1, 'asset_id': 2, 'balance_date': '2021-01-01', 'quantity': 140000000},
                            {'id': 3, 'account_id': 1, 'asset_id': 3, 'balance_date': '2021-01-01', 'quantity': 340000000},
                            {'id': 4, 'account_id': 1, 'asset_id': 4, 'balance_date': '2021-01-01', 'quantity': 40000000},
                            {'id': 5, 'account_id': 1, 'asset_id': 5, 'balance_date': '2021-01-01', 'quantity': 140000000}],
                'component': [{'id': 1, 'asset_id': 1, 'asset_class_id': 1, 'location_id': 1, 'percentage': 10000},
                              {'id': 2, 'asset_id': 2, 'asset_class_id': 1, 'location_id': 2, 'percentage': 10000},
                              {'id': 3, 'asset_id': 3, 'asset_class_id': 2, 'location_id': 1, 'percentage': 10000},
                              {'id': 4, 'asset_id': 4, 'asset_class_id': 2, 'location_id': 2, 'percentage': 10000},
                              {'id': 5, 'asset_id': 5, 'asset_class_id': 3, 'location_id': 1, 'percentage': 10000}],
                'constant': [{'id': 1, 'name': 'decimal', 'amount': 10000}],
                'institution': [{'id': 1, 'name': 'Rearguard Investments'}],
                'location': [{'id': 1, 'name': 'USA'},
                             {'id': 2, 'name': 'International'},
                             {'id': 3, 'name': 'World'}],
                'owner': [{'id': 1, 'name': 'Bob', 'birthday': '1992-10-31'}],
                'price': [{'id': 1, 'asset_id': 1, 'price_date': '2020-01-01', 'amount': 10000},
                          {'id': 2, 'asset_id': 2, 'price_date': '2020-01-01', 'amount': 10000},
                          {'id': 3, 'asset_id': 3, 'price_date': '2020-01-01', 'amount': 10000},
                          {'id': 4, 'asset_id': 4, 'price_date': '2020-01-01', 'amount': 10000},
                          {'id': 5, 'asset_id': 5, 'price_date': '1776-07-04', 'amount': 10000}]}


@pytest.mark.parametrize('table_name', csv_expected.keys())
def test_insert_from_csv_file(test_app_db_0, table_name):
    test_app_db_0.insert_from_csv_file(file_path='./test_csv_data/' + table_name + '.csv', table_name=table_name)

    assert db.fetch_all(database=test_app_db_0.db, cmd=f"SELECT * FROM {table_name}") == csv_expected[table_name]


def test_insert_from_csv_directory(test_app_db_0):
    test_app_db_0.insert_from_csv_directory('./test_csv_data/')
    results_dict = {}

    for table_name in csv_expected.keys():
        result = db.fetch_all(database=test_app_db_0.db, cmd=f"SELECT * FROM {table_name}")
        results_dict.update({table_name: result})

    assert results_dict == csv_expected
