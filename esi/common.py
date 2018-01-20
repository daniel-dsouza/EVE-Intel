import aiohttp

from esi.character import Character
from esi.ship import Ship
from esi.system import System


BASE_URL = "https://esi.tech.ccp.is/latest/"
session = None

name_dict = {}
objectID_dict = {}


def get_session():
    return session


async def universe_names_to_ids(names):
    """
    This function is used to cache names locally.
    In most cases, this will make the request faster
    :param names: a list of names we want IDs for
    :return: dict of name: (id, category)
    """
    result = {}
    query = []
    names = map(str.lower, names)

    for name in names:  # todo: make everything lowercase
        if name in objectID_dict.keys():
            result[name] = name_dict[name]
        else:
            query.append(name)

    endpoint = 'universe/ids/?datasource=tranquility&language=en-us'
    async with get_session().post('{}{}'.format(BASE_URL, endpoint), json=query) as response:
        assert response.status == 200
        json = await response.json()

        for category, items in json.items():
            for item in items:
                options = {
                    'systems': System,
                    'characters': Character,
                    'inventory_types': Ship,
                }
                obj = options[category](name=item['name'], object_id=item['id'])
                result[obj.name] = obj
                name_dict[obj.name] = obj
                objectID_dict[obj.objectID] = obj

    return result


async def universe_ids_to_names(ids):
    """
    This function is used to cache IDs locally.
    In most cases, this will make the request faster
    :param ids: a list of IDs we want names for
    :return: dict of id: object
    """
    result = {}
    query = []

    for objectID in ids:
        if objectID in objectID_dict.keys():
            result[objectID] = name_dict[objectID]
        else:
            query.append(objectID)

    endpoint = 'universe/names/?datasource=tranquility&language=en-us'
    async with get_session().post('{}{}'.format(BASE_URL, endpoint), json=query) as response:
        assert response.status == 200
        json = await response.json()

        for entry in json:
            options = {
                'solar_system': System,
                'character': Character,
                'inventory_type': Ship,
            }
            obj = options[entry['category']](name=entry['name'], object_id=entry['id'])

            result[obj.objectID] = obj  # for the answer
            name_dict[obj.name] = obj  # update both dictionaries
            objectID_dict[obj.objectID] = obj

    return result


async def name_to_id(name):
    d = await universe_names_to_ids([name])
    assert len(d) == 1
    (_, v), = d.items()
    return v.objectID


async def id_to_name(id):
    d = await universe_ids_to_names(id)
    assert len(d) == 1
    return d[id].name


async def create_object(name, object_id, object_type):
    if name is None and object_id is None:
        raise Exception('neither name nor objectID provided')
    elif object_id and name is None:
        return object_type(name=await id_to_name(object_id), object_id=object_id)
    elif name and object_id is None:
        return object_type(name=name, object_id=await name_to_id(name.lower()))
    else:
        return object_type(name, object_id)


async def get_latest_release():
    """
    Get the latest stable release of the bot
    :return: semver
    """
    endpoint = 'https://api.github.com/repos/daniel-dsouza/eve-bot/releases/latest'
    async with get_session().get(endpoint) as response:
        assert response.status == 200
        json = await response.json()

        return json['tag_name']