# action.py
# Code for creating actions
# 2023-12-19
# @juicemcpeso

import os
import portfolio
import structures


class AppAction(structures.Action):
    def __init__(self, name, app):
        super().__init__(name)
        self.app = app

    def __call__(self):
        pass

    def __repr__(self):
        return f"Action({self.name}, {self.app})"

    def __str__(self):
        return self.name


# Generic actions
class Back(AppAction):
    def __init__(self, app, action):
        super().__init__('<- Back', app)
        self.action = action

    def __call__(self):
        self.action()


class Exit(AppAction):
    def __init__(self, app):
        super().__init__('Exit app', app)

    def __call__(self):
        self.app.active = False
        print('\nBye')
        exit()


# File actions
class FileAction(AppAction):
    def __init__(self, name, app, file_name=None):
        super().__init__(name, app)
        self.file_name = file_name

    def file_path(self):
        return self.app.portfolio_directory + self.file_name


class DeleteFile(FileAction):
    def __call__(self):
        os.remove(self.file_path())


class LoadFile(FileAction):
    def __call__(self):
        self.app.portfolio = portfolio.Portfolio(self.file_path())


class NewFile(FileAction):
    def __init__(self, app):
        super().__init__('New', app)

    def __call__(self):
        self.file_name = str(input("Enter new portfolio name: "))
        self.app.portfolio = portfolio.Portfolio(self.file_path())


# Add actions
class AddAccount(AppAction):
    def __init__(self, app):
        super().__init__('Add account', app)

    def __call__(self):
        self.app.portfolio.add_account()
