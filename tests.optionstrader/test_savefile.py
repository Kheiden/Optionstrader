import unittest

class TestSavefile(unittest.TestCase):
    '''
    DEPRICATED, Use test_config.py instead
    '''

    def setUp(self):
        return

    def tearDown(self):
        pass

    @unittest.skip("SKIPPING.")
    def test_save_to_file(self):
        obj_dict = {
            'oauth_access_token': 'oauth_access_token123123',
            'oauth_access_token_secret': 'oauth_access_token_secret123123'
        }
        test_result = self.savefile.save_to_file(obj_dict)
        self.assertTrue(test_result)

    @unittest.skip("SKIPPING.")
    def test_load_from_file(self):
        obj_dict_2 = {
            'oauth_access_token': 'oauth_access_token123123',
            'oauth_access_token_secret': 'oauth_access_token_secret123123'
        }
        obj_dict = self.savefile.load_from_file()
        self.assertEqual(obj_dict, obj_dict_2)
