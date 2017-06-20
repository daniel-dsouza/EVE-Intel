import unittest

from evethings import character


class TestIsCharacter(unittest.TestCase):
    def test_basic_case(self):
        self.assertIs(True, character.is_character('spicy indian'))


class TestCharacter(unittest.TestCase):
    def test_create(self):
        c = character.Character('spicy indian')
        self.assertEqual('spicy indian', c.name)
        self.assertEqual(96863339, c.objectID)

    def test_from_ID(self):
        with self.assertRaises(NotImplementedError):
            c = character.Character(character_id=96863339)
