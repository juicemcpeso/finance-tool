# app.py
# Code for interacting with the database
# 2023-12-18
# @juicemcpeso

import csv
import menu


class App:
    def __init__(self, portfolio=None):
        self.active = True
        self.portfolio = portfolio
        self.portfolio_directory = './portfolios/'

        self.add_to_table = {'account': self.portfolio.add_account,
                             'account_type': self.portfolio.add_account_type,
                             'allocation': self.portfolio.add_allocation,
                             'asset': self.portfolio.add_asset,
                             'asset_class': self.portfolio.add_asset_class,
                             'balance': self.portfolio.add_balance,
                             'component': self.portfolio.add_component,
                             'institution': self.portfolio.add_institution,
                             'location': self.portfolio.add_location,
                             'owner': self.portfolio.add_owner,
                             'price': self.portfolio.add_price}
        # self._menus = {'add': None,
        #                'database menu': None,
        #                'load': None,
        #                'main': None}

    def __call__(self):
        while True:
            menu.Database(self)()

            if self.portfolio is not None:
                menu.Main(self)()

    # CSV loader
    def add_from_csv(self, file_name, table_name):
        for line in csv.DictReader(open(file_name)):
            self.add_to_table[table_name](kwargs=line)
