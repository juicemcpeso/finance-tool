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


def test_display_main_menu(capsys, test_ui_1):
    expected = "Main menu\n" \
               " 0 | Quit\n" \
               " 1 | Net worth\n" \
               " 2 | Where to contribute\n"
    test_ui_1.menus['main']()
    assert capsys.readouterr().out == expected


def test_net_worth_string():
    assert text_ui.net_worth_string({'net_worth': 1000.00}) == "Net worth: $1000.00"


def test_input_string_bool():
    assert text_ui.input_string_bool('tax_in') == "Input tax in (t = true, f = false): "


def test_input_string_date():
    assert text_ui.input_string_date('balance_date') == "Input balance date in YYYY-MM-DD format: "


def test_input_string_text():
    assert text_ui.input_string_text('owner_name') == "Input owner name: "
