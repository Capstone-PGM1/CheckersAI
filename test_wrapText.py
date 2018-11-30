import unittest
from graphics_helpers import *

class TestWrapText(unittest.TestCase):
    def test_one_word_wraps(self):
        message = wrap_text('a' * 20, 15)
        self.assertEqual(message, ['a' * 15, 'a' * 5])

    def test_short_word_then_long_word(self):
        message = wrap_text('a'* 3 + ' ' + 'a' * 20, 15)
        self.assertEqual(message, ['a' * 3, 'a' * 15, 'a' * 5])

    def test_many_short_words(self):
        message = wrap_text(' '.join(['a' * 3 for i in range(10)]), 15)
        self.assertEqual(message, [' '.join(['a' * 3 for i in range(4)]), ' '.join(['a' * 3 for i in range(4)]), ' '.join(['a' * 3 for i in range(2)])])

    def test_normal_words(self):
        message = wrap_text('happily I notice', 15)
        self.assertEqual(message, ['happily I', 'notice'])

    def test_normal_words(self):
        message = wrap_text('happily I am ' + 'k' * 20, 15)
        self.assertEqual(message, ['happily I am', 'k' * 15, 'k' * 5])

    def test_no_overflow(self):
        message = wrap_text('overflow like m', 15)
        self.assertEqual(message, ['overflow like m'])

    def test_overflow_when_next_word_needed(self):
        message = wrap_text('overflow like ma', 15)
        self.assertEqual(message, ['overflow like', 'ma'])

if __name__ == '__main__':
    unittest.main()
