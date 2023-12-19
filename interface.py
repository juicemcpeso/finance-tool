# interface.py
# Code for interacting with the database
# 2023-12-18
# @juicemcpeso

import os
import portfolio
import selection


class Interface:
    def __init__(self):
        self.active = True
        self.portfolio = None
        self.portfolio_directory = './portfolios'
        self.pipe = '|'

    # Portfolio selection/deletion
    def portfolio_menu(self):
        """Portfolio menu"""
        options = {1: self.load_portfolio,
                   2: self.new_portfolio,
                   3: self.delete_portfolio,
                   0: self.exit_program}

        print("\n" + self.portfolio_menu.__doc__)
        for option in options:
            print(f"{option} | {options[option].__doc__}")

        options[selection.verified_input(options.keys())]()

    def load_portfolio(self):
        """Load portfolio"""

        print("Select portfolio to load:")
        options = self.file_options()
        self.print_options(options)

        user_input = selection.verified_input(options)
        if user_input:
            file_path = './portfolios/' + options[user_input]
            self.portfolio = portfolio.Portfolio(file_path)
            self.main_menu()
        else:
            self.portfolio_menu()

    def new_portfolio(self):
        """New portfolio"""
        file_name = str(input("Enter new portfolio name: "))
        file_path = './portfolios/' + file_name + '.db'
        self.portfolio = portfolio.Portfolio(file_path)
        self.main_menu()

    def delete_portfolio(self):
        """Delete portfolio"""

        print("Select portfolio to delete:")
        options = self.file_options()
        self.print_options(options)

        user_input = selection.verified_input(options)
        if user_input:
            file_path = './portfolios/' + options[user_input]
            os.remove(file_path)
            self.portfolio_menu()
        else:
            self.portfolio_menu()

    # Database manipulation
    def main_menu(self):
        """Main menu"""
        options = {1: self.add_menu,
                   2: self.view_menu,
                   3: self.remove_menu,
                   0: self.exit_program}

        while True:
            print("\n" + self.main_menu.__doc__)
            for option in options:
                print(f"{option} | {options[option].__doc__}")

            options[selection.verified_input(options.keys())]()

    def add_menu(self):
        """Add"""
        options = {1: self.portfolio.add_account,
                   2: self.portfolio.add_asset,
                   3: self.portfolio.add_balance,
                   4: self.portfolio.add_owner,
                   5: self.portfolio.add_price,
                   0: self.main_menu}

        print("\n" + self.add_menu.__doc__)
        for option in options:
            print(f"{option} | {options[option].__doc__}")

        options[selection.verified_input(options.keys())]()

    def remove_menu(self):
        """Remove"""
        pass

    def view_menu(self):
        """View"""
        options = {1: self.view_accounts,
                   2: self.view_balance_history,
                   3: self.view_net_worth,
                   4: self.view_price_history,
                   0: self.main_menu}

        print("\n" + self.view_menu.__doc__)
        for option in options:
            print(f"{option} | {options[option].__doc__}")

        options[selection.verified_input(options.keys())]()

    def exit_program(self):
        """Exit"""
        self.active = False
        print('\nBye')
        exit()

    # Views
    def view_accounts(self):
        """Account balances"""
        print(markdown_table_string(self.portfolio.accounts()))

        # accounts = self.portfolio.accounts()
        # for account in accounts:
        #     print(f"{account['name']} | $")

    def view_balance_history(self):
        """Balance history"""
        balances = self.portfolio.balances()
        print(balances)
        # for balance in balances:
        #     print(f"{balance['name']} | {balance['owner']} | $")

    def view_net_worth(self):
        """Net worth"""
        pass

    def view_price_history(self):
        """Price history"""
        print("Select asset:")
        history = self.portfolio.price_history(selection.by_name(self.portfolio.assets()))
        for price in history:
            print(f"{price['price_date']} | ${price['amount']}")

    # Shared
    def print_options(self, option_dict):
        for option in option_dict:
            print(f"{option} | {option_dict[option]}")

    def file_options(self):
        options = {}
        file_names = os.listdir(self.portfolio_directory)

        for count, file_name in enumerate(file_names):
            options.update({(count + 1): file_name})

        options.update({0: 'Cancel'})
        return options


def markdown_table_string(sql_list):
    string = '|'
    if sql_list:
        string.append(markdown_table_column_names(sql_list[0].keys()))
        string.append(markdown_table_topper(len(sql_list[0].keys())))
        string.append(markdown_table_rows(sql_list))

    return string


def markdown_table_column_names(column_keys):
    string = '|'
    for column_name in column_keys:
        string.append(column_name)
        string.append('|')
    string.append('\n')

    return string


def markdown_table_topper(number_of_columns):
    string = '|'
    for _ in number_of_columns:
        string.append('---|')
    string.append('\n')

    return string


def markdown_table_rows(sql_list):
    string = '|'
    for row in sql_list:
        for item in row.keys():
            string.append(row[item])
        string.append('\n')

    return string
