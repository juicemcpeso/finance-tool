# selections.py
# Code for selecting actions
# 2023-12-19
# @juicemcpeso

import action
import structures

import os

import portfolio


# class Selection(collections.abc.MutableSequence):
#     _options = []
#
#     def __init__(self, name, app, option_list=[]):
#         self.name = name
#         self.app = app
#         self._options = option_list
#         self.selected_option = None
#
#     def __call__(self):
#         self.create_options()
#         self.select_option()
#
#         if self.selected_option is not None:
#             self.selected_option()
#
#     def __delitem__(self, key):
#         del self._options[key]
#
#     def __getitem__(self, key):
#         return self._options[key]
#
#     def __setitem__(self, key, value):
#         self._options[key] = value
#
#     def __contains__(self, item):
#         return item in self._options
#
#     def __len__(self):
#         return len(self._options)
#
#     def __iter__(self):
#         return iter(self._options)
#
#     def __repr__(self):
#         return f"Selection({self.name}, {self.app}, {self._options})"
#
#     def __str__(self):
#         return self.name
#
#     def insert(self, position, item):
#         self._options.insert(position, item)
#
#     def create_options(self):
#         pass
#
#     def select_option(self):
#         pass


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
                # else:
                #     print('no')
                #     self.selected_option = None
                # print(self.selected_option)
                # self.selected_option = self[option_number] if option_number in range(len(self)) else None
                # print(self.selected_option)
        #
        # self.selected_option = None if self.selected_option not in  else pass
        # if selection in range(len(self.options)):
        #     return selection
        # else:
        #     selection = None

    def print_options(self):
        print('\n' + self.name)
        for i, option in enumerate(self):
            print(f"{i} | {str(option)}")

#
# class CommandLine(Menu):
#     def __init__(self, name, option_list, next_menu=None):
#         super().__init__(name, option_list, next_menu)
#         self.selected_option = None
#
#     def __call__(self):
#         print('\n' + self.name)
#         for i, option in enumerate(self.options):
#             print(f"{i} | {str(option)}")
#
#         self.selected_option = self.options[select_a.number(self.options)]()
#
#         if self.next_menu:
#             self.next_menu()


class Database(Menu):
    def __init__(self, app):
        options = [action.Exit(app),
                   action.NewFile(app),
                   LoadFile(app),
                   DeleteFile(app)]
        # options = [        option_list = [actions.Actions('Exit', self.exit_program),
        #                actions.Option('Load', self['load']),
        #                actions.Option('New', self.new_portfolio),
        #                actions.Option('Delete', self.delete_portfolio)]]
        super().__init__('Database menu', app, options)


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
        # self.append(DatabaseSelectionMenu(self.app))
        for file_name in os.listdir(self.app.portfolio_directory):
            self.append(action.LoadFile(file_name, self.app, file_name))


# Portfolio menus
class Main(Menu):
    def __init__(self, app):
        # options = [action.Exit(app), AddMenu(app)]

        #     option_list = [options.Option('Exit', self.exit_program),
        #                    actions.Option('Add', self.add_menu),
        #                    actions.Option('Remove', self.remove_menu),
        #                    actions.Option('View', self.view_menu),
        #                    options.Option('Export', self.export_menu)]

        super().__init__('Main menu', app)

    def create_options(self):
        self._options = [action.Exit(self.app),
                         AddMenu(self.app)]


class AddMenu(Menu):
    def __init__(self, app):
        super().__init__('Add menu', app)

    def create_options(self):
        self._options = [action.Back(self.app, Main(self.app)),
                         action.AddAccount(self.app)]

    # option_list = [actions.Option('<--Back', self._menus['main']),
    #                actions.Option('Account', self.portfolio.add_account),
    #                actions.Option('Asset', self.portfolio.add_asset),
    #                actions.Option('Balance', self.portfolio.add_balance),
    #                actions.Option('Owner', self.portfolio.add_owner),
    #                actions.Option('Price', self.portfolio.add_price)]

# Add actions
