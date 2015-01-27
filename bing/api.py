""" Pyhton API client for Bing Webmaster Tools

Method description: https://msdn.microsoft.com/en-us/library/jj572365.aspx
API Reference: https://msdn.microsoft.com/en-us/library/hh969386.aspx

"""
import httplib2
import json
try:
    import socks
except ImportError:
    socks = None
from urllib import urlencode

__author__    = "Karoly 'Charles' Nagy"
__copyright__ = "Copyright 2015, Karoly Nagy"
__licence__   = "GPL"
__version__	  = "0.0.1"
__contact__   = "dr.karoly.nagy@gmail.com"

API_KEY = 'YOUR-API-KEY'


class BingWebmasterApi(object):

    def __init__(self, api_key=None, timeout=3, proxy=None):
        self.api_key = api_key or API_KEY
        self.endpoint = 'https://www.bing.com/webmaster/api.svc/json/'
        if proxy:
            if socks:
                if not (isinstance(proxy, tuple) or isinstance(proxy, list)):
                    proxy = proxy.replace('http://', '').split(':')
                _proxy_info = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, proxy[0], int(proxy[-1]))
            else:
                raise ImportError('You need socks module to use proxy. Please run `pip install PySocks`')
        else:
            _proxy_info = None
        self.h = httplib2.Http("/tmp/.cache", timeout=timeout, proxy_info=_proxy_info)

    def __getattr__(self, item):
        def call(**kwargs):
            kwargs.update({
                'apikey': self.api_key
            })
            _uri = '{endpoint}{function}?{query}'.format(
                endpoint=self.endpoint,
                function=item,
                query=urlencode(kwargs)
            )
            resp, content = self.h.request(_uri, 'GET')
            if not resp.status == 200:
                if resp.status == 404:
                    raise BingMethodNotImplemented('Method does not exists!')
                elif resp.status == 400:
                    _c = json.loads(content)
                    _ec = _c.get('ErrorCode')
                    if _ec == 8:
                        raise BingInvalidParameter('Invalid parameter given to %s function.' % item)
                    elif _ec == 14:
                        raise BingAuthorizationError('Not authorized.')
                raise BingError('Unknown error occured [status code: %d] with response: %s' % (resp.status, content))
            else:
                return json.loads(content)

        return call