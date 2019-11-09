'''HackTheBox Challanges module.'''
from .api import HackTheBox


class Challenges(HackTheBox):
    '''test'''
    def __init__(self):
        '''Initialize HackTheBox Challanges instance.

        No challanges API?
        Only submit flag and start docker instance by ID.
        '''

        HackTheBox.__init__(self)
        self.challenges = []
