import esi.common


async def create_character(name=None, object_id=None):
    return await esi.common.create_object(name, object_id, Character)


class Character:
    def __init__(self, name, object_id):
        self.name = str(name).lower()
        self.objectID = int(object_id)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.__dict__.values())

    def __str__(self):
        return 'name: {} id: {}'.format(self.name, self.objectID)