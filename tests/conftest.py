# import finance_tool
# import pytest
# import json
#
# insert_dict = {'account': finance_tool.insert_account,
#                'account_type': finance_tool.insert_account_type,
#                'allocation': finance_tool.insert_allocation,
#                'asset': finance_tool.insert_asset,
#                'asset_class': finance_tool.insert_asset_class,
#                'balance': finance_tool.insert_balance,
#                'component': finance_tool.insert_component,
#                'constant': finance_tool.insert_constant,
#                'institution': finance_tool.insert_institution,
#                'location': finance_tool.insert_location,
#                'owner': finance_tool.insert_owner,
#                'price': finance_tool.insert_price}
#

# def json_loader(file_name):
#     with open(file_name, "r") as read_file:
#         return json.load(read_file)

#
# @pytest.fixture
# def test_db_0(tmp_path):
#     db_test = tmp_path / "test.db"
#     finance_tool.execute_file(db_test, '../db.sql')
#     return db_test


# # Use for simplified allocation data
# @pytest.fixture
# def test_db_1(tmp_path):
#     db_test = tmp_path / "test_1.db"
#     finance_tool.execute_file(db_test, '../db.sql')
#     data = json_loader('../tests/data/test_db_1.json')
#     for table_name in data:
#         finance_tool.execute_many(database=db_test, cmd=insert_dict[table_name], data_sequence=data[table_name])
#
#     return db_test
#
#
# # Use for general testing (has multiple of each item)
# @pytest.fixture
# def test_db_2(tmp_path):
#     db_test = tmp_path / "test_2.db"
#     finance_tool.execute_file(db_test, '../db.sql')
#     data = json_loader('../tests/data/test_db_2.json')
#     for table_name in data:
#         finance_tool.execute_many(database=db_test, cmd=insert_dict[table_name], data_sequence=data[table_name])
#
#     return db_test
#
#
# @pytest.fixture
# def test_ft_0(tmp_path):
#     return finance_tool.FinanceTool(tmp_path / "test_0.db")

