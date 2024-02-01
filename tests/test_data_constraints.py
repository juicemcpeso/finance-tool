# test_data_constraints.py
# Test database dictionaries for constraints
# 2024-01-31
# @juicemcpeso

# All test cases that should fail
expected = [{'table': 'account',
             'expected': {'id': None, 'name': None, 'account_type_id': 0, 'institution_id': 0, 'owner_id': 0}},
            {'table': 'account_type',
             'expected': {'id': None, 'name': 'test', 'tax_in': 1, 'tax_growth': 4, 'tax_out': 0}},
            {'table': 'account_type',
             'expected': {'id': None, 'name': None, 'tax_in': 1, 'tax_growth': 0, 'tax_out': 0}},
            {'table': 'allocation',
             'expected': {'id': None, 'asset_class_id': 1, 'location_id': 1, 'percentage': 3}},
            {'table': 'allocation',
             'expected': {'id': None, 'asset_class_id': 1, 'location_id': 1, 'percentage': 'test'}},
            {'table': 'allocation',
             'expected': {'id': None, 'asset_class_id': 1, 'location_id': 1, 'percentage': None}},
            {'table': 'asset',
             'expected': {'id': None, 'name': 'test', 'symbol': None}},
            {'table': 'asset',
             'expected': {'id': None, 'name': None, 'symbol': 'TEST'}},
            {'table': 'asset_class',
             'expected': {'id': None, 'name': None}},
            {'table': 'balance',
             'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': 6, 'quantity': 1}},
            {'table': 'balance',
             'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': 'test', 'quantity': 1}},
            {'table': 'balance',
             'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': 'April 16, 2023', 'quantity': 1}},
            {'table': 'balance',
             'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': '2024-15-43', 'quantity': 1}},
            {'table': 'balance',
             'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': None, 'quantity': 1}},
            {'table': 'balance',
             'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': '2022-01-01', 'quantity': None}},
            {'table': 'balance',
             'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': '2022-01-01',
                          'quantity': 'test'}},
            {'table': 'balance',
             'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': '2022-01-01', 'quantity': ''}},
            {'table': 'balance',
             'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': '2022-01-01', 'quantity': -123}},
            {'table': 'component',
             'expected': {'id': None, 'asset_id': 1, 'asset_class_id': 1, 'location_id': 1, 'percentage': 1.01}},
            {'table': 'component',
             'expected': {'id': None, 'asset_id': 1, 'asset_class_id': 1, 'location_id': 1, 'percentage': -0.01}},
            {'table': 'institution',
             'expected': {'id': None, 'name': None}},
            {'table': 'location',
             'expected': {'id': None, 'name': None}}]

formatted_expected = [(line['table'], line['expected']) for line in expected]

# This test does not work, as per SQLite - https://sqlite.org/forum/forumpost/4881adaae991d922
# {'table': 'balance',
# 'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': '2023-02-29', 'quantity': 1}}
