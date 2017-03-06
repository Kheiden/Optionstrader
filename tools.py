from analyzer import Analyzer
from config import Config

class Tools():

    def __init__(self):
        # -----------------------------------------------------------------------------------
        # This file is for the command line tools which can be scheduled as a cron job.
        #
        # All tools which need to be run on a scheduled basis are located in this file too.
        #
        # This is a command line interface for the optionstrader API.
        # The below are in ASC order of completion.  The last ones will be completed last.
        # TODO: Implement a REST API interface for the optionstrader API.
        # TODO: Implement a web service interface on top of the REST API interface
        # TODO: Mark up the HTML/CSS that the web service is service the end user
        # TODO: Design Infrastructure which can handle 10,000 active users
        # TODO: Lawyer up.
        # TODO: Request UX feedback from a small test group of < 20 users (Less Than)
        # -----------------------------------------------------------------------------------

        self.config = Config()
        self.environment = 'staging'

    def start_command_line_interface(self):
        # possible_expiration_dates = self.possible_expiration_dates

        # Major update will add the Negative functionality. For now, we skip.
        # log_msg = "Enter the Maximum percentage change."
        # log_msg = "Use parenthesis () for  negative numbers."
        # log_msg = "Examples:
        # log_msg = "1)`4.0` for positive."
        # log_msg = "2)`(4.0)` for negative."
        # percentage_change_query = input("> ")

        # log_msg = "Input the maximum magic number"
        # magic_number_query = input("> ")

        # Test Examples:
        percentage_change_query = "4.1"
        magic_number_query = "5.54"

        analyzer = Analyzer()
        analyzer_results = analyzer.get_final_analysis(percentage_change=percentage_change_query, magic_number=magic_number_query)
        # Positive Profit
        # analyzer_results.projected_profit = 123.34

        # Negative Profit
        # analyzer_results.projected_profit = (150.00)

        # log_msg = "<best ticker_symbols to purchase options for, listed in descending order > "



        # Ticker Symbol, Percentage Increace, Magic Number, Expiration Date, Projected Profit
        # log_msg = "| ------------- | ------------------- |------------- | --------------- |"
        # log_msg = "| Ticker Symbol | Percentage Increase | Magic Number | Expiration Date |"
        # log_msg = "| ------------- | ------------------- |------------ | --------------- |"
        # log_msg = "| {ticker_symbol} | {percentage_increase} | {magic_number} | {expiration_date} |".format(ticker_symbol=ticker_symbol.rjust(14), percentage_increase=percentage_increase.rjust(19), magic_number=magic_number.rjust(13), expiration_date=expiration_date.rjust(15))
        # log_msg = "| AAPL | 2.5% | {magic_number} | {expiration_date} |".format(ticker_symbol=ticker_symbol.rjust(14), percentage_increase=percentage_increase.rjust(19), magic_number=magic_number.rjust(13), expiration_date=expiration_date.rjust(15))

        return True
