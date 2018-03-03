#from tradier import core
from ..tradier import core

from ..tradier import http
#import http

from ..config import Config


c = Config()
endpoint = c.get_environment_url()
endpoint_streaming = c.get_environment_url_streaming()

def Tradier(token, endpoint=endpoint,
    endpoint_streaming=endpoint_streaming,
    sessionid=None):
    httpclient = http.std.Client(endpoint)
    # sessionid is only used for streaming api
    httpclient_streaming = http.std.Client(endpoint_streaming)
    return core.Tradier(httpclient, httpclient_streaming, token)

class vanilla(object):
    @classmethod
    def Tradier(klass, h, token, endpoint=endpoint):
        httpclient = http.vanilla.Client(h, endpoint)
        return core.Tradier(httpclient, token)
