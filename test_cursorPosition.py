import unittest
from graphics_helpers import *

class TestCursorPosition(unittest.TestCase):
    def test_correctCursorPositionWhenEmpty(self):
        cursor_position = get_cursor_position([""], 0)
        self.assertEqual(cursor_position, (0, 0))

    def test_correctCursorPositionWithOneWord(self):
        cursor_position = get_cursor_position(["abcdefg"], 7)
        self.assertEqual(cursor_position, (0, 7))

    def test_correctCursorPositionMiddleOfOneWord(self):
        cursor_position = get_cursor_position(["abcdefg"], 4)
        self.assertEqual(cursor_position, (0, 4))

    def test_correctCursorPositionWithTwoWords(self):
        cursor_position = get_cursor_position(["abcdefg", "abcdefg"], 7)
        self.assertEqual(cursor_position, (0, 7))

    def test_correctCursorPositionWithTwoWords(self):
        cursor_position = get_cursor_position(["abcdefg", "abcdefg"], 11)
        self.assertEqual(cursor_position, (1, 4))


if __name__ == '__main__':
    unittest.main()
