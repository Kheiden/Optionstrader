import logging

import unittest

from customlogging import CustomLog

class Testcustomlogging(unittest.TestCase):
    # Make sure to test all, before a release

    def setUp(self):
        self.log = CustomLog()
        return

    def tearDown(self):
        return

    @unittest.skip("PASSED")
    def test_log_example(self):
        msg = "TESTING..."
        #logging.debug(msg)
        result = self.log.debug(msg)
        self.assertTrue(result)
