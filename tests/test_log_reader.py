import unittest
from datetime import datetime

from system.log_reader import Message


class TestMessage(unittest.TestCase):
    def test_from_string(self):
        input = '[ 2017.07.31 22:00:58 ] Spartanreign > AZA-QE clr'
        message = Message(input)

        self.assertEqual(message.message, 'AZA-QE clr')
        self.assertEqual(message.sender, 'Spartanreign')
        self.assertEqual(message.timestamp, datetime(2017, 7, 31, 22, 0, 58))