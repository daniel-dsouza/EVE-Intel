import random
import unittest

from message_parser import _get_character_from_tokens, _get_ship_from_tokens, parse_message, TokenType


class TestGetCharacterFromTokens(unittest.TestCase):
    def test_basic(self):
        tokens = ['spicy', 'indian', '']
        self.assertEqual(('spicy indian', 2), _get_character_from_tokens(tokens))

    def test_no_characters(self):
        tokens = ['21546', 'asefswv', '65753']  # not guaranteed to not contain EVE characters! People are weird.
        self.assertEqual((None, 0), _get_character_from_tokens(tokens))


class TestGetShipsFromTokens(unittest.TestCase):
    def test_basic(self):
        tokens = ['Vexor', 'w2e4rsw', 'wergws']
        self.assertEqual(('Vexor', 1), _get_ship_from_tokens(tokens))

    def test_lower(self):
        tokens = ['vexor', 'w2e4rsw', 'wergws']
        self.assertEqual(('vexor', 1), _get_ship_from_tokens(tokens))

    def test_spaces(self):
        tokens = ['Imperial', 'Navy', 'Slicer']
        self.assertEqual(('Imperial Navy Slicer', 3), _get_ship_from_tokens(tokens))


# class TestGetTokenType(unittest.TestCase):  # some things don't need tests....

class TestParseMessage(unittest.TestCase):
    def test_basic(self):
        result = [(TokenType.CHARACTER, 'Jimmy Michaels'), (TokenType.NONE, ''), (TokenType.SYSTEM, 'DYPL-6'), (TokenType.SHIP, 'astero')]
        self.assertListEqual(result, list(parse_message('Jimmy Michaels  DYPL-6 astero')))
