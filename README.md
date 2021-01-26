#Optionstrader
The name is not final.
This project will one day be used to analyze the stock market in an open source fashion, so it will need to have a name which allows for the analysis of many markets.

Background
The purpose of this project is to make 1 million dollars.  We will make 1 million dollars distributed into 100 separate accounts each held by different people for the purpose of testing a privatized Universal Basic Income. Each person should invest between $100 and $20,000 and they will be provided with a recommended option chain to purchase, if they so choose, at differing intervals
such as: "As fast as possible (~ Continuously)", "Minutely", "Hourly", "Daily", "Weekly", "Monthly". The average amount of money in all of the accounts must be within a 100% margin of the lowest amount
of money invested on the platform.  The reason for this is because we want to ensure that everyone gets a nice slice of the pie, before anyone goes in for seconds.

Example:
If the first of two investors (1/2) invests $100, then the second of two investors (2/2) will only be able to invest up to $200 (which is 100% of the current average investment [2x]).
If the first investor has a net increase in their investment, then the second investor would be able to invest more money into the system.

Tradier Developer Documentation:
https://developer.tradier.com/documentation

Steps:
1) Extract the option chains available on the major exchanges.
2) Analyze the option chains
  - Magic number for all strike points
  - Store analysis on MySQL server
3) Draw charts
4) Get recommendation on which options to purchase
5) Manual confirmation of the options to purchase
6) Automatic trading system (Near/~ Continuously Trading)

Other things required to complete:
1) Paper trading API (Accounts)
2) Core engine (Eve Module? / REST API module)
3) Webservice (Flask/Django API)
4) Web server (HTML/JS/CSS- Use an automated tool)

Installation
1) run `pip install requirements.txt`
2) configure `config_data_Dev.json` with MySQL database connection Information and Tradier OAuth credentials
3) run the following to set up the database:
```
import optionstrader
db = optionstrader.Database()
db.configure_database()
```
4) Obtain an Oauth access token from the Traider Developer web portal and add the `oauth_access_token` to `config_data_Dev.json`
5) Start the stock scan with the following code:
```
scanner = optionstrader.Scanner()
scanner.start_stock_scan()
```
6) After the stock data is finished, you can start the option chain scan with the following:

```
scanner.start_option_chain_scan(number_of_weeks=4, scan_type='inside_out',
        query_type='default', ticker_array=None)
```


TESTING
To run the unittests, `cd` into the /tests/optionstrader folder and run the following command:

`python unittest -m discover`
