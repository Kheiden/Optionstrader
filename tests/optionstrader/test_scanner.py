import time
import unittest

from context import optionstrader

class TestScanner(unittest.TestCase):
    # Make sure to test all, before a release
    def log_start(method):
        def __init__(*args, **kwargs):
            log = optionstrader.CustomLog()
            msg = "STARTING UNITTEST".center(100, "-")
            log.debug(msg)
            return method(*args, **kwargs)
        return __init__

    def log_end(method):
        def __init__(*args, **kwargs):
            log = optionstrader.CustomLog()
            msg = "UNITTEST COMPLETE".center(100, "-")
            log.debug(msg)
            return method(*args, **kwargs)
        return __init__

    @log_start
    def setUp(self):
        self.scanner = optionstrader.Scanner()
        self.webservice = optionstrader.Webservice()
        self.log = optionstrader.CustomLog()

    @log_end
    def tearDown(self):
        return

    @unittest.skip("NOT YET PASSED.")
    def test_start_option_chain_scan_for_ticker_array(self):
        ticker_array = ['FB', 'AAPL']

        query_type = 'options_only'
        number_of_weeks = 1
        scan_type = 'inside_out'
        time_before = time.time()

        self.log.debug("Starting option_chain_scan...")

        # TODO improve
        # Scan rate is Currently about 40 seconds per ticker num option chains: (~110)
        # we want to stream the analysis, so we want the ability to scan much faster.
        # Goal scan rate: .20 seconds per ticker

        self.scanner.start_option_chain_scan(scan_type=scan_type,
            number_of_weeks=number_of_weeks,
            query_type=query_type,
            ticker_array=ticker_array)
        time_after = time.time()
        sec = time_after - time_before

        msg = "Completed option_scan with scan_type '{scan_type}' in time: {sec}sec".format(
            sec=sec,
            scan_type=scan_type)
        self.log.debug(msg)

        self.log.debug("OPTION CHAIN SCAN COMPLETED".center(100, "-"))

        self.assertTrue(True)

        #results = self.scanner.process_option_chain(option_chain_array=option_chain_array)
        #self.assertTrue(results)

    @unittest.skip("NOT YET PASSED.")
    def test_process_option_chain(self):
        result = self.scanner.start_option_chain_scan(number_of_weeks=4, scan_type='next_week_only',
                query_type='one_option_only', ticker_array=None)

        self.assertTrue(result)


    #@unittest.skip("NOT YET PASSED.")
    def test_start_option_chain_scan(self):
        # This is a perpetual scan.  It will never pass because it will never complete

        # - inside_out: Scans for option chains for the earliest option expiration date, then goes outwards.
        # Scan start with the AAAA ends with ZZZZ.

        '''
        TOP LEVEL Options Chain scan.  This method determines how the scan will work.

        query_type is used for determining how many companies will be scanned
        - 'default' : will scan for DISTINCT symbol FROM stocks{env} WHERE symbol is not Null
        - 'options_only' : will only scan for DISTINCT underlying FROM {database}{env}

        number_of_weeks is the number of DISTINCT expiration_dates that the code will scan for
        -
        '''

        query_type = 'default'
        #query_type = 'options_only'
        number_of_weeks = 4
        scan_type = 'inside_out'
        time_before = time.time()

        self.log.debug("Starting option_chain_scan...")

        # TODO improve
        # Scan rate is Currently about 40 seconds per ticker num option chains: (~110)
        # we want to stream the analysis, so we want the ability to scan much faster.
        # Goal scan rate: .20 seconds per ticker

        number_iterations = 0
        while True:

            self.scanner.start_option_chain_scan(scan_type=scan_type,
                number_of_weeks=number_of_weeks,
                query_type=query_type)
            time_after = time.time()
            sec = time_after - time_before

            msg = "Completed option_scan with exp_date_type '{exp_date_type}' in time: {sec}sec".format(
                sec=sec,
                exp_date_type=exp_date_type)

            self.log.debug(msg)

            msg = "Number of iterations: {}".format(number_iterations)
            self.log.debug(msg)
        self.log.debug("OPTION CHAIN SCAN COMPLETED".center(100, "-"))

        # - outside_in: Scans for option chains for the farthest option expiration date (set limit manually Eg- 6 months out),
        # then goes inwards. Scan start with the AAAA ends with ZZZZ.
        #self.scanner.start_options_scan(exp_date_type='outside_in')

    @unittest.skip("PASSED.")
    def test_start_stock_scan(self):
        results = self.scanner.start_stock_scan()
        self.assertTrue(results)

    @unittest.skip("PASSED.")
    def test_get_company_information(self):
        results = self.scanner.get_company_information()
        self.assertTrue(results)


    @unittest.skip("PASSED.")
    def test_start_option_chain_scan_next(self):
        '''
        # DEPRICATED. Use start_option_chain_scan()
        '''
        # When ready to scan all of the tickers for their option chains, use this one
        # TODO
        # Make sure that the scanner also analyzes the stock and
        # adds the appropriate analysis information to the database

        # This scans for options which expire at the current or next expiration date
        expiration_date = self.webservice.get_option_chain_expiration_date_after_next()
        log_msg = expiration_date
        expiration_date = self.webservice.get_option_chain_next_expiration_date()
        log_msg = expiration_date
        self.assertTrue(False)
        #result = self.scanner.start_options_scan(exp_date_type='next')
        #self.assertTrue(result)

    @unittest.skip("PASSED.")
    def test_start_option_chain_scan_current(self):
        '''
        # DEPRICATED. Use test_both_option_scan_types()
        '''
        # When ready to scan all of the tickers for their option chains, use this one
        # TODO
        # Make sure that the scanner also analyzes the stock and
        # adds the appropriate analysis information to the database

        # This scans for options which expire at the expiration date after the current one (next)
        result = self.scanner.start_options_scan(exp_date_type='current')
        self.assertTrue(result)
