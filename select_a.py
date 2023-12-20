# select_a.py
# Functions for user selection
# 2023-12-18
# @juicemcpeso

def by_name(option_list):
    for option in option_list:
        print(f"{option['id']:>3} | {option['name']}")
    return number(range(len(option_list) + 1))


def number(option_list):
    selection = None
    while not selection:
        try:
            selection = int(input('Select option number: '))
        except ValueError:
            pass

        if selection in range(len(option_list)):
            return selection
        else:
            selection = None
