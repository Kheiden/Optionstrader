import unittest

from context import Config

class TestSavefile(unittest.TestCase):
    # Make sure to test all, before a release

    def setUp(self):
        self.logging = True
        self.config = Config()
        '''
        Currently supported config pairs:

        file_dict = {
            'oauth_access_token': str,
            'oauth_access_token_secret': str,
            'timestamp': int,
            'config_file_logging': str,
            'api_url': 'https://sandbox.tradier.com/v1/'
            'environment': 'Dev'
        }


        api_URLs = {
            Sandbox: 'https://sandbox.tradier.com/v1/'
            Production: 'https://api.tradier.com/v1/'
            Streaming: 'https://stream.tradier.com/v1/'
            Beta: 'https://api.tradier.com/beta/'
        }
        '''

    def tearDown(self):
        pass


    @unittest.skip("PASSED.")
    def test_load_from_file(self):
        file_dict_comparison = {
            'oauth_access_token': 'oauth_access_token123123',
            'oauth_access_token_secret': 'oauth_access_token_secret123123'
        }
        file_dict = self.config.load_from_file()
        self.assertIn(file_dict['oauth_access_token'], 'oauth_access_token123123')
        self.assertIn(file_dict['oauth_access_token_secret'], 'oauth_access_token_secret123123')

    @unittest.skip("PASSED.")
    def test_add_new_config_to_file(self):
        config_key = 'environment'
        config_value = 'Dev'
        config_pair = {config_key: config_value}
        config_result = self.config.add_new_config_pair_to_file(config_pair)

        self.assertIn(config_key, config_result.keys())
        self.assertIn('timestamp', config_result.keys())

    @unittest.skip("PASSED.")
    def test_remove_config_from_file(self):
        config_key = '<No Longer Exists>'
        config_value = True
        config_pair = {config_key: config_value}
        config_result = self.config.remove_config_from_file(config_pair)

        self.assertNotIn(config_key, config_result.keys())
        self.assertIn('timestamp', config_result.keys())
