import unittest

from evethings import ship


class TestIsShip(unittest.TestCase):
    def test_simple(self):
        self.assertIs(True, ship.is_ship('Vexor'))

    def test_lower(self):
        self.assertIs(True, ship.is_ship('vexor'))

    def test_spaces(self):
        self.assertIs(True, ship.is_ship('Vexor Navy Issue'))

    def test_false(self):
        self.assertIs(False, ship.is_ship('Avenger'))


class TestShip(unittest.TestCase):
    def test_from_name(self):
        s = ship.Ship('Vexor')
        self.assertEqual('Vexor', s.name)
        self.assertEqual(626, s.objectID)

    def test_from_ID(self):
        with self.assertRaises(NotImplementedError):
            s = ship.Ship(ship_id=626)
