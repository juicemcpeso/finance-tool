# actions.py
# Code for creating options
# 2023-12-19
# @juicemcpeso


class Action:
    def __init__(self, name):
        self.name = name

    def __call__(self):
        pass

    def __repr__(self):
        return f"Action({self.name})"

    def __str__(self):
        return self.name


class Selection(Action):
    def __init__(self, name, option_list):
        super().__init__(name)
        self._options = option_list
        self.selected_option = None

    def __repr__(self):
        return f"Selection({self.name})"

