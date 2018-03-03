import os
import unittest
#import tradier

class TestOptionstrader(unittest.TestCase):
    #@unittest.skip("")
    def test_import_optionstrader(self):
        import optionstrader
        self.assertTrue(True)

    def test_import_optionstrader_account(self):
        import optionstrader
        optionstrader.Account()
        self.assertTrue(True)

    def test_import_optionstrader_account_sub(self):
        import optionstrader
        account = optionstrader.Account()
        account.get_checking_account_balance("123")
        self.assertTrue(True)
