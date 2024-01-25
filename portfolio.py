# portfolio.py
# Portfolio is a database. Functions to create and manipulate the portfolio
# 2023-12-18
# @juicemcpeso

import csv
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

create_allocation_table = """
CREATE TABLE IF NOT EXISTS allocation (
id INTEGER PRIMARY KEY,
asset_class_id INTEGER,
location_id INTEGER,
percentage INTEGER,
FOREIGN KEY(asset_class_id) REFERENCES asset_class(id),
FOREIGN KEY(location_id) REFERENCES location(id)
);"""

create_asset_table = """
CREATE TABLE IF NOT EXISTS asset (
id INTEGER PRIMARY KEY,
name TEXT,
symbol TEXT
);"""

create_asset_class_table = """
CREATE TABLE IF NOT EXISTS asset_class (
id INTEGER PRIMARY KEY,
name TEXT
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

# Views
create_account_value_current_by_asset = """
CREATE VIEW IF NOT EXISTS account_value_current_by_asset AS
SELECT 
    b.account_id, 
    b.asset_id, 
    MAX(b.balance_date) balance_date, 
    b.quantity * p.amount / 10000 AS current_value
FROM 
    balance AS b
JOIN
    asset_price_newest AS p ON b.asset_id = p.asset_id
GROUP BY 
    b.account_id, b.asset_id
"""

create_asset_price_newest_view = """
CREATE VIEW IF NOT EXISTS asset_price_newest AS
SELECT asset_id, MAX(price_date) price_date, amount
FROM price
GROUP BY asset_id
"""

create_asset_quantity_by_account_view = """
CREATE VIEW IF NOT EXISTS asset_quantity_by_account_current AS
SELECT
    account_id,
    asset_id,
    MAX(balance_date) balance_date,
    quantity
FROM
    balance
GROUP BY
    account_id, asset_id
"""

create_asset_value_current_view = """
CREATE VIEW IF NOT EXISTS asset_value_current AS
SELECT
    asset_id,
    SUM(current_value) current_value
FROM
    account_value_current_by_asset
GROUP BY
    asset_id
ORDER BY
    asset_id
"""

create_asset_class_value_by_location_view = """
CREATE VIEW IF NOT EXISTS asset_class_value_by_location aS
SELECT
    asset_class_id, 
    location_id,
    SUM(current_value) current_value
FROM
    component_value
GROUP BY
    asset_class_id, location_id
"""

create_component_value = """
CREATE VIEW IF NOT EXISTS component_value AS
SELECT
    c.asset_id,
    c.asset_class_id,
    c.location_id,
    c.percentage * v.current_value / (10000 * 100) as current_value
FROM
    component AS c
JOIN
    asset_value_current AS v ON c.asset_id = v.asset_id
"""

create_tables_and_views_commands = [create_account_table,
                                    create_account_type_table,
                                    create_allocation_table,
                                    create_asset_table,
                                    create_asset_class_table,
                                    create_balance_table,
                                    create_component_table,
                                    create_institution_table,
                                    create_location_table,
                                    create_owner_table,
                                    create_price_table,
                                    create_account_value_current_by_asset,
                                    create_asset_price_newest_view,
                                    create_asset_quantity_by_account_view,
                                    create_asset_class_value_by_location_view,
                                    create_asset_value_current_view,
                                    create_component_value]

drop_tables_and_views_commands = ['DROP TABLE IF EXISTS account',
                                  'DROP TABLE IF EXISTS account_type',
                                  'DROP TABLE IF EXISTS allocation',
                                  'DROP TABLE IF EXISTS asset',
                                  'DROP TABLE IF EXISTS asset_class',
                                  'DROP TABLE IF EXISTS balance',
                                  'DROP TABLE IF EXISTS component',
                                  'DROP TABLE IF EXISTS institution',
                                  'DROP TABLE IF EXISTS location',
                                  'DROP TABLE IF EXISTS owner',
                                  'DROP TABLE IF EXISTS price',
                                  'DROP VIEW IF EXISTS account_value_current_by_asset',
                                  'DROP VIEW IF EXISTS asset_price_newest',
                                  'DROP VIEW IF EXISTS asset_quantity_by_account_current',
                                  'DROP VIEW IF EXISTS asset_class_value_by_location',
                                  'DROP VIEW IF EXISTS asset_value_current',
                                  'DROP VIEW IF EXISTS component_value']


class Portfolio(sql_database.Database):
    def __init__(self, portfolio_path):
        super().__init__(portfolio_path, create_tables_and_views_commands, drop_tables_and_views_commands)

        self._lookup = {}
        # self.decimal = 10000

        self.table_commands = {'account': "SELECT * FROM account",
                               'account_type': "SELECT * FROM account_type",
                               'allocation': "SELECT * FROM allocation",
                               'asset': "SELECT * FROM asset",
                               'asset_class': "SELECT * FROM asset_class",
                               'balance': "SELECT * FROM balance",
                               'component': "SELECT * FROM component",
                               'institution': "SELECT * FROM institution",
                               'location': "SELECT * FROM location",
                               'owner': "SELECT * FROM owner",
                               'price': "SELECT * FROM price"}

        self.add_to_table = {'account': self.add_account,
                             'account_type': self.add_account_type,
                             'allocation': self.add_allocation,
                             'asset': self.add_asset,
                             'asset_class': self.add_asset_class,
                             'balance': self.add_balance,
                             'component': self.add_component,
                             'institution': self.add_institution,
                             'location': self.add_location,
                             'owner': self.add_owner,
                             'price': self.add_price}

        self._construct_lookup()

    def __iter__(self):
        return iter(self._lookup.keys())

    def __getitem__(self, key):
        return self.sql_fetch_all(self._lookup[key])

    def __setitem__(self, key, value):
        self._lookup[key] = value

    def _construct_lookup(self):
        for item in self.table_commands:
            self._lookup[item] = self.table_commands[item]

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

    def add_allocation(self, **kwargs):
        sql = """
        INSERT INTO allocation(asset_class_id, location_id, percentage) 
        VALUES(:asset_class_id, :location_id, :percentage)
        """

        self.execute_many(sql, kwargs.values())

    def add_asset(self, **kwargs):
        sql = """
        INSERT INTO asset(name, symbol) 
        VALUES(:name, :symbol)
        """

        self.execute_many(sql, kwargs.values())

    def add_asset_class(self, **kwargs):
        sql = """
        INSERT INTO asset_class(name) 
        VALUES(:name)
        """

        self.execute_many(sql, kwargs.values())

    def add_balance(self, **kwargs):
        sql = """
        INSERT INTO balance(account_id, asset_id, balance_date, quantity) 
        VALUES(:account_id, :asset_id, :balance_date, :quantity)
        """

        self.execute_many(sql, kwargs.values())

    def add_component(self, **kwargs):
        sql = """
        INSERT INTO component(asset_id, asset_class_id, location_id, percentage) 
        VALUES(:asset_id, :asset_class_id, :location_id, :percentage)
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
    def account_asset_quantity_current(self):
        sql = """
        SELECT * FROM asset_quantity_by_account_current
        """
        return self.sql_fetch_all(sql)

    def account_value_current_by_asset(self):
        sql = """
        SELECT * FROM account_value_current_by_asset 
        """

        return self.sql_fetch_all(sql)

    # Allocation
    def allocation_deviation(self, amount_to_add=0):
        sql = """
        SELECT
            plan.asset_class_id,
            plan.location_id,
            current_values.current_value,
            plan.percentage AS plan_percent,
            plan.percentage * :net_worth / 10000 AS plan_value,
            (10000 * current_values.current_value) / (plan.percentage * :net_worth / 10000) - 10000 as deviation,
            0 AS contribution
        FROM 
            allocation AS plan
        JOIN 
            asset_class_value_by_location AS current_values ON 
                current_values.asset_class_id == plan.asset_class_id AND 
                current_values.location_id == plan.location_id 
        WHERE
            deviation < 0        
        ORDER BY
            deviation ASC
        """

        return self.sql_fetch_all(sql, {'net_worth': self.net_worth() + amount_to_add})

    # Assets
    def asset_price_newest(self):
        sql = """
        SELECT * FROM asset_price_newest
        """

        return self.sql_fetch_all(sql)

    def asset_quantity(self):
        sql = """
        SELECT asset_id, SUM(quantity) quantity
        FROM asset_quantity_by_account_current
        GROUP BY asset_id
        ORDER BY asset_id
        """
        return self.sql_fetch_all(sql)

    def asset_value_current(self):
        sql = """
        SELECT * FROM asset_value_current
        """
        return self.sql_fetch_all(sql)

    # Asset class
    def asset_class_percentage(self):
        sql = """
        SELECT
            asset_class_id, 
            100.0 * SUM(current_value) / :net_worth AS percentage
        FROM
            component_value
        GROUP BY
            asset_class_id
        """
        return self.sql_fetch_all(sql, self.net_worth_dict())

    def asset_class_percentage_by_location(self):
        sql = """
        SELECT
            asset_class_id, 
            location_id,
            100.0 * SUM(current_value) / :net_worth AS percentage
        FROM
            component_value
        GROUP BY
            asset_class_id, location_id
        """
        return self.sql_fetch_all(sql, self.net_worth_dict())

    def asset_class_value(self):
        sql = """
        SELECT
            asset_class_id, 
            SUM(current_value) current_value
        FROM
            component_value
        GROUP BY
            asset_class_id
        """

        return self.sql_fetch_all(sql)

    def asset_class_value_by_location(self):
        sql = """
        SELECT * FROM asset_class_value_by_location
        """

        return self.sql_fetch_all(sql)

    # Net worth
    def net_worth_dict(self):
        sql = """
        SELECT 
            SUM(current_values.current_value) AS net_worth
        FROM
            account_value_current_by_asset AS current_values
        """

        return self.sql_fetch_one(sql)

    def net_worth(self):
        return self.net_worth_dict()['net_worth']

    # I/O
    def add_from_csv(self, file_name, table_name):
        for line in csv.DictReader(open(file_name)):
            self.add_to_table[table_name](kwargs=line)


def print_code(command_list):
    for command in command_list:
        command_string = command.lower().replace(' ', '_')
        new = command_string.replace('if_exists_', '')

        print(new + ' = \"\"\"')
        print(command)
        print('\"\"\"')
        print()


def print_select(command_dict):
    for command in command_dict:
        variable_name = "select_" + command

        print(variable_name + ' = \"\"\"')
        print(command_dict[command])
        print('\"\"\"')
        print()

table_commands = {'account': "SELECT * FROM account",
                               'account_type': "SELECT * FROM account_type",
                               'allocation': "SELECT * FROM allocation",
                               'asset': "SELECT * FROM asset",
                               'asset_class': "SELECT * FROM asset_class",
                               'balance': "SELECT * FROM balance",
                               'component': "SELECT * FROM component",
                               'institution': "SELECT * FROM institution",
                               'location': "SELECT * FROM location",
                               'owner': "SELECT * FROM owner",
                               'price': "SELECT * FROM price"}

print_select(table_commands)