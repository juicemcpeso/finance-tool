# portfolio.py
# Portfolio is a database. Functions to create and manipulate the portfolio
# 2023-12-18
# @juicemcpeso

import copy
import csv
import time
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
                                    create_asset_quantity_by_account_view]

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
                                  'DROP VIEW IF EXISTS asset_quantity_by_account_current']


class Portfolio(sql_database.Database):
    def __init__(self, portfolio_path):
        super().__init__(portfolio_path, create_tables_and_views_commands, drop_tables_and_views_commands)

        self._lookup = {}
        self._construct_lookup()
        self.decimal = 10000

        self.add_to_table = {'accounts': self.add_account,
                             'account_types': self.add_account_type,
                             'allocations': self.add_allocation,
                             'assets': self.add_asset,
                             'asset_classes': self.add_asset_class,
                             'balances': self.add_balance,
                             'components': self.add_component,
                             'institutions': self.add_institution,
                             'locations': self.add_location,
                             'owners': self.add_owner,
                             'prices': self.add_price}

    def __iter__(self):
        return iter(self._lookup.keys())

    def __getitem__(self, key):
        return self.sql_fetch_all(self._lookup[key])

    def __setitem__(self, key, value):
        self._lookup[key] = value

    def _construct_lookup(self):
        get_commands = {'accounts': "SELECT * FROM account",
                        'account_types': "SELECT * FROM account_type",
                        'allocations': "SELECT * FROM allocation",
                        'assets': "SELECT * FROM asset",
                        'asset_classes': "SELECT * FROM asset_class",
                        'balances': "SELECT * FROM balance",
                        'components': "SELECT * FROM component",
                        'institutions': "SELECT * FROM institution",
                        'locations': "SELECT * FROM location",
                        'owners': "SELECT * FROM owner",
                        'prices': "SELECT * FROM price"}

        for item in get_commands:
            self._lookup[item] = get_commands[item]

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

    # def account_asset_quantity_current(self):
    #     sql = """
    #     SELECT account_id, asset_id, MAX(balance_date) balance_date, quantity
    #     FROM balance
    #     GROUP BY account_id, asset_id
    #     """
    #     return self.sql_fetch_all(sql)

    def account_value_current_by_asset(self):
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
        JOIN (
            SELECT
                asset_class_id, 
                location_id,
                SUM(current_value) current_value
            FROM (
                SELECT
                    c.asset_id,
                    c.asset_class_id,
                    c.location_id,
                    c.percentage * v.current_value / (10000 * 100) as current_value
                FROM
                    component AS c
                JOIN (
                    SELECT
                        asset_id,
                        SUM(current_value) current_value
                    FROM (
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
                        )
                    GROUP BY
                        asset_id
                    ORDER BY
                        asset_id
                    ) AS v ON c.asset_id = v.asset_id
                )
            GROUP BY
                asset_class_id,
                location_id
            ) AS current_values ON 
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
        SELECT asset_id, MAX(price_date) price_date, amount
        FROM price
        GROUP BY asset_id
        """

        return self.sql_fetch_all(sql)

    def asset_quantity(self):
        sql = """
        SELECT asset_id, SUM(quantity) quantity
        FROM (
            SELECT account_id, asset_id, MAX(balance_date) balance_date, quantity
            FROM balance
            GROUP BY account_id, asset_id)
        GROUP BY asset_id
        ORDER BY asset_id
        """
        return self.sql_fetch_all(sql)

    def asset_value_current(self):
        sql = """
        SELECT asset_id, SUM(current_value) current_value
        FROM (
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
            )
        GROUP BY asset_id
        ORDER BY asset_id
        """
        return self.sql_fetch_all(sql)

    # Asset class
    def asset_class_percentage(self):
        sql = """
        SELECT
            asset_class_id, 
            100.0 * SUM(current_value) / :net_worth AS percentage
        FROM (
            SELECT
                c.asset_id,
                c.asset_class_id,
                c.percentage * v.current_value / (10000 * 100) as current_value
            FROM
                component AS c
            JOIN (
                SELECT
                    asset_id,
                    SUM(current_value) current_value
                FROM (
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
                )
                GROUP BY asset_id
                ORDER BY asset_id
            ) AS v ON c.asset_id = v.asset_id
        )
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
        FROM (
            SELECT
                c.asset_id,
                c.asset_class_id,
                c.location_id,
                c.percentage * v.current_value / (10000 * 100) as current_value
            FROM
                component AS c
            JOIN (
                SELECT
                    asset_id,
                    SUM(current_value) current_value
                FROM (
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
                )
                GROUP BY asset_id
                ORDER BY asset_id
            ) AS v ON c.asset_id = v.asset_id
        )
        GROUP BY
            asset_class_id, location_id
        """
        return self.sql_fetch_all(sql, self.net_worth_dict())

    def asset_class_value(self):
        sql = """
        SELECT
            asset_class_id, 
            SUM(current_value) current_value
        FROM (
            SELECT
                c.asset_id,
                c.asset_class_id,
                c.percentage * v.current_value / (10000 * 100) as current_value
            FROM
                component AS c
            JOIN (
                SELECT
                    asset_id,
                    SUM(current_value) current_value
                FROM (
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
                )
                GROUP BY asset_id
                ORDER BY asset_id
            ) AS v ON c.asset_id = v.asset_id
        )
        GROUP BY
            asset_class_id
        """

        return self.sql_fetch_all(sql)

    def asset_class_value_by_location(self):
        sql = """
        SELECT
            asset_class_id, 
            location_id,
            SUM(current_value) current_value
        FROM (
            SELECT
                c.asset_id,
                c.asset_class_id,
                c.location_id,
                c.percentage * v.current_value / (10000 * 100) as current_value
            FROM
                component AS c
            JOIN (
                SELECT
                    asset_id,
                    SUM(current_value) current_value
                FROM (
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
                )
                GROUP BY asset_id
                ORDER BY asset_id
            ) AS v ON c.asset_id = v.asset_id
        )
        GROUP BY
            asset_class_id, location_id
        """

        return self.sql_fetch_all(sql)

    # Net worth
    def net_worth_dict(self):
        sql = """
        SELECT 
            SUM(current_values.current_value) AS net_worth
        FROM (
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
            ) AS current_values
        """

        return self.sql_fetch_one(sql)

    def net_worth(self):
        return self.net_worth_dict()['net_worth']

    # Tools
    def where_to_contribute(self, contribution_amount):
        deviation_table = self.allocation_deviation(contribution_amount)
        asset_deviation_level_cost = self.create_asset_deviation_level_cost_dict(deviation_table)
        total_deviation_level_cost = {key: 0 for key in range(len(deviation_table))}
        accessible_level = 0

        for line_number in asset_deviation_level_cost:
            for key in asset_deviation_level_cost[line_number]:
                total_deviation_level_cost[key] += asset_deviation_level_cost[line_number][key]

        for key in total_deviation_level_cost:
            if total_deviation_level_cost[key] < contribution_amount:
                accessible_level = key

        contribution_table = deviation_table[:(accessible_level + 1)]

        for line_number in range(accessible_level):
            contribution_table[line_number]['contribution'] += asset_deviation_level_cost[line_number][accessible_level]

        amount_remaining = contribution_amount - total_deviation_level_cost[accessible_level]

        total_percentage = 0
        for line_number in range(accessible_level + 1):
            total_percentage += contribution_table[line_number]['plan_percent']

        for line_number in range(accessible_level + 1):
            contribution_table[line_number]['contribution'] += amount_remaining * contribution_table[line_number][
                'plan_percent'] // total_percentage

        assign_leftovers(contribution_table, contribution_amount)

        return contribution_table

    def money_to_get_to_target_deviation(self, deviation_dict, target):
        return ((target + self.decimal) * deviation_dict['plan_value'] / self.decimal) - deviation_dict['current_value']

    def create_asset_deviation_level_cost_dict(self, deviation_table):
        asset_deviation_level_cost = {0: 0}

        for line_number, line in enumerate(deviation_table):
            asset_deviation_level_cost.update({line_number: {}})

            for next_number in range(line_number + 1, len(deviation_table)):
                dev_next_level = deviation_table[next_number]['deviation']
                asset_deviation_level_cost[line_number].update(
                    {next_number: self.money_to_get_to_target_deviation(line, dev_next_level)})

        return asset_deviation_level_cost

    # CSV loader
    def add_from_csv(self, file_name, table_name):
        for line in csv.DictReader(open(file_name)):
            self.add_to_table[table_name](kwargs=line)


def assign_leftovers(contribution_table, contribution_amount):
    amount_contributed = 0
    for line in contribution_table:
        amount_contributed += line['contribution']

    leftover = contribution_amount - amount_contributed

    while leftover > 0:
        for line in contribution_table:
            line['contribution'] += 1
            leftover -= 1
            if leftover == 0:
                break
