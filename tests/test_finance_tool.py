# Tests for finance_tool.py
# 2024-01-25
# @juicemcpeso

import finance_tool
import pytest


def create_test_ft_from_json(tmp_path, json_file_name=None):
    test_ft = finance_tool.FinanceTool(tmp_path / "test.db")

    if json_file_name is not None:
        test_ft.insert_from_json(json_file_name)

    return test_ft


# Finance tool with empty database
@pytest.fixture
def test_ft_0(tmp_path):
    return create_test_ft_from_json(tmp_path)


# # Use for simplified allocation data
@pytest.fixture
def test_ft_1(tmp_path):
    return create_test_ft_from_json(tmp_path, '../tests/data/test_db_1.json')


table_names = {'account',
               'account_type',
               'allocation',
               'asset',
               'asset_class',
               'balance',
               'component',
               'constant',
               'institution',
               'location',
               'owner',
               'price'}

# Tests CSV and JSON
data_strings = {'account':
                    [{'id': '1', 'name': 'Work 401k', 'account_type_id': '1', 'institution_id': '1', 'owner_id': '1'}],
                'account_type':
                    [{'id': '1', 'name': '401k', 'tax_in': '0', 'tax_growth': '0', 'tax_out': '1'}],
                'allocation':
                    [{'id': '1', 'asset_class_id': '1', 'location_id': '1', 'percentage': '.4000'},
                               {'id': '2', 'asset_class_id': '1', 'location_id': '2', 'percentage': '.2000'},
                               {'id': '3', 'asset_class_id': '2', 'location_id': '1', 'percentage': '.2500'},
                               {'id': '4', 'asset_class_id': '2', 'location_id': '2', 'percentage': '.0500'},
                               {'id': '5', 'asset_class_id': '3', 'location_id': '1', 'percentage': '.1000'}],
                'asset':
                    [{'id': '1', 'name': 'Rearguard Total Stock Market Index Fund', 'symbol': 'RSUSA'},
                          {'id': '2', 'name': 'Rearguard Total International Stock Index Fund', 'symbol': 'RSINT'},
                          {'id': '3', 'name': 'Rearguard Total Bond Market Index Fund', 'symbol': 'RBUSA'},
                          {'id': '4', 'name': 'Rearguard Total International Bond Index Fund', 'symbol': 'RBINT'},
                          {'id': '5', 'name': 'US Dollars', 'symbol': 'USD'}],
                'asset_class':
                    [{'id': '1', 'name': 'stocks'}, {'id': '2', 'name': 'bonds'},
                                {'id': '3', 'name': 'cash'}, {'id': '4', 'name': 'other'}],
                'balance': [
                    {'id': '1', 'account_id': '1', 'asset_id': '1', 'balance_date': '2021-01-01', 'quantity': '34000'},
                    {'id': '2', 'account_id': '1', 'asset_id': '2', 'balance_date': '2021-01-01', 'quantity': '14000'},
                    {'id': '3', 'account_id': '1', 'asset_id': '3', 'balance_date': '2021-01-01', 'quantity': '34000'},
                    {'id': '4', 'account_id': '1', 'asset_id': '4', 'balance_date': '2021-01-01', 'quantity': '4000'},
                    {'id': '5', 'account_id': '1', 'asset_id': '5', 'balance_date': '2021-01-01', 'quantity': '14000'}],
                'component': [
                    {'id': '1', 'asset_id': '1', 'asset_class_id': '1', 'location_id': '1', 'percentage': '1'},
                    {'id': '2', 'asset_id': '2', 'asset_class_id': '1', 'location_id': '2', 'percentage': '1'},
                    {'id': '3', 'asset_id': '3', 'asset_class_id': '2', 'location_id': '1', 'percentage': '1'},
                    {'id': '4', 'asset_id': '4', 'asset_class_id': '2', 'location_id': '2', 'percentage': '1'},
                    {'id': '5', 'asset_id': '5', 'asset_class_id': '3', 'location_id': '1', 'percentage': '1'}],
                'constant': [{'id': '1', 'name': 'decimal', 'amount': '10000'}],
                'institution': [{'id': '1', 'name': 'Rearguard Investments'}],
                'location': [{'id': '1', 'name': 'USA'}, {'id': '2', 'name': 'International'},
                             {'id': '3', 'name': 'World'}],
                'owner': [{'id': '1', 'name': 'Bob', 'birthday': '1992-10-31'}],
                'price': [{'id': '1', 'asset_id': '1', 'price_date': '2020-01-01', 'amount': '1'},
                          {'id': '2', 'asset_id': '2', 'price_date': '2020-01-01', 'amount': '1'},
                          {'id': '3', 'asset_id': '3', 'price_date': '2020-01-01', 'amount': '1'},
                          {'id': '4', 'asset_id': '4', 'price_date': '2020-01-01', 'amount': '1'},
                          {'id': '5', 'asset_id': '5', 'price_date': '1776-07-04', 'amount': '1'}]}

data_formatted = {'account': [{'id': 1, 'name': 'Work 401k', 'account_type_id': 1, 'institution_id': 1, 'owner_id': 1}],
                 'account_type': [{'id': 1, 'name': '401k', 'tax_in': 0, 'tax_growth': 0, 'tax_out': 1}],
                 'allocation': [{'id': 1, 'asset_class_id': 1, 'location_id': 1, 'percentage': 4000},
                                {'id': 2, 'asset_class_id': 1, 'location_id': 2, 'percentage': 2000},
                                {'id': 3, 'asset_class_id': 2, 'location_id': 1, 'percentage': 2500},
                                {'id': 4, 'asset_class_id': 2, 'location_id': 2, 'percentage': 500},
                                {'id': 5, 'asset_class_id': 3, 'location_id': 1, 'percentage': 1000}],
                 'asset': [{'id': 1, 'name': 'Rearguard Total Stock Market Index Fund', 'symbol': 'RSUSA'},
                           {'id': 2, 'name': 'Rearguard Total International Stock Index Fund', 'symbol': 'RSINT'},
                           {'id': 3, 'name': 'Rearguard Total Bond Market Index Fund', 'symbol': 'RBUSA'},
                           {'id': 4, 'name': 'Rearguard Total International Bond Index Fund', 'symbol': 'RBINT'},
                           {'id': 5, 'name': 'US Dollars', 'symbol': 'USD'}],
                  'asset_class': [{'id': 1, 'name': 'stocks'},
                                 {'id': 2, 'name': 'bonds'},
                                 {'id': 3, 'name': 'cash'},
                                 {'id': 4, 'name': 'other'}],
                  'balance': [
                     {'id': 1, 'account_id': 1, 'asset_id': 1, 'balance_date': '2021-01-01', 'quantity': 340000000},
                     {'id': 2, 'account_id': 1, 'asset_id': 2, 'balance_date': '2021-01-01', 'quantity': 140000000},
                     {'id': 3, 'account_id': 1, 'asset_id': 3, 'balance_date': '2021-01-01', 'quantity': 340000000},
                     {'id': 4, 'account_id': 1, 'asset_id': 4, 'balance_date': '2021-01-01', 'quantity': 40000000},
                     {'id': 5, 'account_id': 1, 'asset_id': 5, 'balance_date': '2021-01-01', 'quantity': 140000000}],
                  'component': [{'id': 1, 'asset_id': 1, 'asset_class_id': 1, 'location_id': 1, 'percentage': 10000},
                               {'id': 2, 'asset_id': 2, 'asset_class_id': 1, 'location_id': 2, 'percentage': 10000},
                               {'id': 3, 'asset_id': 3, 'asset_class_id': 2, 'location_id': 1, 'percentage': 10000},
                               {'id': 4, 'asset_id': 4, 'asset_class_id': 2, 'location_id': 2, 'percentage': 10000},
                               {'id': 5, 'asset_id': 5, 'asset_class_id': 3, 'location_id': 1, 'percentage': 10000}],
                  'constant': [{'id': 1, 'name': 'decimal', 'amount': 10000}],
                  'institution': [{'id': 1, 'name': 'Rearguard Investments'}],
                  'location': [{'id': 1, 'name': 'USA'},
                              {'id': 2, 'name': 'International'},
                              {'id': 3, 'name': 'World'}],
                  'owner': [{'id': 1, 'name': 'Bob', 'birthday': '1992-10-31'}],
                  'price': [{'id': 1, 'asset_id': 1, 'price_date': '2020-01-01', 'amount': 10000},
                           {'id': 2, 'asset_id': 2, 'price_date': '2020-01-01', 'amount': 10000},
                           {'id': 3, 'asset_id': 3, 'price_date': '2020-01-01', 'amount': 10000},
                           {'id': 4, 'asset_id': 4, 'price_date': '2020-01-01', 'amount': 10000},
                           {'id': 5, 'asset_id': 5, 'price_date': '1776-07-04', 'amount': 10000}]}


def test_csv_directory_to_dict():
    assert data_strings == finance_tool.csv_directory_to_dict(directory_path='./test_csv_data/')

def test_insert_from_csv_directory(test_ft_0):
    test_ft_0.insert_from_csv_directory(directory_path='./test_csv_data/')
    results_dict = {}

    for table_name in data_strings.keys():
        result = test_ft_0.fetch_all(cmd=f"SELECT * FROM {table_name}")
        results_dict.update({table_name: result})

    assert data_formatted == results_dict


def test_insert_from_json(test_ft_0):
    test_ft_0.insert_from_json(file_path='./data/test_db_1.json')
    results_dict = {}

    for table_name in data_strings.keys():
        result = test_ft_0.fetch_all(cmd=f"SELECT * FROM {table_name}")
        results_dict.update({table_name: result})

    assert data_formatted == results_dict

# Test CREATE
create_function_entry = {
    'account': {'id': 1, 'name': 'Work 401k', 'account_type_id': 1, 'institution_id': 1, 'owner_id': 1},
    'account_type': {'id': 1, 'name': '401k', 'tax_in': 0, 'tax_growth': 0, 'tax_out': 1},
    'allocation': {'id': 1, 'asset_class_id': 1, 'location_id': 1, 'percentage': .4000},
    'asset': {'id': 1, 'name': 'Rearguard Total Stock Market Index Fund', 'symbol': 'RSUSA'},
    'asset_class': {'id': 1, 'name': 'stocks'},
    'balance': {'id': 1, 'account_id': 1, 'asset_id': 1, 'balance_date': '2021-01-01', 'quantity': 34000},
    'component': {'id': 1, 'asset_id': 1, 'asset_class_id': 1, 'location_id': 1, 'percentage': 1.0000},
    'constant': {'id': 1, 'name': 'decimal', 'amount': 10000},
    'institution': {'id': 1, 'name': 'Rearguard Investments'},
    'location': {'id': 1, 'name': 'USA'},
    'owner': {'id': 1, 'name': 'Bob', 'birthday': '1992-10-31'},
    'price': {'id': 1, 'asset_id': 1, 'price_date': '2020-01-01', 'amount': 1}}

create_function_expected = {
    'account': {'id': 1, 'name': 'Work 401k', 'account_type_id': 1, 'institution_id': 1, 'owner_id': 1},
    'account_type': {'id': 1, 'name': '401k', 'tax_in': 0, 'tax_growth': 0, 'tax_out': 1},
    'allocation': {'id': 1, 'asset_class_id': 1, 'location_id': 1, 'percentage': 4000},
    'asset': {'id': 1, 'name': 'Rearguard Total Stock Market Index Fund', 'symbol': 'RSUSA'},
    'asset_class': {'id': 1, 'name': 'stocks'},
    'balance': {'id': 1, 'account_id': 1, 'asset_id': 1, 'balance_date': '2021-01-01', 'quantity': 340000000},
    'component': {'id': 1, 'asset_id': 1, 'asset_class_id': 1, 'location_id': 1, 'percentage': 10000},
    'constant': {'id': 1, 'name': 'decimal', 'amount': 10000},
    'institution': {'id': 1, 'name': 'Rearguard Investments'},
    'location': {'id': 1, 'name': 'USA'},
    'owner': {'id': 1, 'name': 'Bob', 'birthday': '1992-10-31'},
    'price': {'id': 1, 'asset_id': 1, 'price_date': '2020-01-01', 'amount': 10000}}


@pytest.mark.parametrize('table_name', table_names)
def test_create_function(test_ft_0, table_name):
    test_ft_0.create[table_name](**create_function_entry[table_name])
    assert test_ft_0.fetch_one(cmd=f"SELECT * FROM {table_name}") == create_function_expected[table_name]


insert_function_entry_no_id = {
    'account': {'id': None, 'name': 'Work 401k', 'account_type_id': 1, 'institution_id': 1, 'owner_id': 1},
    'account_type': {'id': None, 'name': '401k', 'tax_in': 0, 'tax_growth': 0, 'tax_out': 1},
    'allocation': {'id': None, 'asset_class_id': 1, 'location_id': 1, 'percentage': .4000},
    'asset': {'id': None, 'name': 'Rearguard Total Stock Market Index Fund', 'symbol': 'RSUSA'},
    'asset_class': {'id': None, 'name': 'stocks'},
    'balance': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': '2021-01-01', 'quantity': 34000},
    'component': {'id': None, 'asset_id': 1, 'asset_class_id': 1, 'location_id': 1, 'percentage': 1.0000},
    'constant': {'id': None, 'name': 'decimal', 'amount': 10000},
    'institution': {'id': None, 'name': 'Rearguard Investments'},
    'location': {'id': None, 'name': 'USA'},
    'owner': {'id': None, 'name': 'Bob', 'birthday': '1992-10-31'},
    'price': {'id': None, 'asset_id': 1, 'price_date': '2020-01-01', 'amount': 1}}


@pytest.mark.parametrize('table_name', table_names)
def test_create_function_no_id(test_ft_0, table_name):
    test_ft_0.create[table_name](**insert_function_entry_no_id[table_name])
    assert test_ft_0.fetch_one(cmd=f"SELECT * FROM {table_name}") == create_function_expected[table_name]

# Test READ
def test_read_net_worth(test_ft_1):
    assert test_ft_1.read_net_worth() == {'net_worth': 100000}


@pytest.mark.parametrize('contribution, expected', [(0, []),
                                                    (1000, [{'asset_class': 'stocks',
                                                             'location': 'International',
                                                             'contribution': 10000000}]),
                                                    (10000, [{'asset_class': 'stocks',
                                                              'location': 'USA',
                                                              'contribution': 41538461},
                                                             {'asset_class': 'stocks',
                                                              'location': 'International',
                                                              'contribution': 50769230},
                                                             {'asset_class': 'bonds',
                                                              'location': 'International',
                                                              'contribution': 7692307}]),
                                                    (100000, [{'asset_class': 'stocks',
                                                               'location': 'USA',
                                                               'contribution': 460000000},
                                                              {'asset_class': 'stocks',
                                                               'location': 'International',
                                                               'contribution': 260000000},
                                                              {'asset_class': 'bonds',
                                                               'location': 'USA',
                                                               'contribution': 160000000},
                                                              {'asset_class': 'bonds',
                                                               'location': 'International',
                                                               'contribution': 60000000},
                                                              {'asset_class': 'cash',
                                                               'location': 'USA',
                                                               'contribution': 60000000}])])
def test_read_where_to_contribute(test_ft_1, contribution, expected):
    assert test_ft_1.read_where_to_contribute(contribution) == expected

# Tests exceptions
# TODO: determine if this is overkill
expected_constraints = [
    {'table': 'account',
     'expected': {'id': None, 'name': None, 'account_type_id': 0, 'institution_id': 0, 'owner_id': 0}},
    {'table': 'account_type',
     'expected': {'id': None, 'name': 'test', 'tax_in': 1, 'tax_growth': 4, 'tax_out': 0}},
    {'table': 'account_type',
     'expected': {'id': None, 'name': None, 'tax_in': 1, 'tax_growth': 0, 'tax_out': 0}},
    {'table': 'allocation',
     'expected': {'id': None, 'asset_class_id': 1, 'location_id': 1, 'percentage': 3}},
    {'table': 'allocation',
     'expected': {'id': None, 'asset_class_id': 1, 'location_id': 1, 'percentage': 'test'}},
    {'table': 'allocation',
     'expected': {'id': None, 'asset_class_id': 1, 'location_id': 1, 'percentage': None}},
    {'table': 'asset',
     'expected': {'id': None, 'name': 'test', 'symbol': None}},
    {'table': 'asset',
     'expected': {'id': None, 'name': None, 'symbol': 'TEST'}},
    {'table': 'asset_class',
     'expected': {'id': None, 'name': None}},
    {'table': 'balance',
     'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': 6, 'quantity': 1}},
    {'table': 'balance',
     'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': 'test', 'quantity': 1}},
    {'table': 'balance',
     'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': 'April 16, 2023', 'quantity': 1}},
    {'table': 'balance',
     'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': '2024-15-43', 'quantity': 1}},
    {'table': 'balance',
     'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': None, 'quantity': 1}},
    {'table': 'balance',
     'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': '2022-01-01', 'quantity': None}},
    {'table': 'balance',
     'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': '2022-01-01', 'quantity': 'test'}},
    {'table': 'balance',
     'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': '2022-01-01', 'quantity': ''}},
    {'table': 'balance',
     'expected': {'id': None, 'account_id': 1, 'asset_id': 1, 'balance_date': '2022-01-01', 'quantity': -123}},
    {'table': 'component',
     'expected': {'id': None, 'asset_id': 1, 'asset_class_id': 1, 'location_id': 1, 'percentage': 1.01}},
    {'table': 'component',
     'expected': {'id': None, 'asset_id': 1, 'asset_class_id': 1, 'location_id': 1, 'percentage': -0.01}},
    {'table': 'institution',
     'expected': {'id': None, 'name': None}},
    {'table': 'location',
     'expected': {'id': None, 'name': None}},
    {'table': 'owner',
     'expected': {'id': None, 'name': None, 'birthday': '2021-01-01'}},
    {'table': 'owner',
     'expected': {'id': None, 'name': 'test', 'birthday': 'test'}},
    {'table': 'owner',
     'expected': {'id': None, 'name': 'test', 'birthday': ''}},
    {'table': 'owner',
     'expected': {'id': None, 'name': 'test', 'birthday': '2024-15-43'}},
    {'table': 'owner',
     'expected': {'id': None, 'name': 'test', 'birthday': 'April 16, 2023'}},
    {'table': 'owner',
     'expected': {'id': None, 'name': 'test', 'birthday': None}},
    {'table': 'owner',
     'expected': {'id': None, 'name': 'test', 'birthday': 6}},
    {'table': 'price',
     'expected': {'id': None, 'asset_id': 1, 'price_date': '2022-01-01', 'amount': ''}},
    {'table': 'price',
     'expected': {'id': None, 'asset_id': 1, 'price_date': '2022-01-01', 'amount': None}},
    {'table': 'price',
     'expected': {'id': None, 'asset_id': 1, 'price_date': '2022-01-01', 'amount': 'six'}},
    {'table': 'price',
     'expected': {'id': None, 'asset_id': 1, 'price_date': '2024-51-51', 'amount': 1}},
    {'table': 'price',
     'expected': {'id': None, 'asset_id': 1, 'price_date': 'test', 'amount': 1}},
    {'table': 'price',
     'expected': {'id': None, 'asset_id': 1, 'price_date': None, 'amount': 1}},
    {'table': 'price',
     'expected': {'id': None, 'asset_id': 1, 'price_date': 'April 16, 2023', 'amount': 1}},
    {'table': 'price',
     'expected': {'id': None, 'asset_id': 1, 'price_date': 6, 'amount': 1}},
    {'table': 'price',
     'expected': {'id': None, 'asset_id': 1, 'price_date': '', 'amount': 1}}]

formatted_expected_constraints = [(line['table'], line['expected']) for line in expected_constraints]


@pytest.mark.parametrize('table_name, params', formatted_expected_constraints)
def test_database_exception(test_ft_0, table_name, params):
    with pytest.raises(finance_tool.DatabaseException):
        test_ft_0.create[table_name](**params)
