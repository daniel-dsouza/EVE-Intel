import esi.common


class EveType:
    def __init__(self, name, object_id):
        self.name = name.lower()
        self.objectID = int(object_id)

    @classmethod
    async def new(cls, name=None, object_id=None):
        return await esi.common.create_object(name, object_id, cls)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.__dict__.values())

    def __str__(self):
        return 'name: {} id: {}'.format(self.name, self.objectID)


class Character(EveType):
    pass


class Corporation(EveType):
    pass


class Ship(EveType):
    pass


class System(EveType):
    def jumps_to(self, other):
        pass
