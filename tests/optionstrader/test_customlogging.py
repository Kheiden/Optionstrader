import logging

import unittest
from unittest import mock

from context import optionstrader

class Testcustomlogging(unittest.TestCase):
    # Make sure to test all, before a release

    def setUp(self):
        self.log = optionstrader.CustomLog()
        return

    def tearDown(self):
        return

    @mock.patch.object(optionstrader, 'CustomLog')
    def test_log_example(self, custom_log_mock):
        msg = "TESTING..."
        #logging.debug(msg)
        result = self.log.debug(msg)
        self.assertTrue(result)
