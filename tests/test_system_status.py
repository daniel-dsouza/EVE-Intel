import unittest

from system_status import IntelParser, Intel
from evethings.character import Character
from evethings.system import System


class TestIntel(unittest.TestCase):
    def test_basic_case(self):
        intel = Intel('\ufeff[ 2017.03.18 07:38:14 ] Roku Gepart > Jimmy Michaels  R-6KYM*\r\n')
        self.assertEqual(intel.timestamp, '2017.03.18 07:38:14')
        self.assertEqual(intel.sender.name, 'Roku Gepart')
        self.assertEqual(intel.system.name, 'R-6KYM')
        self.assertEqual(intel.get_clear(), False)
        self.assertEqual(intel.get_nv(), False)
        self.assertListEqual(intel.get_ships(), [])
        self.assertListEqual(intel.get_characters(), [Character(character_name='Jimmy Michaels')])


class TestIntelParser(unittest.TestCase):
    def test_basic_case(self):
        a = IntelParser(100)
        for m in [
            '\ufeff[ 2017.04.16 19:38:27 ] spicy indian > 1P-QWR Roku Gepart  Jimmy Michaels\r\n',
            '\ufeff[ 2017.04.16 19:38:27 ] spicy indian > Vexor\r\n',
            '\ufeff[ 2017.03.18 07:54:18 ] Lachdanan ImmO > WeTaLeR Lol  Merry Lol  Aleksandr Litwinov  RXA-W1\r\n'
        ]:
            a.process_message(m)

        c = list(a.summarize(System(system_name='BQO-UU')))
        self.assertListEqual(c, [('Roku Gepart, Jimmy Michaels in a Vexor 1 jump away in 1P-QWR', 1),
                                 ('Neutral 20 jumps away in RXA-W1', 20)])
