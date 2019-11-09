'''HackTheBox Machines module.'''
from .exceptions import HackTheBoxException
from .api import HackTheBox


class Machines(HackTheBox):
    '''HackTheBox Machines class.'''
    def __init__(self):
        '''Initialize HackTheBox Machines instance.'''

        HackTheBox.__init__(self)
        self.machines = []
        self.owns = []
        self.load()
        self.get_owns()
        self._combine_owns()

    def load(self) -> list:
        '''Loads complete list of machines.'''

        if not self.machines:
            self.machines = self.request(endpoint='/api/machines/get/all').json()
        return self.machines

    def get_owns(self) -> list:
        '''Find owned machines.'''

        if not self.owns:
            self.owns = self.request(endpoint='/api/machines/owns').json()
        return self.owns

    def get_by_id(self, machine_id: int) -> dict:
        '''Find machine by ID.

        :param int machine_id: Machine ID.
        :rtype: dict
        '''

        machines = self._filter(id=machine_id)
        if len(machines) != 1:
            raise HackTheBoxException('Machine not found')
        return self.get(machines[0]['id'])

    def get_by_name(self, machine_name: str) -> dict:
        '''Find machine by name.

        :param str machine_name: Machine name.
        :rtype: dict
        '''

        machines = self._filter(name=machine_name)
        if len(machines) != 1:
            raise HackTheBoxException('Machine not found')
        return self.get(machines[0]['id'])

    def get_by_ip(self, ipaddr: str) -> dict:
        '''Find machine by IP address.

        :param str ipddr: Machine IP address.
        :rtype: dict
        '''

        machines = self._filter(ip=ipaddr)[0]
        if len(machines) != 1:
            raise HackTheBoxException('Machine not found')
        return self.get(machines[0]['id'])

    def get(self, machine_id: int) -> dict:
        '''Load full information about machine.

        :param int machine_id: Machine ID.
        :rtype: dict
        '''

        return self.request(endpoint='/api/machines/get/{:d}/'.format(machine_id)).json()

    def _filter(self, **kwargs: dict) -> list:
        '''Filter machine list.

        :param int  id        : Machine ID.
        :param str  name      : Machine name.
        :param str  os        : Machine OS.
        :param bool retired   : Machine retired status.
        :param bool owned_user: Machine has been owned (user).
        :param bool owned_root: Machine has been owned (root).
        :rtype: list
        '''

        search = self.machines
        for field in kwargs:
            if field not in self.machines[0].keys():
                raise HackTheBoxException('Invalid search filter: {}'.format(kwargs))
            search = list(filter(
                lambda machine, field=field: machine[field] == kwargs[field], search
            ))
        return search

    def _combine_owns(self) -> list:
        '''Add `owned_user` and `owned_root` properties for each machine in scope.

        HackTheBox API doesn't provide owns information by machine ID or
        other filter.
        '''

        owns = self.get_owns()
        own_ids = [_['id'] for _ in owns]

        notsolved = {'owned_user': False, 'owned_root': False}
        for i, machine in enumerate(self.machines):
            if machine['id'] not in own_ids:
                self.machines[i] = {**machine, **notsolved}
                continue
            k = [i for i, _ in enumerate(owns) if _['id'] == machine['id']][0]
            self.machines[i] = {**machine, **owns[k]}
        return self.machines

    def reset(self, machine_id: int) -> str:
        '''Reset machine by ID.

        :param int machine_id: Machine ID.
        :rtype: str
        '''

        message = self.request(
            method='POST', endpoint='/api/vm/reset/{:d}'.format(machine_id)
        ).json()
        if not int(message['success']):
            return message['output']
        return '{}. [{:d}/{:d}].'.format(message['output'], message['used'], message['total'])

    def submit_flag(self, machine_id: int, difficulty: int, flag: str) -> str:
        '''Submit flag for machine.

        :param int machine_id: Machine ID.
        :param int difficulty: Difficulty in range of [1; 10].
        :param str flag      : Machine flag.
        :rtype: str
        '''

        if not 1 <= difficulty <= 10:
            raise HackTheBoxException('Difficulty should be in range [1; 10]')

        flag = flag.strip()
        if len(flag) != 32:
            raise HackTheBoxException(
                'Incorrect flag format ({:d} of {:d} bytes)'.format(len(flag), 32)
            )

        message = self.request(method='POST', endpoint='/api/machines/own', data={
            'flag': flag,
            'difficulty': difficulty * 10,
            'id': machine_id,
        }).json()
        # success = bool(int(message['success'], 10))
        text = message['status']
        return text
