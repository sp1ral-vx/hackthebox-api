'''HackTheBox API wrapper.'''
import sys
import os
import requests
from .exceptions import HackTheBoxException


class HackTheBox():
    '''HackTheBox API wrapper.'''
    def __init__(self):
        '''Initialize HackTheBox instance.'''

        self.set_key(os.getenv('HTB_API_KEY', None))
        if not self._key:
            raise HackTheBoxException('Please set HTB API key to your environ')

        self.api = requests.Session()
        self.api.headers = {
            'User-Agent'     : 'hackthebox-client/0.0.1a',
            'Authorization'  : 'Bearer {}'.format(self._key),
            'Accept-Encoding': 'gzip, deflate',
            'Accept'         : 'application/json',
            'Connection'     : 'Close',
        }
        self.url = 'https://www.hackthebox.eu'

    def set_key(self, key: str):
        '''Set HTB API key.

        :param str key: secret API key.
        '''
        self._key = key

    def request(self, **kwargs: dict) -> requests.models.Response:
        '''Requests wrapper for HackTheBox API.

        :param str endpoint: The path of endpoint API.
        :param dict **kwargs:
            See `requests.request` documentation

        :rtype: requests.models.Response
        '''

        if 'method' not in kwargs:
            kwargs['method'] = 'GET'
        if 'url' not in kwargs and kwargs['endpoint']:
            kwargs['url'] = '{}/{}'.format(self.url, kwargs['endpoint'])
            del kwargs['endpoint']
        try:
            return self.api.request(**kwargs)
        except Exception as e:
            print(e, file=sys.stderr)
            sys.exit(1)
