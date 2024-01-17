# sql_to_markdown.py
# Markdown exporter for sqlite 3 tables
# 2024-01-17

# def markdown_export(self):
#     for table_name in self.portfolio:
#         print(f"# {table_name}")
#         print(markdown_table_string(self.portfolio[table_name]()))
#
# def markdown_table_string(sql_list):
#     string = ''
#     if sql_list:
#         string += markdown_table_column_names(sql_list[0].keys())
#         string += markdown_table_topper(len(sql_list[0].keys()))
#         string += markdown_table_rows(sql_list)
#
#     return string
#
#
# def markdown_table_column_names(column_keys):
#     string = '|'
#     for column_name in column_keys:
#         string += column_name
#         string += '|'
#     string += '\n'
#
#     return string
#
#
# def markdown_table_topper(number_of_columns):
#     string = '|'
#     for _ in range(number_of_columns):
#         string += '---|'
#     string += '\n'
#
#     return string
#
#
# def markdown_table_rows(sql_list):
#     string = ''
#     for row in sql_list:
#         for item in row.keys():
#             string += '|'
#             string += str(row[item])
#
#         string += '|\n'
#
#     return string