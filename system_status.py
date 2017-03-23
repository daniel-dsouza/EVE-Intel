import datetime
import re

import esi_routes as esi
import log_reader

neutrals_spotted = {'30003230': []}

system_regex = re.compile("[A-Z0-9][A-Z0-9]*-[A-Z0-9][A-Z0-9]*")


class IntelParser(object):
    def __init__(self, game_channels):
        self.systems = {}
        self.intel_channels = log_reader.LogReader(game_channels, '\Documents\EVE\logs\Chatlogs')

    def start(self):
        log_reader.start_observer()

    def process_new_intel(self, manual=None):
        briefcase = []
        raw = self.intel_channels.read_logs() if manual is None else manual
        for line in raw:
            systems = system_regex.findall(line)
            if len(systems) == 0:
                continue
            system_id = esi.get_system_id(systems[0])
            if system_id is None:
                continue

            intel = {
                'eve_timestamp': line[line.find(' [ ')+3: line.find(' ] ')],
                'sender': line[line.find(' ] ')+3: line.find(' > ')],
                'message': line[line.find(' > ')+3:],
                'system_name': systems[0],
                'system_id': system_id
            }
            tokens = intel['message'].split(' ')
            intel['clear'] = 'clr' in tokens or 'clear' in tokens

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
        return "i am bacon"

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
    [print(i) for i in intel]

    # try:
    #     while True:
    #         intel = de.process_new_intel(['[ 2017.03.22 22:08:56 ] spicy indian > ok'])
    #         print(intel)
    # except KeyboardInterrupt as e:
    #     pass


# def add_intel(system_id):
#     if system_id not in neutrals_spotted:
#         neutrals_spotted[system_id] = [datetime.datetime.now()]
#     else:
#         neutrals_spotted[system_id] += [datetime.datetime.now()]
#
#
# def process_new_intel(intel):
#     """
#     Processes new intel
#     :param intel: list of lines of new intel.
#     """
#     new_neuts = []
#     for line in intel:
#         system = system_regex.findall(line)
#         if len(system) == 0:
#             continue
#
#         system_id = esi_routes.get_system_id(system[0])
#         if system_id is None:
#             continue
#
#         tokens = line.rstrip().split(" ")
#         if 'Bookmark' in tokens:
#             continue
#         elif 'clr' in tokens or 'clear' in tokens:  # this does not catch 'Clr'...
#             neutrals_spotted[system_id] = []
#             print("{0} clear".format(system[0]))
#             continue
#
#         add_intel(system_id)
#         new_neuts.append((system[0], esi_routes.get_jumps(system_id, 30003230)))
#
#     return new_neuts


# def get_newest_neut(jumps):
#     newest_system, newest_delta, now = "", datetime.timedelta(1, 0, 0), datetime.datetime.now()
#     for system, readings in neutrals_spotted.items():
#         if now - v[1] < newest_delta and neutrals_spotted[system] < jumps:
#             newest_delta = now - v[1]
#             newest_system = system
#
#     return newest_system, neutrals_spotted[newest_system], newest_delta

# print(process_new_intel(['[ 2017.03.17 04:28:59 ] spicy indian > Solar System - 1P-QWR\r\n']))
