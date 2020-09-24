from kson import dumps
import unittest


class FormatterTest(unittest.TestCase):
    def test_simple(self):
        assert dumps('') == "''\n"
