# app.py
# Code for interacting with the database
# 2023-12-18
# @juicemcpeso

import csv
import menu


class App:
    def __init__(self, portfolio=None):
        self.active = True
        self.decimal = 10000
        self.portfolio = portfolio
        self.portfolio_directory = './portfolios/'

        self._add_to_table = {'account': self.portfolio.add_account,
                              'account_type': self.portfolio.add_account_type,
                              'allocation': self.portfolio.add_allocation,
                              'asset': self.portfolio.add_asset,
                              'asset_class': self.portfolio.add_asset_class,
                              'balance': self.portfolio.add_balance,
                              'component': self.portfolio.add_component,
                              'institution': self.portfolio.add_institution,
                              'location': self.portfolio.add_location,
                              'owner': self.portfolio.add_owner,
                              'price': self.portfolio.add_price}
        # self._menus = {'add': None,
        #                'database menu': None,
        #                'load': None,
        #                'main': None}

    def __call__(self):
        while True:
            menu.Database(self)()

            if self.portfolio is not None:
                menu.Main(self)()

    # Add
    def add_row_to_table(self, table_name, kwargs):
        self._add_to_table[table_name](kwargs=kwargs)

    # CSV loader
    def add_from_csv(self, file_name, table_name):
        for line in csv.DictReader(open(file_name)):
            self.add_row_to_table(table_name, kwargs=line)
            # self.add_to_table[table_name](kwargs=line)

    # Tools
    def where_to_contribute(self, contribution_amount):
        deviation_table = self.portfolio.allocation_deviation(contribution_amount)
        asset_deviation_level_cost = self.create_asset_deviation_level_cost_dict(deviation_table)
        total_deviation_level_cost = {key: 0 for key in range(len(deviation_table))}
        accessible_level = 0

        for line_number in asset_deviation_level_cost:
            for key in asset_deviation_level_cost[line_number]:
                total_deviation_level_cost[key] += asset_deviation_level_cost[line_number][key]

        for key in total_deviation_level_cost:
            if total_deviation_level_cost[key] < contribution_amount:
                accessible_level = key

        contribution_table = deviation_table[:(accessible_level + 1)]

        for line_number in range(accessible_level):
            contribution_table[line_number]['contribution'] += asset_deviation_level_cost[line_number][accessible_level]

        amount_remaining = contribution_amount - total_deviation_level_cost[accessible_level]

        total_percentage = 0
        for line_number in range(accessible_level + 1):
            total_percentage += contribution_table[line_number]['plan_percent']

        for line_number in range(accessible_level + 1):
            contribution_table[line_number]['contribution'] += amount_remaining * contribution_table[line_number][
                'plan_percent'] // total_percentage

        assign_leftovers(contribution_table, contribution_amount)

        return contribution_table

    def money_to_get_to_target_deviation(self, deviation_dict, target):
        return ((target + self.decimal) * deviation_dict['plan_value'] / self.decimal) - deviation_dict['current_value']

    def create_asset_deviation_level_cost_dict(self, deviation_table):
        asset_deviation_level_cost = {0: 0}

        for line_number, line in enumerate(deviation_table):
            asset_deviation_level_cost.update({line_number: {}})

            for next_number in range(line_number + 1, len(deviation_table)):
                dev_next_level = deviation_table[next_number]['deviation']
                asset_deviation_level_cost[line_number].update(
                    {next_number: self.money_to_get_to_target_deviation(line, dev_next_level)})

        return asset_deviation_level_cost


def assign_leftovers(contribution_table, contribution_amount):
    amount_contributed = 0
    for line in contribution_table:
        amount_contributed += line['contribution']

    leftover = contribution_amount - amount_contributed

    while leftover > 0:
        for line in contribution_table:
            line['contribution'] += 1
            leftover -= 1
            if leftover == 0:
                break
