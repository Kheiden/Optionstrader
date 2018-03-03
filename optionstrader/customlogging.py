import os
import logging


class CustomLog:
    """
    Used to debug issues with the platform
    """
    def __init__(self):
        log_path = "../logs/dev.log"
        if not os.path.exists(os.path.dirname(log_path)):
            os.makedirs(os.path.dirname(log_path))
        logging.basicConfig(
            filename=os.path.abspath(log_path),
            level=logging.DEBUG,
            format='%(asctime)s %(message)s')

    def debug(self, message):
        logging.debug(message)
        return True

class Analyzed_Ticker_Stream:
    """
    Used to stream the best of the best deals, provided certain parameters
    """

    def __init__(self):
        logging.basicConfig(filename='analyzed_ticker_stream_dev.log',
            level=logging.DEBUG,
            format='%(asctime)s %(message)s')

    def debug(self, message):
        logging.debug(message)
        return True
