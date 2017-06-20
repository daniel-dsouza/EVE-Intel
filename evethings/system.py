import esi_routes as esi
import re


nullsec_regex = re.compile("[A-Z0-9][A-Z0-9]*-[A-Z0-9][A-Z0-9]*")
wh_regex = re.compile("J[0-9]{6}$")
# named_systems = set()


def is_system(system_name):
    if len(nullsec_regex.findall(system_name)) > 0 and esi.get_system_id(system_name):
        return True
    else:
        return False


class System:
    def __init__(self, system_name=None, system_id=None):
        self.name, self.objectID = system_name, system_id
        assert self.name or self.objectID  # at least one should be specified!
        if self.name:
            self.objectID = esi.get_system_id(self.name)
        else:
            raise NotImplementedError  # TODO: implement system name lookup...

    def get_jumps_to(self, system):
        return esi.get_jumps(system.objectID, self.objectID)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.__dict__.values())
