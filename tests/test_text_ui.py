# test_text_ui.py
# Tests for text_ui.py
# 2024-01-23
# @juicemcpeso

import subprocess
import text_ui
import pytest

test_verify_bool_results = [(True, True),
                            (False, True),
                            ('a', False),
                            ('G', False),
                            ('0', False),
                            ('test', False),
                            ('$', False),
                            ('', False)]

test_user_input_bool_results = [('T', True),
                                ('t', True),
                                ('F', False),
                                ('f', False),
                                ('a', None),
                                ('G', None),
                                ('0', None),
                                ('test', None),
                                ('$', None),
                                ('', None)]

test_format_bool_results = [('T', True),
                            ('t', True),
                            ('F', False),
                            ('f', False),
                            ('a', 'a'),
                            ('G', 'G'),
                            ('0', '0'),
                            ('test', 'test'),
                            ('$', '$'),
                            ('', '')]


def test_close(test_ui_empty):
    with pytest.raises(SystemExit) as expected:
        test_ui_empty.close()

    assert expected.type == SystemExit


@pytest.mark.parametrize('response, expected', test_user_input_bool_results)
def test_user_input_bool(monkeypatch, response, expected):
    monkeypatch.setattr('builtins.input', lambda _: response)
    assert text_ui.user_input('bool', 'test label') == expected


def test_input_bool(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'input')
    assert text_ui.input_bool('test label') == 'input'


# TODO - rewrite this test to make sure it is printing the correct output
# I don't really know if I need to test this since it is just using input and an f string
@pytest.mark.xfail
def test_input_bool_print(monkeypatch, capsys):
    # print('test')
    # monkeypatch.setattr('builtins.input', lambda _: 'input')
    text_ui.input_bool('test label')
    captured = capsys.readouterr().out
    assert captured == "Input test label (t = true, f = false): "


@pytest.mark.parametrize('response, expected', test_format_bool_results)
def test_format_bool(response, expected):
    assert text_ui.format_bool(response) == expected


@pytest.mark.parametrize('response, expected', test_verify_bool_results)
def test_verify_bool(response, expected):
    assert text_ui.verify_bool(response) == expected


@pytest.mark.parametrize('response, expected', [('2021-01-23', '2021-01-23'),
                                                ('test', None),
                                                ('12-23-2023', None),
                                                ('2023-02-29', None),
                                                ('', None)])
def test_verify_date_true(response, expected):
    assert text_ui.verify_date(response) == expected
