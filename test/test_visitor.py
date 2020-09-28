from kson.write.options import Options
from kson.write.visitor import Visitor
import math
import unittest


def visit_raw(x, **kwargs):
    return list(Visitor(Options(**kwargs)).visit(x))


def visit(x, **kwargs):
    return ''.join(visit_raw(x, **kwargs))


class VisitorTest(unittest.TestCase):
    def test_simple(self):
        assert visit('') == "''"
        assert visit('', double_quote=True) == '""'
        assert visit(False) == 'false'
        assert visit(12) == '12'
        assert visit([]) == '[]'
        assert visit({}) == '{}'
        assert visit(23.5) == '23.5'
        assert visit('hello') == "'hello'"
        assert visit(math.inf) == 'inf'
        assert visit(-math.inf) == '-inf'
        assert visit(math.nan) == 'nan'

    def test_list(self):
        assert visit([]) == '[]'
        assert visit([1]) == '[1]'
        assert visit([1, 'frog', {}]) == "[1,'frog',{}]"

    def test_dict(self):
        assert visit({}) == '{}'
        assert visit({'one': 1}) == "{'one':1}"
        assert visit({'one': 1}, double_quote=True) == '{"one":1}'

    def test_bytes(self):
        assert visit_raw({'one': b'1234'}) == ['{', "'one'", ':', b'1234', '}']
