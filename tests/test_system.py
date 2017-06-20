import unittest

from evethings import system


class TestIsSystem(unittest.TestCase):
    def test_null_system(self):
        self.assertIs(True, system.is_system('BQ0-UU'))

    # def test_wh_system(self):
    #     self.assertIs(True, system. is_system('J101408'))


class TestSystem(unittest.TestCase):
    def test_from_system_name(self):
        s = system.System(system_name='F-NXLQ')
        self.assertEqual('F-NXLQ', s.name)
        self.assertEqual('30004032', s.objectID)

    # def test_from_system_name2(self):
    #     s = system.System(system_name='J111458')
    #     self.assertEqual('J111458', s.name)
    #     self.assertEqual('31001671', s.objectID)
