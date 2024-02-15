# text_ui.py
# Text based user interface
# 2024-01-22
# @juicemcpeso

import finance_tool
import sys


class TextUI:
    def __init__(self, _finance_tool=None):
        self.ft = _finance_tool

    def print_allocation_dashboard(self):
        print(markdown_table(self.ft.read_allocation_dashboard()))

    def print_net_worth(self):
        print(net_worth_string(self.ft.read_net_worth()))


def close():
    sys.exit()


def net_worth_string(net_worth_dict):
    return f"Net worth: ${net_worth_dict['net_worth']:.2f}"


def input_string_bool(column_name):
    return f"Input {column_name.replace('_', ' ')} (t = true, f = false): "


def input_string_date(column_name):
    return f"Input {column_name.replace('_', ' ')} in YYYY-MM-DD format: "


def input_string_text(column_name):
    return f"Input {column_name.replace('_', ' ')}: "


def markdown_header(column_names):
    return f"|{'|'.join(column_names)}|\n"


def markdown_hyphen_line(number_of_columns):
    return ''.join('|---' for _ in range(number_of_columns)) + '|\n'


def markdown_row(row):
    return f"|{'|'.join(str(cell) for cell in row.values())}|"


def markdown_rows(list_of_rows):
    return '\n'. join(markdown_row(row) for row in list_of_rows)


def markdown_table(list_of_dictionaries):
    header = markdown_header(list_of_dictionaries[0].keys())
    hyphen_line = markdown_hyphen_line(len(list_of_dictionaries[0]))
    rows = markdown_rows(list_of_dictionaries)
    return header + hyphen_line + rows

