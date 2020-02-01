import json
import time
import datetime

from context import optionstrader

import unittest

class TestScript(unittest.TestCase):
    """
    DEPRICATED.  Please use 'optionstrader.tools.Tools' for any methods related to this Class.

    # Make sure to test all, before a release

    # Read the README.md for more information
    # Developer Documentation:
    # https://developer.tradier.com/documentation    """





    def setUp(self):
        self.w = optionstrader.Webservice()
        self.d = optionstrader.Database()
        self.savefile = optionstrader.Savefile()
        self.scanner = optionstrader.Scanner()
        # Get from Tradier
        self.access_token = ""
        # Get from Tradier
        self.access_token_secret = ""
        # Sandbox is `self.environment_url="https://sandbox.tradier.com/v1/"`
        # Production is `self.environment_url = "https://api.tradier.com/v1/"`
        self.environment_url = "https://sandbox.tradier.com/v1/"

        self.access_token = "JmIr55aKnCmigEeEsClRnUvMtPEK"

        self.endpoint = 'staging'

        self.chain_test_date = self.get_next_friday_date()



    def tearDown(self):
        pass


    @unittest.skip("NOT YET STARTED.")
    def test_start_script(self):
        # TODO
        # create a stand-alone file (tools.py) which starts the option_chain scan.  It needs to be schedulable via cron.
        #
        # default to stage environment.


        # Important parts to remember:
        # obtain the option_chain for each company listed on the exchange.
        # Analyze the volume, ask, and bid price for each strikepoint available.
        # Compare this with the current stock price
        # The difference will show where investors think that the market is going (by the provided expiration_date)

        pass


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~ CURRENTLY TESTING ~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    unittest.main()
