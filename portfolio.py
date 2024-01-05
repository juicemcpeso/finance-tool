# portfolio.py
# Portfolio is a database. Functions to create and manipulate the portfolio
# 2023-12-18
# @juicemcpeso

import csv
import file_processing
import sql_database

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
quantity INT,
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
percentage INT,
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
amount INT,
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
        return self.sql_fetch_all_dict(self._lookup[key])
        # return self._lookup[key]

    def __setitem__(self, key, value):
        self._lookup[key] = value

    # def _construct_lookup(self):
    #     getters = {self.accounts,
    #                self.account_types,
    #                self.assets,
    #                self.balances,
    #                self.institutions,
    #                self.locations,
    #                self.owners,
    #                self.prices}
    #
    #     for item in getters:
    #         self._lookup[item.__name__] = item

    def _construct_lookup(self):
        get_commands = {'accounts': "SELECT * FROM account",
                        'account_types': "SELECT * FROM account_type",
                        'assets': "SELECT * FROM asset",
                        'balances': "SELECT * FROM balance",
                        'institutions': "SELECT * FROM institution",
                        'locations': "SELECT * FROM location",
                        'owners': "SELECT * FROM owner",
                        'prices': "SELECT * FROM price"}

        for item in get_commands:
            self._lookup[item] = get_commands[item]

    # Table dictionaries
    # def accounts(self):
    #     return self.sql_fetch_all_dict("SELECT * FROM account")
    #
    # def account_types(self):
    #     return self.sql_fetch_all_dict("SELECT * FROM account_type")
    #
    # def assets(self):
    #     return self.sql_fetch_all_dict("SELECT * FROM asset")
    #
    # def balances(self):
    #     return self.sql_fetch_all_dict("SELECT * FROM balance")
    #
    # def institutions(self):
    #     return self.sql_fetch_all_dict("SELECT * FROM institution")
    #
    # def locations(self):
    #     return self.sql_fetch_all_dict("SELECT * FROM location")
    #
    # def owners(self):
    #     return self.sql_fetch_all_dict("SELECT * FROM owner")

    #
    # def prices(self):
    #     return self.sql_fetch_all_dict("SELECT * FROM price")

    # IO
    # Add
    def add_account(self, **kwargs):
        sql = """
        INSERT INTO account(name, account_type_id, institution_id, owner_id) 
        VALUES(:name, :account_type_id, :institution_id, :owner_id)
        """

        self.execute_many(sql, kwargs.values())

    def add_account_type(self, **kwargs):
        sql = """
        INSERT INTO account_type(name, tax_in, tax_growth, tax_out) 
        VALUES(:name, :tax_in, :tax_growth, :tax_out)
        """

        self.execute_many(sql, kwargs.values())

    def add_asset(self, **kwargs):
        sql = """
        INSERT INTO asset(name, symbol) 
        VALUES(:name, :symbol)
        """

        self.execute_many(sql, kwargs.values())

    def add_balance(self, **kwargs):
        sql = """
        INSERT INTO balance(account_id, asset_id, balance_date, quantity) 
        VALUES(:account_id, :asset_id, :balance_date, :quantity)
        """

        self.execute_many(sql, kwargs.values())

    def add_institution(self, **kwargs):
        sql = """
        INSERT INTO institution(name) 
        VALUES(:name)
        """

        self.execute_many(sql, kwargs.values())

    def add_location(self, **kwargs):
        sql = """
        INSERT INTO location(name) 
        VALUES(:name)
        """

        self.execute_many(sql, kwargs.values())

    def add_owner(self, **kwargs):
        sql = """
        INSERT INTO owner(name, birthday) 
        VALUES(:name, :birthday)
        """

        self.execute_many(sql, kwargs.values())

    def add_price(self, **kwargs):
        sql = """
        INSERT INTO price(asset_id, price_date, amount) 
        VALUES(:asset_id, :price_date, :amount)
        """

        self.execute_many(sql, kwargs.values())

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
    def newest_prices(self):
        sql = """
        SELECT asset_id, MAX(price_date) price_date, amount
        FROM price
        GROUP BY asset_id
        """

        return self.sql_fetch_all_dict(sql)

    def current_balances(self):
        sql = """
        SELECT account_id, asset_id, MAX(balance_date) balance_date, quantity
        FROM balance
        GROUP BY account_id, asset_id
        """
        return self.sql_fetch_all_dict(sql)

    def value_of_balances(self):
        sql = """
        SELECT 
            b.account_id, 
            b.asset_id, 
            MAX(b.balance_date) balance_date, 
            b.quantity * p.amount / 10000 AS current_value
        FROM 
            balance AS b
        JOIN (
            SELECT 
                asset_id, MAX(price_date) price_date, amount
            FROM 
                price
            GROUP BY 
                asset_id
            ) AS p ON b.asset_id = p.asset_id
        GROUP BY 
            b.account_id, b.asset_id
        """

        return self.sql_fetch_all_dict(sql)


    # def asset_price_current(self, asset_id):
    #     sql = """
    #     SELECT amount
    #     FROM price
    #     WHERE asset_id = ?
    #     ORDER BY price_date DESC LIMIT 1
    #     """
    #     if asset_id:
    #         return self.sql_fetch_one_params(sql, (asset_id,))['amount']
    #
    # def asset_price_history(self, asset_id):
    #     sql = """
    #     SELECT price_date, amount
    #     FROM price
    #     WHERE asset_id = ?
    #     ORDER BY price_date DESC
    #     """
    #     return self.sql_fetch_all_dict_params(sql, (asset_id,))

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
        for line in csv.DictReader(open(file_name)):
            self.add_account(kwargs=line)

    def add_from_csv_account_type(self, file_name):
        for line in csv.DictReader(open(file_name)):
            self.add_account_type(kwargs=line)

    def add_from_csv_asset(self, file_name):
        for line in csv.DictReader(open(file_name)):
            self.add_asset(kwargs=line)

    def add_from_csv_balance(self, file_name):
        for line in csv.DictReader(open(file_name)):
            self.add_balance(kwargs=line)

    def add_from_csv_institution(self, file_name):
        for line in csv.DictReader(open(file_name)):
            self.add_institution(kwargs=line)

    def add_from_csv_location(self, file_name):
        for line in csv.DictReader(open(file_name)):
            self.add_location(kwargs=line)

    def add_from_csv_owner(self, file_name):
        for line in csv.DictReader(open(file_name)):
            self.add_owner(kwargs=line)

    def add_from_csv_price(self, file_name):
        for line in csv.DictReader(open(file_name)):
            self.add_price(kwargs=line)
