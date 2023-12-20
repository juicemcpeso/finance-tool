# app.py
# Code for interacting with the database
# 2023-12-18
# @juicemcpeso

import menu


class App:
    def __init__(self):
        self.active = True
        self.portfolio = None
        self.portfolio_directory = './portfolios/'

        # self._menus = {'add': None,
        #                'database menu': None,
        #                'load': None,
        #                'main': None}

    def __call__(self):
        while True:
            menu.Database(self)()

            if self.portfolio is not None:
                menu.Main(self)()

    # def __getitem__(self, key):
    #     return self._menus[key]
    #
    # def __setitem__(self, key, value):
    #     self._menus[key] = value
