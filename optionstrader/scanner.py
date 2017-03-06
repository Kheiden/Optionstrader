import time

from database import Database
from webservice import Webservice
from config import Config
from customlogging import CustomLog
from analyzer import Analyzer

class Scanner:

    def __init__(self):
        self.database = Database()
        self.webservice = Webservice()
        self.config = Config()
        self.analyzer = Analyzer()
        # Example option chain (First in the )
        self.example_ticker = self.database.get_list_of_tickers()[0]
        self.next_timestamp_request_available = time.time()
        # Add this to the config later
        self.number_requests_per_second = 1.0
        self.log = CustomLog()


    def process_option_chain(self, option_chain):
        #log_msg = "Starting self.database.save_option_chain_to_database..."
        #self.log.debug(log_msg)
        #time.time()
        # Uncomment below
        results_save = self.database.save_option_chain_to_database(option_chain)
        #time.time()
        #log_msg = "Starting self.analyzer.analyze_single_option_chain..."
        #self.log.debug(log_msg)
        results_analyze = self.analyzer.analyze_single_option_chain(option_chain)
        return results_save, results_analyze


    def traider_call_get_option_chains(self, environment_url, ticker, expiration_date):

        self.log.debug("Getting all all_option_chains for ticker '{}'".format(ticker))
        all_option_chains = self.webservice.get_option_chain_for_ticker(environment_url, ticker, expiration_date)

        # TODO Time this to make sure that it's optimal.  Set optimization goal.
        # Implement later: Send this to a separate thread for processing

        count_all_option_chains = len(all_option_chains)
        log_msg = "Saving {0} option chain(s) to database then analyzing and saving analysis to db...".format(
            count_all_option_chains)
        self.log.debug(log_msg)

        time_start = time.time()
        iteration_heartbeat_threshold = 10
        for iteration, option_chain in enumerate(all_option_chains):
            results_save, results_analyze = self.process_option_chain(option_chain)

            if iteration % iteration_heartbeat_threshold == 0:
                if iteration > 0:
                    # Current processing speed: ~ 1.6 option chains per second.
                    # Goal processing speed: 1600 option chains per second
                    log_msg = "Saved 10 option chains to database.  Saved Analysis to db. Remaining: {0}. Avg Processing Speed: {1} option chains per second".format(
                        count_all_option_chains - iteration,
                        iteration/(time.time()-time_start))
                    self.log.debug(log_msg)
            else:
                pass


        if results_save:
            log_msg = "All {0} option chains which expire on {1} for Ticker {2} added to db".format(len(all_option_chains), expiration_date, ticker)
        if results_analyze:
            log_msg = "All {0} Analysis of option chains which expire on {1} for Ticker {2} been added to db".format(len(all_option_chains), expiration_date, ticker)
        else:
            log_msg = "ERROR: results_1: '{}', results_2: '{}'".format(results_save, results_analyze)

        self.log.debug(log_msg)

        return True


    def start_option_chain_scan(self, number_of_weeks=4, scan_type='inside_out',
            query_type='options_only', ticker_array=None):
        # TODO Change the variable names
        search_direction = scan_type
        db_query_type = query_type
        # This code will start the option scan for all tickers currently available
        # at the next expiration_date
        # TODO
        # Friendly reminder that options expire on the Saturday following the option expiration date
        environment_url = self.config.get_environment_url


        expiration_date_array = []
        """
        `query_type` is the type of database query that the scanner will use for the list_of_tickers

        list_of_tickers can either originate from an external method via the parameter ticker_array
        or it could originate from a database SQL call
        """

        if ticker_array is None:
            list_of_tickers = self.database.get_list_of_tickers(query_type)
        else:
            list_of_tickers = ticker_array


        if scan_type == 'next_week_only':
            expiration_date_array.append(self.webservice.get_option_chain_expiration_date_after_next())
        if scan_type == 'current_week_only':
            expiration_date_array.append(self.webservice.get_option_chain_next_expiration_date())
        if scan_type == 'inside_out':
            expiration_date_array = self.webservice.get_option_chain_expiration_date_for_timeperiod(number_of_weeks, search_direction)
        else:
            expiration_date_array.append(self.webservice.get_option_chain_expiration_date_after_next())
            log_msg = "Warning. 'scan_type' not specified, defaulting to {}".format(expiration_date_array)
            self.log.debug(log_msg)


        log_msg = "Scanning {0} week(s) worth of option chain expiration dates for {1} companies.".format(len(expiration_date_array), len(list_of_tickers))
        self.log.debug(log_msg)
        num_exp_date = 0

        """
        This method uses expiration_date_array before list_of_tickers.
        """

        for expiration_date in expiration_date_array:
            log_msg = "{0} Remaining week(s) worth of option chain expiration dates to scan.".format(
                len(expiration_date_array) - num_exp_date)
            self.log.debug(log_msg)

            for ticker in list_of_tickers:
                self.traider_call_get_option_chains(environment_url, ticker, expiration_date)
                log_msg = "Option Chains analyzed for ticker: {0}".format(ticker)
                self.log.debug(log_msg)

            num_exp_date += 1

            #expiration_date_array.pop()

        return True

    def chunks(self, l, n):
        n = max(1, n)
        return (l[i:i+n] for i in xrange(0, len(l), n))

    def start_stock_scan(self):
        list_of_tickers = self.database.get_list_of_tickers()
        for ticker_chunk in self.chunks(list_of_tickers, 1000):
            chunk_stock_data = self.webservice.get_market_quote_for_ticker(self.config.get_environment_url, ticker_chunk)
            for single_stock_data in chunk_stock_data:
                self.database.save_option_chain_to_database(single_stock_data)
                log_msg = "Ticker has been added to database: {}".format(single_stock_data['symbol'])
                self.log.debug(log_msg)
            log_msg = len(chunk_stock_data)
        return True

    def get_company_information(self):
        list_of_tickers = self.database.get_list_of_tickers()
        for ticker_chunk in self.chunks(list_of_tickers, 1000):
            chunk_stock_data = self.webservice.get_company_information_for_ticker(self.config.get_environment_url, ticker_chunk)
            for single_stock_data in chunk_stock_data:
                self.database.save_option_chain_to_database(single_stock_data)
                #log_msg = "Ticker has been added to database: {}".format(single_stock_data['symbol'])
            msg = "first {0} symbols complete".format(len(chunk_stock_data))
            self.log.debug(msg)
        return True


    def scan_single_option_chain(self):
        option_chain = self.webservice.get_option_chain_for_ticker(self.example_ticker)
        return option_chain

    def get_single_option_chain(self, option_chain):
        single_result = scan_single_option(self.example_ticker)
        try:
            save_result_to_database(single_result)
        except:
            return False
        #       # Fail for now
        #       # Later, check if there is:
        #       #   - a connection issue to the db
        #       #   - extra fields in the option_scan result
        #
        return True
