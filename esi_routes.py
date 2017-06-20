import requests

from evethings import character

system_ids = {'BQO-UU': '30003230'}
jumps = {}
ship_ids = {}
counte = 0

BASE_URL = "https://esi.tech.ccp.is/latest/"


def get_system_id(system_name):
    """
    Looks up a system in the ESI api, returns none if not found.
    :param system_name: the 6 character system name.
    :return: the system_id according to the API
    """
    if system_name in system_ids:
        return system_ids[system_name]

    params = {
        'categories': 'solarsystem',
        'datsource': 'tranquility',
        'language': 'en-us',
        'search': system_name
    }
    r = requests.get(BASE_URL + 'search/', params=params)
    if r.status_code == requests.codes.ok and 'solarsystem' in r.json():
        system_ids[system_name] = str(r.json()['solarsystem'][0])
        return system_ids[system_name]


def get_jumps(origin, destination):
    """
    Get the number of jumps between systems.
    :param origin: system_id of the origin system
    :param destination: system_id of the destination system
    :return: the number of jumps between the two systems (same as lookup the route in game)
    """
    if (origin, destination) in jumps:
        return jumps[(origin, destination)]

    uri = 'https://esi.tech.ccp.is/latest/route/{0}/{1}/?datasource=tranquility'.format(origin, destination)  # add flag shortest?
    r = requests.get(uri)
    if r.status_code == requests.codes.ok:
        count = len(r.json()) - 1
        jumps[(origin, destination)] = count
        jumps[(destination, origin)] = count
        return count


def get_ship_id(ship_name):
    """
    Get the item_id of a ship from the name
    :param ship_name: 
    :return: the smallest ID for the ship
    """
    if ship_name in ship_ids:
        return ship_ids[ship_name]

    params = {
        'categories': 'inventorytype',
        'datasource': 'tranquility',
        'language': 'en-us',
        'search': ship_name,
        'strict': 'true'
    }
    r = requests.get(BASE_URL + 'search/', params=params)
    if r.status_code == requests.codes.ok and 'inventorytype' in r.json():
        ship_ids[ship_name] = min(r.json()['inventorytype'])
        return ship_ids[ship_name]


def get_character_id(character_name):
    """
    Get the character id from the name
    :param character_name: the name
    :return: the ID
    """
    global counte
    if character_name in character.character_ids:
        return character.character_ids[character_name]

    counte = counte + 1
    # print(counte, character_name)

    params = {
        'categories': 'character',
        'datasource': 'tranquility',
        'language': 'en-us',
        'search': character_name,
        'strict': 'true'
    }
    r = requests.get(BASE_URL + 'search/', params=params)
    if r.status_code == requests.codes.ok and 'character' in r.json():
        character.character_ids[character_name] = r.json()['character']
        return r.json()['character'][0]


def get_partial_character_id(partial_name):
    if len(partial_name) < 3:
        raise Exception(partial_name + " is not longer than 3")

    params = {
        'categories': 'character',
        'datasource': 'tranquility',
        'language': 'en-us',
        'search': partial_name,
        'strict': 'false'
    }
    r = requests.get(BASE_URL + 'search/', params=params)
    if r.status_code == requests.codes.ok and 'character' in r.json():
        return r.json()['character']

    raise Exception("'character' not found in JSON")


def bulk_character_lookup(ids):
    # print(ids)
    r = requests.post('https://esi.tech.ccp.is/latest/universe/names/?datasource=tranquility', json=ids)
    if r.status_code == requests.codes.ok and 'error' not in r.json():
        return r.json()

    raise Exception("'character' not found in JSON")


def get_latest_stable_release():
    """
    Get the latest release of the bot.
    :return: the semver of the latest executable
    """
    r = requests.get("https://api.github.com/repos/daniel-dsouza/eve-bot/releases/latest")
    return r.json()['tag_name']

