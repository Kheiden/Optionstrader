import os
import re
import json


#from optionstrader.database import Database
from optionstrader.webservice import Webservice

class Parser:

    def __init__(self):
      '''
      This class is only used for when text needs parsing
      '''
      return

    def add_stock_to_database(self, symbol):
      # DEPRECATED FUNCTION
      # This was used to download a list of ticker symbols and current prices.
      # Depricated since we are moving foward with tradier, not yahoo as the
      # source for the data.

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
      """ This method sanitizes ticker symbols read from disk.

          Returns:
            list() of list() of sanitized ticker symbols. Example:
            [['T', 'AT&T Inc.'], ['V', 'Visa Inc']]
      """
      file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'nasdaq_symbols.txt')
      #file_data = open(file_path, 'r')
      with open(file_path, 'r') as file_data:
          file_string = file_data.read()
      regex = re.compile("^[A-z]{1,}\|.+?\|", re.MULTILINE)
      symbols_and_names = re.findall(regex, file_string)

      cleaned_symbols_and_names = []
      for i in symbols_and_names:
          cleaned_symbols_and_names.append(i.split("|")[:-1])

      return cleaned_symbols_and_names
      #for i in output:
      #    self.add_stock_to_database(i[:-1])
