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
# Allocation
allocation_deviation_with_next_level = """
SELECT
    allocation_deviation.asset_class_id,
    allocation_deviation.location_id,
    allocation_deviation.current_value,
    allocation_deviation.plan_percent,
    allocation_deviation.plan_value,
    allocation_deviation.deviation,
    d.deviation AS next_deviation
FROM 
    allocation_deviation
CROSS JOIN
    (SELECT DISTINCT deviation FROM allocation_deviation) AS d 
WHERE
    allocation_deviation.deviation < next_deviation
ORDER BY
    allocation_deviation.deviation ASC,
    next_deviation ASC
"""

value_at_each_deviation_level = """
SELECT
    allocation_deviation.asset_class_id,
    allocation_deviation.location_id,
    allocation_deviation.current_value,
    allocation_deviation.plan_percent,
    allocation_deviation.plan_value,
    allocation_deviation.deviation,
    d.deviation AS next_deviation,
    (d.deviation + decimal.constant) * allocation_deviation.plan_value / decimal.constant AS level_value 
FROM 
    allocation_deviation, decimal 
CROSS JOIN
    (SELECT deviation FROM allocation_deviation) AS d 
WHERE
    allocation_deviation.deviation < next_deviation
ORDER BY
    allocation_deviation.deviation ASC,
    next_deviation ASC
"""


# TODO: make this use the above view
sum_value_difference_at_each_deviation_level = """
WITH value_difference_each_deviation_level  AS (
SELECT
    allocation_deviation.asset_class_id,
    allocation_deviation.location_id,
    allocation_deviation.current_value,
    allocation_deviation.plan_percent,
    allocation_deviation.plan_value,
    allocation_deviation.deviation,
    d.deviation AS next_deviation,
    (d.deviation + decimal.constant) * allocation_deviation.plan_value / decimal.constant AS level_value,
    ((d.deviation + decimal.constant) * allocation_deviation.plan_value / 
        decimal.constant) - allocation_deviation.current_value AS value_difference 
FROM 
    allocation_deviation, decimal 
CROSS JOIN
    (SELECT deviation FROM allocation_deviation) AS d 
ORDER BY
    allocation_deviation.deviation ASC,
    next_deviation ASC
)
SELECT
    next_deviation AS deviation,
    SUM(value_difference) AS total_difference 
FROM
    value_difference_each_deviation_level 
WHERE
    value_difference >= 0
GROUP BY
    next_deviation
"""

which_deviation_level = """
WITH value_difference_each_deviation_level  AS (
SELECT
    allocation_deviation.asset_class_id,
    allocation_deviation.location_id,
    allocation_deviation.current_value,
    allocation_deviation.plan_percent,
    allocation_deviation.plan_value,
    allocation_deviation.deviation,
    d.deviation AS next_deviation,
    (d.deviation + decimal.constant) * allocation_deviation.plan_value / decimal.constant AS level_value,
    ((d.deviation + decimal.constant) * allocation_deviation.plan_value / 
        decimal.constant) - allocation_deviation.current_value AS value_difference 
FROM 
    allocation_deviation, decimal 
CROSS JOIN
    (SELECT deviation FROM allocation_deviation) AS d 
ORDER BY
    allocation_deviation.deviation ASC,
    next_deviation ASC
)
SELECT
    MAX(deviation) AS deviation
FROM (
    SELECT
        next_deviation AS deviation,
        SUM(value_difference) AS total_difference 
    FROM
        value_difference_each_deviation_level 
    WHERE
        value_difference >= 0
    GROUP BY
        next_deviation),
    decimal
WHERE
    total_difference <= :contribution * decimal.constant
"""

fill_full_amounts = """
WITH value_difference_each_deviation_level  AS (
SELECT
    allocation_deviation.asset_class_id,
    allocation_deviation.location_id,
    allocation_deviation.current_value,
    allocation_deviation.plan_percent,
    allocation_deviation.plan_value,
    allocation_deviation.deviation,
    d.deviation AS next_deviation,
    (d.deviation + decimal.constant) * allocation_deviation.plan_value / decimal.constant AS level_value,
    ((d.deviation + decimal.constant) * allocation_deviation.plan_value / 
        decimal.constant) - allocation_deviation.current_value AS value_difference 
FROM 
    allocation_deviation, decimal 
CROSS JOIN
    (SELECT deviation FROM allocation_deviation) AS d 
ORDER BY
    allocation_deviation.deviation ASC,
    next_deviation ASC
)
SELECT
    asset_class_id,
    location_id,
    value_difference AS contribution
FROM (
    SELECT
        MAX(deviation) AS deviation
    FROM (
        SELECT
            next_deviation AS deviation,
            SUM(value_difference) AS total_difference 
        FROM
            value_difference_each_deviation_level 
        WHERE
            value_difference >= 0
        GROUP BY
            next_deviation),
        decimal
    WHERE
        total_difference <= :contribution * decimal.constant) AS which_deviation_level,
    value_difference_each_deviation_level
WHERE
    next_deviation == which_deviation_level.deviation AND
    value_difference > 0
ORDER BY
    contribution DESC
"""

# Returns asset_class_id, location_id, and contribution for all accounts lower than target deviation, and 0 for account
# at target deviation
fill_full_amounts_inclusive = """
WITH value_difference_each_deviation_level  AS (
SELECT
    allocation_deviation.asset_class_id,
    allocation_deviation.location_id,
    allocation_deviation.current_value,
    allocation_deviation.plan_percent,
    allocation_deviation.plan_value,
    allocation_deviation.deviation,
    d.deviation AS next_deviation,
    (d.deviation + decimal.constant) * allocation_deviation.plan_value / decimal.constant AS level_value,
    ((d.deviation + decimal.constant) * allocation_deviation.plan_value / 
        decimal.constant) - allocation_deviation.current_value AS value_difference 
FROM 
    allocation_deviation, decimal 
CROSS JOIN
    (SELECT deviation FROM allocation_deviation) AS d 
ORDER BY
    allocation_deviation.deviation ASC,
    next_deviation ASC
)
SELECT
    asset_class_id,
    location_id,
    value_difference AS contribution
FROM (
    SELECT
        MAX(deviation) AS deviation
    FROM (
        SELECT
            next_deviation AS deviation,
            SUM(value_difference) AS total_difference 
        FROM
            value_difference_each_deviation_level 
        WHERE
            value_difference >= 0
        GROUP BY
            next_deviation),
        decimal
    WHERE
        total_difference <= :contribution * decimal.constant) AS which_deviation_level,
    value_difference_each_deviation_level
WHERE
    next_deviation == which_deviation_level.deviation AND
    value_difference >= 0 AND
    :contribution > 0
ORDER BY
    contribution DESC
"""

which_accounts_receive_funds = """
WITH which_deviation_level AS (WITH value_difference_each_deviation_level  AS (
SELECT
    allocation_deviation.asset_class_id,
    allocation_deviation.location_id,
    allocation_deviation.current_value,
    allocation_deviation.plan_percent,
    allocation_deviation.plan_value,
    allocation_deviation.deviation,
    d.deviation AS next_deviation,
    (d.deviation + decimal.constant) * allocation_deviation.plan_value / decimal.constant AS level_value,
    ((d.deviation + decimal.constant) * allocation_deviation.plan_value / 
        decimal.constant) - allocation_deviation.current_value AS value_difference 
FROM 
    allocation_deviation, decimal 
CROSS JOIN
    (SELECT deviation FROM allocation_deviation) AS d 
ORDER BY
    allocation_deviation.deviation ASC,
    next_deviation ASC
)
SELECT
    MAX(deviation) AS deviation
FROM (
    SELECT
        next_deviation AS deviation,
        SUM(value_difference) AS total_difference 
    FROM
        value_difference_each_deviation_level 
    WHERE
        value_difference >= 0
    GROUP BY
        next_deviation),
    decimal
WHERE
    total_difference <= :contribution * decimal.constant
)
SELECT
    asset_class_id,
    location_id
FROM
    allocation_deviation,
    which_deviation_level
WHERE
    allocation_deviation.deviation <= which_deviation_level.deviation and :contribution > 0
"""

remaining_amount = """
WITH deviation_checkpoint_values AS (
    WITH value_difference_each_deviation_level  AS (
    SELECT
        allocation_deviation.asset_class_id,
        allocation_deviation.location_id,
        allocation_deviation.current_value,
        allocation_deviation.plan_percent,
        allocation_deviation.plan_value,
        allocation_deviation.deviation,
        d.deviation AS next_deviation,
        (d.deviation + decimal.constant) * allocation_deviation.plan_value / decimal.constant AS level_value,
        ((d.deviation + decimal.constant) * allocation_deviation.plan_value / 
            decimal.constant) - allocation_deviation.current_value AS value_difference 
    FROM 
        allocation_deviation, decimal 
    CROSS JOIN
        (SELECT deviation FROM allocation_deviation) AS d 
    ORDER BY
        allocation_deviation.deviation ASC,
        next_deviation ASC
    )
    SELECT
        next_deviation AS deviation,
        SUM(value_difference) AS total_difference 
    FROM
        value_difference_each_deviation_level 
    WHERE
        value_difference >= 0
    GROUP BY
        next_deviation
)
SELECT
    :contribution * decimal.constant - MAX(total_difference) AS remainder
FROM 
    deviation_checkpoint_values,
    decimal
WHERE
    total_difference <= :contribution * decimal.constant 
"""

assign_remainder_proportionally = """
WITH 
remaining_amount AS (
    WITH deviation_checkpoint_values AS (
        WITH value_difference_each_deviation_level  AS (
        SELECT
            allocation_deviation.asset_class_id,
            allocation_deviation.location_id,
            allocation_deviation.current_value,
            allocation_deviation.plan_percent,
            allocation_deviation.plan_value,
            allocation_deviation.deviation,
            d.deviation AS next_deviation,
            (d.deviation + decimal.constant) * allocation_deviation.plan_value / decimal.constant AS level_value,
            ((d.deviation + decimal.constant) * allocation_deviation.plan_value / 
                decimal.constant) - allocation_deviation.current_value AS value_difference 
        FROM 
            allocation_deviation, decimal 
        CROSS JOIN
            (SELECT deviation FROM allocation_deviation) AS d 
        ORDER BY
            allocation_deviation.deviation ASC,
            next_deviation ASC
        )
        SELECT
            next_deviation AS deviation,
            SUM(value_difference) AS total_difference 
        FROM
            value_difference_each_deviation_level 
        WHERE
            value_difference >= 0
        GROUP BY
            next_deviation
    )
    SELECT
        :contribution * decimal.constant - MAX(total_difference) AS remainder
    FROM 
        deviation_checkpoint_values,
        decimal
    WHERE
        total_difference <= :contribution * decimal.constant),
accounts_receiving_funds AS (
    WITH which_deviation_level AS (WITH value_difference_each_deviation_level  AS (
    SELECT
        allocation_deviation.asset_class_id,
        allocation_deviation.location_id,
        allocation_deviation.current_value,
        allocation_deviation.plan_percent,
        allocation_deviation.plan_value,
        allocation_deviation.deviation,
        d.deviation AS next_deviation,
        (d.deviation + decimal.constant) * allocation_deviation.plan_value / decimal.constant AS level_value,
        ((d.deviation + decimal.constant) * allocation_deviation.plan_value / 
            decimal.constant) - allocation_deviation.current_value AS value_difference 
    FROM 
        allocation_deviation, decimal 
    CROSS JOIN
        (SELECT deviation FROM allocation_deviation) AS d 
    ORDER BY
        allocation_deviation.deviation ASC,
        next_deviation ASC
    )
    SELECT
        MAX(deviation) AS deviation
    FROM (
        SELECT
            next_deviation AS deviation,
            SUM(value_difference) AS total_difference 
        FROM
            value_difference_each_deviation_level 
        WHERE
            value_difference >= 0
        GROUP BY
            next_deviation),
        decimal
    WHERE
        total_difference <= :contribution * decimal.constant
    )
    SELECT
        asset_class_id,
        location_id,
        plan_percent
    FROM
        allocation_deviation,
        which_deviation_level
    WHERE
        allocation_deviation.deviation <= which_deviation_level.deviation and :contribution > 0)
SELECT
    asset_class_id,
    location_id,
    remainder * plan_percent / sum AS contribution
FROM
    accounts_receiving_funds,
    remaining_amount,
    (SELECT
        SUM(plan_percent) AS sum
    FROM
        accounts_receiving_funds)
GROUP BY
    asset_class_id,
    location_id
"""

# where_to_contribute = """
# WITH assign_remainder AS (
#     WITH
#     remaining_amount AS (
#         WITH deviation_checkpoint_values AS (
#             WITH value_difference_each_deviation_level  AS (
#             SELECT
#                 allocation_deviation.asset_class_id,
#                 allocation_deviation.location_id,
#                 allocation_deviation.current_value,
#                 allocation_deviation.plan_percent,
#                 allocation_deviation.plan_value,
#                 allocation_deviation.deviation,
#                 d.deviation AS next_deviation,
#                 (d.deviation + decimal.constant) * allocation_deviation.plan_value / decimal.constant AS level_value,
#                 ((d.deviation + decimal.constant) * allocation_deviation.plan_value /
#                     decimal.constant) - allocation_deviation.current_value AS value_difference
#             FROM
#                 allocation_deviation, decimal
#             CROSS JOIN
#                 (SELECT deviation FROM allocation_deviation) AS d
#             ORDER BY
#                 allocation_deviation.deviation ASC,
#                 next_deviation ASC
#             )
#             SELECT
#                 next_deviation AS deviation,
#                 SUM(value_difference) AS total_difference
#             FROM
#                 value_difference_each_deviation_level
#             WHERE
#                 value_difference >= 0
#             GROUP BY
#                 next_deviation
#         )
#         SELECT
#             :contribution * decimal.constant - MAX(total_difference) AS remainder
#         FROM
#             deviation_checkpoint_values,
#             decimal
#         WHERE
#             total_difference <= :contribution * decimal.constant),
#     accounts_receiving_funds AS (
#         WITH which_deviation_level AS (WITH value_difference_each_deviation_level  AS (
#         SELECT
#             allocation_deviation.asset_class_id,
#             allocation_deviation.location_id,
#             allocation_deviation.current_value,
#             allocation_deviation.plan_percent,
#             allocation_deviation.plan_value,
#             allocation_deviation.deviation,
#             d.deviation AS next_deviation,
#             (d.deviation + decimal.constant) * allocation_deviation.plan_value / decimal.constant AS level_value,
#             ((d.deviation + decimal.constant) * allocation_deviation.plan_value /
#                 decimal.constant) - allocation_deviation.current_value AS value_difference
#         FROM
#             allocation_deviation, decimal
#         CROSS JOIN
#             (SELECT deviation FROM allocation_deviation) AS d
#         ORDER BY
#             allocation_deviation.deviation ASC,
#             next_deviation ASC
#         )
#         SELECT
#             MAX(deviation) AS deviation
#         FROM (
#             SELECT
#                 next_deviation AS deviation,
#                 SUM(value_difference) AS total_difference
#             FROM
#                 value_difference_each_deviation_level
#             WHERE
#                 value_difference >= 0
#             GROUP BY
#                 next_deviation),
#             decimal
#         WHERE
#             total_difference <= :contribution * decimal.constant
#         )
#         SELECT
#             asset_class_id,
#             location_id,
#             plan_percent
#         FROM
#             allocation_deviation,
#             which_deviation_level
#         WHERE
#             allocation_deviation.deviation <= which_deviation_level.deviation and :contribution > 0)
#     SELECT
#         asset_class_id,
#         location_id,
#         remainder * plan_percent / sum AS contribution
#     FROM
#         accounts_receiving_funds,
#         remaining_amount,
#         (SELECT
#             SUM(plan_percent) AS sum
#         FROM
#             accounts_receiving_funds)
#     GROUP BY
#         asset_class_id,
#         location_id),
# fill_to_checkpoint AS (
#     WITH value_difference_each_deviation_level  AS (
#     SELECT
#         allocation_deviation.asset_class_id,
#         allocation_deviation.location_id,
#         allocation_deviation.current_value,
#         allocation_deviation.plan_percent,
#         allocation_deviation.plan_value,
#         allocation_deviation.deviation,
#         d.deviation AS next_deviation,
#         (d.deviation + decimal.constant) * allocation_deviation.plan_value / decimal.constant AS level_value,
#         ((d.deviation + decimal.constant) * allocation_deviation.plan_value /
#             decimal.constant) - allocation_deviation.current_value AS value_difference
#     FROM
#         allocation_deviation, decimal
#     CROSS JOIN
#         (SELECT deviation FROM allocation_deviation) AS d
#     ORDER BY
#         allocation_deviation.deviation ASC,
#         next_deviation ASC
#     )
#     SELECT
#         asset_class_id,
#         location_id,
#         value_difference AS contribution
#     FROM (
#         SELECT
#             MAX(deviation) AS deviation
#         FROM (
#             SELECT
#                 next_deviation AS deviation,
#                 SUM(value_difference) AS total_difference
#             FROM
#                 value_difference_each_deviation_level
#             WHERE
#                 value_difference >= 0
#             GROUP BY
#                 next_deviation),
#             decimal
#         WHERE
#             total_difference <= :contribution * decimal.constant) AS which_deviation_level,
#         value_difference_each_deviation_level
#     WHERE
#         next_deviation == which_deviation_level.deviation AND
#         value_difference >= 0 AND
#         :contribution > 0
#     ORDER BY
#         contribution DESC)
# SELECT
#     fill_to_checkpoint.asset_class_id,
#     fill_to_checkpoint.location_id,
#     fill_to_checkpoint.contribution + assign_remainder.contribution AS contribution
# FROM
#     fill_to_checkpoint,
#     assign_remainder
# WHERE
#     fill_to_checkpoint.asset_class_id = assign_remainder.asset_class_id AND
#     fill_to_checkpoint.location_id == assign_remainder.location_id
# """

where_to_contribute = """
WITH assign_remainder AS (
    WITH 
    remaining_amount AS (
        WITH deviation_checkpoint_values AS (
            WITH value_difference_each_deviation_level  AS (
            SELECT
                allocation_deviation.asset_class_id,
                allocation_deviation.location_id,
                allocation_deviation.current_value,
                allocation_deviation.plan_percent,
                allocation_deviation.plan_value,
                allocation_deviation.deviation,
                d.deviation AS next_deviation,
                (d.deviation + decimal.constant) * allocation_deviation.plan_value / decimal.constant AS level_value,
                ((d.deviation + decimal.constant) * allocation_deviation.plan_value / 
                    decimal.constant) - allocation_deviation.current_value AS value_difference 
            FROM 
                allocation_deviation, decimal 
            CROSS JOIN
                (SELECT deviation FROM allocation_deviation) AS d 
            ORDER BY
                allocation_deviation.deviation ASC,
                next_deviation ASC
            )
            SELECT
                next_deviation AS deviation,
                SUM(value_difference) AS total_difference 
            FROM
                value_difference_each_deviation_level 
            WHERE
                value_difference >= 0
            GROUP BY
                next_deviation
        )
        SELECT
            :contribution * decimal.constant - MAX(total_difference) AS remainder
        FROM 
            deviation_checkpoint_values,
            decimal
        WHERE
            total_difference <= :contribution * decimal.constant),
    accounts_receiving_funds AS (
        WITH which_deviation_level AS (WITH value_difference_each_deviation_level  AS (
        SELECT
            allocation_deviation.asset_class_id,
            allocation_deviation.location_id,
            allocation_deviation.current_value,
            allocation_deviation.plan_percent,
            allocation_deviation.plan_value,
            allocation_deviation.deviation,
            d.deviation AS next_deviation,
            (d.deviation + decimal.constant) * allocation_deviation.plan_value / decimal.constant AS level_value,
            ((d.deviation + decimal.constant) * allocation_deviation.plan_value / 
                decimal.constant) - allocation_deviation.current_value AS value_difference 
        FROM 
            allocation_deviation, decimal 
        CROSS JOIN
            (SELECT deviation FROM allocation_deviation) AS d 
        ORDER BY
            allocation_deviation.deviation ASC,
            next_deviation ASC
        )
        SELECT
            MAX(deviation) AS deviation
        FROM (
            SELECT
                next_deviation AS deviation,
                SUM(value_difference) AS total_difference 
            FROM
                value_difference_each_deviation_level 
            WHERE
                value_difference >= 0
            GROUP BY
                next_deviation),
            decimal
        WHERE
            total_difference <= :contribution * decimal.constant
        )
        SELECT
            asset_class_id,
            location_id,
            plan_percent
        FROM
            allocation_deviation,
            which_deviation_level
        WHERE
            allocation_deviation.deviation <= which_deviation_level.deviation and :contribution > 0)
    SELECT
        asset_class_id,
        location_id,
        remainder * plan_percent / sum AS contribution
    FROM
        accounts_receiving_funds,
        remaining_amount,
        (SELECT
            SUM(plan_percent) AS sum
        FROM
            accounts_receiving_funds)
    GROUP BY
        asset_class_id,
        location_id),
fill_to_checkpoint AS (
    WITH value_difference_each_deviation_level  AS (
    SELECT
        allocation_deviation.asset_class_id,
        allocation_deviation.location_id,
        allocation_deviation.current_value,
        allocation_deviation.plan_percent,
        allocation_deviation.plan_value,
        allocation_deviation.deviation,
        d.deviation AS next_deviation,
        (d.deviation + decimal.constant) * allocation_deviation.plan_value / decimal.constant AS level_value,
        ((d.deviation + decimal.constant) * allocation_deviation.plan_value / 
            decimal.constant) - allocation_deviation.current_value AS value_difference 
    FROM 
        allocation_deviation, decimal 
    CROSS JOIN
        (SELECT deviation FROM allocation_deviation) AS d 
    ORDER BY
        allocation_deviation.deviation ASC,
        next_deviation ASC
    )
    SELECT
        asset_class_id,
        location_id,
        value_difference AS contribution
    FROM (
        SELECT
            MAX(deviation) AS deviation
        FROM (
            SELECT
                next_deviation AS deviation,
                SUM(value_difference) AS total_difference 
            FROM
                value_difference_each_deviation_level 
            WHERE
                value_difference >= 0
            GROUP BY
                next_deviation),
            decimal
        WHERE
            total_difference <= :contribution * decimal.constant) AS which_deviation_level,
        value_difference_each_deviation_level
    WHERE
        next_deviation == which_deviation_level.deviation AND
        value_difference >= 0 AND
        :contribution > 0
    ORDER BY
        contribution DESC)
SELECT
    fill_to_checkpoint.asset_class_id,
    fill_to_checkpoint.location_id,
    fill_to_checkpoint.contribution + assign_remainder.contribution AS contribution 
FROM
    fill_to_checkpoint,
    assign_remainder
WHERE
    fill_to_checkpoint.asset_class_id = assign_remainder.asset_class_id AND
    fill_to_checkpoint.location_id == assign_remainder.location_id 
"""

net_worth_formatted = """   
SELECT
    net_worth.net_worth / decimal.constant AS net_worth
FROM
    net_worth, decimal 
"""
