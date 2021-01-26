import time
import random
import mysql.connector

from optionstrader.customlogging import CustomLog
from optionstrader.config import Config

class Account:

    def __init__(self):
        self.log = CustomLog()
        self.config = Config()

        try:
            # Using loopback for testing purposes.  Might use socket level later.

            self.database = 'algotrader_{env}'.format(env=self.config.get_environment())
            self.log.debug("*Setting database to {db}".format(db=self.database))

            self.connection = mysql.connector.connect(user='root', password='root',
                                                          host='127.0.0.1',
                                                          port='3306',
                                                          database=self.database)
        except Exception as e:
            msg = "Error! Please check the MySQL database connection: {error}".format(error=e)
            self.log.debug(msg)
            print(msg)
            raise Exception

        # CONFIGURATION
        # Possible Values: "Dev", "Stage", "Production"
        # Changebelow code when config file exists
        self.environment = "dev"

    def close_connection(self):
        # check if the connection is alive.
        # if so, close it.
        return

    def get_checking_account_balance(self, account_number):

        cursor = self.connection.cursor()
        query = ("SELECT balance FROM accounts where account_type='checking' AND account_number=\'{0}\'".format(account_number))
        result = cursor.execute(query)
        self.connection.commit()
        self.close_connection()
        for balance in cursor:
            return balance[0]

    def update_checking_account(self, value):
        # Make the account value whatever the value variable is
        cursor = self.connection.cursor()
        query = ("SELECT balance FROM accounts where account_type='checking'".format(env=self.environment))
        self.connection.commit()
        result = cursor.execute(query)
        for balance in cursor:
            return balance[0]
        return

    def create_new_account(self, account_type, initial_deposit):
        # TODO Implement this method
        # RAND() * POWER(10, 20) AS UNSIGNED

        # We want a random 20 digit number. Any leading zeroes will be appended
        # to the account number on the database side.
        if not account_type in ['checking', 'savings']:
          return False
        data = {}

        account_number = str(random.randint(pow(10,20), pow(10,21)-1))

        # TODO Make sure that the account_number does not collide with an existing account number
        data['account_number'] = account_number
        data['account_type'] = 'checking'
        data['balance'] = initial_deposit
        data['total_deposits'] = initial_deposit
        data['total_withdrawls'] = 0

        keys_formatted = str(tuple(data.keys())).replace("'", "")
        self.log.debug("keys_formatted: {}".format(keys_formatted))

        values_formatted = str(tuple(data.values()))
        self.log.debug("values_formatted: {}".format(values_formatted))

        cursor = self.connection.cursor()
        table = 'accounts'

        query = ("INSERT INTO {table} {keys} VALUES {values}").format(
                    table=table,
                    keys=keys_formatted,
                    values=values_formatted
                )

        self.log.debug("query: {}".format(query))
        cursor.execute(query)

        self.connection.commit()
        self.log.debug("Update Successful!")
        return True

    def get_balance(self, account_number, account_type):
        cursor = self.connection.cursor()
        query = ("SELECT balance FROM {table} where account_type=\'{account_type}\' AND account_number=\'{account_number}\'".format(
                table='accounts',
                account_type=account_type,
                account_number=account_number
                ))

        self.connection.commit()
        result = cursor.execute(query)
        for balance in cursor:
            return balance[0]

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
