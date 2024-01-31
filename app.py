# app.py
# Code for interacting with the database
# 2023-12-18
# @juicemcpeso

import db


class App:
    def __init__(self, database=None):
        self.decimal = 10000
        self.db = database

    # Tools
    def where_to_contribute(self, contribution_amount):
        new_net_worth = db.fetch_one(database=self.db, cmd=db.net_worth)['net_worth'] + contribution_amount
        deviation_table = db.fetch_all(database=self.db,
                                       cmd=db.allocation_deviation,
                                       params={'net_worth': new_net_worth})
        asset_deviation_level_cost = self.create_asset_deviation_level_cost_dict(deviation_table)
        total_deviation_level_cost = {key: 0 for key in range(len(deviation_table))}
        accessible_level = 0

        for line_number in asset_deviation_level_cost:
            for key in asset_deviation_level_cost[line_number]:
                total_deviation_level_cost[key] += asset_deviation_level_cost[line_number][key]

        for key in total_deviation_level_cost:
            if total_deviation_level_cost[key] < contribution_amount:
                accessible_level = key

        for line_number in range(accessible_level):
            deviation_table[line_number]['contribution'] += asset_deviation_level_cost[line_number][accessible_level]

        amount_remaining = contribution_amount - total_deviation_level_cost[accessible_level]

        total_percentage = 0
        for line_number in range(accessible_level + 1):
            total_percentage += deviation_table[line_number]['plan_percent']

        for line_number in range(accessible_level + 1):
            deviation_table[line_number]['contribution'] += amount_remaining * deviation_table[line_number][
                'plan_percent'] // total_percentage

        assign_leftovers(deviation_table, contribution_amount)

        return deviation_table

    # TODO - test if where to contribute is not refactored
    def money_to_get_to_target_deviation(self, deviation_dict, target):
        return ((target + self.decimal) * deviation_dict['plan_value'] / self.decimal) - deviation_dict['current_value']

    # TODO - test if where to contribute is not refactored
    def create_asset_deviation_level_cost_dict(self, deviation_table):
        asset_deviation_level_cost = {0: 0}

        for line_number, line in enumerate(deviation_table):
            asset_deviation_level_cost.update({line_number: {}})

            for next_number in range(line_number + 1, len(deviation_table)):
                dev_next_level = deviation_table[next_number]['deviation']
                asset_deviation_level_cost[line_number].update(
                    {next_number: self.money_to_get_to_target_deviation(line, dev_next_level)})

        return asset_deviation_level_cost


# TODO - test if where to contribute is not refactored
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
