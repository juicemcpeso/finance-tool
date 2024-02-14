# test_text_ui.py
# Tests for text_ui.py
# 2024-01-23
# @juicemcpeso

import subprocess
import text_ui
import pytest

bool_date = [{'input': 'T', 'format': True, 'verify': True, 'response': True},
             {'input': 't', 'format': True, 'verify': True, 'response': True},
             {'input': 'F', 'format': False, 'verify': True, 'response': False},
             {'input': 'f', 'format': False, 'verify': True, 'response': False},
             {'input': 'a', 'format': 'a', 'verify': False, 'response': None},
             {'input': 'G', 'format': 'G', 'verify': False, 'response': None},
             {'input': '0', 'format': '0', 'verify': False, 'response': None},
             {'input': 'test', 'format': 'test', 'verify': False, 'response': None},
             {'input': '$', 'format': '$', 'verify': False, 'response': None},
             {'input': '', 'format': '', 'verify': False, 'response': None}]

date_data = [{'input': '2021-01-23', 'verify': True, 'response': '2021-01-23'},
             {'input': 'test', 'verify': False, 'response': None},
             {'input': '12-23-2023', 'verify': False, 'response': None},
             {'input': '2023-02-29', 'verify': False, 'response': None},
             {'input': '', 'verify': False, 'response': None}]

data = {'bool': bool_date,
        'date': date_data}

input_params = [(input_type, td['input'], td['response']) for input_type in data for td in data[input_type]]

format_params = []
for input_type in data:
    for td in data[input_type]:
        try:
            format_params.append((input_type, td['input'], td['format']))
        except KeyError:
            pass

verify_params = []
for input_type in data:
    for td in data[input_type]:
        try:
            verify_params.append((input_type, td['format'], td['verify']))
        except KeyError:
            verify_params.append((input_type, td['input'], td['verify']))


@pytest.mark.xfail(reason="UI is not yet updated to new format")
def test_close(test_ui_empty):
    with pytest.raises(SystemExit) as expected:
        test_ui_empty.close()

    assert expected.type == SystemExit


# @pytest.mark.parametrize('input_type', data.keys())
# def test_input(monkeypatch, input_type):
#     monkeypatch.setattr('builtins.input', lambda _: 'input')
#     assert text_ui.input_lookup[input_type]['input']('test label') == 'input'
#
#
# # TODO - rewrite this test to make sure it is printing the correct output
# # I don't really know if I need to test this since it is just using input and an f string
# @pytest.mark.skip("Test doesn't work and I don't know how to make it work")
# @pytest.mark.parametrize('input_type', data.keys())
# def test_input_print(monkeypatch, capsys, input_type):
#     # monkeypatch.setattr('builtins.input', lambda _: 'input')
#     text_ui.input_lookup[input_type]['input']('test label')
#     captured = capsys.readouterr().out
#     assert captured == "Input test label (t = true, f = false): "


def test_main_menu(capsys):
    expected = "\nMain menu\n" \
               " 0 | Quit\n" \
               " 1 | Net worth\n" \
               " 2 | Where to contribute\n"
    text_ui.print_menu(text_ui.main_menu)
    assert capsys.readouterr().out == expected
