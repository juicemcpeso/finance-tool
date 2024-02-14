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
