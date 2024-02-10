# test_lookup.py
# Lookup tables for the tests to use
# 2024-02-02
# @juicemcpeso

import finance_tool

insert_dict = {'account': finance_tool.insert_account,
               'account_type': finance_tool.insert_account_type,
               'allocation': finance_tool.insert_allocation,
               'asset': finance_tool.insert_asset,
               'asset_class': finance_tool.insert_asset_class,
               'balance': finance_tool.insert_balance,
               'component': finance_tool.insert_component,
               'constant': finance_tool.insert_constant,
               'institution': finance_tool.insert_institution,
               'location': finance_tool.insert_location,
               'owner': finance_tool.insert_owner,
               'price': finance_tool.insert_price}

insert_sequence = {(table_name, sql) for table_name, sql in insert_dict.items()}
