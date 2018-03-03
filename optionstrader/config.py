import os
import json
import time

from optionstrader.customlogging import CustomLog

class Config:

    def __init__(self):
        '''
        Used to control the saving/loading process for all of the configurations

        Example below:

        file_dict = {
            'oauth_access_token': 'oauth_access_token123123',
            'timestamp': '1234567890',
            ...,
            'oauth_access_token_secret': 'oauth_access_token_secret123123'
        }

        '''

        # Environment Choices:
        # - "Dev"
        # - "Stage"
        # - "Production"
        self.environment = "Dev"
        self.log = CustomLog()
        directory_path = os.path.dirname(os.path.realpath(__file__))
        self.file_location = directory_path + "/config_data/config_data_{env}.json".format(env=self.environment)

    def save_to_file(self, file_dict):
        # obj_dict is related to authentication credentials
        #oauth_access_token = obj_dict['oauth_access_token']
        #oauth_access_token_secret = obj_dict['oauth_access_token_secret']
        try:
            for iteration, key in enumerate(file_dict.keys()):
                file_dict[key] = file_dict.values()[iteration]
        except:
            log_msg = "ERROR. Saving to file"

        file_dict['timestamp'] = int(time.time()) - 10 # Subtract a few seconds, as a buffer
        with open(self.file_location, "w") as data_file_obj:
            data_file_obj.write(json.dumps(file_dict))
        print("config.py_.save_to_file : file_dict Saved to {0}".format(self.file_location))
        return True

    def load_from_file(self):
        file_location = "/Users/kheiden/Desktop/algotrader/config_data.json"
        with open(self.file_location, "r") as data_file_obj:
            obj_str = data_file_obj.read()
        file_dict = json.loads(obj_str)
        try:
            if file_dict['config_file_logging'] == 'True':
                msg = "config.py_.load_from_file : file_dict Loaded from {0}".format(self.file_location)
                log_msg = msg
                self.log.debug(msg)
        except:
            log_msg = ""
            log_msg = "`config_file_logging` parameter not set in config.py"
        return file_dict

    def add_new_config_pair_to_file(self, config_pair):
        # Only 1 config value at a time
        file_dict = self.load_from_file()
        file_dict[list(config_pair.keys())[0]] = list(config_pair.values())[0]
        self.save_to_file(file_dict)
        # returns file_dict if successful
        return file_dict

    def remove_config_from_file(self, config_pair):
        # Only 1 config value at a time
        file_dict = self.load_from_file()
        try:
            del file_dict[list(config_pair.keys())[0]]
            if file_dict['config_file_logging'] == 'True':
                msg = "{0} removed from file_dict Loaded from {1}".format(list(config_pair.keys())[0], self.file_location)
                log_msg = msg
                self.log.debug(msg)
        except:
            if file_dict['config_file_logging'] == 'True':
                log_msg = ""
                log_msg = "ERROR: {0} unable to be removed from file_dict Loaded from {1}".format(list(config_pair.keys())[0], self.file_location)
        self.save_to_file(file_dict)
        # returns file_dict if successful
        return file_dict

    def get_config_item(self, config_item):
        file_dict = self.load_from_file()
        config_item = file_dict[config_item]
        return config_item

    def get_minimum_contract_cost_threshold(self):
        config_item = self.get_config_item('minimum_contract_cost_threshold')
        return config_item

    def get_environment(self):
        config_item = self.get_config_item('environment')
        return config_item

    def get_environment_url(self):
        config_item = self.get_config_item('api_url')
        return config_item

    def get_environment_url_streaming(self):
        config_item = self.get_config_item('api_url_streaming')
        return config_item

    def get_access_token(self):
        config_item = self.get_config_item('oauth_access_token')
        return config_item
