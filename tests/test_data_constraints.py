# test_data_constraints.py
# Test database dictionaries for constraints
# 2024-01-31
# @juicemcpeso

expected = [{'table': 'account_type',
             'expected': {'id': None, 'name': 'test', 'tax_in': 'test', 'tax_growth': 0, 'tax_out': 0}},
            {'table': 'account_type',
             'expected': {'id': None, 'name': 'test', 'tax_in': 1, 'tax_growth': 4, 'tax_out': 0}},
            {'table': 'account_type',
             'expected': {'id': None, 'name': None, 'tax_in': 1, 'tax_growth': 0, 'tax_out': 0}}]

formatted_expected = [(line['table'], line['expected']) for line in expected]
