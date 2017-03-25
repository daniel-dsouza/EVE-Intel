import requests

system_ids = {'BQO-UU': '30003230'}
jumps = {}


def get_system_id(system_name):
    """
    Looks up a system in the ESI api, returns none if not found.
    :param system_name: the 6 character system name.
    :return: the system_id according to the API
    """
    if system_name in system_ids:
        return system_ids[system_name]

    uri = 'https://esi.tech.ccp.is/latest/search/?categories=solarsystem&datasource=tranquility&language=en-us&search=' + system_name
    r = requests.get(uri)
    if r.status_code == requests.codes.ok:
        try:
            system_ids[system_name] = str(r.json()['solarsystem'][0])
            return system_ids[system_name]
        except KeyError:
            print('no system ' + system_name)
            return None


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
