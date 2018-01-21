import aiohttp
import asynctest

import esi.common
from system.tokenizer import Message


class Base(asynctest.TestCase):
    use_default_loop = True
    forbid_get_event_loop = False

    async def setUp(self):
        esi.common.session = aiohttp.ClientSession()

    async def tearDown(self):
        await esi.common.session.close()


class TestMessage(Base):
    async def test_basic2(self):
        m = await Message.new('[ 2017.07.31 20:13:35 ] Sofi Stoun > W5-VBR  Dreya Starhunt')
        print(m.tokens)

    async def test_basic(self):
        m = await Message.new('[ 2017.07.31 22:00:58 ] Spartanreign > AZA-QE clr')
        print(m.raw_text)