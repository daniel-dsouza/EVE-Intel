from enum import Enum

from evethings.character import Character, is_character_partial
from evethings.ship import Ship, is_ship
from evethings.system import System, is_system

ignore_words = {''}


class TokenType(Enum):
    NONE = 0
    CLEAR = 1
    NV = 2
    SYSTEM = 3
    SHIP = 4
    CHARACTER = 5


def _get_character_from_tokens(tokens):
    tokens = tokens[:tokens.index('') if '' in tokens else None]
    possible_names = [" ".join(tokens[0:i]) for i in range(1, len(tokens)+1)]
    verified_names = [i for i, item in enumerate(possible_names) if is_character_partial(item)]
    best_length = max(verified_names) if len(verified_names) > 0 else -1
    return (possible_names[best_length], best_length+1) if best_length > -1 else (None, best_length+1)


def _get_ship_from_tokens(tokens):
    possible_names = [" ".join(tokens[0:i]) for i in range(1, len(tokens)+1)]
    verified_names = [i for i, item in enumerate(possible_names) if is_ship(item)]
    best_length = max(verified_names) if len(verified_names) > 0 else -1
    return (possible_names[best_length], best_length+1) if best_length > -1 else (None, best_length+1)


def _get_token_type(s, disable_character=False):
    if s[0] in ignore_words:
        return TokenType.NONE, 1  # this saves having to look through everything

    if s[0] in ['clr', 'CLR', 'clear', 'Clear']:
        return TokenType.CLEAR, 1

    if s[0] == 'nv':
        return TokenType.NV, 1

    if is_system(s[0]):
        return TokenType.SYSTEM, 1

    _, length = _get_ship_from_tokens(s)
    if length > 0:
        return TokenType.SHIP, length

    if not disable_character:
        _, length = _get_character_from_tokens(s)
        if length > 0:
            return TokenType.CHARACTER, length

    return TokenType.NONE, 1  # the default case


def parse_message(message):
    tokens = list(map(lambda x: x.strip('*'), message.rstrip().split(' ')))
    index = 0
    disable = True if len(tokens) > 6 else False
    while index < len(tokens):
        token_type, token_length = _get_token_type(tokens[index:index+min(3, len(tokens)-index)], disable)
        yield (token_type, " ".join(tokens[index:index+token_length]))
        index += token_length


if __name__ == '__main__':
    from chat_reader import ChatReader
    import asyncio

    async def hmm():
        await c.wait_until_ready()
        while True:
            messages = await c.get_messages()

            for message in messages:
                objects = {k: v for v, k in parse_message(message[message.find(' > ')+3:])}
                print(objects)


    c = ChatReader(["The Drone Den"], '\Documents\EVE\logs\Chatlogs')
    event_loop = asyncio.get_event_loop()
    b = asyncio.ensure_future(hmm())
    event_loop.run_until_complete(b)
    event_loop.close()
