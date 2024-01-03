# portfolio.py
# Portfolio is a database. Functions to create and manipulate the portfolio
# 2023-12-18
# @juicemcpeso

import file_processing
import sql_database
import select_a
import sqlite3

create_account_table = """
CREATE TABLE IF NOT EXISTS account (
id INTEGER PRIMARY KEY,
name TEXT,
account_type_id INTEGER,
institution_id INTEGER,
owner_id INTEGER,
FOREIGN KEY(account_type_id) REFERENCES account_type(id)
FOREIGN KEY(owner_id) REFERENCES owner(id),
FOREIGN KEY(institution_id) REFERENCES institution(id)
);"""

create_account_type_table = """
CREATE TABLE IF NOT EXISTS account_type (
id INTEGER PRIMARY KEY,
name TEXT,
tax_in INTEGER,
tax_growth INTEGER,
tax_out INTEGER
);"""

create_asset_table = """
CREATE TABLE IF NOT EXISTS asset (
id INTEGER PRIMARY KEY,
name TEXT,
symbol TEXT
);"""

create_balance_table = """
CREATE TABLE IF NOT EXISTS balance (
id INTEGER PRIMARY KEY,
account_id INTEGER,
asset_id INTEGER,
balance_date TEXT,
quantity REAL,
FOREIGN KEY(account_id) REFERENCES account(id),
FOREIGN KEY(asset_id) REFERENCES asset(id)
);"""

create_asset_class_table = """
CREATE TABLE IF NOT EXISTS asset_class (
id INTEGER PRIMARY KEY,
name TEXT
);"""

create_component_table = """
CREATE TABLE IF NOT EXISTS component (
id INTEGER PRIMARY KEY,
name TEXT,
asset_id INTEGER,
asset_class_id INTEGER,
location_id INTEGER,
percentage REAL,
FOREIGN KEY(asset_id) REFERENCES asset(id),
FOREIGN KEY(asset_class_id) REFERENCES asset_class(id),
FOREIGN KEY(location_id) REFERENCES location(id)
);"""

create_institution_table = """
CREATE TABLE IF NOT EXISTS institution(
id INTEGER PRIMARY KEY,
name TEXT
);"""

create_location_table = """
CREATE TABLE IF NOT EXISTS location (
id INTEGER PRIMARY KEY,
name TEXT
);"""

create_owner_table = """
CREATE TABLE IF NOT EXISTS owner (
id INTEGER PRIMARY KEY,
name TEXT,
birthday TEXT
);"""

create_price_table = """
CREATE TABLE IF NOT EXISTS price (
id INTEGER PRIMARY KEY,
asset_id INTEGER,
price_date TEXT,
amount REAL,
FOREIGN KEY(asset_id) REFERENCES asset(id)
);"""

create_commands = [create_account_table,
                   create_account_type_table,
                   create_asset_table,
                   create_asset_class_table,
                   create_balance_table,
                   create_component_table,
                   create_institution_table,
                   create_location_table,
                   create_owner_table,
                   create_price_table]

drop_commands = ['DROP TABLE IF EXISTS account',
                 'DROP TABLE IF EXISTS account_type',
                 'DROP TABLE IF EXISTS asset',
                 'DROP TABLE IF EXISTS asset_class',
                 'DROP TABLE IF EXISTS balance',
                 'DROP TABLE IF EXISTS component',
                 'DROP TABLE IF EXISTS institution',
                 'DROP TABLE IF EXISTS location',
                 'DROP TABLE IF EXISTS owner',
                 'DROP TABLE IF EXISTS price']


class Portfolio(sql_database.Database):
    def __init__(self, portfolio_path):
        super().__init__(portfolio_path, create_commands, drop_commands)

        self._lookup = {}
        self._construct_lookup()

    def __iter__(self):
        return iter(self._lookup.keys())

    def __getitem__(self, key):
        return self._lookup[key]

    def __setitem__(self, key, value):
        self._lookup[key] = value

    def _construct_lookup(self):
        getters = {self.accounts,
                   self.account_types,
                   self.assets,
                   self.balances,
                   self.institutions,
                   self.locations,
                   self.owners,
                   self.prices}

        for item in getters:
            self._lookup[item.__name__] = item

    # Table dictionaries
    def accounts(self):
        return self.sql_fetch_all_dict("SELECT * FROM account")

    def account_types(self):
        return self.sql_fetch_all_dict("SELECT * FROM account_type")

    def assets(self):
        return self.sql_fetch_all_dict("SELECT * FROM asset")

    def balances(self):
        return self.sql_fetch_all_dict("SELECT * FROM balance")

    def institutions(self):
        return self.sql_fetch_all_dict("SELECT * FROM institution")

    def locations(self):
        return self.sql_fetch_all_dict("SELECT * FROM location")

    def owners(self):
        return self.sql_fetch_all_dict("SELECT * FROM owner")

    def prices(self):
        return self.sql_fetch_all_dict("SELECT * FROM price")

    # IO
    # Add
    # def add_account(self):
    #     """Add account"""
    #     name = input('Enter account name: ')
    #     institution = str(input('Enter institution name: '))
    #     account_type = select_a.by_name(self.account_types())
    #     owner = select_a.by_name(self.owners())
    #     new_account = (name, account_type, owner, institution)
    #
    #     sql = """
    #     INSERT INTO account(name, account_type_id, owner_id, institution)
    #     VALUES(?, ?, ?, ?)
    #     """
    #
    #     self.execute_parameters(sql, new_account)

    def add_account(self, **kwargs):
        """Add account"""
        sql = """
        INSERT INTO account(name, account_type_id, institution_id, owner_id) 
        VALUES(:name, :account_type_id, :institution_id, :owner_id)
        """
        self.execute_many(sql, kwargs.values())

    def add_asset(self):
        """Add asset"""
        pass

    def add_balance(self):
        """Add balance"""
        account = selection.by_name(self.accounts())
        asset = select_a.by_name(self.accounts())
        date = input('Enter date in YYYY-MM-DD format: ')
        quantity = float(input('Enter number of shares: '))
        new_balance = (account, asset, date, quantity)

        sql = """
        INSERT INTO balance(account_id, asset_id, balance_date, quantity) 
        VALUES(?, ?, ?, ?)
        """

        self.execute_parameters(sql, new_balance)

    def add_owner(self, **kwargs):
        """Add owner"""
        sql = """
        INSERT INTO owner(name, birthday) 
        VALUES(:name, :birthday)
        """
        self.execute_many(sql, kwargs.values())

    def add_price(self):
        """Add price"""
        asset = selection.by_name(self.assets())
        date = input('Enter date in YYYY-MM-DD format: ')
        amount = float(input('Enter price: $'))
        new_price = (asset, date, amount)

        sql = """
        INSERT INTO price(asset_id, price_date, amount) 
        VALUES(?, ?, ?)
        """

        self.execute_parameters(sql, new_price)

    # Remove

    # Calculations
    # Accounts
    def account_value(self, account_id):
        pass
        # value = 0
        # balances = sql_fetch_all_dict_params("SELECT asset_id, quantity FROM balance WHERE account_id = ?",
        #                                      (account_id,))
        # for balance in balances:
        #     pass
        #
        # print(value)

    # Assets
    def asset_price_current(self, asset_id):
        sql = """
        SELECT amount 
        FROM price 
        WHERE asset_id = ? 
        ORDER BY price_date DESC LIMIT 1
        """
        if asset_id:
            return self.sql_fetch_one_params(sql, (asset_id,))['amount']

    def asset_price_history(self, asset_id):
        sql = """
        SELECT price_date, amount 
        FROM price 
        WHERE asset_id = ? 
        ORDER BY price_date DESC
        """
        return self.sql_fetch_all_dict_params(sql, (asset_id,))

    # Net worth
    def net_worth(self):
        sql = """
        SELECT account_id, asset_id, MAX(balance_date)
        FROM balance
        GROUP BY account_id, asset_id
        """
        print(self.sql_fetch_all_dict(sql))

    # CSV loader
    def add_from_csv_account(self, file_name):
        csv_values = file_processing.get_split_lines(file_name)
        sql = """
        INSERT INTO account(id, name, account_type_id, institution_id, owner_id) 
        VALUES(?, ?, ?, ?, ?)
        """

        self.execute_many(sql, csv_values)

    def add_from_csv_account_type(self, file_name):
        csv_values = file_processing.get_split_lines(file_name)
        sql = """
        INSERT INTO account_type(id, name, tax_in, tax_growth, tax_out) 
        VALUES(?, ?, ?, ?, ?)
        """

        self.execute_many(sql, csv_values)

    def add_from_csv_asset(self, file_name):
        csv_values = file_processing.get_split_lines(file_name)
        sql = """
        INSERT INTO asset(id, name, symbol) 
        VALUES(?, ?, ?)
        """

        self.execute_many(sql, csv_values)

    def add_from_csv_balance(self, file_name):
        csv_values = file_processing.get_split_lines(file_name)
        sql = """
        INSERT INTO balance(id, account_id, asset_id, balance_date, quantity) 
        VALUES(?, ?, ?, ?, ?)
        """

        self.execute_many(sql, csv_values)

    def add_from_csv_institution(self, file_name):
        csv_values = file_processing.get_split_lines(file_name)
        sql = """
        INSERT INTO institution(id, name) 
        VALUES(?, ?)
        """

        self.execute_many(sql, csv_values)

    def add_from_csv_location(self, file_name):
        csv_values = file_processing.get_split_lines(file_name)
        sql = """
        INSERT INTO location(id, name) 
        VALUES(?, ?)
        """

        self.execute_many(sql, csv_values)

    def add_from_csv_owner(self, file_name):
        csv_values = file_processing.get_split_lines(file_name)
        sql = """
        INSERT INTO owner(id, name, birthday) 
        VALUES(?, ?, ?)
        """

        self.execute_many(sql, csv_values)

    def add_from_csv_price(self, file_name):
        csv_values = file_processing.get_split_lines(file_name)
        sql = """
        INSERT INTO price(id, asset_id, price_date, amount) 
        VALUES(?, ?, ?, ?)
        """

        self.execute_many(sql, csv_values)

    # def add_initial_assets():
    #     initial_values = file_processing.get_split_lines('/asset-allocator/initial_values/initial_assets.csv')
    #     sql_execute_many("INSERT INTO asset(symbol, name) VALUES(?, ?)", initial_values)
    #
    #
    # def add_initial_locations():
    #     initial_values = file_processing.get_split_lines('/asset-allocator/initial_values/initial_locations.csv')
    #     sql_execute_many("INSERT INTO location(name) VALUES(?)", initial_values)
    #
    #
    # def add_initial_owners():
    #     initial_values = file_processing.get_split_lines('/asset-allocator/initial_values/initial_owners.csv')
    #     sql_execute_many("INSERT INTO owner(name, birthday) VALUES(?, ?)", initial_values)

    def populate_test_portfolio(self):
        self.drop_all_tables()
        self.create_all_tables()
        self.add_from_csv_account('./test_data/test_accounts.csv')
        self.add_from_csv_account_type('./test_data/test_account_types.csv')
        self.add_from_csv_asset('./test_data/test_assets.csv')
        self.add_from_csv_balance('./test_data/test_balances.csv')
        self.add_from_csv_institution('./test_data/test_institutions.csv')
        self.add_from_csv_owner('./test_data/test_owners.csv')
        self.add_from_csv_price('./test_data/test_prices.csv')
