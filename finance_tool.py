# finance_tool.py
# Main program for the finance tool
# 2023-12-18
# @juicemcpeso

import interface
import portfolio

if __name__ == "__main__":
    program = interface.Interface(portfolio.Portfolio())
    program.main_menu()
