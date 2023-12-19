# interface.py
# Code for interacting with the database
# 2023-12-18
# @juicemcpeso

import select


class Interface:
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.active = True

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

            options[select.verified_input(options.keys())]()

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

        options[select.verified_input(options.keys())]()

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

        options[select.verified_input(options.keys())]()

    def exit_program(self):
        """Exit"""
        self.active = False
        print('\nBye')
        exit()

    # Views
    def view_accounts(self):
        """Account balances"""
        accounts = self.portfolio.accounts()
        for account in accounts:
            print(f"{account['name']} | $")

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
        history = self.portfolio.price_history(select.by_name(self.portfolio.assets()))
        for price in history:
            print(f"{price['price_date']} | ${price['amount']}")
