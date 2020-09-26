from kson.read import decoder
from kson.read import parser
import unittest


class NamesTest(unittest.TestCase):
    def test_names(self):
        names = []

        for rule in parser.lark(decoder.DECODER._transformer()).rules:
            name = rule.origin.name
            if not (name.startswith('_') or name in names):
                names.append(name)

        assert decoder.NAMES == names
