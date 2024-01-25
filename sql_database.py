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

    # Execute
    def execute(self, command, params=None):
        """Execute a single command"""
        con = sqlite3.connect(self.database)
        cur = con.cursor()
        cur.execute(command, params) if params is not None else cur.execute(command)
        con.commit()
        con.close()

    def execute_many(self, command, data_sequence):
        """Execute a single command multiple times with different data"""
        con = sqlite3.connect(self.database)
        cur = con.cursor()
        cur.executemany(command, data_sequence)
        con.commit()
        con.close()

    def execute_list_commands(self, command_list):
        """Execute a list of commands"""
        for command in command_list:
            self.execute(command)

    # Fetch
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

    def column_names(self, command):
        con = sqlite3.connect(self.database)
        cur = con.execute(command)
        column_names = [description[0] for description in cur.description]
        con.commit()
        con.close()
        return column_names

    def execute_from_file(self, file_name):
        with open(file_name, 'r') as sql_file:
            sql_script = sql_file.read()

        con = sqlite3.connect(self.database)
        cur = con.cursor()
        cur.executescript(sql_script)
        con.commit()
        con.close()
