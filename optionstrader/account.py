from database import Account
from account import Account

class Account:

	def __init__(self):
		self.account = Account()
		return

	def create_new_account(self, account_type, initial_deposit):
		# TODO Implement this method
		# RAND() * POWER(10, 20) AS UNSIGNED
		return

	def get_balance(self):
		output = self.account.base.get_checking_account_balance()
		self.account.connection.close_connection()
		return output

	def change_checking_account_balance(self, var):
		self.account.update_checking_account(var)
		self.account.close_connection()

	def add_money_to_checking(self, var):
		self.account.add_money_to_checking(var)
		self.account.close_connection()

	def subtract_money_from_checking(self, var):
		self.account.subtract_money_from_checking(var)
		self.account.close_connection()

	def add_option_chain_to_account(self, option_chain):
		self.account.add_stock_to_self.account(option_chain)
		self.account.close_connection()
