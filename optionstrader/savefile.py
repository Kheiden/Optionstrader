import json

class Savefile:

    def __init__(self):
        '''
        DEPRICATED, use config.py instead
        '''

        self.file_location = "/Users/kheiden/Desktop/algotrader/auth_data.json"

    def save_to_file(self, obj_dict):
        # obj_dict is related to authentication credentials
        #oauth_access_token = obj_dict['oauth_access_token']
        #oauth_access_token_secret = obj_dict['oauth_access_token_secret']
        obj_dict['timestamp'] = int(time.time()) - 10 # Subtract a few seconds, as a buffer
        with open(self.file_location, "w") as data_file_obj:
            data_file_obj.write(json.dumps(obj_dict))
        print("obj_dict Saved to {0}".format(file_location))
        return True

    def load_from_file(self):
        file_location = "/Users/kheiden/Desktop/algotrader/auth_data.json"
        with open(self.file_location, "r") as data_file_obj:
            obj_str = data_file_obj.read()
        obj_dict = json.loads(obj_str)
        #obj_dict = {
        #    'oauth_access_token': 'oauth_access_token123123',
        #    'oauth_access_token_secret': 'oauth_access_token_secret123123'
        #}
        print("obj_dict Loaded from {0}".format(file_location))
        return obj_dict
