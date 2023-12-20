# menus.py
# Code for creating menus
# 2023-12-19
# @juicemcpeso

import actions
import collections
import os

import portfolio


class Action:
    def __init__(self, name, app):
        self.name = name
        self.app = app

    def __call__(self):
        pass

    def __repr__(self):
        return f"Action({self.name}, {self.app})"

    def __str__(self):
        return self.name


class Selection(collections.abc.MutableSequence):
    def __init__(self, name, app, option_list=[]):
        self.name = name
        self.app = app
        self._options = option_list
        self.selected_option = None

    def __call__(self):
        self.select_option()
        if self.selected_option:
            self.selected_option()

    def __delitem__(self, key):
        del self._options[key]

    def __getitem__(self, key):
        return self._options[key]

    def __setitem__(self, key, value):
        self._options[key] = value

    def __contains__(self, item):
        return item in self._options

    def __len__(self):
        return len(self._options)

    def __iter__(self):
        return iter(self._options)

    def __repr__(self):
        return f"Selection({self.name}, {self.app}, {self._options})"

    def __str__(self):
        return self.name

    def insert(self, position, item):
        self._options.insert(position, item)

    def create_options(self):
        pass

    def select_option(self):
        pass


class Menu(Selection):
    def __call__(self):
        self.print_options()
        self.select_option()
        super().__call__()

    def select_option(self):
        while not self.selected_option:
            try:
                option_number = int(input('Select option number: '))
            except ValueError:
                pass
            else:
                self.selected_option = self[option_number] if option_number in range(len(self)) else None

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


class DatabaseSelectionMenu(Menu):
    def __init__(self, name, app):
        options = [ExitAction(app),
                   NewFileAction(app),
                   LoadFileSelection(app),
                   DeleteFileSelection(app)]
        # options = [        option_list = [actions.Actions('Exit', self.exit_program),
        #                actions.Option('Load', self['load']),
        #                actions.Option('New', self.new_portfolio),
        #                actions.Option('Delete', self.delete_portfolio)]]
        super().__init__(name, app, options)


class ExitAction(Action):
    def __init__(self, app):
        super().__init__('Exit app', app)

    def __call__(self):
        self.app.active = False
        print('\nBye')
        exit()


# File actions
class FileAction(Action):
    def __init__(self, name, app, file_name=None):
        super().__init__(name, app)
        self.file_name = file_name

    def file_path(self):
        return self.app.portfolio_directory + self.file_name


class LoadFileAction(FileAction):
    def __call__(self):
        self.app.portfolio = portfolio.Portfolio(self.file_path())


class LoadFileSelection(Selection):
    def __init__(self, app):
        super().__init__('Load', app)
        self.create_options()

    def create_options(self):
        # self.append(DatabaseSelectionMenu('<- Back', self.app))
        for file_name in os.listdir(self.app.portfolio_directory):
            self.append(LoadFileAction(self.name, self.app, file_name))


class DeleteFileAction(FileAction):
    def __call__(self):
        os.remove(self.file_path())


class DeleteFileSelection(Selection):
    def __init__(self, app):
        super().__init__('Delete', app)

    def create_options(self):
        # self.append(DatabaseSelectionMenu('<- Back', self.app))
        for file_name in os.listdir(self.portfolio_directory):
            self.append(DeleteFileAction(self.name, self.app, file_name))


class NewFileAction(FileAction):
    def __init__(self, app):
        super().__init__('New', app)

    def __call__(self):
        self.file_name = str(input("Enter new portfolio name: "))
        self.app.portfolio = portfolio.Portfolio(self.file_path())
