import unittest

from context import optionstrader

class TestTools(unittest.TestCase):
    # Make sure to test all, before a release

    def setUp(self):
        self.tools = optionstrader.Tools()
        self.scanner = optionstrader.Scanner()
        self.analyzer = optionstrader.Analyzer()

    def tearDown(self):
        return

    @unittest.skip("")
    def test_update_database_command(self):
        # TODO Important.
        # This tool will perform the following functions:
        # --- 1 ---
        results_1 = self.scanner.get_company_information()
        # PASSED
        self.assertTrue(results_1)
        # - Estimated REST API calls: 1 to 3
        # - Downloads company info including stock price
        # --- 2 ---
        # scan_type='inside_out' (or 'outside_in')
        # - inside_out: Scans for option chains for the earliest option expiration date, then goes outwards.
        # Scan start with the AAAA ends with ZZZZ.
        # - outside_in: Scans for option chains for the farthest option expiration date (set limit manually Eg- 6 months out),
        # then goes inwards. Scan start with the AAAA ends with ZZZZ.
        # PASSED
        results_2 = self.scanner.start_option_chain_scan(scan_type='inside_out')
        self.assertTrue(results_2)
        # - Estimated REST API calls: ~3000
        # - Adds option chains to db
        # --- 3 ---
        self.analyzer.analyze_all_option_chains()
        # - Estimated REST API calls: 0
        # - Analyzes the option chains, then updates the db
        # - Can be run in parallel with Steps 1 and 2
        #self.assertTrue(False)
        pass

    @unittest.skip("skipped...")
    def test_command_line_interface(self):
        result = self.tools.start_command_line_interface()
        self.assertTrue(result)

    @unittest.skip("NOT YET PASSED.")
    def test_option_chain_scan_loop(self):
        results = self.scanner.start_option_chain_scan(scan_type='inside_out')
        # Will start when an button is pressed on the command line interface
        #
        # Check to see if the market is open.  If the market is open, then start option scan.
        # If the market isn't open, check to see when the market will be open next.
        # Schedule a 'wait' until the market is open again.  When the market is open again,
        # start the option chain scan again with type 'inside_out' and default to 4 week scan.
        #
        # Main Thread: print "press 'x' to cancel out of the option chain scan loop."
        self.assertTrue(results)

    @unittest.skip("skipped...")
    def test_start_ticker_scanner(self):
        # This is used for obtaining new ticker symbols
        # This will also download company information and update the database
        # if any information is different
        self.assertTrue(False)

    @unittest.skip("skipped...")
    def test_start_option_chain_scan(self):
        # Should complete in less than an hour

        # The person who initially writes the call option is the one who has set the bar for where
        # they think the underlying stock will go by the expiration date

        # We have a problem regarding how often we want to retrieve the stock market price
        # Why?
        # The Stock market underlyer price is not retrieved when the option_chain is retrieved.
        # Why isn't it?
        # This is a very curious one.  I would think that the underlying asset price would be
        # retrieved because the derivatives (options) are based on the price of the underlying asset.
        # The underlying asset is not affected by the derivative prices.
        # We will want to see how many option_chains we can retrieve with each 1 REST call
        #
        # If it's NOT possible to retrieve multiple symbols per REST call:
        # We then have X options:
        # Option 1:
        # We scan all options daily and use the closing price as the price to use in analysis
        #
        # Option 2:
        #


        # Check if it's possible to retrieve option_chains for multiple symbols per 1 REST call
        #
        # If it's possible to retrieve multiple symbols per REST call:

        #
        result = self.scanner.start_options_scan()
        self.assertTrue(result)

    @unittest.skip("skipping...")
    def test_get_recommended_option_purchase(self):
        # TODO Implement a stock ticker blacklist at the recommendation level
        self.assertTrue(False)

    @unittest.skip("NOT YET PASSED.")
    def test_rest_API_endpoint(self):
        # This will be used to test the API endpoint which will be used by the webservice
        # in order to provide data to the website and to other APIs
        # TODO: Handle oauth authentication
        self.assertTrue(False)

    @unittest.skip("NOT YET PASSED.")
    def test_analyze_all_option_chains(self):
        '''
        Moved from test_analyzer.TestAnalyzer.test_analyze_all_option_chains()

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
