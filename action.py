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
        self.data = {}

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
class AddToTable(AppAction):
    def __init__(self, app, table_name):
        self.table_name = table_name
        super().__init__('Add ' + self.table_name, app)

    def __call__(self):
        self.app.portfolio.add_to_table[self.table_name](kwargs={})


# class AddAccount(AppAction):
#     def __init__(self, app):
#         super().__init__('Add account', app)
#
#     def __call__(self):
#         sql = """
#         "INSERT INTO account
#         VALUES (:name, :account_type_id, :owner_id, :institution)"
#         """
#         self.app.portfolio.add_account()
#
#
# class AddOwner(AppAction):
#     def __init__(self, app):
#         super().__init__('Add owner', app)
#
#     def __call__(self):
#         self.app.portfolio.add_owner(kwargs=self.data)


# Input actions
class UserInput:
    pass


class InputDate(UserInput):
    pass


class InputText(UserInput):
    pass

# Export actions
# TODO - write export actions. May want this to be in it's own module.


# View actions
# TODO - write view actions
# def view_accounts(self):
#     """Account balances"""
#     print(self.portfolio.accounts())
#     print(markdown_table_string(self.portfolio.accounts()))
#
# def view_balance_history(self):
#     """Balance history"""
#     balances = self.portfolio.balances()
#     print(balances)
#     # for balance in balances:
#     #     print(f"{balance['name']} | {balance['owner']} | $")
#
# def view_net_worth(self):
#     """Net worth"""
#     pass
#
# def view_price_history(self):
#     """Price history"""
#     print("Select asset:")
#     history = self.portfolio.price_history(select_a.by_name(self.portfolio.assets()))
#     for price in history:
#         print(f"{price['price_date']} | ${price['amount']}")
