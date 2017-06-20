import esi_routes as esi

character_ids = {}
searched_partials = set()


def is_character(character_name):
    return False if esi.get_character_id(character_name) is None else True


def is_character_partial(partial_name):
    if partial_name not in character_ids:
        try:
            ids = esi.get_partial_character_id(partial_name)
            a = esi.bulk_character_lookup(ids)
            character_ids.update([(x['name'], x['id']) for x in a if x['category'] == 'character'])
            searched_partials.add(partial_name)
        except Exception:
            return False

    return is_character(partial_name)


class Character:
    def __init__(self, character_name=None, character_id=None):
        self.name, self.objectID = character_name, character_id
        assert self.name or self.objectID

        if self.name:
            self.objectID = esi.get_character_id(character_name)
        else:
            raise NotImplementedError

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.__dict__.values())
