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
    def menu(self, menu_dict):
        self.menu_print_options(menu_dict)
        selected_option = select_option(menu_dict['options'])

        if selected_option is not None:
            selected_option['function']()

    def menu_no_execute(self, menu_dict):
        self.menu_print_options(menu_dict)
        return select_option(menu_dict['options'])

    def menu_print_options(self, menu_dict):
        print('\n' + menu_dict['name'])
        for i, option in enumerate(menu_dict['options']):
            print(f"{i} | {option['name']}")

    def menu_main(self):
        options = [{'name': 'Quit', 'function': self.quit}]
        self.menu({'name': 'Main menu', 'options': options})

    # TODO - file selection module
    # def menu_select_portfolio(self):
    #     options = [{'name': 'Load', 'function': self.menu_load_file},
    #                {'name': 'Quit', 'function': self.quit}]
    #     self.menu({'name': 'Select portfolio', 'options': options})
    #
    # # File
    # def menu_load_file(self):
    #     options = []
    #     for file_name in os.listdir(self.app.portfolio_directory):
    #         options.append({'name': file_name})
    #     selected_option = self.menu_no_execute({'name': 'Load file', 'options': options})
    #     self.app.load_file(selected_option['name'])


    # User - input
    def user_input(self, input_function):
        response = None
        while response is None:
            response = input_function

        return response

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

    # User - selection

    def quit(self):
        self.app.active = False
        print('bye')
        exit()


def select_option(option_list):
    while True:
        try:
            option_number = int(input('Select option number: '))
        except ValueError:
            pass
        else:
            if option_number in range(len(option_list)):
                return option_list[option_number]
