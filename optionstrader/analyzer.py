# -*- coding: UTF-8 -*-
import math
import time
import queue

import threading

from multiprocessing import Pool, TimeoutError

from optionstrader.database import Database
from optionstrader.config import Config
from optionstrader.customlogging import CustomLog
from optionstrader.customlogging import Analyzed_Ticker_Stream

class Analyzer:

    def __init__(self):
        self.database = Database()
        self.config = Config()
        self.log = CustomLog()
        self.log_analysis = Analyzed_Ticker_Stream()
        self.minimum_contract_cost_threshold = self.config.get_minimum_contract_cost_threshold()
        # config

        # Max number of option chains to analyze, per symbol
        self.max_num_option_chains = 500
        # About 3.5 days in seconds = 302400
        self.option_chain_timestamp_threshold = 300000
        self.db_update_queue = queue.Queue()

    # Decorator to time each method
    # Will be used for future optimization
    def timeit(method):
        def timed(*args, **kw):
            ts = time.time()
            result = method(*args, **kw)
            ticker = args[1]
            te = time.time()
            completion_time_ms = round(te-ts, 4)*1000
            completion_time_mcs = round(te-ts, 4)*1000000
            avg_one_option_analyzed_time = -1
            if result is -1:
                log_msg = "Warning: Wasting resources.  Symbol '{ticker}' does not have option chains.".format(ticker=ticker)
                log = CustomLog()
                log.debug(log_msg)
                return result

            if result is not -1: avg_one_option_analyzed_time = completion_time_mcs / result
            log_msg = "Completed in {completion_time_ms} ms - analyzer.{0}(ticker='{ticker}'). Avg 1 option scanned in {avg_one_option_analyzed_time} microseconds".format(
                method.__name__,
                completion_time_ms=completion_time_ms,
                ticker=ticker,
                avg_one_option_analyzed_time=avg_one_option_analyzed_time)
            log = CustomLog()
            log.debug(log_msg)
            return result

        return timed

    def save_to_db(self):
        queue_item = self.db_update_queue.get()
        log_msg = queue_item
        return log_msg

    def start_db_update_queue_workers(self):
        processes = 10
        pool = Pool(processes)
        log_msg = "TESTING"
        self.log.debug(log_msg)
        log_msg = "Starting pool of {} processes".format(processes)
        self.log.debug(log_msg)
        result = pool.apply_async(self.save_to_db)
        self.log.debug(log_msg)
        return True


    def get_final_analysis(self, percentage_change, magic_number):
        # We want to return the results for each possible_expiration_dates
        # Example: We want to return the results of the provided parameters for
        # the week of 02/17/2017 and for the week of 02/24/2017, if
        # possible_expiration_dates had only those two dates in it.
        return

    def sanitize_stock_price(self, symbol):
        # TODO
        # Implement later
        # I'll use this function to ensure that the stock price is not widly
        # above or below the current stock price.
        stock_price = self.database.get_current_stock_price(symbol)
        return stock_price


    def analyze_all_option_chains(self):
        # There's two ways to analyze all option chains
        # - inside_out: Scans for option chains for the earliest option expiration date, then goes outwards.
        # Scan start with the AAAA ends with ZZZZ.
        # - outside_in: Scans for option chains for the farthest option expiration date (set limit manually Eg- 6 months out),
        # then goes inwards. Scan start with the AAAA ends with ZZZZ.

        # We will later want the ability to prioritize the scan of the option chains of specific companies.

        # We need to speed up this process by 2 orders of magnitude.
        # Goal: 1.65 sec for maximum_number_of_option_chains=10, option_chain_timestamp_threshold=30000
        list_of_tickers = self.database.get_list_of_tickers(query_type='options_only')
        log_msg = "Number of DISTINCT symbols to analyze: {0}".format(len(list_of_tickers))



        for ticker in list_of_tickers:
            self.analyze_all_option_chains_for_ticker(ticker)

        return True

    @timeit
    def analyze_all_option_chains_for_ticker(self, ticker, *args):

        current_timestamp = int(time.time())
        time_threshold = self.option_chain_timestamp_threshold
        max_num_option_chains = self.max_num_option_chains

        # Improve efficiency here
        option_chains = self.database.query_option_chains_for_analysis(ticker,
            current_timestamp,
            time_threshold,
            max_num_option_chains)

        num_option_chains = len(option_chains)

        log_msg = "{0} chains for symbol '{1}', time_threshold : {2}, max_num_option_chains : {3}".format(
            num_option_chains,
            ticker,
            time_threshold,
            max_num_option_chains)
        self.log.debug(log_msg)
        # Improve efficiency here
        result = self.analyze_option_chains(option_chains)

        if num_option_chains <= 0: return -1

        # returning the num_option_chains so that performance can be tuned.
        return num_option_chains
        #except:
        #    log_msg = "ERROR Processing option_chain for ticker {0}".format(ticker)
        #    return False


    def async_analyze_option_chains(self, option_chains):

        return


    def analyze_option_chains(self, option_chains):
        # option_chains is a list of all option chains for a given ticker,
        # soreted by timestamp in descending order




        # Spawn a new thread
        #while option_chains
        #for option_chain in option_chains:
            #pass
        option_chain_queue = queue.Queue()

        for option_chain in option_chains:
            option_chain_queue.put(option_chain)

        while option_chain_queue.qsize() > 0:
            max_number_threads = 16
            for i in range(max_number_threads):
                thread = threading.Thread(target=self.async_analyze_option_chains, args=(option_chain_queue.get(),))
                thread.start()
            # All 8 threads have completed the job
            break
        return False



        for option_chain in option_chains:
            result = self.analyze_single_option_chain(option_chain)
            if result == False:
                # There was an error analyzing option chain 'option_chain'
                log_msg = "Error! There was an error analyzing option chain "
                self.log.debug(log_msg)
                # Change later
                raise SyntaxError
                return False

        # main thread
        # poll to ensure that the other threads are executing properly


        return True

    def analyze_single_option_chain(self, option_chain):
        # Currently using the ask price for the option chain in analysis
        #log_msg = "type(option_chain) : {}".format(type(option_chain))

        # First analyze for each percentage Increase
        # Then analyze examples for each number contracts array




        # We want to make sure that the 'last_' price is within reason.  We don't want to
        # pay 100x the average price of the item.
        symbol = option_chain['underlying']

        #self.log.debug("SYMBOL: {}".format(symbol))
        current_stock_price = self.sanitize_stock_price(symbol)
        #self.log.debug("current_stock_price: {}".format(current_stock_price))
        # strike_price = float(option_chain['strikePrice'])
        strike_price = option_chain['strike']

        #log_msg = "Strike Price: {}".format(option_chain['strike'])


        # for calulating the price per contract, we should take into consideration both the bid and the ask
        price_per_contract_bid = float(option_chain['bid'])
        price_per_contract_ask = float(option_chain['ask'])

        #log_msg = "price_per_contract_bid: {}".format(price_per_contract_bid)
        #log_msg = "price_per_contract_ask: {}".format(price_per_contract_ask)


        # iterate for each of these thresholds
        stock_price_increase_total = [1.0, 1.5, 2.0, 2.25, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

        for stock_price_increase in stock_price_increase_total:
            percentage_increase_analysis = {}

            percentage_increase_analysis['timestamp'] = time.time()
            #log_msg = "timestamp: {}".format(time.time())
            percentage_increase_analysis['expiration_date'] = option_chain['expiration_date']

            percentage_increase_analysis['symbol'] = symbol
            #log_msg = "symbol: {}".format(symbol)

            percentage_increase_analysis['stock_price_increase'] = stock_price_increase
            #log_msg = "stock_price_increase: {}".format(stock_price_increase)


            stock_exercise_price = current_stock_price * (1 + (float(stock_price_increase)/100))
            percentage_increase_analysis['stock_exercise_price'] = stock_exercise_price
            #log_msg = "stock_exercise_price: {}".format(stock_exercise_price)
            #log_msg = stock_exercise_price

            theoretical_commission_fees = 0.35 * math.pow(3,33)
            contract_price_per_share = stock_exercise_price - strike_price
            if contract_price_per_share < 0:
                contract_price_per_share = 0

            # This is the potential value of the contract near the expiration date.
            # This is the price that the option should be sold at
            percentage_increase_analysis['contract_price_per_share'] = contract_price_per_share
            #log_msg = "contract_price_per_share: {}".format(contract_price_per_share)

            # This is the price per contract that the analysis was performed at
            # This is how much the user should buy the contract for
            percentage_increase_analysis['price_per_contract_ask'] = price_per_contract_ask
            #magic_number = contract_price_per_share
            try:
                magic_number = ((contract_price_per_share * math.pow(3,33)) - ((price_per_contract_ask * math.pow(3,33))-(theoretical_commission_fees)))/(price_per_contract_ask * math.pow(3,33))
            except:
                magic_number = -100

            percentage_increase_analysis['magic_number'] = magic_number
            #log_msg = "magic_number: {}".format(magic_number)
            # Potential Profit

            percentage_increase_analysis['strike_price'] = strike_price
            #log_msg = "strike_price: {}".format(strike_price)


            number_contracts_array = [1, 10, 100]
            for total_number_of_contracts in number_contracts_array:
                #log_msg = "---"
                #total_number_of_contracts = 1
                total_number_of_shares = total_number_of_contracts * 100
                total_price_paid = price_per_contract_ask * total_number_of_shares

                percentage_increase_analysis['total_price_paid_{0}x'.format(total_number_of_contracts)] = total_price_paid
                #log_msg = "total_price_paid_{0}x: {1}".format(total_number_of_contracts, total_price_paid)

                if (0.35 * total_number_of_contracts) < self.minimum_contract_cost_threshold:
                    total_commission_cost = 5.00
                else:
                    total_commission_cost = 0.35 * total_number_of_contracts

                if ((price_per_contract_ask * total_number_of_shares) - total_price_paid - total_commission_cost) > 0:
                    potential_profit = 0
                else:
                    potential_profit = (contract_price_per_share * total_number_of_shares) - total_price_paid - total_commission_cost

                percentage_increase_analysis['potential_profit_{0}x'.format(total_number_of_contracts)] = potential_profit
                #log_msg = "potential_profit_{0}x : {1}".format(total_number_of_contracts, potential_profit)
                try:
                    risk_percentage =  round((total_price_paid / potential_profit) * 100, 2)
                except:
                    risk_percentage = -100.0

                percentage_increase_analysis['risk_percentage_{0}x'.format(total_number_of_contracts)] = risk_percentage
                #log_msg = "risk_percentage_{0}x : {1}".format(total_number_of_contracts, risk_percentage)

            # uncomment below for all percentage_increase
            #log_msg = "------------------"
            #log_msg = percentage_increase_analysis

            # update database
            # TODO
            #self.add_to_db_update_queue(percentage_increase_analysis)
            self.database.update_option_chain_with_analysis(percentage_increase_analysis)
            # percentage_increase_analysis is the variable used to determine if the choice is good or not
            #self.log.debug("percentage_increase_analysis:")
            #self.log.debug(percentage_increase_analysis)
            # Uncommenting until further testing has been done.  TODO finish this part.
            # TODO finish the analysis part
            #self.get_recommended_option_purchase(percentage_increase_analysis)
        return True

    def get_recommended_option_purchase(self, percentage_increase_analysis):
        # There is similar code in the database.py module
        # This is used for analyzing the datastream to check if an option_chain
        # meets certain criteria for a "good" match
        #self.log.debug("Checking percentage_increase_analysis...")

        if (0 <= percentage_increase_analysis['total_price_paid_1x'] <= 100) == False:
            return None
        if (50 <= percentage_increase_analysis['potential_profit_1x'] <= 100) == False:
            return None
        if (0 <= percentage_increase_analysis['stock_price_increase'] <= 3.5) == False:
            return None
        if (3 <= percentage_increase_analysis['magic_number'] <= 10) == False:
            return None
        if (0 <= percentage_increase_analysis['risk_percentage_1x'] <= 18) == False:
            return None

        # If the option_chain has made it through this tribunal, I want to know about it
        #
        self.log.debug("Preferred Analysis Detected in percentage_increase_analysis!")
        self.log.debug("Sending details to analysis log...")
        self.log_analysis.debug("PREFERRED ANALYSIS DETECTED".center(50, "-"))
        self.log_analysis.debug(percentage_increase_analysis)
        return percentage_increase_analysis




    def add_to_db_update_queue(self, percentage_increase_analysis):
        #self.database.update_option_chain_with_analysis(percentage_increase_analysis)
        self.db_update_queue.put(percentage_increase_analysis)
        return True
