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
             'expected': {'id': None, 'name': None}}]

formatted_expected = [(line['table'], line['expected']) for line in expected]
