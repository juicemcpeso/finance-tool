# test_text_ui.py
# Tests for text_ui.py
# 2024-01-23
# @juicemcpeso

import os
import shutil
import text_ui
import pytest


def add_test_csvs():
    shutil.copytree('./test_csv_data/', '../csv_files', dirs_exist_ok=True)


def remove_test_csvs():
    shutil.rmtree('../csv_files')
    os.makedirs('../csv_files')


@pytest.fixture
def test_ui_1(test_ft_1):
    return text_ui.TextUI(test_ft_1)


@pytest.fixture
def test_ui_csv(test_ft_0):
    add_test_csvs()
    ui = text_ui.TextUI(test_ft_0)
    ui.insert_from_csv()
    remove_test_csvs()

    return ui


def test_close():
    with pytest.raises(SystemExit) as expected:
        text_ui.close()

    assert expected.type == SystemExit


def test_input_string_bool():
    assert text_ui.input_string_bool('tax_in') == "Input tax in (t = true, f = false): "


def test_input_string_date():
    assert text_ui.input_string_date('balance_date') == "Input balance date in YYYY-MM-DD format: "


def test_input_string_text():
    assert text_ui.input_string_text('owner_name') == "Input owner name: "


markdown_mock = [{'a': 'a1', 'b': 'b1', 'c': 'c1'},
                 {'a': 'a2', 'b': 'b2', 'c': 'c2'},
                 {'a': 'a3', 'b': 'b3', 'c': 'c3'}]


def test_markdown_header():
    column_names = ['a', 'b', 'c']
    assert text_ui.markdown_header(column_names) == "|a|b|c|\n"


def test_markdown_hyphen_line():
    assert text_ui.markdown_hyphen_line(3) == "|---|---|---|\n"


def test_markdown_row():
    assert text_ui.markdown_row(markdown_mock[0]) == '|a1|b1|c1|'


def test_markdown_rows():
    assert text_ui.markdown_rows(markdown_mock) == '|a1|b1|c1|\n' \
                                                   '|a2|b2|c2|\n' \
                                                   '|a3|b3|c3|'


def test_markdown_table():
    assert text_ui.markdown_table(markdown_mock) == "|a|b|c|\n" \
                                                    "|---|---|---|\n" \
                                                    "|a1|b1|c1|\n" \
                                                    "|a2|b2|c2|\n" \
                                                    "|a3|b3|c3|"


@pytest.mark.parametrize('ui_fixture', ['test_ui_1', 'test_ui_csv'])
def test_print_allocation_dashboard(capsys, request, ui_fixture):
    ui = request.getfixturevalue(ui_fixture)
    expected = \
        "## Allocation dashboard\n" \
        "|Asset class|Location|Current %|Current value|Plan %|Plan value|\n" \
        "|---|---|---|---|---|---|\n" \
        "|stocks|USA|34%|$34,000.00|40%|$40,000.00|\n" \
        "|stocks|International|14%|$14,000.00|20%|$20,000.00|\n" \
        "|cash|USA|14%|$14,000.00|10%|$10,000.00|\n" \
        "|bonds|USA|34%|$34,000.00|25%|$25,000.00|\n" \
        "|bonds|International|4%|$4,000.00|5%|$5,000.00|\n"

    ui.print_allocation_dashboard()

    assert capsys.readouterr().out == expected


@pytest.mark.parametrize('ui_fixture', ['test_ui_1', 'test_ui_csv'])
def test_print_net_worth(capsys, request, ui_fixture):
    ui = request.getfixturevalue(ui_fixture)
    expected = \
        "## Net worth\n" \
        "$100,000.00\n"
    ui.print_net_worth()
    assert capsys.readouterr().out == expected


@pytest.mark.parametrize('ui_fixture', ['test_ui_1', 'test_ui_csv'])
def test_print_where_to_contribute_1000(capsys, request, ui_fixture):
    ui = request.getfixturevalue(ui_fixture)
    expected = "" \
        "|asset_class|location|contribution|\n" \
        "|---|---|---|\n" \
        "|stocks|International|$1,000.00|\n" \

    ui.print_where_to_contribute(1000)
    assert capsys.readouterr().out == expected


@pytest.mark.parametrize('ui_fixture', ['test_ui_1', 'test_ui_csv'])
def test_print_where_to_contribute_10000(capsys, request, ui_fixture):
    ui = request.getfixturevalue(ui_fixture)
    expected = "" \
               "|asset_class|location|contribution|\n" \
               "|---|---|---|\n" \
               "|stocks|USA|$4,153.85|\n" \
               "|stocks|International|$5,076.92|\n" \
               "|bonds|International|$769.23|\n"

    ui.print_where_to_contribute(10000)
    assert capsys.readouterr().out == expected


@pytest.mark.parametrize('ui_fixture', ['test_ui_1', 'test_ui_csv'])
def test_print_where_to_contribute_100000(capsys, request, ui_fixture):
    ui = request.getfixturevalue(ui_fixture)
    expected = "" \
        "|asset_class|location|contribution|\n" \
        "|---|---|---|\n" \
        "|stocks|USA|$46,000.00|\n" \
        "|stocks|International|$26,000.00|\n" \
        "|bonds|USA|$16,000.00|\n" \
        "|bonds|International|$6,000.00|\n" \
        "|cash|USA|$6,000.00|\n"

    ui.print_where_to_contribute(100000)
    assert capsys.readouterr().out == expected


@pytest.mark.parametrize('ui_fixture', ['test_ui_1', 'test_ui_csv'])
def test_main_dashboard(capsys, request, ui_fixture):
    ui = request.getfixturevalue(ui_fixture)
    expected = \
        "## Net worth\n" \
        "$100,000.00\n" \
        "## Allocation dashboard\n" \
        "|Asset class|Location|Current %|Current value|Plan %|Plan value|\n" \
        "|---|---|---|---|---|---|\n" \
        "|stocks|USA|34%|$34,000.00|40%|$40,000.00|\n" \
        "|stocks|International|14%|$14,000.00|20%|$20,000.00|\n" \
        "|cash|USA|14%|$14,000.00|10%|$10,000.00|\n" \
        "|bonds|USA|34%|$34,000.00|25%|$25,000.00|\n" \
        "|bonds|International|4%|$4,000.00|5%|$5,000.00|\n"

    ui.main_dashboard()

    assert capsys.readouterr().out == expected


def test_format_currency():
    assert text_ui.format_currency(1000.567) == '$1,000.57'


def test_add_test_csvs():
    file_set = set(file for file in os.listdir('./test_csv_data/'))
    add_test_csvs()
    assert set(file for file in os.listdir('../csv_files/')) == file_set


def test_remove_test_csvs():
    add_test_csvs()
    remove_test_csvs()
    assert os.listdir('../csv_files') == []
