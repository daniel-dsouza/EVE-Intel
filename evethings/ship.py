from os import path

import esi_routes as esi

file_path = path.dirname(__file__)
with open(path.join(file_path, 'shiplist.dat')) as file:
    ships = set([item.rstrip().lower() for item in file.readlines()])


def is_ship(ship_string):
    """
    Returns True if a string names a ship
    :param ship_string: something that may be a ship
    :return: True if a ship
    """
    return True if ship_string.lower() in ships else False


class Ship(object):
    def __init__(self, ship_name=None, ship_id=None):
        self.name, self.objectID = ship_name, ship_id
        assert ship_name or ship_id
        if ship_name and is_ship(ship_name):
            self.objectID = esi.get_ship_id(ship_name)
        else:
            raise NotImplementedError
