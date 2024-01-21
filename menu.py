# selections.py
# Code for selecting actions
# 2023-12-19
# @juicemcpeso

import action
import structures
import os


class Menu(structures.Selection):
    def __init__(self, name, app, option_list=[]):
        super().__init__(name, option_list)
        self.app = app

    def __repr__(self):
        return f"Menu({self.name}, {self.app}, {self._options})"

    def select_option(self):
        self.print_options()
        while True:
            try:
                option_number = int(input('Select option number: '))
            except ValueError:
                pass
            else:
                if option_number in range(len(self)):
                    self.selected_option = self[option_number]
                    break

    def print_options(self):
        print('\n' + self.name)
        for i, option in enumerate(self):
            print(f"{i} | {str(option)}")


# Database menus
class Database(Menu):
    def __init__(self, app):
        super().__init__('Database menu', app)

    def create_options(self):
        self._options = [action.Exit(self.app),
                         action.NewFile(self.app),
                         LoadFile(self.app),
                         DeleteFile(self.app)]


# File menus
class DeleteFile(Menu):
    def __init__(self, app):
        super().__init__('Delete', app)

    def create_options(self):
        self._options = []
        self.append(action.Back(self.app, Database(self.app)))
        for file_name in os.listdir(self.app.portfolio_directory):
            self.append(action.DeleteFile(file_name, self.app, file_name))


class LoadFile(Menu):
    def __init__(self, app):
        super().__init__('Load', app)

    def create_options(self):
        self._options = []
        self.append(action.Back(self.app, Database(self.app)))
        for file_name in os.listdir(self.app.portfolio_directory):
            self.append(action.LoadFile(file_name, self.app, file_name))


# Portfolio menus
class Main(Menu):
    def __init__(self, app):
        super().__init__('Main menu', app)

    def create_options(self):
        self._options = [action.Exit(self.app),
                         Add(self.app)]
        #     option_list = [options.Option('Exit', self.exit_program),
        #                    actions.Option('Add', self.add_menu),
        #                    actions.Option('Remove', self.remove_menu),
        #                    actions.Option('View', self.view_menu),
        #                    options.Option('Export', self.export_menu)]


class Add(Menu):
    def __init__(self, app):
        super().__init__('Add menu', app)

    def create_options(self):
        self._options = [action.Back(self.app, Main(self.app)),
                         action.AddToTable(self.app, 'account')]

    # option_list = [actions.Option('<--Back', self._menus['main']),
    #                actions.Option('Account', self.portfolio.add_account),
    #                actions.Option('Asset', self.portfolio.add_asset),
    #                actions.Option('Balance', self.portfolio.add_balance),
    #                actions.Option('Owner', self.portfolio.add_owner),
    #                actions.Option('Price', self.portfolio.add_price)]


class Export(Menu):
    pass
    # options = {1: self.markdown_export(),
    #            0: self.main_menu}


class Remove(Menu):
    pass


class View(Menu):
    pass

    # options = {1: self.view_accounts,
    #            2: self.view_balance_history,
    #            3: self.view_net_worth,
    #            4: self.view_price_history,
    #            0: self.main_menu}