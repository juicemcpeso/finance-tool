# portfolio_db.py
# SQL statements for the portfolio logic
# 2024-01-25
# @juicemcpeso

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

create_table_asset = """
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

create_table_asset = """
CREATE TABLE IF NOT EXISTS asset_class (
    id INTEGER PRIMARY KEY,
    name TEXT
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

# Views
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
"""

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
"""

create_view_asset_quantity_by_account = """
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
"""

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
"""

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
"""

# Drop
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

# INSERT
insert_account = """
INSERT INTO account(name, account_type_id, institution_id, owner_id) 
VALUES(:name, :account_type_id, :institution_id, :owner_id)
"""

insert_account_type = """
INSERT INTO account_type(name, tax_in, tax_growth, tax_out) 
VALUES(:name, :tax_in, :tax_growth, :tax_out)
"""

insert_allocation = """
INSERT INTO allocation(asset_class_id, location_id, percentage) 
VALUES(:asset_class_id, :location_id, :percentage)
"""

insert_asset = """
INSERT INTO asset(name, symbol) 
VALUES(:name, :symbol)
"""

insert_asset_class = """
INSERT INTO asset_class(name) 
VALUES(:name)
"""

insert_balance = """
INSERT INTO balance(account_id, asset_id, balance_date, quantity) 
VALUES(:account_id, :asset_id, :balance_date, :quantity)
"""

insert_component = """
INSERT INTO component(asset_id, asset_class_id, location_id, percentage) 
VALUES(:asset_id, :asset_class_id, :location_id, :percentage)
"""

insert_institution = """
INSERT INTO institution(name) 
VALUES(:name)
"""

insert_location = """
INSERT INTO location(name) 
VALUES(:name)
"""

insert_owner = """
INSERT INTO owner(name, birthday) 
VALUES(:name, :birthday)
"""

insert_price = """
INSERT INTO price(asset_id, price_date, amount) 
VALUES(:asset_id, :price_date, :amount)
"""

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