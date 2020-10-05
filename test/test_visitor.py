from kson.write.options import Options
from kson.write.visitor import Visitor
import math
import random
import string
import unittest


def visit_raw(x, **kwargs):
    return list(Visitor(Options(**kwargs)).visit(x))


def visit(x, **kwargs):
    return ''.join(visit_raw(x, **kwargs))


class VisitorTest(unittest.TestCase):
    def test_simple(self):
        assert visit('', single_quote=True) == "''"
        assert visit('') == '""'
        assert visit(False) == 'false'
        assert visit(12) == '12'
        assert visit([]) == '[]'
        assert visit({}) == '{}'
        assert visit(23.5) == '23.5'
        assert visit('hello') == '"hello"'
        assert visit(math.inf) == 'inf'
        assert visit(-math.inf) == '-inf'
        assert visit(math.nan) == 'nan'

    def test_list(self):
        assert visit([]) == '[]'
        assert visit([1]) == '[1,]'
        assert visit([1, 'frog', {}]) == '[1,"frog",{},]'

    def test_dict(self):
        assert visit({}) == '{}'
        assert visit({'one': 1}, single_quote=True) == "{'one':1,}"
        assert visit({'one': 1}) == '{"one":1,}'

    def test_bytes(self):
        expected = ['{', '"one"', ':', b'1234', ',', '}']
        assert visit_raw({'one': b'1234'}) == expected

    def test_default_error(self):
        with self.assertRaises(TypeError) as m:
            visit(self)
        expected = "Cannot visit <class 'test.test_visitor.VisitorTest'>"
        assert m.exception.args[0] == expected

    def test_default_ok(self):
        actual, = visit_raw(self, default=lambda x: x)
        assert actual is self

    def test_skipkeys_error(self):
        with self.assertRaises(TypeError) as m:
            visit({self: True, 'a': 1})
        assert m.exception.args[0] == 'Keys must be strings'

    def test_skipkeys_ok(self):
        actual = visit({self: True, 'a': 1}, skipkeys=True)
        assert actual == '{"a":1,}'

    def test_sortkeys(self):
        lower = list(string.ascii_lowercase[:12])
        random.shuffle(lower)
        source = {k: i for i, k in enumerate(lower)}
        v1 = visit(source)
        v2 = visit(source, sort_keys=True)
        assert v1 != v2

        actual = ''.join(k for k in v2 if k in lower)
        assert actual == 'abcdefghijkl'
