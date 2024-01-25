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

# DROP