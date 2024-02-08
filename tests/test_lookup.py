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

select_sequence = {(table_name, sql) for table_name, sql in select_dict.items()}

# table_dict = {'account': db.create_table_account,
#               'account_type': db.create_table_account_type,
#               'allocation': db.create_table_allocation,
#               'asset': db.create_table_asset,
#               'asset_class': db.create_table_asset_class,
#               'balance': db.create_table_balance,
#               'component': db.create_table_component,
#               'constant': db.create_table_constant,
#               'institution': db.create_table_institution,
#               'location': db.create_table_location,
#               'owner': db.create_table_owner,
#               'price': db.create_table_price}
#
# table_names = table_dict.keys()

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

# table_sequence = {(table_name, sql) for table_name, sql in table_dict.items()}

# view_dict = {'account_value_current_by_asset': db.create_view_account_value_current_by_asset,
#              'allocation_deviation': db.create_view_allocation_deviation,
#              'asset_price_newest': db.create_view_asset_price_newest,
#              'asset_quantity_by_account_current': db.create_view_asset_quantity_by_account_current,
#              'asset_value_current': db.create_view_asset_value_current,
#              'asset_class_value_by_location': db.create_view_asset_class_value_by_location,
#              'component_value': db.create_view_component_value,
#              'decimal': db.create_view_decimal,
#              'net_worth': db.create_view_net_worth}
#
# view_names = view_dict.keys()
#
# view_sequence = {(view_name, sql) for view_name, sql in view_dict.items()}

view_names = {'account_value_current_by_asset',
              'allocation_deviation',
              'asset_price_newest',
              'asset_quantity_by_account_current',
              'asset_value_current',
              'asset_class_value_by_location',
              'component_value',
              'decimal',
              'net_worth'}
