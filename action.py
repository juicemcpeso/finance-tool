# action.py
# Code for creating actions
# 2023-12-19
# @juicemcpeso

import datetime
import os
import portfolio
import structures


class AppAction(structures.Action):
    def __init__(self, app, name):
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
        super().__init__(app, '<- Back')
        self.action = action

    def __call__(self):
        self.action()


class Exit(AppAction):
    def __init__(self, app):
        super().__init__(app, 'Exit app')

    def __call__(self):
        self.app.active = False
        print('\nBye')
        exit()


# File actions
class FileAction(AppAction):
    def __init__(self, app, name, file_name=None):
        super().__init__(app, name)
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
        super().__init__(app, 'New')

    def __call__(self):
        self.file_name = str(input("Enter new portfolio name: "))
        self.app.portfolio = portfolio.Portfolio(self.file_path())


# Add actions
# class InputAction(AppAction):
#     def __init__(self, app, name):
#         super().__init__(app, name)
#
#     def __call__(self):
#         self.input_method[self.name]()


class AddToTable(AppAction):
    def __init__(self, app, table_name):
        self.table_name = table_name
        super().__init__(app, 'Add ' + self.table_name)

    def __call__(self):
        for column_name in self.app.portfolio.column_names(self.app.portfolio.table_commands[self.table_name])[1:]:
            UserInput(self.app, self.table_name, column_name)()
        # self.app.portfolio.add_to_table[self.table_name](kwargs={})


class UserInput(AppAction):
    def __init__(self, app, table_name, column_name):
        self.column_name = column_name
        self.display_text = 'Input ' + table_name + ' ' + self.column_name
        super().__init__(app, column_name)
        self.response = None

        self.input_method = {'birthday': self.input_date,
                             'name': self.input_text,
                             'symbol': self.input_text}

    def __call__(self):
        while self.response is None:
            self.input_method[self.column_name]()

    def input_bool(self):
        pass

    def input_date(self):
        try:
            self.response = datetime.date.fromisoformat(input(f"{self.display_text} in YYYY-MM-DD format: "))
        except ValueError:
            print("Date must be in YYYY-MM-DD format")

    def input_number(self):
        pass

    def input_text(self):
        self.response = input(f"{self.display_text}: ")


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
