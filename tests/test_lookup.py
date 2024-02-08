# test_lookup.py
# Lookup tables for the tests to use
# 2024-02-02
# @juicemcpeso

import db

insert_dict = {'account': db.insert_account,
               'account_type': db.insert_account_type,
               'allocation': db.insert_allocation,
               'asset': db.insert_asset,
               'asset_class': db.insert_asset_class,
               'balance': db.insert_balance,
               'component': db.insert_component,
               'constant': db.insert_constant,
               'institution': db.insert_institution,
               'location': db.insert_location,
               'owner': db.insert_owner,
               'price': db.insert_price}

insert_sequence = {(table_name, sql) for table_name, sql in insert_dict.items()}


