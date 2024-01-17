# sql_database.py
# Generic sql command module
# 2023-12-18
# @juicemcpeso

import sqlite3


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


class Database:
    def __init__(self, sql_database, create_list, drop_list):
        self.database = sql_database
        self.create_table_commands = create_list
        self.drop_table_commands = drop_list

        self.create_all_tables()

    def create_all_tables(self):
        self.execute_list_commands(self.create_table_commands)

    def drop_all_tables(self):
        self.execute_list_commands(self.drop_table_commands)

    # TODO - clean up which of these are actually used
    def execute(self, command):
        """Execute a single command"""
        con = sqlite3.connect(self.database)
        cur = con.cursor()
        cur.execute(command)
        con.commit()
        con.close()

    def execute_parameters(self, command, parameters):
        """Execute a single command with parameters"""
        con = sqlite3.connect(self.database)
        cur = con.cursor()
        cur.execute(command, parameters)
        con.commit()
        con.close()

    def execute_kwargs(self, command, kwargs):
        con = sqlite3.connect(self.database)
        cur = con.cursor()
        cur.execute(command, kwargs)
        con.commit()
        con.close()

    def execute_list_commands(self, command_list):
        """Execute a list of commands"""
        for command in command_list:
            self.execute(command)

    def execute_many(self, command, data_sequence):
        """Execute a single command multiple times with different data"""
        con = sqlite3.connect(self.database)
        cur = con.cursor()
        cur.executemany(command, data_sequence)
        con.commit()
        con.close()

    # def sql_fetch_all_dict(self, command_text):
    #     con = sqlite3.connect(self.database)
    #     con.row_factory = dict_factory
    #     cur = con.cursor()
    #     result = cur.execute(command_text).fetchall()
    #     con.commit()
    #     con.close()
    #     return result
    #
    # def sql_fetch_all_dict_params(self, command_text, params):
    #     con = sqlite3.connect(self.database)
    #     con.row_factory = dict_factory
    #     cur = con.cursor()
    #     result = cur.execute(command_text, params).fetchall()
    #     con.commit()
    #     con.close()
    #     return result

    # def sql_fetch_one_params(self, command_text, params):
    #     con = sqlite3.connect(self.database)
    #     con.row_factory = dict_factory
    #     cur = con.cursor()
    #     result = cur.execute(command_text, params).fetchone()
    #     con.commit()
    #     con.close()
    #     return result

    def sql_fetch_one(self, command, params=None):
        con = sqlite3.connect(self.database)
        con.row_factory = dict_factory
        cur = con.cursor()
        result = cur.execute(command, params).fetchone() if params is not None else cur.execute(command).fetchone()
        con.commit()
        con.close()
        return result

    def sql_fetch_all(self, command, params=None):
        con = sqlite3.connect(self.database)
        con.row_factory = dict_factory
        cur = con.cursor()
        result = cur.execute(command, params).fetchall() if params is not None else cur.execute(command).fetchall()
        con.commit()
        con.close()
        return result
