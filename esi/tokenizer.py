import aiohttp
import asyncio

from esi.common import get_session, BASE_URL


async def validate_tokens(tokens):
    """
    Runs tokens through esi
    :param tokens: list of tokens
    :return: map of names to token objects
    """
    endpoint = 'universe/ids/?datasource=tranquility&language=en-us'

    async with get_session().post('{}{}'.format(BASE_URL, endpoint), json=tokens) as response:
        assert response.status == 200

        print(await response.json())


