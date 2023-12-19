# file_processing.py
# Module for file processing csv
# 2023-12-18
# @juicemcpeso

def get_split_lines(file_name):
    split_lines = []
    full_file_path = '/Users/ryan/PycharmProjects' + file_name
    with open(full_file_path, 'r') as handle:
        handle.readline()  # Removes header
        lines = handle.read().splitlines()

    for line in lines:
        split_lines.append(tuple(line.split(',')))

    return split_lines
