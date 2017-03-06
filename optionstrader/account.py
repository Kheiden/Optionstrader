import time
import mysql.connector

from customlogging import CustomLog

class Account:

	def __init__(self):
		self.log = CustomLog()

		try:
			# Using loopback for testing purposes.  Might use socket level later.
			self.connection = mysql.connector.connect(user='root', password='root',
														  host='127.0.0.1',
														  port='8889',
														  database='algotrader_data')
		except Exception as e:
			msg = "Error! Please check the MySQL database connection: {error}".format(error=e)
			self.log.debug(msg)
			log_msg = msg

		# CONFIGURATION
		# Possible Values: "Dev", "Stage", "Production"
		# Changebelow code when config file exists
		self.environment = "Dev"

	def get_checking_account_balance(self):
		cursor = self.connection.cursor()
		query = ("SELECT balance FROM accounts{env} where account_type='checking'".format(env=self.environment))
		self.connection.commit()
		result = cursor.execute(query)
		for balance in cursor:
			return balance[0]


	def update_checking_account(self, value):
		# Make the account value whatever the value variable is
		cursor = self.connection.cursor()
		query = ("SELECT balance FROM accounts{env} where account_type='checking'".format(env=self.environment))
		self.connection.commit()
		result = cursor.execute(query)
		for balance in cursor:
			return balance[0]
		return

	def create_new_account(self, account_type, initial_deposit):
		# TODO Implement this method
		# RAND() * POWER(10, 20) AS UNSIGNED
		return

	def get_balance(self):
		output = self.get_checking_account_balance()
		self.connection.close_connection()
		return output

	def change_checking_account_balance(self, var):
		self.update_checking_account(var)
		self.close_connection()

	def add_money_to_checking(self, var):
		self.add_money_to_checking(var)
		self.close_connection()

	def subtract_money_from_checking(self, var):
		self.subtract_money_from_checking(var)
		self.close_connection()

	def add_option_chain_to_account(self, option_chain):
		self.add_stock_to_self.account(option_chain)
		self.close_connection()
