import unittest
import esi_routes


class TestGetSystemID(unittest.TestCase):
    def test_get_system_id(self):
        system_id = esi_routes.get_system_id('MTO2-2')
        self.assertEqual(system_id, '30005189')

    def test_cache_get_system_id(self):
        _ = esi_routes.get_system_id('TP-APY')
        system_id = esi_routes.get_system_id('TP-APY')
        self.assertEqual(system_id, '30001127')


class TestGetJumps(unittest.TestCase):
    def test_get_jumps(self):
        jumps = esi_routes.get_jumps('30005189', '30003230')
        self.assertEqual(jumps, 15)

    def test_cache_get_jumps(self):
        _ = esi_routes.get_jumps('30001127', '30003230')
        jumps = esi_routes.get_jumps('30001127', '30003230')
        self.assertEqual(jumps, 20)

    def test_reverse_get_jumps(self):
        jumps_forward = esi_routes.get_jumps('30003195', '30003230')
        jumps_backwards = esi_routes.get_jumps('30003230', '30003195')
        self.assertEqual(jumps_forward, jumps_backwards)
        self.assertEqual(jumps_forward, 5)


class TestGetShipID(unittest.TestCase):
    def test_lowercase(self):
        ship_id = esi_routes.get_ship_id('vexor')
        self.assertEqual(ship_id, 626)

    def test_uppercase(self):
        ship_id = esi_routes.get_ship_id('Vexor')
        self.assertEqual(ship_id, 626)

    def test_error(self):
        ship_id = esi_routes.get_ship_id('sdfasdf')
        self.assertIsNone(ship_id)