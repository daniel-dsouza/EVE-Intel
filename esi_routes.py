import requests

system_ids = {'BQO-UU': '30003230'}
jumps = {}


def get_system_id(system_name):
    if system_name in system_ids:
        return system_ids[system_name]

    uri = 'https://esi.tech.ccp.is/latest/search/?categories=solarsystem&datasource=tranquility&language=en-us&search=' + system_name
    r = requests.get(uri)
    if r.status_code == requests.codes.ok:
        system_ids[system_name] = str(r.json()['solarsystem'][0])
        return system_ids[system_name]


def get_jumps(origin, destination):
    if (origin, destination) in jumps:
        return jumps[(origin, destination)]

    uri = 'https://esi.tech.ccp.is/latest/route/{0}/{1}/?datasource=tranquility'.format(origin, destination)  # add flag shortest?
    r = requests.get(uri)
    if r.status_code == requests.codes.ok:
        count = len(r.json()) - 1
        jumps[(origin, destination)] = count
        jumps[(destination, origin)] = count
        return count
