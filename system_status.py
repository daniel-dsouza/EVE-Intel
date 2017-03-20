import datetime
import re

import esi_routes

neutrals_spotted = {'30003230': []}

system_regex = re.compile("[A-Z0-9][A-Z0-9]*-[A-Z0-9][A-Z0-9]*")


def add_intel(system_id):
    if system_id not in neutrals_spotted:
        neutrals_spotted[system_id] = [datetime.datetime.now()]
    else:
        neutrals_spotted[system_id] += [datetime.datetime.now()]


def process_new_intel(intel):
    """
    Processes new intel
    :param intel: list of lines of new intel.
    """
    new_neuts = []
    for line in intel:
        system = system_regex.findall(line)
        if len(system) == 0:
            continue

        system_id = esi_routes.get_system_id(system[0])
        if system_id is None:
            continue

        tokens = line.rstrip().split(" ")
        if 'Bookmark' in tokens:
            continue
        elif 'clr' in tokens or 'clear' in tokens:  # this does not catch 'Clr'...
            neutrals_spotted[system_id] = []
            print("{0} clear".format(system[0]))
            continue

        add_intel(system_id)
        new_neuts.append((system[0], esi_routes.get_jumps(system_id, 30003230)))

    return new_neuts


# def get_newest_neut(jumps):
#     newest_system, newest_delta, now = "", datetime.timedelta(1, 0, 0), datetime.datetime.now()
#     for system, readings in neutrals_spotted.items():
#         if now - v[1] < newest_delta and neutrals_spotted[system] < jumps:
#             newest_delta = now - v[1]
#             newest_system = system
#
#     return newest_system, neutrals_spotted[newest_system], newest_delta

# print(process_new_intel(['[ 2017.03.17 04:28:59 ] spicy indian > Solar System - 1P-QWR\r\n']))
