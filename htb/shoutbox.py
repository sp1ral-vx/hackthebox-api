'''HackTheBox Shoutbox module.'''
from .api import HackTheBox


class Shoutbox(HackTheBox):
    '''HackTheBox Shoutbox class.'''
    def __init__(self):
        '''Initialize HackTheBox Shoutbox instance.'''

        HackTheBox.__init__(self)

    def send(self, message: str) -> str:
        '''Send message to HackTheBox chat.

        :param str message: text message.
        :rtype: str
        '''

        shout = self.request(
            method='POST', endpoint='/api/shouts/new/', data={'text': message}
        ).json()
        # success = bool(int(shout['success'], 10))
        text = ''
        if 'text' in shout:
            text = shout['text']
        elif 'output' in shout:
            text = shout['output']
        return text

    def recv(self, message_id: int) -> str:
        '''Receive message from HackTheBox chat by ID.

        :param int message_id: Message ID.
        :rtype: str
        '''
        shout = self.request(
            method='POST', endpoint='/api/shouts/get/single/{:d}'.format(message_id)
        ).json()
        # success = bool(int(shout['success'], 10))
        text = shout['shout']
        return text
