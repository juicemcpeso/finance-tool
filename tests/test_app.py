# test_app.py
# Tests for app.py
# 2024-01-22
# @juicemcpeso

import pytest
import tests.test_data_deviation as td_deviation


@pytest.mark.parametrize('amount', [0, 1000, 10000, 100000])
def test_where_to_contribute(test_app_db_1, amount):
    expected = td_deviation.expected[amount]
    assert expected == test_app_db_1.where_to_contribute(amount * test_app_db_1.decimal)
