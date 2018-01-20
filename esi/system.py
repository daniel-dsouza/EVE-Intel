import esi.common


async def create_system(name=None, object_id=None):
    """
    Creates a system object, populating missing fields
    :param name: system name (optional if given object_id)
    :param object_id: ESI id (optional if given system name)
    :return:
    """
    return await esi.common.create_object(name, object_id, System)


class System:
    def __init__(self, name, object_id):
        self.name = name.lower()
        self.objectID = int(object_id)

    def jumps_to(self, other):
        pass

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.__dict__.values())

    def __str__(self):
        return 'name: {} id: {}'.format(self.name, self.objectID)
