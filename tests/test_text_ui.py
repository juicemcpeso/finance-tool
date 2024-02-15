# test_text_ui.py
# Tests for text_ui.py
# 2024-01-23
# @juicemcpeso

import text_ui
import pytest


@pytest.fixture
def test_ui_1(test_ft_1):
    return text_ui.TextUI(test_ft_1)


def test_close():
    with pytest.raises(SystemExit) as expected:
        text_ui.close()

    assert expected.type == SystemExit


def test_net_worth_string():
    assert text_ui.net_worth_string({'net_worth': 1000.00}) == "Net worth: $1000.00"


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


def test_print_allocation_dashboard(capsys, test_ui_1):
    expected = "|asset_class|location|current_percent|current_value|plan_percent|plan_value|\n" \
        "|---|---|---|---|---|---|\n" \
        "|stocks|USA|0.34|34000|0.4|40000|\n" \
        "|stocks|International|0.14|14000|0.2|20000|\n" \
        "|cash|USA|0.14|14000|0.1|10000|\n" \
        "|bonds|USA|0.34|34000|0.25|25000|\n" \
        "|bonds|International|0.04|4000|0.05|5000|\n"

    test_ui_1.print_allocation_dashboard()

    assert capsys.readouterr().out == expected
