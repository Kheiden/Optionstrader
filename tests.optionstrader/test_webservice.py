import unittest

import time
import datetime

from context import Config
from context import Webservice
from context import CustomLog

class TestScript(unittest.TestCase):
    # Make sure to test all, before a release
    def log_start(method):
        def __init__(*args, **kwargs):
            log = CustomLog()
            msg = "STARTING UNITTEST".center(100, "-")
            log.debug(msg)
            return method(*args, **kwargs)
        return __init__

    def log_end(method):
        def __init__(*args, **kwargs):
            log = CustomLog()
            msg = "UNITTEST COMPLETE".center(100, "-")
            log.debug(msg)
            return method(*args, **kwargs)
        return __init__

    @log_start
    def setUp(self):
        self.config = Config()
        self.webservice = Webservice()
        self.next_expiration_date = self.webservice.get_option_chain_next_expiration_date()

    @log_end
    def tearDown(self):
        pass

    @unittest.skip("PASSED.")
    def test_import_module(self):
        #import requests
        self.assertTrue(True)

    @unittest.skip("PASSED.")
    def test_get_quote(self):
        stock_symbols = ['AAPL', 'FB']
        results = self.webservice.get_market_quote_for_ticker(environment_url=self.config.get_environment_url, stock_symbols=stock_symbols)
        final_results = results[0]['symbol']
        self.assertTrue(final_results)

    #@unittest.skip("PASSED.")
    def test_get_option_chain_for_ticker(self):
        stock_ticker = "FB"
        option_chain = self.webservice.get_option_chain_for_ticker(environment_url=self.config.get_environment_url, stock_ticker=stock_ticker, exp_date=self.next_expiration_date)
        #log_msg = "option_chain {}".format(option_chain)
        self.assertTrue(option_chain)

    @unittest.skip("PASSED.")
    def test_get_option_chain_expiration_date_current(self):
        expiration_date = self.webservice.get_option_chain_next_expiration_date()
        log_msg = expiration_date
        self.assertEqual(expiration_date, '2017-03-03')

    @unittest.skip("PASSED.")
    def test_get_option_chain_expiration_date_after_next(self):
        expiration_date = self.webservice.get_option_chain_expiration_date_after_next()
        log_msg = expiration_date
        self.assertEqual(expiration_date, '2017-03-10')


    @unittest.skip("PASSED")
    def test_get_option_chain_expiration_date_for_timeperiod(self):
        # timeperiod is the number of weeks in advance
        # this will determine which dates get returned
        number_of_weeks = 4
        timeperiod = number_of_weeks
        search_direction = 'inside_out'
        results = self.webservice.get_option_chain_expiration_date_for_timeperiod(timeperiod, search_direction)
        log_msg = results
        self.assertTrue(results)

        search_direction = 'outside_in'
        results = self.webservice.get_option_chain_expiration_date_for_timeperiod(timeperiod, search_direction)
        log_msg = results
        self.assertTrue(results)


    @unittest.skip("NOT YET PASSED...")
    def test_renew_oauth_token(self):
        # Still has bugs
        access_token = self.webservice.renew_access_token(self.access_token)
        print(access_token)
        self.assertTrue(access_token)

    @unittest.skip("NOT YET PASSED...")
    def test_authorize_tradier(self):
        # Tradier has an inactivity charge of $50.00 per year.  So we need to
        # load the account with at least $2000.00 USD before the end of the 1 year cycle
        self.assertTrue(self.webservice.authorize_traider())

    @unittest.skip("NOT YET PASSED...")
    def test_get_traider_account_list(self):
        account_list = self.webservice.get_traider_account_list_test(self.environment_url)
        self.assertTrue(account_list)
