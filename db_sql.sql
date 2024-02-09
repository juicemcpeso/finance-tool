CREATE TABLE IF NOT EXISTS account (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    account_type_id INTEGER,
    institution_id INTEGER,
    owner_id INTEGER,
    FOREIGN KEY(account_type_id) REFERENCES account_type(id),
    FOREIGN KEY(owner_id) REFERENCES owner(id),
    FOREIGN KEY(institution_id) REFERENCES institution(id)
);

CREATE TABLE IF NOT EXISTS account_type (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    tax_in INTEGER,
    tax_growth INTEGER,
    tax_out INTEGER,

    CHECK (tax_in IN (0, 1)
        AND tax_growth IN (0, 1)
        AND tax_out IN (0, 1))
);

CREATE TABLE IF NOT EXISTS allocation (
    id INTEGER PRIMARY KEY,
    asset_class_id INTEGER,
    location_id INTEGER,
    percentage INTEGER NOT NULL,
    FOREIGN KEY(asset_class_id) REFERENCES asset_class(id),
    FOREIGN KEY(location_id) REFERENCES location(id)

    CHECK (percentage BETWEEN 0 AND 10000)
);

CREATE TABLE IF NOT EXISTS asset (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    symbol TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS asset_class (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS balance (
    id INTEGER PRIMARY KEY,
    account_id INTEGER,
    asset_id INTEGER,
    balance_date TEXT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY(account_id) REFERENCES account(id),
    FOREIGN KEY(asset_id) REFERENCES asset(id)

    CHECK (TYPEOF(balance_date) IS "text")
    CHECK (balance_date IS strftime('%Y-%m-%d', balance_date))
    CHECK (TYPEOF(quantity) IS "integer" OR TYPEOF(quantity) IS "real")
    CHECK (quantity >= 0)
);

CREATE TABLE IF NOT EXISTS component (
    id INTEGER PRIMARY KEY,
    asset_id INTEGER,
    asset_class_id INTEGER,
    location_id INTEGER,
    percentage INT,
    FOREIGN KEY(asset_id) REFERENCES asset(id),
    FOREIGN KEY(asset_class_id) REFERENCES asset_class(id),
    FOREIGN KEY(location_id) REFERENCES location(id)

    CHECK (percentage BETWEEN 0 AND 10000)
);

CREATE TABLE IF NOT EXISTS constant (
    id INTEGER PRIMARY KEY,
    name TEXT,
    amount INT
);

CREATE TABLE IF NOT EXISTS institution(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS location (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS owner (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    birthday TEXT

    CHECK (TYPEOF(birthday) IS "text")
    CHECK (birthday IS strftime('%Y-%m-%d', birthday))
);

CREATE TABLE IF NOT EXISTS price (
    id INTEGER PRIMARY KEY,
    asset_id INTEGER,
    price_date TEXT,
    amount INT,
    FOREIGN KEY(asset_id) REFERENCES asset(id)

    CHECK (TYPEOF(price_date) IS "text")
    CHECK (price_date IS strftime('%Y-%m-%d', price_date))
    CHECK (TYPEOF(amount) IS "integer" OR TYPEOF(amount) IS "real")
);

CREATE VIEW IF NOT EXISTS account_value_current_by_asset AS
SELECT
    b.account_id,
    b.asset_id,
    MAX(b.balance_date) balance_date,
    b.quantity * p.amount / decimal.constant AS current_value
FROM
    balance AS b, decimal
JOIN
    asset_price_newest AS p ON b.asset_id = p.asset_id
GROUP BY
    b.account_id, b.asset_id
;

-- TODO: test to make sure this works with decimal contributions
-- Divide by the decimal constant at the end, otherwise integer division results in 0
--
-- In calculation for deviation, multiply by constant twice: once to convert plan.percentage to a decimal, and the second
-- time to convert the entire calculation from a decimal to an integer.
CREATE VIEW IF NOT EXISTS allocation_deviation AS
SELECT
    plan.asset_class_id,
    plan.location_id,
    current_values.current_value,
    plan.percentage AS plan_percent,
    plan.percentage * net_worth.net_worth / decimal.constant AS plan_value,
    current_values.current_value * decimal.constant * decimal.constant /
        (plan.percentage * net_worth.net_worth) - decimal.constant AS deviation
FROM
    allocation AS plan, decimal, net_worth
JOIN
    asset_class_value_by_location AS current_values ON current_values.asset_class_id == plan.asset_class_id AND
    current_values.location_id == plan.location_id
ORDER BY
    deviation ASC
;

CREATE VIEW IF NOT EXISTS allocation_deviation_all_levels AS
SELECT
    allocation_deviation.asset_class_id,
    allocation_deviation.location_id,
    allocation_deviation.current_value,
    allocation_deviation.plan_percent,
    allocation_deviation.plan_value,
    allocation_deviation.deviation,
    d.deviation AS next_deviation,
    (d.deviation + decimal.constant) * allocation_deviation.plan_value / decimal.constant AS value_at_next_deviation,
    ((d.deviation + decimal.constant) * allocation_deviation.plan_value /
        decimal.constant) - allocation_deviation.current_value AS value_difference
FROM
    allocation_deviation, decimal
CROSS JOIN
     deviation_level AS d
WHERE
    allocation_deviation.deviation <= next_deviation
ORDER BY
    allocation_deviation.deviation ASC,
    next_deviation ASC
;

CREATE VIEW IF NOT EXISTS asset_price_newest AS
SELECT
    asset_id,
    MAX(price_date) price_date,
    amount
FROM
    price
GROUP BY
    asset_id
;

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
;

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
;

CREATE VIEW IF NOT EXISTS asset_class_value_by_location AS
SELECT
    asset_class_id,
    location_id,
    SUM(current_value) current_value
FROM
    component_value
GROUP BY
    asset_class_id, location_id
;

CREATE VIEW IF NOT EXISTS component_value AS
SELECT
    c.asset_id,
    c.asset_class_id,
    c.location_id,
    c.percentage * v.current_value / decimal.constant AS current_value
FROM
    component AS c, decimal
JOIN
    asset_value_current AS v ON c.asset_id = v.asset_id
;

CREATE VIEW IF NOT EXISTS decimal AS
    SELECT amount AS constant
    FROM constant
    WHERE name = 'decimal'
;

-- TODO: make sure this works with non distinct values
CREATE VIEW IF NOT EXISTS deviation_level AS
    SELECT DISTINCT deviation FROM allocation_deviation
;

CREATE VIEW IF NOT EXISTS deviation_level_value AS
    SELECT
        next_deviation as deviation,
        SUM(value_difference) AS level_value
    FROM
        allocation_deviation_all_levels
    WHERE
        value_difference >= 0
    GROUP BY
        next_deviation
;

CREATE VIEW IF NOT EXISTS net_worth AS
    SELECT
        SUM(current_values.current_value) AS net_worth
    FROM
        account_value_current_by_asset AS current_values
;

CREATE TRIGGER IF NOT EXISTS format_allocation AFTER INSERT ON allocation
BEGIN
    UPDATE allocation SET percentage = ROUND(percentage * 10000) WHERE id = NEW.id;
END
;

CREATE TRIGGER IF NOT EXISTS format_balance AFTER INSERT ON balance
BEGIN
    UPDATE balance SET quantity = ROUND(quantity * 10000) WHERE id = NEW.id;
    UPDATE balance SET balance_date = date(balance_date, '0 days') WHERE id = NEW.id;
END
;

CREATE TRIGGER IF NOT EXISTS format_component AFTER INSERT ON component
BEGIN
    UPDATE component SET percentage = ROUND(percentage * 10000) WHERE id = NEW.id;
END
;

CREATE TRIGGER IF NOT EXISTS format_owner AFTER INSERT ON owner
BEGIN
    UPDATE owner SET birthday = date(birthday, '0 days') WHERE id = NEW.id;
END
;

CREATE TRIGGER IF NOT EXISTS format_price AFTER INSERT ON price
BEGIN
    UPDATE price SET amount = ROUND(amount * 10000) WHERE id = NEW.id;
END
;
