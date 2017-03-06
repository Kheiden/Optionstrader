import json

from ..customlogging import CustomLog

class Tradier(object):
    def __init__(self, httpclient, httpclient_streaming, token):
        self.httpclient_streaming = httpclient_streaming
        self.streams = Tradier.Streams(self)

        self.httpclient = httpclient
        self.token = token
        self.user = Tradier.User(self)
        self.accounts = Tradier.Accounts(self)
        self.markets = Tradier.Markets(self)
        self.fundamentals = Tradier.Fundamentals(self)
        self.options = Tradier.Options(self)
        self.watchlists = Tradier.Watchlists(self)

    def request_streaming(
            self,
            method,
            path,
            headers=None,
            params=None,
            data=None,
            callback=None):

        log_msg = "callback", callback

        headers = headers or {}
        headers['Authorization'] = 'Bearer %s' % self.token
        headers['Accept'] = 'application/json'

        def base_callback(response):
            if response.code != 200:
                raise Exception(response.code, response.body)
            return json.loads(response.body)

        if callback == None:
            cb = base_callback
        else:
            cb = lambda x: callback(base_callback(x))

        log_msg = cb # <function <lambda> at 0x10a620b18>
        log_msg = method # GET/POST
        log_msg = path # markets/events/session
        log_msg = headers # {'Accept': 'application/json', 'Authorization': u'Bearer JmIr55aKnCmigEeEsClRnUvMtPEK'}
        log_msg = params # None
        log_msg = data # None

        return self.httpclient_streaming.request(
            cb,
            method,
            path,
            headers=headers,
            params=params,
            data=data)


    def request(
            self,
            method,
            path,
            headers=None,
            params=None,
            data=None,
            callback=None):

        headers = headers or {}
        headers['Authorization'] = 'Bearer %s' % self.token
        headers['Accept'] = 'application/json'

        def base_callback(response):
            if response.code != 200:
                raise Exception(response.code, response.body)
            return json.loads(response.body)

        if callback == None:
            cb = base_callback
        else:
            cb = lambda x: callback(base_callback(x))

        log_msg = cb # <function <lambda> at 0x10a620b18>
        log_msg = method # GET
        log_msg = path # markets/events/session
        log_msg = headers # {'Accept': 'application/json', 'Authorization': u'Bearer JmIr55aKnCmigEeEsClRnUvMtPEK'}
        log_msg = params # None
        log_msg = data # None

        return self.httpclient.request(
            cb,
            method,
            path,
            headers=headers,
            params=params,
            data=data)

    class Streams(object):
        # TESTING
        def __init__(self, agent):
            self.log = CustomLog()
            self.agent = agent

        def auth(self):
            # Get the sessionid required for connecting to the stream
            results = self.agent.request('POST', 'markets/events/session')
            self.log.debug("Results: ".center(10, "-"))
            self.log.debug(results)

            return results['stream']['sessionid'].encode()

        def start_stream(self, symbols):
            def callback(response):
                quote = response['quotes'].get('quote', [])
                if not isinstance(quote, list):
                    quote = [quote]
                return quote
            # We're getting a stream with a POST
            sessionid = self.auth()
            log_msg = sessionid
            response = self.agent.request_streaming(
                'POST',
                'markets/events',
                params= \
                {
                    'sessionid': sessionid,
                    'symbols': ','.join(x.upper() for x in symbols),
                    'filter': 'quote'
                },
                callback=callback)
            return response

    class User(object):
        def __init__(self, agent):
            self.agent = agent

        def profile(self):
            response = self.agent.request('GET', 'user/profile')
            return response

        def balances(self):
            response = self.agent.request('GET', 'user/balances')
            return response

    class Accounts(object):
        def __init__(self, agent):
            self.agent = agent

        def orders(self, account_id):
            response = self.agent.request(
                'GET', 'accounts/%s/orders' % account_id)
            return response['orders']['order']

        def order(self, account_id, order_id):
            response = self.agent.request(
                'GET', 'accounts/%s/orders/%s' % (account_id, order_id))
            return response

    class Markets(object):
        def __init__(self, agent):
            self.agent = agent

        def quotes(self, symbols):
            def callback(response):
                quote = response['quotes'].get('quote', [])
                if not isinstance(quote, list):
                    quote = [quote]
                return quote
            return self.agent.request(
                'GET',
                'markets/quotes',
                params={'symbols': ','.join(symbols)},
                callback=callback)

    class Fundamentals(object):
        def __init__(self, agent):
            self.agent = agent

        def calendars(self, symbols):
            def callback(response):
                return response
            return self.agent.request(
                'GET',
                'markets/fundamentals/calendars',
                params={'symbols': ','.join(x.upper() for x in symbols)},
                callback=callback)

    class Options(object):
        def __init__(self, agent):
            self.agent = agent

        def expirations(self, symbol):
            return self.agent.request(
                'GET',
                'markets/options/expirations',
                params={'symbol': symbol},
                callback=(lambda x: x['expirations']['date']))

        def chains(self, symbol, expiration):
            def callback(response):
                if response['options']:
                    return response['options']['option']
                return []
            return self.agent.request(
                'GET',
                'markets/options/chains',
                params={'symbol': symbol, 'expiration': expiration},
                callback=callback)

    class Watchlists(object):
        def __init__(self, agent):
            self.agent = agent

        def __call__(self):
            response = self.agent.request('GET', 'watchlists')
            return response['watchlists']['watchlist']

        def get(self, watchlist_id):
            response = self.agent.request(
                'GET', 'watchlists/%s' % watchlist_id)
            return response['watchlist']

        def create(self, name, *symbols):
            response = self.agent.request(
                'POST',
                'watchlists',
                params={'name': name, 'symbols': ','.join(list(symbols))})
            return response['watchlist']

        def delete(self, watchlist_id):
            response = self.agent.request(
                'DELETE', 'watchlists/%s' % watchlist_id)
            return response['watchlists']['watchlist']
