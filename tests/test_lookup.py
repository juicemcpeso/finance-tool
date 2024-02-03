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

insert_sequence = {(table_name, insert_statement) for table_name, insert_statement in insert_dict.items()}

select_dict = {'account': db.select_account,
               'account_type': db.select_account_type,
               'allocation': db.select_allocation,
               'asset': db.select_asset,
               'asset_class': db.select_asset_class,
               'balance': db.select_balance,
               'component': db.select_component,
               'constant': db.select_constant,
               'institution': db.select_institution,
               'location': db.select_location,
               'owner': db.select_owner,
               'price': db.select_price}

select_sequence = {(table_name, select_statement) for table_name, select_statement in select_dict.items()}

table_names = select_dict.keys()
