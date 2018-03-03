import unittest
from context import optionstrader

class TestAccount(unittest.TestCase):
    # Make sure to test all, before a release

    def setUp(self):
        self.account = optionstrader.Account()
        self.log = optionstrader.CustomLog()

    def tearDown(self):
        return

    @unittest.skip("Passed.")
    def test_create_new_account(self):
        account_type = 'checking'
        initial_deposit = 10000.50

        results = self.account.create_new_account(
            account_type=account_type,
            initial_deposit=initial_deposit
        )

        self.assertTrue(results)

    @unittest.skip("Passed.")
    def test_get_balance(self):
        account_number = '537166657303428193258'
        account_type = 'checking'
        balance = self.account.get_balance(
            account_number=account_number,
            account_type=account_type
        )

        self.log.debug('Account number: {0}, Balance: {1}'.format(account_number, balance))

    @unittest.skip("skipping...")
    def test_create_new_account_no_collisions(self):
        # TODO Implement later
        # make sure that account_number collisions are impossible
        # This logic should probably be implemented inside the account.create_new_account
        # method.
        self.assertTrue(False)
