from message_parser import parse_message, TokenType
from evethings.character import Character
from evethings.ship import Ship
from evethings.system import System


class Intel(object):
    def __init__(self, raw):
        self.timestamp = raw[raw.find(' [ ')+4:raw.find(' ] ')]  # TODO, make this a timestamp
        self.sender = Character(character_name=raw[raw.find(' ] ')+3: raw.find(' > ')])
        self.contents = list(parse_message(raw[raw.find(' > ')+3:]))
        print(self.contents)
        self.system = None
        for x, y in self.contents:
            if x is TokenType.SYSTEM:
                self.system = System(system_name=y)
                break

    def get_characters(self):
        return [Character(y) for x, y in self.contents if x is TokenType.CHARACTER]

    def get_ships(self):
        return [Ship(ship_name=y) for x, y in self.contents if x is TokenType.SHIP]

    def get_clear(self):
        return True if TokenType.CLEAR in [x for x, y in self.contents] else False

    def get_nv(self):
        return True if TokenType.NV in [x for x, y in self.contents] else False

    def combine(self, other):
        self.contents += [x for x in other.contents if x not in self.contents]
        if self.system is None and other.system is not None:
            self.system = other.system

    def __eq__(self, other):
        return self.sender.name == other.sender.name


class IntelParser(object):
    def __init__(self, jump_range):
        self.jump_range = jump_range
        self.briefcase = []

    def process_message(self, message):
        if type(message) is Intel:
            intel = message
        else:
            intel = Intel(message)

        for i, x in enumerate(self.briefcase):
            if intel.sender.name == x.sender.name or (intel.system and x.system and intel.system == x.system):
                self.briefcase[i].combine(intel)
                return

        self.briefcase.append(intel)

    def summarize(self, home_system):
        for intel in [x for x in self.briefcase if x.system is not None]:
            jumps = home_system.get_jumps_to(intel.system)

            if jumps >= self.jump_range or intel.get_clear():
                continue

            characters = ', '.join([x.name for x in intel.get_characters()])
            if len(characters) == 0:
                characters = 'Neutral'

            ships = ', '.join([x.name for x in intel.get_ships()])
            if len(ships) > 0:
                ships = 'in a ' + ships + ' '

            jumps_str = str(jumps) + ' jump' if jumps==1 else str(jumps) + ' jumps'

            message = '{0} {1}{2} away in {3}'.format(characters, ships, jumps_str, intel.system.name)
            yield message, jumps


if __name__ == '__main__':
    from chat_reader import ChatReader
    from message_parser import parse_message
    import asyncio

    async def hmm():
        await c.wait_until_ready()
        while True:
            intel = IntelParser(jump_range=9)
            messages = await c.get_messages()
            for m in messages:
                intel.process_message(m)

            for m in intel.summarize(home_system=System('BQO-UU')):
                print(m)

    c = ChatReader(["The Drone Den"], '\Documents\EVE\logs\Chatlogs')
    event_loop = asyncio.get_event_loop()
    b = asyncio.ensure_future(hmm())
    event_loop.run_until_complete(b)
    event_loop.close()
