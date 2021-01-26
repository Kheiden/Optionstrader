import optionstrader
db = optionstrader.Database()
db.configure_database()

scanner = optionstrader.Scanner()
# scanner.start_stock_scan()
scanner.start_option_chain_scan(query_type='default')
