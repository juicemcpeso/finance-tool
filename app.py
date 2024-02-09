# app.py
# Code for interacting with the database
# 2023-12-18
# @juicemcpeso

import csv
import db
import os


class App:
    def __init__(self, database=None):
        self.decimal = 10000
        self.db = database

        self._lookup_insert = {'account': db.insert_account,
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

        self._lookup = {'insert': self._lookup_insert}

    def __getitem__(self, key):
        return self._lookup[key]

    def __setitem__(self, key, value):
        self._lookup[key] = value

    def __iter__(self):
        return self._lookup.keys()

    # CSV
    # TODO: convert to JSON
    # def insert_from_csv_file(self, file_path, table_name):
    #     with open(file_path) as csv_file:
    #         csv_dict = csv.DictReader(csv_file)
    #         db.execute_many(database=self.db, cmd=self['insert'][table_name], data_sequence=csv_dict)
    #
    # def insert_from_csv_directory(self, directory_path):
    #     for file_name in os.listdir(directory_path):
    #         self.insert_from_csv_file(file_path=directory_path + file_name, table_name=os.path.splitext(file_name)[0])
