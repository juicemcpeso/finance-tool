import pytest

import action


def test_add_owner(test_app):
    entry = {'name': 'Carlos', 'birthday': '2000-01-01'}
    add_action = action.AddOwner(test_app)
    add_action.data.update(entry)
    add_action()

    sql = """
    SELECT name, birthday FROM owner WHERE id = 3
    """

    assert entry == test_app.portfolio.sql_fetch_one(sql)
