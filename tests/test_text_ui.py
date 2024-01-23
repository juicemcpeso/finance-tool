# test_text_ui.py
# Tests for text_ui.py
# 2024-01-23
# @juicemcpeso

import text_ui
import pytest


def test_close(test_ui_empty):
    with pytest.raises(SystemExit) as expected:
        test_ui_empty.close()

    assert expected.type == SystemExit


@pytest.mark.parametrize('response, expected', [('T', True),
                                                ('t', True),
                                                ('F', False),
                                                ('f', False),
                                                ('a', None),
                                                ('G', None),
                                                ('0', None),
                                                ('test', None),
                                                ('$', None)])
def test_verify_input_bool(response, expected):
    assert text_ui.verify_bool(response) == expected


@pytest.mark.parametrize('response, expected', [('2021-01-23', '2021-01-23'),
                                                ('test', None),
                                                ('12-23-2023', None),
                                                ('2023-02-29', None)])
def test_verify_date_true(response, expected):
    assert text_ui.verify_date(response) == expected
