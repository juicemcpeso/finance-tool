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
        while True:
            self.menu_main()

    # Menus
    def menu_main(self):
        options = [{'name': 'Quit', 'function': self.quit}]
        menu({'name': 'Main menu', 'options': options})

    def input_bool(self):
        user_input = input(f"{self.display_text} (T = True, F = False): ").lower()
        if user_input in {'t', 'f'}:
            return True if user_input == 't' else False

    def input_date(self):
        user_input = input(f"{self.display_text} in YYYY-MM-DD format: ")
        try:
            datetime.date.fromisoformat(user_input)
        except ValueError:
            print("Date must be in YYYY-MM-DD format")
        else:
            response = user_input

    def input_number(self):
        pass

    def input_text(self):
        response = input(f"{self.display_text}: ")

    def quit(self):
        self.app.active = False
        print('bye')
        exit()


def menu(menu_dict):
    print_menu(menu_dict)
    selected_option = user_selection(menu_dict['options'])

    if selected_option is not None:
        selected_option['function']()


def print_menu(menu_dict):
    print('\n' + menu_dict['name'])
    for i, option in enumerate(menu_dict['options']):
        print(f"{i} | {option['name']}")


# User - input
def user_input(input_function):
    response = None
    while response is None:
        response = input_function

    return response


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
