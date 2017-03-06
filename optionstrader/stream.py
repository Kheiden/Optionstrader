from tradier import Tradier

from config import Config
from customlogging import CustomLog
from database import Database

class Stream():

    def __init__(self):
        self.config = Config()
        self.log = CustomLog()
        self.database = Database()
        self.access_token = self.config.get_access_token()

    def get_streaming_session_id(self):
        self.session = Tradier(self.access_token)
        results = self.session.streams.auth()
        sessionid =  results
        log_msg = sessionid
        self.log.debug("***Session id: {0}".format(log_msg))
        return True

    def get_tradier_stream_no_sessid(self):
        self.session = Tradier(self.access_token)
        results = self.session.streams.start_stream(['FB'])

    #def get_tradier_stream(self, sessionid=sessionid):
    #    self.session = Tradier(self.access_token, sessionid=sessionid)
    #    results = self.session.streams.start_stream(['FB'])

    def get_test_stream(self, stream_type='symbols_only', num_chains_limit=5):
        """
        # I'll use this to simulate a datastream using data from the database
        # datastream_connected # Bool
        # datastream_disconnected # Bool

        # This will stream 1 second or less of ticker information
        # This is NOT a persistant connection
        # returns a generator
        # Calling .next() on the generator will retrieve the streamable item

        `stream_type` is used to denote
        `num_chains_limit`
        """


        if stream_type == 'symbols_only':
            # Note: num_chains_limit does not apply here.
            list_of_tickers = self.database.get_list_of_tickers()
            datastream_generator = (i for i in list_of_tickers)
            return datastream_generator

        if stream_type == 'option_chains':
            list_of_option_chains = self.database.get_example_option_chains(num_chains_limit)
            datastream_generator = (i for i in list_of_option_chains)
            return datastream_generator

        if stream_type == 'option_chains_sorted':

            option_chains_msql_buffered_dict = self.database.query_option_chains_for_analysis(
        			ticker=None)

            #

            # Uncomment below to see the SQL query
            #self.log.debug("***** {0}".format(option_chains_msql_buffered_dict))
            #datastream_generator = (i for i in option_chains_msql_buffered_dict)
            # Returning a dictionary instead of the generator object to save resources
            return option_chains_msql_buffered_dict

        else:
            self.log.debug("ERROR: stream_type not specified, defaulting to 'symbols_only'")
            # Note: num_chains_limit does not apply here.
            list_of_tickers = self.database.get_list_of_tickers()
            datastream_generator = (i for i in list_of_tickers)
            return datastream_generator
