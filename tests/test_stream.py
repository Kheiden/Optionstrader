import unittest

from stream import Stream
from customlogging import CustomLog

class TestStream(unittest.TestCase):

    def log_start(method):
        def __init__(*args, **kwargs):
            log = CustomLog()
            msg = "STARTING UNITTEST".center(100, "-")
            log.debug(msg)
            return method(*args, **kwargs)
        return __init__

    def log_end(method):
        def __init__(*args, **kwargs):
            log = CustomLog()
            msg = "UNITTEST COMPLETE".center(100, "-")
            log.debug(msg)
            return method(*args, **kwargs)
        return __init__

    @log_start
    def setUp(self):
        self.stream = Stream()
        self.log = CustomLog()

    @log_end
    def tearDown(self):
        return

    #@unittest.skip("PASSED.")
    def test_get_test_stream(self):
        datastream_generator = self.stream.get_test_stream(stream_type='option_chains_exp')
        # results should be a datastream_generator

        first_generator_item = datastream_generator.next()

        self.log.debug("Database Query: ".format(datastream_generator))
        self.log.debug("First response from query: '{0}'".format(
            first_generator_item))

        self.assertTrue(first_generator_item)
        self.assertTrue(datastream_generator)


    @unittest.skip("NOT YET PASSED.")
    def test_get_streaming_session_id(self):
        # first get a streaming sessionid
        # then get the stream

        sessionid = self.stream.get_streaming_session_id()
        results = self.stream.get_stream(sessionid)
        self.assertTrue(results)
