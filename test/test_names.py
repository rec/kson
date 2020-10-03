from kson.read import decoder
import unittest


class NamesTest(unittest.TestCase):
    def test_names(self):
        names = []

        for rule in decoder.DECODER._lark(False).rules:
            name = rule.origin.name
            if not (name.startswith('_') or name in names):
                names.append(name)

        assert decoder.NAMES == names
