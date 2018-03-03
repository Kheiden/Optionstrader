import timeit

import unittest
from context import optionstrader

class TestAccountDatabase(unittest.TestCase):
    def log_start(method):
        def __init__(*args, **kwargs):
            log = optionstrader.CustomLog()
            msg = "STARTING UNITTEST".center(100, "-")
            log.debug(msg)
            msg = "Elapsed Time: {0:.10f}".format(0.0)
            return method(*args, **kwargs)
        return __init__

    def log_end(method):
        def __init__(*args, **kwargs):
            log = optionstrader.CustomLog()
            msg = "UNITTEST COMPLETE".center(100, "-")
            log.debug(msg)
            return method(*args, **kwargs)
        return __init__

    @log_start
    def setUp(self):
        return

    @log_end
    def tearDown(self):
        pass



class TestDatabase(unittest.TestCase):
    # Make sure to test all, before a release
    def log_start(method):
        def __init__(*args, **kwargs):
            log = optionstrader.CustomLog()
            msg = "STARTING UNITTEST".center(100, "-")
            log.debug(msg)
            msg = "Elapsed Time: {0:.10f}".format(0.0)
            return method(*args, **kwargs)
        return __init__

    def log_end(method):
        def __init__(*args, **kwargs):
            log = optionstrader.CustomLog()
            msg = "UNITTEST COMPLETE".center(100, "-")
            log.debug(msg)
            return method(*args, **kwargs)
        return __init__


    @log_start
    def setUp(self):
        self.config = optionstrader.Config()
        self.database = optionstrader.Database()
        self.log = optionstrader.CustomLog()
        self.webservice = optionstrader.Webservice()

    @log_end
    def tearDown(self):
        pass

# ---------------------------------------- TESTING ----------------------------------------


# ---------------------------------------- SKIPPING ----------------------------------------
    @unittest.skip("NOT YET PASSED.")
    def test_add_option_chain_to_database(self):
        expiration_date = self.webservice.get_option_chain_next_expiration_date()
        example_option_chain = self.webservice.get_example_option_chain(self.config.get_environment_url, expiration_date)
        result = self.database.save_option_chain_to_database(example_option_chain)

        self.assertTrue(result)

    @unittest.skip("NOT YET PASSED...")
    def test_get_single_example_option_chain(self):
        output = self.database.get_single_example_option_chain()
        log_msg = output
        self.assertTrue(output)

    @unittest.skip("NOT YET PASSED.")
    def test_query_option_chains_for_analysis(self):
        """
        time_threshold is set to 300k because it's been a while since I've analyzed option_chains
        """
        cursor = self.database.query_option_chains_for_analysis(time_threshold=300000)

        # We want to preprocess the datastream, so that we don't waste CPU resourses on database calls
        option_chain_dict = cursor.fetchall()

        self.log.debug(option_chain_dict)
        self.assertTrue(option_chain_dict)

    @unittest.skip("NOT YET PASSED")
    def test_get_recommended_option_purchase_array(self):
        results_table = self.database.get_recommended_option_purchase()
        log_msg = results_table
        # They should be similar in timestamp, so their expiration should be the sanitized_field_name
        # TODO Implement a method for the below functionality
        log_msg = "Recommended Option Chains for {0}:".format(results_table[0][16])
        log_msg = "------------------------------------------------------"
        for column in results_table:
            log_msg = "Symbol: {0} potential_profit_1x: {1}".format(column[6], column[11])
        #for i in array:
        #    log_msg = i
        self.assertTrue(array)

# ----------------------------------------- PASSED -----------------------------------------
    @unittest.skip("PASSED.")
    def test_parse_symbols_and_add_to_db(self):
        result = self.database.parse_symbols_and_add_to_db()
        self.assertTrue(result)

    @unittest.skip("PASSED.")
    def test_create_database(self):
        database_name = "algotrader_dev"
        created = self.database.create_database(database_name)
        self.assertTrue(created)

    @unittest.skip("PASSED")
    def test_configure_database(self):
        result = self.database.configure_database()
        self.assertTrue(result)

    @unittest.skip("PASSED.")
    def test_get_list_of_tickers(self):
        # 0.56 for 10 tests
        #time_results = timeit.timeit(self.database.get_list_of_tickers(), number=1)
        # 1 test 0.126 sec. Goal 1 test: 0.00126
        # 10 tests 1.441 sec. Goal 10 tests: X / 100 = 0.01441
        num_tests = 10

        for i in range(num_tests):
            list_of_tickers = self.database.get_list_of_tickers()
            self.assertEqual(len(list_of_tickers), 3078)
        #self.assertTrue(time_results < 10)
        self.log.debug("Completed {} tests".format(num_tests))

    @unittest.skip("PASSED.")
    def test_type_conversion(self):
        self.assertEqual(self.database.type_conversion("hi_there"), "text")
        self.assertEqual(self.database.type_conversion(1.0), "float")
        self.assertEqual(self.database.type_conversion(None), "text")
        self.assertEqual(self.database.type_conversion(10), "bigint(20)")
