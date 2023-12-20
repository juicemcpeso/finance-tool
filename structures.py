# structures.py
# Basic control structures
# 2023-12-19
# @juicemcpeso

import collections


class Action:
    def __init__(self, name):
        self.name = name

    def __call__(self):
        pass

    def __repr__(self):
        return f"Action({self.name}, {self.app})"

    def __str__(self):
        return self.name


class Selection(collections.abc.MutableSequence):
    _options = []

    def __init__(self, name, option_list=[]):
        self.name = name
        self._options = option_list
        self.selected_option = None

    def __call__(self):
        self.create_options()
        self.select_option()

        if self.selected_option is not None:
            self.selected_option()

    def __delitem__(self, key):
        del self._options[key]

    def __getitem__(self, key):
        return self._options[key]

    def __setitem__(self, key, value):
        self._options[key] = value

    def __contains__(self, item):
        return item in self._options

    def __len__(self):
        return len(self._options)

    def __iter__(self):
        return iter(self._options)

    def __repr__(self):
        return f"Selection({self.name}, {self._options})"

    def __str__(self):
        return self.name

    def insert(self, position, item):
        self._options.insert(position, item)

    def create_options(self):
        pass

    def select_option(self):
        pass
