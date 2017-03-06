import json, re

from database import Database
from webservice import Webservice

class Parser:

	def __init__(self):
		'''
		This class is only used for when text needs parsing
		'''
		return

	def add_stock_to_database(self, symbol):
		# DEPRECATED FUNCTION
		webservice = Webservice()
		parsed_json = json.loads(webservice.get_from_yahoo(symbol))
		dictionary = parsed_json['query']['results']['quote']

		database = Database()

		column_string = ""
		for i in dictionary.items():
			column_string = column_string + ", " + i[0]

		column_string = "(" + column_string[2:] + ")"

		value_string = ""
		for i in dictionary.items():
			value_string = value_string + "\", \"" + str(i[1])
		value_string = "(\"" + value_string[4:] + "\")"

		# Because for some reason there are two "Symbol" fields
		column_string = column_string.replace("Symbol", "Symbol_2")
		column_string = column_string.replace(", Change, ", ", Change_percent, ")
		column_string = column_string.replace(", Name, ", ", Name_of_company, ")
		column_string = column_string.replace(", Open, ", ", Open_price, ")

		database.insert_values_into_table(column_string, value_string)
		#print(column_string)
		#print(value_string)

		database.close_connection()
		#print(noob)
		print("%s Added to database.") % (symbol)

	def extract_symbols(self):
		file_data = open("/Users/kheiden/Desktop/algotrader/nasdaq_symbols.txt", 'r')
		file_string = file_data.read()
		regex = re.compile("^[A-Z]{1,}\|", re.MULTILINE)
		output = re.findall(regex, file_string)
		for i in output:
			self.add_stock_to_database(i[:-1])
