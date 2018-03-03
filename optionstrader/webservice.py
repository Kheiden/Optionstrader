# Builtin modules
import json
import time
import math
import datetime

# Downloaded via pip
import requests

# Downloaded via GitHub
from .tradier import Tradier

# Local Code
from .config import Config
#from .database import Database
from .savefile import Savefile
#from .analyzer import Analyzer
from .customlogging import CustomLog

# UNSURE IF USING / USED FOR TESTING
# None

class Webservice:

    def __init__(self):
        #self.consumer_key = self.savefile.load_from_file()['consumer_key']
        #self.consumer_secret = 'self.savefile.load_from_file()
        self.base_url = ""
        #self.savefile = Savefile()
        #self.oauth_access_token = self.savefile.load_from_file()['oauth_access_token']
        #self.oauth_access_token_secret = self.savefile.load_from_file()['oauth_access_token']
        self.oauth_session_started = False
        # Removing database and analyzer since it would cause a circular import
        #self.d = Database()
        #self.analyzer = Analyzer()
        self.config = Config()
        self.access_token = self.config.get_access_token()

        self.tradier = Tradier(self.access_token)

    def api_limiter(method):
        def timed(*args, **kw):
            # Only allowed X request(s) per second
            # Only allowed X/1000 request(s) per millisecond
            ts = time.time()
            result = method(*args, **kw)
            te = time.time()
            # TODO Clean this up later
            ticker_type = None

            try:
                ticker = kw['stock_ticker']
                ticker_type = "@api_limiter value type used for symbol '{0}' : kwargs".format(ticker)
            except:
                ticker = args[1]
                ticker_type = "@api_limiter value type used for symbol '{0}' : args".format(ticker)


            api_completion_time = te-ts

            # TODO Change later to the config
            maximum_api_calls_per_second = 1
            if api_completion_time < maximum_api_calls_per_second:
                sleep_time = maximum_api_calls_per_second - api_completion_time
                time.sleep(sleep_time)
            else:
                sleep_time = 0

            log_msg = "Completed {method} in {api_completion_time} millisec. Slept for {sleep_time} millisec".format(
                method=method.__name__,
                api_completion_time=api_completion_time*1000,
                sleep_time=1000*sleep_time)
            log = CustomLog()
            log.debug(log_msg)
            # TODO Clean this up later
            log.debug(ticker_type)
            return result
        return timed


    def get_option_chain_expiration_date_for_timeperiod(self, number_of_weeks, search_direction):
        timeperiod = number_of_weeks

        option_chain_expiration_dates_for_timeperiod = []

        for i in range(timeperiod):
            #first_option_expiration_date
            if option_chain_expiration_dates_for_timeperiod == []:
                log_msg = option_chain_expiration_dates_for_timeperiod
                option_expiration_date = self.get_option_chain_next_expiration_date()
            else:
                option_expiration_date = option_chain_expiration_dates_for_timeperiod[i-1]
            expiration_date_obj = datetime.datetime.strptime(option_expiration_date, '%Y-%m-%d')
            # Add 7 days to the datetime object, then return a string
            date_after_next = expiration_date_obj + datetime.timedelta(days=7)
            option_chain_expiration_dates_for_timeperiod.append(date_after_next.strftime("%Y-%m-%d"))

        if search_direction == 'inside_out':
            log_msg = search_direction
            return option_chain_expiration_dates_for_timeperiod

        if search_direction == 'outside_in':
            log_msg = search_direction
            return sorted(option_chain_expiration_dates_for_timeperiod, reverse=True)

    def get_option_chain_next_expiration_date(self):
        days_between_today_and_friday = 5-int(time.strftime("%w"))
        todays_date_object = datetime.datetime.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d")
        if days_between_today_and_friday == 0:
            # Today's Friday! Return today's date as a string
            return time.strftime("%Y-%m-%d")
        else:
            # Today's not friday.  Return next friday's date
            next_friday_date = todays_date_object + datetime.timedelta(days=days_between_today_and_friday)
        # return with type string '2017-02-17'
        return next_friday_date.strftime("%Y-%m-%d")

    def get_option_chain_expiration_date_after_next(self):
        days_between_today_and_friday = 5-int(time.strftime("%w"))
        next_expiration_date = self.get_option_chain_next_expiration_date()
        # Convert the string to a datetime object
        next_expiration_date_obj = datetime.datetime.strptime(next_expiration_date, '%Y-%m-%d')
        # Add 7 days to the datetime object, then return a string
        date_after_next = next_expiration_date_obj + datetime.timedelta(days=7)
        return date_after_next.strftime("%Y-%m-%d")

    def test_get_stock(self):
        # TESTING
        #auth_data = self.authorize_etrade()


        stock_ticker = "AAPL"
        exp_month = time.strftime("%m")
        exp_year = time.strftime("%Y")
        chainType = 'CALLPUT'
        skipAdjusted = 'FALSE'

        # TESTING
        #option_chain = self.get_option_chain_for_ticker(stock_ticker=stock_ticker, exp_month=exp_month, exp_year=exp_year, chainType=chainType, skipAdjusted=skipAdjusted)
        #print("optionPairs: {0}".format(stock_bid['optionPairs']))
        # TESTING
        option_chain = {
            'timestamp': round(time.time(), 4),
            'symbol': stock_ticker
        }
        return option_chain


    def renew_access_token(self, old_oauth_token):
        return False


    # This *should* only need to happen once in order to receive a request_token
    def authorize_tradier(self):
        # Not being used right now
        return False

    def get_traider_account_list_test(self, environment_url):
        return False

    def get_example_option_chain(self, environment_url, exp_date):
        stock_ticker = "AAPL"
        self.session = Tradier(self.access_token)
        results = self.session.options.chains(stock_ticker, str(exp_date))
        results[0]['timestamp_record_received'] = int(time.time())
        # log_msg = "~~~~~~~~~~"
        # log_msg = results[0]
        # log_msg = "~~~~~~~~~~"
        # returns a single option_chain
        return results[0]

    def get_market_quote_for_ticker(self, environment_url, stock_symbols):
        self.session = Tradier(self.access_token)
        results = self.session.markets.quotes(stock_symbols)
        return results

    def get_company_information_for_ticker(self, environment_url, stock_symbols):
        self.session = Tradier(self.access_token)
        results = self.session.markets.quotes(stock_symbols)
        return results

    @api_limiter
    def get_option_chain_for_ticker(self, environment_url, stock_ticker, exp_date):

        #tradier
        self.session = Tradier(self.access_token)

        results = self.session.options.chains(stock_ticker, exp_date)
        # TODO
        # Check that this part works

            #.update(timestamp=int(time.time()))
            # Implement the code below
            #results[i].update(magic_number=magic_number)
        #log_msg = "~~~~~~~~~~"
        #log_msg = len(results)
        # for record in results:
        #    add_to_database(record)
        #log_msg = results[0]
        #log_msg = "~~~~~~~~~~"
        #log_msg = results[1]
        #log_msg = "~~~~~~~~~~"

        return results
