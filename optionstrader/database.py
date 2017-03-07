import time
import mysql.connector

from customlogging import CustomLog

class Database:

	def __init__(self):
		"""
		There's some confusion with database vs table.

		We will have separate environments for Dev/Stage and Prd,
		so we will want to ensure that the databases are seperate.

		TODO: Ensure that the Dev/Stage and Prod environments are fully seggregared
		with their own databases.  This will allows us to migrate the databases when
		the time comes.

		environment = 'dev' ('dev', 'stage', 'production')
		database = "algotrader_".format(environment)

		table = ('accounts', 'optionchainanalysis', 'optionchains', 'stocks')

		"""

		# initiate the connection when the database object is created
		# Standard procedure will be to open the connection,
		# perform the action, then close the connection

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
		# Below is used to determine how far back in seconds the analyzer tool should go
		# The reason behind this is because we do not want to delete stock market date
		# Instead, we would rather query the database and only select the records that
		# are within the threshold



	def close_connection(self):
		self.connection.close()

# ====================================
# ====================================
# === Code used for Account Class ====
# ====================================
# ====================================

	def update_account(self, balance, account_type):
		cursor = self.connection.cursor()
		query = ("UPDATE accounts{env} SET balance={balance} WHERE account_type=\'{account_type}\'".format(env=self.environment, balance=balance, account_type=account_type))
		cursor.execute(query)
		self.connection.commit()
		cursor.close()


	def get_recommended_option_purchase(self):
		# TODO
		results_table_cursor = self.connection.cursor()
		#query = ("SELECT balance FROM accounts{env} where account_type='checking'".format(env=self.environment))
		_query = ("SELECT * FROM optionchainanalysisDev ",
		"WHERE `total_price_paid_1x` BETWEEN 0 and 100 AND ",
		"`potential_profit_1x` BETWEEN 50 and 100 AND ",
		"`stock_price_increase` < 3.5 AND ",
		"`magic_number` BETWEEN 3 and 10 AND ",
		"`expiration_date` LIKE '2017-03-03' AND ",
		"`risk_percentage_1x` BETWEEN 0 and 18 ",
		"ORDER BY `timestamp` DESC")

		query = "".join(_query)
		log_msg = query
		#
		#
		self.connection.commit()
		result = results_table_cursor.execute(query)
		results_table = []
		for record in results_table_cursor:
			results_table.append(record)

		return results_table
		#for record in results_table:
		#	return record

	def get_list_of_tickers(self, query_type='Default'):
		# TODO Implement the following:
		# We will want to stream data from external to the database then stream the symbols from the database
		# as they're made available.

		database = 'optionchains'
		if query_type == 'Default':
			# Run the normal code here
			query = ("SELECT DISTINCT symbol FROM stocks{env} WHERE symbol is not Null".format(env=self.environment))
		if query_type == 'options_only':
			# Run the code to only retrieve symbols which have had stock options in the past
			query = ("SELECT DISTINCT underlying FROM {database}{env} WHERE underlying is not Null".format(database=database,
			env=self.environment))
		if query_type == 'one_option_only':
			# Arbritrary first option only.
			# Usually used for testing purposes
			query = ("SELECT DISTINCT underlying FROM {database}{env} WHERE underlying is not Null LIMIT 1".format(database=database,
			env=self.environment))
		else:
			# Run a special SQL query here, which returns the symbols in a specific order
			pass
		cursor = self.connection.cursor()
		# As of 2/11/17, there are 3078 total results from this query
		self.connection.commit()
		result = cursor.execute(query)
		list_of_tickers = list()
		for ticker in cursor:
			#print(ticker[0])
			list_of_tickers.append(ticker[0])

		# Return type is a python list [u'AAPL', ..., u'GOOG']
		return list_of_tickers

	def get_current_stock_price(self, symbol):
		# We want to make sure that the 'last_' price is within reason.  We don't want to
		# pay 100x the average price of the item.
		cursor = self.connection.cursor(dictionary=True)
		query = "SELECT * FROM optionchainsDev WHERE symbol LIKE \'{symbol}\' ORDER BY `timestamp` DESC LIMIT 1".format(symbol=symbol)
		self.connection.commit()
		result = cursor.execute(query)
		for stock_data in cursor:
			return stock_data['last_']

	def get_example_option_chains(self, num_chains_limit=1):
		# This function has a much less accurate query than query_option_chains_for_analysis
		# This function is typically used for testing purposes

		cursor = self.connection.cursor(dictionary=True, buffered=True)
		query = ("SELECT * from optionchains{env} LIMIT {num_chains_limit}".format(
			env=self.environment,
			num_chains_limit=num_chains_limit))
		self.connection.commit()
		cursor.execute(query)


		self.log.debug("****Type:{0}".format(type(cursor)))
		return cursor
		# Only iterate once
		#for option_chain in cursor:
		#	return option_chain, cursor[option_chain]

		# list_of_option_chains is all of the option chains for the ticker
		# therefore, we need to select and return the most recent one.


		cursor = self.connection.cursor()
		# As of 2/11/17, there are 3078 total results from this query
		query = ("SELECT * from optionchains{env} LIMIT 1".format(env=self.environment))
		self.connection.commit()
		option_chain = cursor.execute(query)
		return option_chain

	def query_option_chains_for_analysis(self,
			ticker=None, current_timestamp=int(time.time()), time_threshold=30000,
			max_num_option_chains=40):

		# This function has a more precise query than get_example_option_chains
		# If no tickers are specified, retrieve the most recent option_chains
		if ticker == None:
			cursor = self.connection.cursor(dictionary=True, buffered=True)
			query_1 = "SELECT * FROM optionchains{env} WHERE type LIKE 'option' and ".format(env=self.environment)

			query_2 = "timestamp > ({current_timestamp}-{time_threshold}) and ".format(
				time_threshold=time_threshold,
				current_timestamp=current_timestamp)
			query_3 = "option_type LIKE 'call' ORDER BY `timestamp` DESC LIMIT {max_num_option_chains}".format(max_num_option_chains=max_num_option_chains)

			query = (query_1 + query_2 + query_3)
			self.log.debug(query)
			result = cursor.execute(query)
			self.log.debug(cursor.fetchone())
			self.connection.commit()
		# If a ticker is specified, retrieve the most recent option_chains
		else:
			# We want to return the dictionary type
			# we need a MySQL buffered response
			cursor = self.connection.cursor(dictionary=True, buffered=True)
			query_1 = "SELECT * FROM optionchains{env} WHERE type LIKE 'option' and ".format(env=self.environment)

			query_2 = "timestamp > ({current_timestamp}-{time_threshold}) and underlying LIKE '{ticker}' and ".format(ticker=ticker,
				time_threshold=time_threshold,
				current_timestamp=current_timestamp)
			query_3 = "option_type LIKE 'call' ORDER BY `timestamp` DESC LIMIT {max_num_option_chains}".format(max_num_option_chains=max_num_option_chains)

			query = (query_1 + query_2 + query_3)
			result = cursor.execute(query)
			self.connection.commit()

		"""
		# cursor is a MySQLCursorDict object.

		# cursor is a MySQLCursorDict: SELECT * FROM optionchainsDev WHERE type..

		# retrieve results using cursor.fetchall()
		"""
		return cursor
		# DEPRICATED

		#result = cursor.execute(query)
		# Iterate over all options in the option chains in the database for that ticker.
		# Sorted by time in descending order

		#all_options = []
		#for option_chain in cursor:
		#	all_options.append(option_chain)
		#return all_options

	def sanitize_field_names(self, field_name):
		sanitized_field_names_pairs = {
			'change': 'change_',
			'close': 'close_',
			'open': 'open_',
			'last': 'last_'
		}

		field_name = str(field_name)
		for name in sanitized_field_names_pairs.keys():
			if field_name == name:
				sanitized_field_name = sanitized_field_names_pairs[name]
				return sanitized_field_name
		return field_name

	def save_option_chain_to_database(self, option_chain, database='optionchains'):
		# PLEASE NOTE:
		# If a new keyword (column) is detected, then the INSERT INTO command will fail
		# The next time that the option chain is attempted to be saved, the record
		# will update.
		attempt_number = 0

		while True:
			try:
				# add timestamp here
				option_chain['timestamp']=int(time.time())
				cursor = self.connection.cursor()
				#"{} {}".format(str(a.keys()).replace("'", ""), str(a.values()).replace("'", ""))
				#option_chain.keys(), option_chain.values()
				KEYS = [self.sanitize_field_names(i) for i in option_chain.keys()]
				VALUES = [str(i) for i in option_chain.values()]


				# Should never have the single character apostrophy.
				# Error out, if it contains once
				keys_error = [str(i).find("'") for i in option_chain.keys()]
				values_error = [str(i).find("'") for i in option_chain.values()]
				if max(max(keys_error), max(values_error)) != -1:
					log_msg = ""
					log_msg = "Error: single character apostrophy located in option_chain!"

				keys_formatted = str("(" + str(KEYS)[1:-1] + ")").replace("'", "")
				values_formatted = str("(" + str(VALUES)[1:-1] + ")")
				query = ("INSERT INTO {database}{env} {keys} VALUES {values}").format(env=self.environment,
							keys=keys_formatted,
							values=values_formatted,
							database=database)
				#log_msg = "~~~~-----------------~~~"
				#print(query)
				cursor.execute(query)
				self.connection.commit()
				cursor.close()
				# Break the while loop
				break
			except mysql.connector.ProgrammingError:
				# This means that the fields don't exist on the database
				# time to add the fields to the database
				log_msg = "Warning. Trying to update the database with fields which don't yet exist in the table."
				# Unsure which key is the problem one.
				# Try to create a field with each key.
				# if the key is already a field on the database, then pass without error
				for field_name in KEYS:
					# mySQL database needs specific table names to be off limits
					try:
						field_type = self.type_conversion(option_chain[field_name])
					except:
						field_type = self.type_conversion(option_chain[field_name[:-1]])
					try:
						self.add_new_column_to_database_table(field_name, field_type, database=database)
					except mysql.connector.ProgrammingError:
						pass
				log_msg = "Information. The fields were updated in table '{0}'.".format(database)
				if attempt_number == 1:
					log_msg = "Error: Unable to update SQL Database"
					break
				else:
					log_msg = "Retrying the update to the database"
					attempt_number += 1
		return True


	def update_option_chain_with_analysis(self, percentage_increase_analysis):
		# This is the analysis done for the percentage increase (1,2,5 percent)
		# of an underlyer
		result = self.save_option_chain_to_database(percentage_increase_analysis, database='optionchainanalysis')
		return True

	def add_new_column_to_database_table(self, column_name, data_type, database):
		cursor = self.connection.cursor()
		env = self.environment
		query = ("ALTER TABLE {database}{env} ADD {column_name} {data_type}".format(env=env,
			column_name=column_name,
			data_type=data_type,
			database=database))
		cursor.execute(query)
		self.connection.commit()
		return True



	def add_money_to_account(self, amount_of_money, account_type):
		current_balance = self.get_checking_account_balance()
		output = str(current_balance + amount_of_money)
		self.update_checking_account(output)
		print(self.get_checking_account_balance())

	def subtract_money_from_account(self, amount_of_money, account_type):
		current_balance = self.get_checking_account_balance()
		output = str(current_balance - amount_of_money)
		self.update_checking_account(output)
		print(self.get_checking_account_balance())

	def add_field_to_table(self, field, type):
		cursor = self.connection.cursor()
		query = ("ALTER TABLE stocks ADD %s %s") % (field, type)
		cursor.execute(query)
		self.connection.commit()
		cursor.close()

	def insert_values_into_table(self, column_string, value_string):
		cursor = self.connection.cursor()
		query = ("INSERT INTO stocks %s VALUES %s") % (column_string, value_string)
		cursor.execute(query)
		self.connection.commit()
		cursor.close()

	def type_conversion(self, object_item):
		# We need to convert the types so that the sql database knows what to do
		# The names of the types differs between python and mysql

		# Examples: unicode, NoneType, int, float
		obj_type = type(object_item)
		obj_type_str = str(obj_type).lstrip("< type '").rstrip("'>")
		if obj_type_str == 'unicode':
				return "text"
		if obj_type_str == 'float':
				return "float"
		if obj_type_str == 'NoneType':
				return "text"
		if obj_type_str == 'int':
				return "bigint(20)"
		else:
				return "text"
