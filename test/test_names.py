from kson.read import hooks
from kson.read import parser
import unittest


class NamesTest(unittest.TestCase):
    def test_names(self):
        names = []

        for rule in parser.lark(hooks.HOOKS._transformer()).rules:
            name = rule.origin.name
            if not (name.startswith('_') or name in names):
                names.append(name)

        assert hooks.NAMES == names
