import unittest

from context import stream
from context import customlogging

class TestStream(unittest.TestCase):

    def log_start(method):
        def __init__(*args, **kwargs):
            log = customlogging.CustomLog()
            msg = "STARTING UNITTEST".center(100, "-")
            log.debug(msg)
            return method(*args, **kwargs)
        return __init__

    def log_end(method):
        def __init__(*args, **kwargs):
            log = customlogging.CustomLog()
            msg = "UNITTEST COMPLETE".center(100, "-")
            log.debug(msg)
            return method(*args, **kwargs)
        return __init__

    @log_start
    def setUp(self):
        self.stream = stream.Stream()
        self.log = customlogging.CustomLog()

    @log_end
    def tearDown(self):
        return

    def test_get_tradier_stream(self):
        """
        Currently blocked by Tradier.
        Tradier only provides streaming services within their Production capacity.

        I will need to use their Production environment to feed data to my
        Dev/Stage/Prod environments

        """


        #sessionid = self.stream.get_streaming_session_id()
        self.log.debug("**sessionid obtained.  Starting the Stream...")
        results = self.stream.get_tradier_stream_no_sessid()
        self.log.debug(results)
        self.assertTrue(results)

    @unittest.skip("PASSED.")
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
