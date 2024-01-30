# db.py
# SQL statements for the portfolio logic that are not currently being used
# 2024-01-30
# @juicemcpeso

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

# View related queries
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

