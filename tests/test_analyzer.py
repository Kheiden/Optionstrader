import time
import unittest

from analyzer import Analyzer
from database import Database
from customlogging import CustomLog
from stream import Stream

class TestAnalyzer(unittest.TestCase):
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
            log.debug("-".center(100, "-"))
            return method(*args, **kwargs)
        return __init__

    @log_start
    def setUp(self):
        self.analyzer = Analyzer()
        self.database = Database()
        self.stream = Stream()
        self.log = CustomLog()

    @log_end
    def tearDown(self):
        pass


    def test_analyzer_example_stream(self):
        # mysqlid CPU utilization is above 90%  Memory is about 588 MB
        # Current median records analyzed is about 21.22 records per seconds
        # Goal is 2122.0 records per second


        option_chains_dict = self.stream.get_test_stream(stream_type='option_chains_sorted', num_chains_limit=5)
        # We want to preprocess the datastream, so that we don't waste CPU resourses on database calls

        self.assertEqual(type(option_chains_dict), type({}))
        self.assertTrue(option_chains_dict)
        #return

        #self.log.debug(datastream_generator.next())
        records_per_second = []
        results = []

        self.log.debug("Starting Analysis...".format())
        time_before = time.time()
        for option_chain in datastream_generator:
            # This can be changed to a "while True" loop when it's migrated to the tools module
            record_time_before = time.time()

            results.append(self.analyzer.analyze_single_option_chain(option_chain))
            results_len = len(results) - 1
            if (results_len % 10 == True) and (results_len > 10):
                record_time_after = time.time()

                record_time = record_time_after - record_time_before
                self.log.debug("Analyzed {0} total option_chains".format(results_len-1))
                self.log.debug("Analyzed 10 option_chains in {1} seconds. {2} Records per second".format(
                    results_len,
                    record_time,
                    10 / record_time))
                records_per_second.append(10 / record_time)
                self.log.debug("Median Records per second: {}".format(
                    sorted(records_per_second)[len(records_per_second)/2]))
                self.log.debug("Continuing Analysis...")

        time_after = time.time()

        self.log.debug("Number of option_chains analyzed: {0} in {1} seconds".format(
            len(results),
            time_after-time_before))

        self.assertTrue(len(results)>0)

    @unittest.skip("skipping...")
    def test_analyze_option_chain(self):


        # This module take the stock's most recent price into account when
        # performing the analysis.
        # This function will eventually be run on a scheduled basis


        # all of the option chains for a given ticker will be pulled
        # sorted by timestamp in descending order
        # option_chains is a list of all option chains for a given ticker,
        # sorted by timestamp in descending order

        ticker = 'FB'
        #ticker_array_len = len(ticker_array) = number of cores (num workers)
        ticker_array = ['FB', 'GOOG', 'GOOGL', 'V', 'T', 'NFLX', 'NVDI', 'VZ']

        self.analyzer.start_db_update_queue_workers()
        # Arbritrary n cores workers

        completion_list = []

        for ticker in ticker_array:
            # Currently at 2043 microseconds per option chain analyzed
            # Goal: 2.043 microseconds per option chain analyzed
            result = self.analyzer.analyze_all_option_chains_for_ticker(ticker)
            completion_list.append(result)

        # if completion_list has -1 in it, then we need to improve our processing from the
        # datastream
        # -1 means that there was a processing error downstream

        # Make sure that at least one of the tickers in the ticker_array comes back
        # successful
        self.assertGreater(max(completion_list), -1)

    @unittest.skip("skipping...")
    def test_analyze_all_option_chains(self):
        '''
        # First Run:
        # Completed in 504.353s
        #
        # Second Run:
        # Completed in 422.943s 75-93% CPU utilization on Mac mini
        #
        # Third Run:
        # Completed in 413.556s x% CPU utilization on Mac mini
        #
        # Fourth Run
        #  - option_chain_timestamp_threshold = 300000
        #  - maximum_number_of_option_chains = 10
        # Completed in 164.522s x% CPU utilization on Mac mini
        #
        # Fifth Run
        #  - option_chain_timestamp_threshold = 300000
        #  - maximum_number_of_option_chains = 10
        # Completed in 149.962s x% CPU utilization on Mac mini
        #
        # Sixth Run
        #  - option_chain_timestamp_threshold = 300000
        #  - maximum_number_of_option_chains = 10
        #  - max_number_threads = 8
        # Completed in 24.169s ~69% CPU utilization on Mac mini
        #
        # Seventh Run
        #  - option_chain_timestamp_threshold = 300000
        #  - maximum_number_of_option_chains = 10
        #  - max_number_threads = 10
        # Completed in 22.770s ~72% CPU utilization on Mac mini
        #
        # Eighth Run
        #  - option_chain_timestamp_threshold = 300000
        #  - maximum_number_of_option_chains = 10
        #  - max_number_threads = 16
        # Completed in 22.770s ~72% CPU utilization on Mac mini
        '''

        # TODO
        # Confirm that the option expiration date has been added to the database appropiately
        results = self.analyzer.analyze_all_option_chains()
        self.assertTrue(results)

    @unittest.skip("PASSED")
    def test_get_recommended_option_purchase(self):
        # returns a dictionary of the top 10 recommended purchases
        result = self.database.get_recommended_option_purchase()
        sanitized = self.analyzer.sanitize_recommended_option_purchase(result)
        log_msg = sanitized
        self.assertTrue(sanitized)


    @unittest.skip("NOT PASSING...")
    def test_stock_volatility_analysis(self):
        # Used to see how volatile a stock is over the year
        # (Greater Than) '>' 0 = volatile in a downward trend
        # (Less Than) '<' 0  = voletile in an upward test_get_recommended_option_purchase
        # 0 = zero volatility (No pricve changes for time period)
        #
        # Example:
        # curr_price = 100
        # price_array = [100 for i in range(365)]
        # len_price_array = len(price_array)
        # volatility = sum(price_array) / len_price_array / curr_price

        results = False
        self.assertTrue(results)
