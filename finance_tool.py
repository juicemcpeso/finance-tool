# finance_tool.py
# SQL statements for the portfolio logic
# 2024-01-25
# @juicemcpeso

import csv
import json
import os
import sql
import sqlite3


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


# CSV
def csv_loader(file_path):
    with open(file_path) as csv_file:
        return list(csv.DictReader(csv_file))


def csv_directory_to_dict(directory_path):
    csv_dict = {}
    for file_name in os.listdir(directory_path):
        file_path = directory_path + file_name
        table_name = os.path.splitext(file_name)[0]
        csv_dict.update({table_name: csv_loader(file_path)})
    return csv_dict


# JSON
def json_loader(file_path):
    with open(file_path, "r") as read_file:
        return json.load(read_file)


class FinanceTool:
    def __init__(self, db_path=None):
        self.db = db_path
        self.execute_file('../db.sql')

        self.create = {'account': self.create_account,
                       'account_type': self.create_account_type,
                       'allocation': self.create_allocation,
                       'asset': self.create_asset,
                       'asset_class': self.create_asset_class,
                       'balance': self.create_balance,
                       'component': self.create_component,
                       'constant': self.create_constant,
                       'institution': self.create_institution,
                       'location': self.create_location,
                       'owner': self.create_owner,
                       'price': self.create_price}

    # TODO: test
    def execute(self, cmd, params=None):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute(cmd, params) if params is not None else cur.execute(cmd)
        con.commit()
        con.close()

    # TODO - test?
    def execute_script(self, cmd):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.executescript(cmd)
        con.commit()
        con.close()

    # TODO: test?
    def execute_file(self, file_name):
        with open(file_name, 'r') as sql_file:
            self.execute_script(sql_file.read())

    # TODO: test
    def fetch_one(self, cmd, params=None):
        con = sqlite3.connect(self.db)
        con.row_factory = dict_factory
        cur = con.cursor()
        result = cur.execute(cmd, params).fetchone() if params is not None else cur.execute(cmd).fetchone()
        con.commit()
        con.close()
        return result

    # TODO: test?
    def fetch_all(self, cmd, params=None):
        con = sqlite3.connect(self.db)
        con.row_factory = dict_factory
        cur = con.cursor()
        result = cur.execute(cmd, params).fetchall() if params is not None else cur.execute(cmd).fetchall()
        con.commit()
        con.close()
        return result

    def insert_from_csv_directory(self, directory_path):
        self.insert_from_dict(csv_directory_to_dict(directory_path))

    def insert_from_json(self, file_path):
        self.insert_from_dict(json_loader(file_path))

    def insert_from_dict(self, insert_dict):
        for table_name in insert_dict:
            for line in insert_dict[table_name]:
                self.create[table_name](**line)

    # CREATE
    def create_account(
            self,
            name,
            account_type_id,
            institution_id,
            owner_id,
            id=None):

        self.execute(
            cmd=sql.insert_account,
            params={
                'id': id,
                'name': name,
                'account_type_id': account_type_id,
                'institution_id': institution_id,
                'owner_id': owner_id})

    def create_account_type(
            self,
            name: str,
            tax_in: bool,
            tax_growth: bool,
            tax_out: bool,
            id: int = None):

        self.execute(
            cmd=sql.insert_account_type,
            params={
                'id': id,
                'name': name,
                'tax_in': tax_in,
                'tax_growth': tax_growth,
                'tax_out': tax_out})

    def create_allocation(
            self,
            asset_class_id: int,
            location_id: int,
            percentage: float,
            id: int = None):

        self.execute(
            cmd=sql.insert_allocation,
            params={
                'id': id,
                'asset_class_id': asset_class_id,
                'location_id': location_id,
                'percentage': percentage})

    def create_asset(
            self,
            name: str,
            symbol: str,
            id: int = None):

        self.execute(
            cmd=sql.insert_asset,
            params={
                'id': id,
                'name': name,
                'symbol': symbol})

    def create_asset_class(
            self,
            name: str,
            id: int = None):

        self.execute(
            cmd=sql.insert_asset_class,
            params={
                'id': id,
                'name': name})

    def create_balance(
            self,
            account_id: int,
            asset_id: int,
            balance_date: str,
            quantity: float,
            id: int = None):

        self.execute(
            cmd=sql.insert_balance,
            params={
                'id': id,
                'account_id': account_id,
                'asset_id': asset_id,
                'balance_date': balance_date,
                'quantity': quantity})

    def create_component(
            self,
            asset_id: int,
            asset_class_id: int,
            location_id: int,
            percentage: float,
            id: int = None):

        self.execute(
            cmd=sql.insert_component,
            params={
                'id': id,
                'asset_id': asset_id,
                'asset_class_id': asset_class_id,
                'location_id': location_id,
                'percentage': percentage})

    def create_constant(
            self,
            amount: float,
            name: str,
            id: int = None):

        self.execute(
            cmd=sql.insert_constant,
            params={
                'id': id,
                'amount': amount,
                'name': name})

    def create_institution(
            self,
            name: str,
            id: int = None):

        self.execute(
            cmd=sql.insert_institution,
            params={
                'id': id,
                'name': name})

    def create_location(
            self,
            name: str,
            id: int = None):

        self.execute(
            cmd=sql.insert_location,
            params={
                'id': id,
                'name': name})

    def create_owner(
            self,
            name: str,
            birthday: str,
            id: int = None):

        self.execute(
            cmd=sql.insert_owner,
            params={
                'id': id,
                'birthday': birthday,
                'name': name})

    def create_price(
            self,
            asset_id: int,
            price_date: str,
            amount: float,
            id: int = None):

        self.execute(
            cmd=sql.insert_price,
            params={
                'id': id,
                'asset_id': asset_id,
                'price_date': price_date,
                'amount': amount})

    # READ
    def read_net_worth(self):
        return self.fetch_one("SELECT * FROM net_worth_formatted")

    def read_where_to_contribute(self, contribution):
        return self.fetch_all(
            cmd=sql.where_to_contribute_formatted,
            params={'contribution': contribution})
