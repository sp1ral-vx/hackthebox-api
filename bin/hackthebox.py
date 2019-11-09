#!/usr/bin/env python3
import sys
import re
import time

from htb.exceptions import HackTheBoxException
from htb.api import HackTheBox
from htb.machines import Machines
# from htb.challenges import Challenges
from htb.shoutbox import Shoutbox
from htb.pusher import Pusher
from htb.views import MachineViews
from htb.cli import HackTheBoxCLI
from htb.colorize import colorize


class HackTheBoxClient(HackTheBox):
    '''HackTheBox Client app.'''
    def __init__(self):
        self.cli = HackTheBoxCLI()
        self._reset_pattern = re.compile(
            r'^([^ ]+) requested a reset on (\w+) \[([^\]]+)\] \[Type /cancel (\d+)'
        )
        self._timeout = 5

    def error(self, message: str):
        '''Error message logger.

        :param str message: error string.
        '''

        print(colorize('red', '[!] {}'.format(message)))
        sys.exit(1)

    def success(self, message: str):
        '''Success message logger.

        :param str message: message string.
        '''

        print(colorize('green', '[!] {}'.format(message)))

    def alert(self, message: str):
        '''Alert message logger.

        :param str message: message string.
        '''

        print(colorize('yellow', '[!] {}'.format(message)))

    def run(self):
        '''Main CLI aggregator.'''

        opts = self.cli.namespace
        if opts.reset:
            self.reset(opts)
        elif opts.flag:
            self.submit_flag(opts)
        elif opts.shout:
            self.shout(opts)
        elif opts.aggressive:
            self.aggressive(opts)
        else:
            self.list(opts)

    def reset(self, opts):
        '''Reset handler.'''

        if not opts.machine_name:
            self.error('Please specify exact machine name')

        machines = Machines()
        machine = machines.get_by_name(opts.machine_name)
        try:
            self.success(machines.reset(machine['id']))
        except HackTheBoxException as e:
            self.error(e)

    def submit_flag(self, opts):
        '''Flag submission handler.'''

        if not opts.machine_name:
            self.error('Please specify exact machine name')
        if opts.difficulty is None:
            self.error('Please specify difficulty')

        machines = Machines()
        machine = machines.get_by_name(opts.machine_name)
        try:
            self.success(
                machines.submit_flag(machine['id'], opts.difficulty, opts.flag)
            )
        except HackTheBoxException as e:
            self.error(e)

    def shout(self, opts):
        '''Shout handler.'''

        shoutbox = Shoutbox()
        result = shoutbox.send(opts.shout)
        self.success(result)

    def _wait_for_reset(self, machine: dict):
        chat = Pusher()
        while True:
            match = chat.match(self._reset_pattern)
            if match:
                self._handle_reset(machine, match)
            chat.flush()
            time.sleep(self._timeout)

    def _handle_reset(self, machine: dict, match: tuple):
        username, machine_name, vpn, reset_id = match
        self.alert('{} requested a reset on {} | {}. Reset id: {}'.format(
            username, machine_name, vpn, reset_id
        ))
        if machine_name == machine['name'] and vpn == 'us-free-1':
            shoutbox = Shoutbox()
            message = shoutbox.send('/cancel {}'.format(reset_id))
            self.success(message)

    def aggressive(self, opts):
        '''Aggressive handler.'''

        if not opts.machine_name:
            self.error('Please specify exact machine name')

        machines = Machines()
        machine = machines.get_by_name(opts.machine_name)
        self.success('Aggressive on {}'.format(machine['name']))
        try:
            self._wait_for_reset(machine)
        except KeyboardInterrupt:
            pass
        except HackTheBoxException as e:
            self.error(e)

    def list(self, opts):
        '''List machines handler.'''

        machines = Machines()
        machines.machines = machines._filter(
            retired=False, owned_user=False, owned_root=False,
        )
        if opts.machine_name:
            machines.machines = machines._filter(name=opts.machine_name)
        print(MachineViews(machines.machines))


if __name__ == '__main__':
    try:
        HTB = HackTheBoxClient()
        HTB.run()
    except HackTheBoxException as e:
        print(e, file=sys.stderr)
        sys.exit(1)
