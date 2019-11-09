'''HackTheBox pusher.com API module.'''
import re
import warnings
import json

import pysher
from bs4 import BeautifulSoup

PUSHER_APP_ID = '97608bf7532e6f0fe898'
PUSHER_APP_CLUSTER = 'eu'


class Pusher():
    '''HackTheBox pusher.com class.'''
    def __init__(self):
        '''Initialize HackTheBux pusher.com API instance.'''

        warnings.filterwarnings('ignore', category=UserWarning, module='bs4')
        self.pusher = pysher.Pusher(PUSHER_APP_ID, PUSHER_APP_CLUSTER)
        self.pusher.connection.bind('pusher:connection_established', self.connect_handler)
        self.pusher.connect()
        self.channels = {
            'notifications-channel': None,
            'shoutbox-channel'     : None,
            'infobox-channel'      : None,
            'VPN-us-free-1'        : None,
            'VPN-eu-free-1'        : None,
            'owns-channel'         : None,
        }
        self.events = []

    # def display(self):
    #     for event in self.events:
    #         print('@ {!r}'.format(event))
    #     if len(self.events):
    #         print('-' * 20)

    def match(self, pattern: re.Pattern) -> list:
        '''Find pattern in pusher events.

        :param re.pattern pattern: regexp.
        :rtype: list
        '''

        for event in self.events:
            match = pattern.search(event)
            if match:
                return match.groups()
        return []

    def flush(self):
        '''Flush pusher events.'''

        self.events = []

    def log(self, *args):
        '''Log pusher events.

        :param list event: event.
        '''

        self.events.append(args[2])

    def connect_handler(self, data: str):
        '''Connection handler for pusher.

        :param str data: connection-event.
        '''

        for name in self.channels:
            self.channels[name] = self.pusher.subscribe(name)
            self.channels[name].bind('display-shout', self.shout)
            self.channels[name].bind('display-info', self.info)
            self.channels[name].bind('display-notification', self.notification)

    def _unhtml(self, html: str) -> str:
        '''HTML sanitizer.

        :param str html: HTML string.
        :rtype: str
        '''

        return BeautifulSoup(html, features='html5lib').text

    def shout(self, message: str):
        '''Shoutbox channel handler.

        :param str message: Message from channel.
        '''

        message = json.loads(message)

        name = message['name']
        text = self._unhtml(message['text'])
        text = '{}: {}'.format(name, text)
        self.log('shout', name, text)

    def info(self, message: str):
        '''Info channel handler.

        :param str message: Message from channel.
        '''

        message = json.loads(message)

        channel = message['channel']
        text = self._unhtml(message['text'])
        self.log('info', channel, text)

    def notification(self, message: str):
        '''Notification channel handler.

        :param str message: Message from channel.
        '''

        message = json.loads(message)

        server = message['server']
        text = self._unhtml(message['text'])
        self.log('notification', server, text)
