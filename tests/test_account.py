import unittest
from context import account


class TestAccount(unittest.TestCase):
    # Make sure to test all, before a release

    def setUp(self):
        self.account = account.Account()

    def tearDown(self):
        return

    @unittest.skip("skipping...")
    def test_create_new_account(self):
        results = self.account.create_new_account
        self.assertTrue(results)

    def test_get_balance(self):
        self.account.get_balance()
