import asynctest
import aiohttp
import esi.common
from esi.common import universe_names_to_ids, name_to_id
from esi.eve_types import Character, System


class TestUniverseNamesToIds(asynctest.TestCase):
    use_default_loop = True
    forbid_get_event_loop = False

    async def setUp(self):
        esi.common.session = aiohttp.ClientSession()

    async def tearDown(self):
        await esi.common.session.close()

    async def test_systems(self):
        names = ['MF-PGF', 'AL-JSG', 'C6C-K9']
        correct = {
            'mf-pgf': System('mf-pgf', 30002299),
            'al-jsg': System('al-jsg', 30001534),
            'c6c-k9': System('c6c-k9', 30001533)
        }
        result = await universe_names_to_ids(names)
        self.assertDictEqual(result, correct)

    async def test_characters(self):
        names = ['Lyzars Cruiz', 'Bagadonuts Ostus']
        correct = {
            'lyzars cruiz': Character('lyzars cruiz', 91190164),
            'bagadonuts ostus': Character('bagadonuts ostus', 90383098)
        }
        result = await universe_names_to_ids(names)
        self.assertDictEqual(result, correct)


class TestNameToId(asynctest.TestCase):
    use_default_loop = True
    forbid_get_event_loop = False

    async def setUp(self):
        esi.common.session = aiohttp.ClientSession()

    async def tearDown(self):
        await esi.common.session.close()

    async def test_system(self):
        result = await name_to_id('BQ0-UU')
        self.assertEqual(result, 30003230)

    async def test_character(self):
        result = await name_to_id('Lyzars Cruiz')
        self.assertEqual(result, 91190164)
