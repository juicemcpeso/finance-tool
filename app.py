# app.py
# Code for interacting with the database
# 2023-12-18
# @juicemcpeso

import menus
import actions
import os
import portfolio
import select_a


class App:
    def __init__(self):
        self.active = True
        self.portfolio = None
        self.portfolio_directory = './portfolios/'

        self._menus = {'add': None,
                       'database menu': None,
                       'load': None,
                       'main': None}

        self._construct_database_menus()

    def __call__(self):
        while True:
            self['database menu']()

            if self.portfolio is not None:
                self._construct_menus()
                self['main menu']()
        # self._construct_menus()
        # self['main']()

    def __getitem__(self, key):
        return self._menus[key]

    def __setitem__(self, key, value):
        self._menus[key] = value

    def _construct_database_menus(self):
        self['database menu'] = menus.DatabaseSelectionMenu(self)
        # self._construct_database_main_menu()

    def _construct_menus(self):
        self['main menu'] = menus.MainMenu(self)

        #
        # self._construct_main_menu()
        # self._construct_add_menu()
    #
    # def _construct_main_menu(self):
    #     option_list = [options.Option('Exit', self.exit_program),
    #                    actions.Option('Add', self.add_menu),
    #                    actions.Option('Remove', self.remove_menu),
    #                    actions.Option('View', self.view_menu),
    #                    options.Option('Export', self.export_menu)]



        # options = [menus.Command'1', '' self.add_menu,
        #            2: self.view_menu,
        #            3: self.remove_menu,
        #            4: self.export_menu,
        #            0: self.main_menu]

    def _construct_add_menu(self):
        option_list = [actions.Option('<--Back', self._menus['main']),
                       actions.Option('Account', self.portfolio.add_account),
                       actions.Option('Asset', self.portfolio.add_asset),
                       actions.Option('Balance', self.portfolio.add_balance),
                       actions.Option('Owner', self.portfolio.add_owner),
                       actions.Option('Price', self.portfolio.add_price)]

        self._menus['add'] = menus.CommandLine('Add...', option_list)
        # optionssdf= {1: self.portfolio.add_account,
        #            2: self.portfolio.add_asset,
        #            3: self.portfolio.add_balance,
        #            4: self.portfolio.add_owner,
        #            5: self.portfolio.add_price,
        #            0: self.main_menu}

    # Portfolio selection/deletion
    def _construct_database_main_menu(self):
        # option_list = [actions.Option('Exit', self.exit_program),
        #                actions.Option('Load', self['load']),
        #                actions.Option('New', self.new_portfolio),
        #                actions.Option('Delete', self.delete_portfolio)]

        self['database'] = menus.DatabaseSelectionMenu('Database menu', self)

        # """Portfolio menu"""
        # options = {1: self.load_portfolio,
        #            2: self.new_portfolio,
        #            3: self.delete_portfolio,
        #            0: self.exit_program}
        #
        # print("\n" + self.portfolio_menu.__doc__)
        # for option in options:
        #     print(f"{option} | {options[option].__doc__}")
        #
        # options[selection.verified_input(options.keys())]()

    def _construct_database_load_menu(self):
        self['load'] = menus.CommandLine('Load', self.file_list(self['database']), self['main'])

    # def load_portfolio(self):
    #     """Load portfolio"""
    #
    #     print("Select portfolio to load:")
    #     options = self.file_options()
    #     self.print_options(options)
    #
    #     user_input = select_a.number(options)
    #     if user_input:
    #         file_path = './portfolios/' + options[user_input]
    #         self.portfolio = portfolio.Portfolio(file_path)
    #         self['main']
    #     else:
    #         self['database']

    def new_portfolio(self):
        """New portfolio"""
        file_name = str(input("Enter new portfolio name: "))
        file_path = './portfolios/' + file_name + '.db'
        self.portfolio = portfolio.Portfolio(file_path)
        self.main_menu()

    def delete_portfolio(self):
        pass
        # """Delete portfolio"""
        #
        # print("Select portfolio to delete:")
        # options = self.file_options()
        # self.print_options(options)
        #
        # user_input = select_a.number(options)
        # if user_input:
        #     file_path = './portfolios/' + options[user_input]
        #     os.remove(file_path)
        #     self.portfolio_menu()
        # else:
        #     self.portfolio_menu()

    # Database manipulation

    # def main_menu(self):
    #     """Main menu"""

        # self.menu()
        #
        # while True:
        #     print("\n" + self.main_menu.__doc__)
        #     for option in options:
        #         print(f"{option} | {options[option].__doc__}")
        #
        #     options[selection.verified_input(options.keys())]()

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

        options[select_a.number(options.keys())]()

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

        options[select_a.number(options.keys())]()

    def export_menu(self):
        """Export"""
        options = {1: self.markdown_export(),
                   0: self.main_menu}

        print("\n" + self.export_menu.__doc__)
        for option in options:
            print(f"{option} | {options[option].__doc__}")

        options[select_a.number(options.keys())]()
    #
    # def exit_program(self):
    #     """Exit"""
    #     self.active = False
    #     print('\nBye')
    #     exit()

    # Views
    def view_accounts(self):
        """Account balances"""
        print(self.portfolio.accounts())
        print(markdown_table_string(self.portfolio.accounts()))

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
        history = self.portfolio.price_history(select_a.by_name(self.portfolio.assets()))
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

    def file_list(self, back_function):
        option_list = [actions.Option('<- Back', back_function)]

        for file_name in os.listdir(self.portfolio_directory):
            option_list.append(actions.Option(file_name, self.return_file_name))

        return option_list

    def set_portfolio(self, file_path):
        self.portfolio = portfolio.Portfolio(file_path)

    def return_file_name(self):
        return self.name

    def markdown_export(self):
        for table_name in self.portfolio:
            print(f"# {table_name}")
            print(markdown_table_string(self.portfolio[table_name]()))

    def select_action(self):
        selection = None
        while not selection:
            try:
                selection = int(input('Select option number: '))
            except ValueError:
                pass

            if selection in range(len(option_list)):
                return selection
            else:
                selection = None


def markdown_table_string(sql_list):
    string = ''
    if sql_list:
        string += markdown_table_column_names(sql_list[0].keys())
        string += markdown_table_topper(len(sql_list[0].keys()))
        string += markdown_table_rows(sql_list)

    return string


def markdown_table_column_names(column_keys):
    string = '|'
    for column_name in column_keys:
        string += column_name
        string += '|'
    string += '\n'

    return string


def markdown_table_topper(number_of_columns):
    string = '|'
    for _ in range(number_of_columns):
        string += '---|'
    string += '\n'

    return string


def markdown_table_rows(sql_list):
    string = ''
    for row in sql_list:
        for item in row.keys():
            string += '|'
            string += str(row[item])

        string += '|\n'

    return string
