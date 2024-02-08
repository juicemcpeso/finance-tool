# test_app.py
# Tests for app.py
# 2024-01-22
# @juicemcpeso

import app
import db
import pytest


# @pytest.mark.parametrize('table_name, select_statement', test_lookup.select_sequence)
# def test_insert_from_csv_file(test_app_db_0, table_name, select_statement):
#     test_app_db_0.insert_from_csv_file(file_path='./test_csv_data/' + table_name + '.csv', table_name=table_name)
#     assert db.fetch_all(database=test_app_db_0.db, cmd=select_statement) == expected.db_1[table_name]


# def test_insert_from_csv_directory(test_app_db_0):
#     test_app_db_0.insert_from_csv_directory('./test_csv_data/')
#     results_dict = {}
#
#     for table_name in test_app_db_0['select']:
#         result = db.fetch_all(database=test_app_db_0.db, cmd=test_app_db_0['select'][table_name])
#         results_dict.update({table_name: result})
#     assert results_dict == expected.db_1


@pytest.mark.parametrize('amount', [0, 1000, 10000, 100000])
@pytest.mark.xfail(reason='Not yet updated to new sql format')
def test_where_to_contribute(test_app_db_1, amount):
    expected = {0: [],
                1000: [{'asset_class_id': 1,
                        'location_id': 2,
                        'contribution': 10000000}],
                10000: [{'asset_class_id': 1,
                         'location_id': 2,
                         'contribution': 50765539},
                        {'asset_class_id': 2,
                         'location_id': 2,
                         'contribution': 7691385},
                        {'asset_class_id': 1,
                         'location_id': 1,
                         'contribution': 41543076}],
                100000: [{'asset_class_id': 1,
                          'location_id': 2,
                          'contribution': 260000000},
                         {'asset_class_id': 2,
                          'location_id': 2,
                          'contribution': 60000000},
                         {'asset_class_id': 1,
                          'location_id': 1,
                          'contribution': 460000000},
                         {'asset_class_id': 2,
                          'location_id': 1,
                          'contribution': 160000000},
                         {'asset_class_id': 3,
                          'location_id': 1,
                          'contribution': 60000000}]}

    assert expected[amount] == test_app_db_1.where_to_contribute(amount)
