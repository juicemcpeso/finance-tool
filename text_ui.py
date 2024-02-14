# text_ui.py
# Text based user interface
# 2024-01-22
# @juicemcpeso

import finance_tool
import sys


class TextUI:
    def __init__(self, _finance_tool=None):
        self.ft = _finance_tool

        self.menu_main_options = []

    def __repr__(self):
        return f"TextUI({self.ft})"

    def __call__(self):
        self.menu_main()

    # Menus
    # TODO - test
    def menu_main(self):
        menu_dict = {'label': 'Main menu',
                     'options': [{'label': 'Quit', 'function': self.close}]}
        menu(menu_dict)

    def close(self):
        print('bye')
        sys.exit()


# TODO - test
def menu(menu_dict):
    print_menu(menu_dict)
    while True:
        selected_option = user_selection(menu_dict['options'])

        if selected_option is not None:
            selected_option['function']()


# TODO - test
def print_menu(menu_dict):
    print('\n' + menu_dict['label'])
    for i, option in enumerate(menu_dict['options']):
        print(f"{i:>2} | {option['label']}")


# User - input
# TODO - test
def user_input_loop(input_type):
    response = None
    while response is None:
        response = input_dict['function'](input_dict['label'])

    return response


def user_input(input_type, label):
    input_dict = input_lookup[input_type]

    if 'format' in input_dict.keys():
        response = input_dict['format'](input_dict['input'](label))
    else:
        response = input_dict['input'](label)

    return response


def input_bool(label):
    return input(f"Input {label} (t = true, f = false): ")


def input_date(label):
    return input(f"Input {label} in YYYY-MM-DD format: ")


# TODO - test
def input_text(label):
    return input(f"Input {label}: ")


# User - selection
# TODO - test
def user_selection(option_list):
    while True:
        try:
            option_number = int(input('Select option number: '))
        except ValueError:
            pass
        else:
            if option_number in range(len(option_list)):
                return option_list[option_number]


input_lookup = {'bool': {'input': input_bool},
                'date': {'input': input_date}}

#
# class MenuOption:
#     def __init__(self, label, function):
#         self.label = label
#         self.function = function
#
#     def __call__(self):
#         self.function()


def close():
    print('bye')
    sys.exit()


main_menu = {'label': 'Main menu',
             'options': [{'label': 'Quit', 'function': close},
                         {'label': 'Net worth', 'function': None},
                         {'label': 'Where to contribute', 'function': None}]}
