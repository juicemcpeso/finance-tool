# select.py
# Functions for user selection
# 2023-12-18
# @juicemcpeso

def by_name(option_list):
    for option in option_list:
        print(f"{option['id']:>3} | {option['name']}")
    return verified_input(range(len(option_list) + 1))


def verified_input(acceptable_options):
    selection = None
    while not selection:
        try:
            selection = int(input('Select option number: '))
        except ValueError:
            pass

        if selection in acceptable_options:
            return selection
