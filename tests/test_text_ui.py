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


@pytest.mark.parametrize('input_type, response, expected', input_params)
def test_user_input(monkeypatch, input_type, response, expected):
    monkeypatch.setattr('builtins.input', lambda _: response)
    assert text_ui.user_input(input_type, 'test label') == expected


@pytest.mark.parametrize('input_type, response, expected', format_params)
def test_format(input_type, response, expected):
    assert text_ui.input_lookup[input_type]['format'](response) == expected


@pytest.mark.parametrize('input_type', data.keys())
def test_input(monkeypatch, input_type):
    monkeypatch.setattr('builtins.input', lambda _: 'input')
    assert text_ui.input_lookup[input_type]['input']('test label') == 'input'


# TODO - rewrite this test to make sure it is printing the correct output
# I don't really know if I need to test this since it is just using input and an f string
@pytest.mark.skip("Test doesn't work and I don't know how to make it work")
@pytest.mark.parametrize('input_type', data.keys())
def test_input_print(monkeypatch, capsys, input_type):
    # monkeypatch.setattr('builtins.input', lambda _: 'input')
    text_ui.input_lookup[input_type]['input']('test label')
    captured = capsys.readouterr().out
    assert captured == "Input test label (t = true, f = false): "


@pytest.mark.parametrize('input_type, response, expected', verify_params)
def test_verify(input_type, response, expected):
    assert text_ui.input_lookup[input_type]['verify'](response) == expected
