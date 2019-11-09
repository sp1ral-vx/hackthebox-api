'''HackTheBox CLI module.'''
import argparse


class HackTheBoxCLI():
    '''HackTheBox CLI class.'''
    def __init__(self):
        '''Initialize HackTheBox CLI instance.'''

        parser = argparse.ArgumentParser(
            description='HackTheBox CLI',
        )

        parser.add_argument(
            '-l',
            default=False,
            action='store_true',
            help='list available machines',
            dest='list_machines',
        )
        parser.add_argument(
            '-n',
            type=str,
            metavar='NAME',
            help='filter machine by name',
            dest='machine_name',
        )
        parser.add_argument(
            '--reset',
            default=False,
            action='store_true',
            help='reset machine',
            dest='reset',
        )
        parser.add_argument(
            '-f', '--flag',
            type=str,
            metavar='flag',
            help='Submit flag',
            dest='flag',
        )
        parser.add_argument(
            '-d',
            type=int,
            metavar='difficulty',
            help='Rate difficulty',
            dest='difficulty',
        )
        parser.add_argument(
            '--shout',
            type=str,
            metavar='message',
            help='Write message to shoutbox',
            dest='shout',
        )
        parser.add_argument(
            '--aggressive',
            default=False,
            action='store_true',
            help='Monitor shoutbox for machine resets and automatically cancel them',
            dest='aggressive',
        )

        self.namespace = parser.parse_args()
