# text_ui.py
# Text based user interface
# 2024-01-22
# @juicemcpeso

import datetime
import os


class TextUI:
    def __init__(self, _app=None):
        self.app = _app

        self.menu_main_options = []

    def __repr__(self):
        return f"TextUI({self.app})"

    def __str__(self):
        return f"{self.app.name} TextUI"

    def __call__(self):
        self.menu_main()

    # Menus
    def menu_main(self):
        menu_dict = {'label': 'Main menu',
                     'options': [{'label': 'Quit', 'function': self.quit}]}
        menu(menu_dict)

    def quit(self):
        self.app.active = False
        print('bye')
        exit()


def menu(menu_dict):
    print_menu(menu_dict)
    while True:
        selected_option = user_selection(menu_dict['options'])

        if selected_option is not None:
            selected_option['function']()


def print_menu(menu_dict):
    print('\n' + menu_dict['label'])
    for i, option in enumerate(menu_dict['options']):
        print(f"{i} | {option['label']}")


# User - input
def user_input(input_dict):
    response = None
    while response is None:
        response = input_dict['function'](input_dict['label'])

    return response


def user_input_bool(label):
    response = input(f"Input {label} (t = true, f = false): ").lower()
    if response in {'t', 'f'}:
        return True if response == 't' else False


def user_input_date(label):
    response = input(f"Input {label} in YYYY-MM-DD format: ")
    try:
        datetime.date.fromisoformat(response)
    except ValueError:
        print(f"{label} must be in YYYY-MM-DD format")
    else:
        return response


def user_input_number(label):
    pass


def user_input_text(label):
    return input(f"Input {label}: ")


# User - selection
def user_selection(option_list):
    while True:
        try:
            option_number = int(input('Select option number: '))
        except ValueError:
            pass
        else:
            if option_number in range(len(option_list)):
                return option_list[option_number]
