# TODO
# Fix the importing
# import CustomName
# ...
# obj = CustomName()
# obj.account.get_balance()
# obj.parser.extract_symbols()

import __init__
from __init__ import Account
from __init__ import Webservice
from __init__ import Database
from __init__ import Parser

import sys, json

if __name__ == "__main__":
	# TODO
	# Rename or Depricate this code

	myaccount = Account()
	webservice = Webservice()

	input_data = raw_input("Function to Process > ")

	if input_data == "g":
		print(myaccount.get_balance())

	if input_data == "a":
		money = raw_input("Amount of money > ")
		myaccount.add_money_to_checking(money)

	if input_data == "s":
		money = raw_input("Amount of money > ")
		myaccount.subtract_money_from_checking(money)

	if input_data =='x':
		parser = Parser()
		#symbol = raw_input("Enter Symbol > ")
		parser.extract_symbols()

	if input_data =='l':
		parser = Parser()
		#symbol = raw_input("Enter Symbol > ")
		parser.start_options_scan()
