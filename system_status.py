import datetime
import re

import esi_routes as esi
import log_reader

neutrals_spotted = {'30003230': []}

system_regex = re.compile("[A-Z0-9][A-Z0-9]*-[A-Z0-9][A-Z0-9]*")


class Intel(object):
    def __init__(self, message, timestamp=None, sender=None):
        self.eve_timestamp = timestamp
        self.sender = sender
        self.raw_message = message

        systems = system_regex.findall(message)
        self.system_name = systems[0] if len(systems) != 0 else None
        self.system_id = esi.get_system_id(self.system_name) if self.system_name else None

        tokens = self.raw_message.split(' ')
        self.clear = 'clr' in tokens or 'clear' in tokens


class IntelParser(object):
    def __init__(self, game_channels):
        self.systems = {}
        self.intel_channels = log_reader.LogReader(game_channels, '\Documents\EVE\logs\Chatlogs')
        # self.intel_channels = log_reader.LogReader(game_channels, '/Documents/EVE/logs/Chatlogs')

    def start(self):
        log_reader.start_observer()

    def process_new_intel(self, manual=None):
        briefcase = []
        raw = self.intel_channels.read_logs() if manual is None else manual

        if raw is None:
            return

        for line in raw:
            intel = Intel(
                message=line[line.find(' > ')+3:],
                timestamp=line[line.find(' [ ')+3: line.find(' ] ')],
                sender=line[line.find(' ] ')+3: line.find(' > ')]
            )
            if intel.system_id is not None:
                briefcase.append(intel)

        return briefcase

    def reset(self):
        raise NotImplementedError


class System(object):
    def __init__(self, home_system):
        self.home_system_name = home_system
        self.home_system_id = esi.get_system_id(home_system)
        self.neutrals = {}
        self.new_neutrals = []

    def add_intel(self, intel):
        self.new_neutrals = []
        for entry in intel:
            jumps = esi.get_jumps(entry.system_id, self.home_system_id)
            if jumps <= 100:
                self.new_neutrals.append((entry, jumps))

        return self.new_neutrals

    def nearest_neutral(self, jumps):
        raise NotImplementedError

    def newest_neutrals(self, jumps):
        raise NotImplementedError


if __name__ == '__main__':
    bq = System('BQO-UU')
    de = IntelParser(["The Drone Den", "Obliteroids", "oba"])

    raw = [
        '[ 2017.03.22 22:08:56 ] spicy indian > ok',
        '[ 2017.03.18 10:01:35 ] Andrei Nikitin > BY-7PY* Tiranda',
        '[ 2017.03.18 09:31:48 ] Line chef > MN9P-A  clr DU'
    ]
    intel = de.process_new_intel(raw)
    ne = bq.add_intel(intel)
    [print(i[0].system_name + str(i[1])) for i in ne]

    # try:
    #     while True:
    #         intel = de.process_new_intel(['[ 2017.03.22 22:08:56 ] spicy indian > ok'])
    #         print(intel)
    # except KeyboardInterrupt as e:
    #     pass
