# # app.py
# # Code for interacting with the database
# # 2023-12-18
# # @juicemcpeso
#
# import csv
# import finance_tool
# import os
#
#
# class App:
#     def __init__(self, database=None):
#         self.decimal = 10000
#         self.db = database
#
#         self._lookup_insert = {'account': db.insert_account,
#                                'account_type': db.insert_account_type,
#                                'allocation': db.insert_allocation,
#                                'asset': db.insert_asset,
#                                'asset_class': db.insert_asset_class,
#                                'balance': db.insert_balance,
#                                'component': db.insert_component,
#                                'constant': db.insert_constant,
#                                'institution': db.insert_institution,
#                                'location': db.insert_location,
#                                'owner': db.insert_owner,
#                                'price': db.insert_price}
#
#         self._lookup = {'insert': self._lookup_insert}
#
#     def __getitem__(self, key):
#         return self._lookup[key]
#
#     def __setitem__(self, key, value):
#         self._lookup[key] = value
#
#     def __iter__(self):
#         return self._lookup.keys()
