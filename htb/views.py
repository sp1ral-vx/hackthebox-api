'''HackTheBox Views module.'''
from prettytable import PrettyTable
from htb.colorize import colorize


class MachineViews():
    '''HackTheBox MachineViews class.'''
    def __init__(self, machines: list):
        '''Initialize view instance for machines.'''

        self.table = PrettyTable()
        self.machines = machines

        self.table.field_names = [
            'Name',
            'IP',
            'Difficulty',
            'Rating',
            'Owns',
            'Release Date',
        ]
        self.table.align['Name'] = 'l'
        self.table.align['IP'] = 'l'
        self.table.align['Difficulty'] = 'l'

    def _name(self, machine: dict) -> str:
        return colorize('green', machine['name'])

    def _ip(self, machine: dict) -> str:
        return colorize('cyan', machine['ip'])

    def _difficulty(self, machine: dict) -> str:
        word = ''
        if machine['points'] <= 20:
            word = colorize('green', 'Easy')
        elif machine['points'] <= 30:
            word = colorize('yellow', 'Medium')
        elif machine['points'] <= 40:
            word = colorize('red', 'Hard')
        elif machine['points'] > 40:
            word = colorize('lightred', u'\u27c1 Insane')
        return word

    def _rating(self, machine: dict) -> str:
        return machine['rating']

    def _owned(self, machine: dict) -> str:
        user = colorize('red', u'\u2717')
        root = colorize('red', u'\u2717')

        if machine['owned_user']:
            user = colorize('green', u'\u2713')
        if machine['owned_root']:
            root = colorize('green', u'\u2713')

        return f'{user}  {root}'

    def _release(self, machine: dict) -> str:
        return machine['release']

    def __str__(self):
        for machine in self.machines:
            self.table.add_row([
                self._name(machine),
                self._ip(machine),
                self._difficulty(machine),
                self._rating(machine),
                self._owned(machine),
                self._release(machine),
            ])
        return str(self.table)
