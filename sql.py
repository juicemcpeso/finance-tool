# SQL functions that take params

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

subset_percent = f"""
WITH
level AS ({level})

SELECT
    SUM(plan_percent) AS sum
FROM
    allocation_deviation,
    level
WHERE
    allocation_deviation.deviation <= level.deviation
"""

fill_to_level = f"""
WITH
level AS ({level})

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

assign_remainder = f"""
WITH 
level AS ({level}),
remaining_amount AS ({remaining_amount}),
subset_percent AS ({subset_percent})

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

where_to_contribute = f"""
WITH 
    level AS ({level}),
    subset_percent AS ({subset_percent}),
    fill_to_level AS ({fill_to_level}),
    remaining_amount AS ({remaining_amount}),
    assign_remainder AS ({assign_remainder})

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

where_to_contribute_formatted = f"""
WITH where_to_contribute AS ({where_to_contribute})

SELECT
    asset_class.name AS asset_class,
    location.name AS location,
    printf("$%,.2f", (CAST(contribution AS FLOAT) / decimal.constant)) AS contribution
FROM
    asset_class,
    decimal,
    location,
    where_to_contribute
WHERE
    asset_class.id == where_to_contribute.asset_class_id AND
    location.id == where_to_contribute.location_id
"""
