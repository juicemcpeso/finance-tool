# db.py
# SQL statements for the portfolio logic
# 2024-01-25
# @juicemcpeso

import sqlite3


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


# TODO - figure out the best way to write these
# def execute(database, cmd, params=None):
#     with sqlite3.connect(database) as con:
#         cur = con.cursor()
#         cur.execute(cmd, params) if params is not None else cur.execute(cmd)
#     con.close()


# TODO - test?
def execute(database, cmd, params=None):
    """Execute a single command"""
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute(cmd, params) if params is not None else cur.execute(cmd)
    con.commit()
    con.close()


# TODO - test?
def execute_many(database, cmd, data_sequence):
    """Execute a single command multiple times with different data"""
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.executemany(cmd, data_sequence)
    con.commit()
    con.close()
#
#
# def execute_set(database, cmd_set):
#     """Execute a set of commands"""
#     for command in cmd_set:
#         execute(database=database, cmd=command)


# TODO - test?
def execute_script(database, cmd):
    """Execute script of commands"""
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.executescript(cmd)
    con.commit()
    con.close()


# TODO - test
def sql_fetch_one(database, cmd, params=None):
    con = sqlite3.connect(database)
    con.row_factory = dict_factory
    cur = con.cursor()
    result = cur.execute(cmd, params).fetchone() if params is not None else cur.execute(cmd).fetchone()
    con.commit()
    con.close()
    return result


# TODO - test
def sql_fetch_all(database, cmd, params=None):
    con = sqlite3.connect(database)
    con.row_factory = dict_factory
    cur = con.cursor()
    result = cur.execute(cmd, params).fetchall() if params is not None else cur.execute(cmd).fetchall()
    con.commit()
    con.close()
    return result


# TODO - test
def column_names(database, cmd):
    con = sqlite3.connect(database)
    cur = con.execute(cmd)
    result = [description[0] for description in cur.description]
    con.commit()
    con.close()
    return result


# CREATE - tables
create_table_account = """
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

create_table_account_type = """
CREATE TABLE IF NOT EXISTS account_type (
    id INTEGER PRIMARY KEY,
    name TEXT,
    tax_in INTEGER,
    tax_growth INTEGER,
    tax_out INTEGER
);"""

create_table_allocation = """
CREATE TABLE IF NOT EXISTS allocation (
    id INTEGER PRIMARY KEY,
    asset_class_id INTEGER,
    location_id INTEGER,
    percentage INTEGER,
    FOREIGN KEY(asset_class_id) REFERENCES asset_class(id),
    FOREIGN KEY(location_id) REFERENCES location(id)
);"""

create_table_asset = """
CREATE TABLE IF NOT EXISTS asset (
    id INTEGER PRIMARY KEY,
    name TEXT,
    symbol TEXT
);"""

create_table_asset_class = """
CREATE TABLE IF NOT EXISTS asset_class (
    id INTEGER PRIMARY KEY,
    name TEXT
);"""

create_table_balance = """
CREATE TABLE IF NOT EXISTS balance (
    id INTEGER PRIMARY KEY,
    account_id INTEGER,
    asset_id INTEGER,
    balance_date TEXT,
    quantity INT,
    FOREIGN KEY(account_id) REFERENCES account(id),
    FOREIGN KEY(asset_id) REFERENCES asset(id)
);"""

create_table_component = """
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

create_table_institution = """
CREATE TABLE IF NOT EXISTS institution(
    id INTEGER PRIMARY KEY,
    name TEXT
);"""

create_table_location = """
CREATE TABLE IF NOT EXISTS location (
    id INTEGER PRIMARY KEY,
    name TEXT
);"""

create_table_owner = """
CREATE TABLE IF NOT EXISTS owner (
    id INTEGER PRIMARY KEY,
    name TEXT,
    birthday TEXT
);"""

create_table_price = """
CREATE TABLE IF NOT EXISTS price (
    id INTEGER PRIMARY KEY,
    asset_id INTEGER,
    price_date TEXT,
    amount INT,
    FOREIGN KEY(asset_id) REFERENCES asset(id)
);"""

# create_tables = {create_table_account,
#                  create_table_account_type,
#                  create_table_allocation,
#                  create_table_asset,
#                  create_table_asset_class,
#                  create_table_balance,
#                  create_table_component,
#                  create_table_institution,
#                  create_table_location,
#                  create_table_owner,
#                  create_table_price}

create_tables = create_table_account + \
                create_table_account_type + \
                create_table_allocation + \
                create_table_asset + \
                create_table_asset_class + \
                create_table_balance + \
                create_table_component + \
                create_table_institution + \
                create_table_location + \
                create_table_owner + \
                create_table_price

# CREATE - views
# TODO - test
create_view_account_value_current_by_asset = """
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
;"""

# TODO - test
create_view_asset_price_newest = """
CREATE VIEW IF NOT EXISTS asset_price_newest AS
SELECT
    asset_id, 
    MAX(price_date) price_date, 
    amount
FROM
    price
GROUP BY
    asset_id
;"""

# TODO - test
create_view_asset_quantity_by_account_current = """
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
;"""

# TODO - test
create_view_asset_value_current = """
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
;"""

# TODO - test
create_view_asset_class_value_by_location = """
CREATE VIEW IF NOT EXISTS asset_class_value_by_location aS
SELECT
    asset_class_id, 
    location_id,
    SUM(current_value) current_value
FROM
    component_value
GROUP BY
    asset_class_id, location_id
;"""

# TODO - test
create_view_component_value = """
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
;"""

# create_views = {create_view_account_value_current_by_asset,
#                 create_view_asset_price_newest,
#                 create_view_asset_quantity_by_account,
#                 create_view_asset_value_current,
#                 create_view_asset_class_value_by_location,
#                 create_view_component_value}

create_views = create_view_account_value_current_by_asset + \
               create_view_asset_price_newest + \
               create_view_asset_quantity_by_account_current + \
               create_view_asset_value_current + \
               create_view_asset_class_value_by_location + \
               create_view_component_value

# TODO - write tests for drop functions (if still needed)
# DROP - tables
drop_table_account = """
DROP TABLE IF EXISTS account
"""

drop_table_account_type = """
DROP TABLE IF EXISTS account_type
"""

drop_table_allocation = """
DROP TABLE IF EXISTS allocation
"""

drop_table_asset = """
DROP TABLE IF EXISTS asset
"""

drop_table_asset_class = """
DROP TABLE IF EXISTS asset_class
"""

drop_table_balance = """
DROP TABLE IF EXISTS balance
"""

drop_table_component = """
DROP TABLE IF EXISTS component
"""

drop_table_institution = """
DROP TABLE IF EXISTS institution
"""

drop_table_location = """
DROP TABLE IF EXISTS location
"""

drop_table_owner = """
DROP TABLE IF EXISTS owner
"""

drop_table_price = """
DROP TABLE IF EXISTS price
"""

drop_tables = {drop_table_account,
               drop_table_account_type,
               drop_table_allocation,
               drop_table_asset,
               drop_table_asset_class,
               drop_table_balance,
               drop_table_component,
               drop_table_institution,
               drop_table_location,
               drop_table_owner,
               drop_table_price}

# TODO - test
# DROP - views
drop_view_account_value_current_by_asset = """
DROP VIEW IF EXISTS account_value_current_by_asset
"""

drop_view_asset_price_newest = """
DROP VIEW IF EXISTS asset_price_newest
"""

drop_view_asset_quantity_by_account_current = """
DROP VIEW IF EXISTS asset_quantity_by_account_current
"""

drop_view_asset_class_value_by_location = """
DROP VIEW IF EXISTS asset_class_value_by_location
"""

drop_view_asset_value_current = """
DROP VIEW IF EXISTS asset_value_current
"""

drop_view_component_value = """
DROP VIEW IF EXISTS component_value
"""

drop_views = {drop_view_account_value_current_by_asset,
              drop_view_asset_price_newest,
              drop_view_asset_quantity_by_account_current,
              drop_view_asset_class_value_by_location,
              drop_view_asset_value_current,
              drop_view_component_value}

# INSERT
insert_account = """
INSERT INTO account(id, name, account_type_id, institution_id, owner_id) 
VALUES(:id, :name, :account_type_id, :institution_id, :owner_id)
"""

insert_account_type = """
INSERT INTO account_type(id, name, tax_in, tax_growth, tax_out) 
VALUES(:id, :name, :tax_in, :tax_growth, :tax_out)
"""

insert_allocation = """
INSERT INTO allocation(id, asset_class_id, location_id, percentage) 
VALUES(:id, :asset_class_id, :location_id, :percentage)
"""

insert_asset = """
INSERT INTO asset(id, name, symbol)
VALUES(:id, :name, :symbol)
"""

insert_asset_class = """
INSERT INTO asset_class(id, name) 
VALUES(:id, :name)
"""

insert_balance = """
INSERT INTO balance(id, account_id, asset_id, balance_date, quantity) 
VALUES(:id, :account_id, :asset_id, :balance_date, :quantity)
"""

insert_component = """
INSERT INTO component(id, asset_id, asset_class_id, location_id, percentage) 
VALUES(:id, :asset_id, :asset_class_id, :location_id, :percentage)
"""

insert_institution = """
INSERT INTO institution(id, name) 
VALUES(:id, :name)
"""

insert_location = """
INSERT INTO location(id, name) 
VALUES(:id, :name)
"""

insert_owner = """
INSERT INTO owner(id, name, birthday) 
VALUES(:id, :name, :birthday)
"""

insert_price = """
INSERT INTO price(id, asset_id, price_date, amount) 
VALUES(:id, :asset_id, :price_date, :amount)
"""

# TODO - test
# SELECT
select_account = """
SELECT * FROM account
"""

select_account_type = """
SELECT * FROM account_type
"""

select_allocation = """
SELECT * FROM allocation
"""

select_asset = """
SELECT * FROM asset
"""

select_asset_class = """
SELECT * FROM asset_class
"""

select_balance = """
SELECT * FROM balance
"""

select_component = """
SELECT * FROM component
"""

select_institution = """
SELECT * FROM institution
"""

select_location = """
SELECT * FROM location
"""

select_owner = """
SELECT * FROM owner
"""

select_price = """
SELECT * FROM price
"""


# Calculations
# Accounts
# TODO - test
account_asset_quantity_current = """
SELECT * FROM asset_quantity_by_account_current
"""

# TODO - test
account_value_current_by_asset = """
SELECT * FROM account_value_current_by_asset 
"""

# Allocation
# TODO - test
allocation_deviation = """
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

# Assets
# TODO - test
asset_price_newest = """
SELECT * FROM asset_price_newest
"""

# TODO - test
asset_quantity = """
SELECT
    asset_id,
    SUM(quantity) quantity
FROM
    asset_quantity_by_account_current
GROUP BY
    asset_id
ORDER BY
    asset_id
"""

# TODO - test
asset_value_current = """
SELECT * FROM asset_value_current
"""

# Asset class
# TODO - test
asset_class_percentage = """
SELECT
    asset_class_id, 
    100.0 * SUM(current_value) / :net_worth AS percentage
FROM
    component_value
GROUP BY
    asset_class_id
"""

# TODO - test
asset_class_percentage_by_location = """
SELECT
    asset_class_id, 
    location_id,
    100.0 * SUM(current_value) / :net_worth AS percentage
FROM
    component_value
GROUP BY
    asset_class_id, location_id
"""

# TODO - test
asset_class_value = """
SELECT
    asset_class_id, 
    SUM(current_value) current_value
FROM
    component_value
GROUP BY
    asset_class_id
"""

# TODO - test
asset_class_value_by_location = """
SELECT * FROM asset_class_value_by_location
"""

# Net worth
net_worth = """
SELECT 
    SUM(current_values.current_value) AS net_worth
FROM
    account_value_current_by_asset AS current_values
"""
