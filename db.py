# db.py
# SQL statements for the portfolio logic
# 2024-01-25
# @juicemcpeso

import csv
import os
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
    try:
        cur.execute(cmd, params) if params is not None else cur.execute(cmd)
    except sqlite3.IntegrityError:
        pass

    con.commit()
    con.close()


# TODO - test?
def execute_many(database, cmd, data_sequence):
    """Execute a single command multiple times with different data"""
    con = sqlite3.connect(database)
    cur = con.cursor()
    try:
        cur.executemany(cmd, data_sequence)
    except sqlite3.IntegrityError:
        pass
    con.commit()
    con.close()


# TODO - test?
def execute_script(database, cmd):
    """Execute script of commands"""
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.executescript(cmd)
    con.commit()
    con.close()


def execute_file(database, file_name):
    with open(file_name, 'r') as sql_file:
        execute_script(database, sql_file.read())


# TODO - test
def fetch_one(database, cmd, params=None):
    con = sqlite3.connect(database)
    con.row_factory = dict_factory
    cur = con.cursor()
    result = cur.execute(cmd, params).fetchone() if params is not None else cur.execute(cmd).fetchone()
    con.commit()
    con.close()
    return result


# TODO - test
def fetch_all(database, cmd, params=None):
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


def insert_from_csv_file(database, file_path, table_name):
    with open(file_path) as csv_file:
        csv_dict = csv.DictReader(csv_file)
        execute_many(database=database, cmd=insert[table_name], data_sequence=csv_dict)


def insert_from_csv_directory(database, directory_path):
    for file_name in os.listdir(directory_path):
        insert_from_csv_file(database=database, file_path=directory_path + file_name, table_name=os.path.splitext(file_name)[0])


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

insert_constant = """
INSERT INTO constant(id, name, amount)
VALUES(:id, :name, :amount)
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

# Calculations
# Where to contribute
level = """
SELECT
    MAX(deviation) AS deviation
FROM
    deviation_level_value,
    decimal
WHERE
    level_value <= :contribution * decimal.constant
"""

subset_percent = """
WITH
level AS (
    SELECT
        MAX(deviation) AS deviation
    FROM
        deviation_level_value,
        decimal
    WHERE
        level_value <= :contribution * decimal.constant
)
SELECT
    SUM(plan_percent) AS sum
FROM
    allocation_deviation,
    level
WHERE
    allocation_deviation.deviation <= level.deviation
"""

fill_to_level = """
WITH
level AS (
    SELECT
        MAX(deviation) AS deviation
    FROM
        deviation_level_value,
        decimal
    WHERE
        level_value <= :contribution * decimal.constant
)
SELECT
    asset_class_id,
    location_id,
    value_difference AS contribution
FROM
    level,
    allocation_deviation_all_levels 
WHERE
    next_deviation == level.deviation AND
    value_difference >= 0 AND
    :contribution > 0
ORDER BY
    contribution DESC
"""

remaining_amount = """
SELECT
    :contribution * decimal.constant - MAX(level_value) AS remainder
FROM 
    deviation_level_value, 
    decimal
WHERE
    level_value <= :contribution * decimal.constant
"""

assign_remainder = """
WITH 
level AS (
    SELECT
        MAX(deviation) AS deviation
    FROM
        deviation_level_value,
        decimal
    WHERE
        level_value <= :contribution * decimal.constant
),
remaining_amount AS (
    SELECT
        :contribution * decimal.constant - MAX(level_value) AS remainder
    FROM 
        deviation_level_value, 
        decimal
    WHERE
        level_value <= :contribution * decimal.constant
),
subset_percent AS (
    SELECT
        SUM(plan_percent) AS sum
    FROM
        allocation_deviation,
        level
    WHERE
        allocation_deviation.deviation <= level.deviation
)
SELECT
    asset_class_id,
    location_id,
    remainder * plan_percent / subset_percent.sum AS contribution
FROM
    allocation_deviation,
    level,
    remaining_amount,
    subset_percent
WHERE
    allocation_deviation.deviation <= level.deviation AND
    :contribution > 0
GROUP BY
    asset_class_id,
    location_id
"""

where_to_contribute = """
WITH 
level AS (
    SELECT
        MAX(deviation) AS deviation
    FROM
        deviation_level_value,
        decimal
    WHERE
        level_value <= :contribution * decimal.constant
),
subset_percent AS (
    SELECT
        SUM(plan_percent) AS sum
    FROM
        allocation_deviation,
        level
    WHERE
        allocation_deviation.deviation <= level.deviation
),
fill_to_level AS (
    SELECT
        asset_class_id,
        location_id,
        value_difference AS contribution
    FROM
        level,
        allocation_deviation_all_levels 
    WHERE
        next_deviation == level.deviation AND
        value_difference >= 0 AND
        :contribution > 0
    ORDER BY
        contribution DESC
),
remaining_amount AS (
    SELECT
        :contribution * decimal.constant - MAX(level_value) AS remainder
    FROM 
        deviation_level_value, 
        decimal
    WHERE
        level_value <= :contribution * decimal.constant
),
assign_remainder AS (
    SELECT
        asset_class_id,
        location_id,
        remainder * plan_percent / subset_percent.sum AS contribution
    FROM
        allocation_deviation,
        level,
        remaining_amount,
        subset_percent
    WHERE
        allocation_deviation.deviation <= level.deviation AND
        :contribution > 0
    GROUP BY
        asset_class_id,
        location_id
)

SELECT
    fill_to_level.asset_class_id,
    fill_to_level.location_id,
    fill_to_level.contribution + assign_remainder.contribution AS contribution 
FROM
    fill_to_level,
    assign_remainder
WHERE
    fill_to_level.asset_class_id = assign_remainder.asset_class_id AND
    fill_to_level.location_id == assign_remainder.location_id 
"""

# Net worth
net_worth_formatted = """   
SELECT
    net_worth.net_worth / decimal.constant AS net_worth
FROM
    net_worth, decimal 
"""

insert = {'account': insert_account,
          'account_type': insert_account_type,
          'allocation': insert_allocation,
          'asset': insert_asset,
          'asset_class': insert_asset_class,
          'balance': insert_balance,
          'component': insert_component,
          'constant': insert_constant,
          'institution': insert_institution,
          'location': insert_location,
          'owner': insert_owner,
          'price': insert_price}