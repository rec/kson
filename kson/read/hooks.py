from . import get_lark
from . import unquote
import base64
import functools
import lark
import math


class Hooks:
    def array(self, *args):
        return list(args)

    def object(self, *args):
        return dict(args)

    def key_value(self, k, v):
        return k, v

    def integer(self, i):
        return int(i)

    def floating(self, i):
        return float(i)

    def null(self):
        return None

    def false(self):
        return False

    def true(self):
        return True

    def string(self, s):
        return unquote.unquote(s)

    def astring(self, s):
        return base64.b85decode(s[2:-1])

    def bstring(self, s):
        v = s.value
        tsize = 1 + v.index(v[1], 2)
        assert v.endswith(v[1:tsize])
        return v[tsize : -tsize + 1]

    def nan(self):
        return math.nan

    def inf(self):
        return math.inf

    def minus_inf(self):
        return -math.inf

    @functools.lru_cache()
    def _lark(self, use_bytes):
        return get_lark.get_lark(self._transformer(), use_bytes)

    @functools.lru_cache()
    def _transformer(self):
        def wrap(name):
            attr = getattr(self, name)
            return lambda x: attr(*x)

        t = lark.Transformer()
        t.__dict__.update((name, wrap(name)) for name in NAMES)
        return t

    def __call__(self, s):
        return self._lark(not isinstance(s, str)).parser.parse(s)


NAMES = tuple(i for i in dir(Hooks) if not i.startswith('_'))
HOOKS = Hooks()
